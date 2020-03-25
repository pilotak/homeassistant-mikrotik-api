# HomeAssistant component: `MikroTik`
The `mikrotik` platform enables you to execute scripts and perform API requests in MikroTik router

To enable MikroTik platform in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
mikrotik:
  host: !secret router_host
  username: !secret router_user
  password: !secret router_pass
```

Configuration variables:

- **host** (*Required*): URL of router
- **port** (*Optional*): default is `8728`
- **username** (*Required*)
- **password** (*Optional*)

## Install via [HACS](https://github.com/custom-components/hacs)
You can find this integration in a store.

## Install manually
You need to copy `mikrotik` folder from this repo to the `custom_components` folder in the root of your configuration, file tree should look like this:
```
└── ...
└── configuration.yaml
└── secrects.yaml
└── custom_components
    └── mikrotik
        └── __init__.py
        └── manifest.json
        └── services.yaml
```

>__Note__: if the `custom_components` directory does not exist, you need to create it.

## Usage
You will have a 5 new services to call either from Development Tools or from scripts.