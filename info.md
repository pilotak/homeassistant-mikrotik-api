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

You will have a 5 new services to call either from Development Tools or from scripts.