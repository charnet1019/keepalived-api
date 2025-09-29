# keepalived-config

Python API for configuration files for linux [keepalived package](https://www.keepalived.org/).

This project is forked from [https://github.com/Slinred/keepalived-config](https://github.com/Slinred/keepalived-config). 
Special thanks to the original author for their work.

## License

This project is licensed under the GPL-3 License - see the [LICENSE](LICENSE) file for details.

## Features

- Parse a keepalived configuration from file or string
- Modify the config object and any parameter inside
- Save back the (modified) config to another (or the same) file
- Comments in the config file are supported and can also be added via the python API
- empty lines in the config file, can be kept and are represented as empty config parameters

## Main Classes and Methods

### Core Classes

- `KeepAlivedConfig` - Main configuration class representing a keepalived configuration
- `KeepAlivedConfigManager` - Unified entry point for managing all keepalived configurations
- `KeepAlivedConfigVRRP` - VRRP instance management
- `KeepAlivedConfigVirtualServer` - Virtual server management
- `KeepAlivedConfigTemplates` - Template system for creating configurations
- `OperationResult` - Result wrapper for operations

### Configuration Objects

- `VRRPConfig` - Configuration object for VRRP instances
- `VirtualServerConfig` - Configuration object for virtual servers

### Main Methods

#### KeepAlivedConfigManager (Recommended Entry Point)
- `load_config(config_file)` - Load configuration from file
- `save_config(file_path)` - Save configuration to file
- `validate()` - Validate configuration integrity
- `vrrp` - Access to VRRP management functions
- `virtual_server` - Access to virtual server management functions

#### KeepAlivedConfigVRRP
- `create_vrrp_instance()` - Create VRRP instance
- `update_vrrp_instance()` - Update VRRP instance
- `remove_vrrp_instance()` - Remove VRRP instance
- `get_vrrp_instance()` - Get VRRP instance
- `list_vrrp_instances()` - List all VRRP instances
- `create_from_template()` - Create VRRP instance from template

#### KeepAlivedConfigVirtualServer
- `create_virtual_server()` - Create virtual server
- `update_virtual_server()` - Update virtual server
- `remove_virtual_server()` - Remove virtual server
- `get_virtual_server()` - Get virtual server
- `list_virtual_servers()` - List all virtual servers
- `add_real_server()` - Add real server to virtual server
- `update_real_server()` - Update real server
- `remove_real_server()` - Remove real server
- `create_from_template()` - Create virtual server from template

#### KeepAlivedConfigTemplates
- `from_template()` - Create configuration from template
- `register_template()` - Register custom template
- `unregister_template()` - Unregister template
- `list_templates()` - List all available templates

## Basic Usage Examples

### Simple Configuration Creation

```python
from keepalived_config import KeepAlivedConfigManager, VRRPConfig, VirtualServerConfig

# Create configuration manager (recommended entry point)
manager = KeepAlivedConfigManager()

# Create VRRP instance using configuration object
vrrp_config = VRRPConfig(
    state="MASTER",
    interface="eth0",
    virtual_router_id=51,
    priority=100
)

result = manager.vrrp.create_vrrp_instance(
    instance_name="VI_1",
    config=vrrp_config,
    virtual_ipaddresses=["192.168.1.100/24"]
)

if result:
    print("VRRP instance created successfully")
else:
    print(f"Failed to create VRRP instance: {result.message}")

# Create virtual server
vs_config = VirtualServerConfig(
    delay_loop=6,
    lb_algo="rr",
    lb_kind="DR",
    protocol="TCP"
)

result = manager.virtual_server.create_virtual_server(
    virtual_server_ip="192.168.1.100",
    virtual_server_port=80,
    config=vs_config
)

if result:
    print("Virtual server created successfully")
else:
    print(f"Failed to create virtual server: {result.message}")

# Add real server to virtual server
result = manager.virtual_server.add_real_server(
    virtual_server_ip="192.168.1.100",
    virtual_server_port=80,
    real_server_ip="192.168.1.10",
    real_server_port=80,
    weight=1,
    health_check="TCP_CHECK",
    health_check_params={
        "connect_timeout": 3,
        "delay_before_retry": 3
    }
)

if result:
    print("Real server added successfully")
else:
    print(f"Failed to add real server: {result.message}")

# Save configuration to file
result = manager.save_config("keepalived.conf")
if result:
    print("Configuration saved successfully")
else:
    print(f"Failed to save configuration: {result.message}")
```

### Template Usage

```python
from keepalived_config import KeepAlivedConfigTemplates, KeepAlivedConfigManager

# Create configuration from template
config = KeepAlivedConfigTemplates.from_template(
    "basic_vrrp",
    "VI_1",
    state="MASTER",
    interface="eth0",
    virtual_router_id=51,
    priority=100,
    virtual_ipaddress="192.168.1.100/24"
)

print(config.params[0].to_str())

# Using templates with manager
manager = KeepAlivedConfigManager()
result = manager.vrrp.create_from_template(
    "complete_vrrp_backup",
    "VI_2",
    interface="eth1",
    virtual_router_id=52,
    priority=90,
    advert_int=2,
    auth_type="PASS",
    auth_pass="backup_password",
    virtual_ipaddress="192.168.2.100/24"
)

if result:
    print("VRRP instance created from template successfully")
else:
    print(f"Failed to create VRRP instance from template: {result.message}")
```

### Custom Template Registration

```python
from keepalived_config import KeepAlivedConfigTemplates

# Define custom template
custom_template = {
    "type": "vrrp_instance",
    "params": {
        "state": "{state}",
        "interface": "{interface}",
        "virtual_router_id": "{virtual_router_id}",
        "priority": "{priority}",
        "virtual_ipaddress": ["{virtual_ipaddress}"],
        "nopreempt": "",
        "preempt_delay": "{preempt_delay}"
    }
}

# Register template
KeepAlivedConfigTemplates.register_template("my_vrrp_template", custom_template)

# Use custom template
config = KeepAlivedConfigTemplates.from_template(
    "my_vrrp_template",
    "VI_CUSTOM",
    state="BACKUP",
    interface="eth1",
    virtual_router_id=52,
    priority=90,
    virtual_ipaddress="192.168.2.100/24",
    preempt_delay=5
)

print(config.params[0].to_str())
```

### Configuration Loading and Validation

```python
from keepalived_config import KeepAlivedConfigManager

# Load existing configuration
manager = KeepAlivedConfigManager()
result = manager.load_config("existing_keepalived.conf")

if result:
    print("Configuration loaded successfully")
    
    # List existing VRRP instances
    print("VRRP instances:")
    for instance in manager.vrrp_instances:
        print(f"  - {instance}")
    
    # List existing virtual servers
    print("Virtual servers:")
    for vs in manager.virtual_servers:
        print(f"  - {vs}")
    
    # Validate configuration
    result = manager.validate()
    if result:
        print("Configuration is valid")
    else:
        print("Configuration validation issues:")
        for issue in result.data:
            print(f"  - {issue}")
else:
    print(f"Failed to load configuration: {result.message}")
```

### Extended Configuration Parameters

```python
from keepalived_config import KeepAlivedConfigManager, VRRPConfig, VirtualServerConfig

manager = KeepAlivedConfigManager()

# Using extended VRRP parameters
vrrp_config = VRRPConfig(
    state="MASTER",
    interface="eth0",
    virtual_router_id=51,
    priority=100,
    # Extended parameters
    unicast_src_ip="192.168.1.1",
    unicast_peer=["192.168.1.2", "192.168.1.3"],
    smtp_alert=True,
    notify_master="/etc/keepalived/scripts/notify_master.sh",
    notify_backup="/etc/keepalived/scripts/notify_backup.sh"
)

result = manager.vrrp.create_vrrp_instance(
    instance_name="VI_EXTENDED",
    config=vrrp_config,
    virtual_ipaddresses=["192.168.1.100/24"]
)

# Using extended virtual server parameters
vs_config = VirtualServerConfig(
    delay_loop=10,
    lb_algo="wrr",
    lb_kind="DR",
    protocol="TCP",
    # Extended parameters
    ha_suspend=True,
    alpha=True,
    omega=True,
    quorum=2,
    quorum_up="/etc/keepalived/scripts/quorum_up.sh",
    quorum_down="/etc/keepalived/scripts/quorum_down.sh",
    hysteresis=3,
    retry=5
)

result = manager.virtual_server.create_virtual_server(
    virtual_server_ip="192.168.1.100",
    virtual_server_port=80,
    config=vs_config
)
```

## TODO

- Support for included config files

## Development

### Setup

To setup your dev environment, you have 2 options:

1. local: execute the command `main.sh setup`. This will install a virtual python environment and install the required packages.
2. container: Use the provided devcontainer, where everything is already installed (no need to run the setup command)

### Tests

Units tests are to be developed for all public modules and methods and placed inside the `tests` directory.
They can be executed via the command `main.sh test`

### Packaging

The source build and wheel distrubtions can be generated via the command `main.sh build`.
The package can then be uploaded to PyPi via the command `main.sh upload`.