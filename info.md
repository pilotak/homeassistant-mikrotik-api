The `mikrotik_api` platform enables you to execute scripts and perform API requests in MikroTik router

To enable MikroTik API platform in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
mikrotik_api:
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

> `params` and `find_params` is key=value scheme. All strings have to be wrapped with a single of double quotes, numbers not. Special case is boolean - no quotes but the string would be `True/False` ie.: `enabled=True` or `enabled=true`

### Service: `mikrotik_api.call` examples
In case you need to disable exact item, you can search for it. Then the command will be call only if `find` command returns ids, you can also specify `find_params` to the search.
```yaml
command: /ip firewall address-list disable
find: /ip firewall address-list
find_params: list="internet" comment="test"
```

```yaml
command: /ping
params: address="1.1.1.1" count=3
```
```yaml
command: tools ping
params: mac="00:00:00:00:00"
```