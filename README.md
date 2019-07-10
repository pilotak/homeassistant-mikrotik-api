# HomeAssistant component: `MikroTik`
The `mikotik` platform enables you to execute scripts in MikroTik router

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
You need to clone this repo to the root folder of your configuration, file tree should look like this:
```
└── ...
└── configuration.yaml
└── secrects.yaml
└── custom_components
    └── mikotik
        └── __init__.py
        └── manifest.json
        └── services.yaml
```