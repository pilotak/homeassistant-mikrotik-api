import asyncio
import logging

import voluptuous as vol
import re

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT, CONF_NAME,
    CONF_COMMAND)

from librouteros import connect
from librouteros.query import Key

from .const import (
    DEFAUL_PORT,
    RUN_SCRIPT_COMMAND,
    API_COMMAND,
    CONF_FIND
)

__version__ = '1.1.0'

REQUIREMENTS = ['librouteros==3.0.0']

DOMAIN = "mikrotik"

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PORT): cv.port
    }),
}, extra=vol.ALLOW_EXTRA)

SCRIPT_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string
})

API_SCHEMA = vol.Schema({
    vol.Required(CONF_COMMAND): cv.string,
    vol.Optional(CONF_FIND): cv.string
})


@asyncio.coroutine
def async_setup(hass, config):
    """Initialize of Mikrotik component."""
    conf = config[DOMAIN]
    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD, "")
    port = conf.get(CONF_PORT, DEFAUL_PORT)

    _LOGGER.info("Setup")

    @asyncio.coroutine
    def run(call):
        """Run script service."""

        try:
            api = connect(
                host=host,
                username=username,
                password=password,
                port=port
            )

            if CONF_NAME in call.data:
                req_script = call.data.get(CONF_NAME)

                _LOGGER.debug("Sending request to run '%s' script", req_script)

                try:
                    name = Key('name')
                    id = Key('.id')

                    for script_id in api.path(
                            'system',
                            'script').select(id).where(name == req_script):
                        _LOGGER.info("Running script: %s", script_id)

                        cmd = api.path('system', 'script')
                        tuple(cmd('run', **script_id))

                except Exception as e:
                    _LOGGER.error("Run script error: %s", str(e))

            elif CONF_COMMAND in call.data:
                try:
                    command = call.data.get(CONF_COMMAND).split(' ')
                    find = call.data.get(CONF_FIND)

                    _LOGGER.info("API request: %s", command)

                    if len(command) >= 2:
                        if find:
                            required_params = re.findall(
                                r'(\w+)="([^"]+)"', find)

                            _LOGGER.info("Find required params: %s",
                                         required_params)

                            for item in api.path(*command[:-1]):
                                param_counter = 0

                                for param in required_params:
                                    param_name = item.get(param[0])

                                    if param_name and param_name == param[1]:
                                        param_counter += 1

                                if len(required_params) == param_counter:
                                    params = {'.id': item.get('.id')}
                                    _LOGGER.debug("Found item: %s", item)

                                    cmd = api.path(*command[:-1])

                                    _LOGGER.info("Result: %s", list(
                                        cmd(command[len(command)-1], **params)
                                    ))

                        else:
                            _LOGGER.info("Result: %s", list(
                                api.path(*command)
                            ))

                    else:
                        _LOGGER.error(
                            "Invalid command, must include at least 2 words")

                except Exception as e:
                    _LOGGER.error("API error: %s", str(e))

        except (librouteros.exceptions.TrapError,
                librouteros.exceptions.MultiTrapError,
                librouteros.exceptions.ConnectionError) as api_error:
            _LOGGER.error("Connection error: %s", str(api_error))

    hass.services.async_register(
        DOMAIN, RUN_SCRIPT_COMMAND, run,
        schema=SCRIPT_SCHEMA)

    hass.services.async_register(
        DOMAIN, API_COMMAND, run,
        schema=API_SCHEMA)

    return True
