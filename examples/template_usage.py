#!/usr/bin/env python3
"""
Keepalived Config Templates Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates
from keepalived_config.keepalived_config import KeepAlivedConfig


def example_basic_vrrp():
    """Example: Create a basic VRRP instance configuration"""
    print("=== Basic VRRP Instance Template ===")
    config = KeepAlivedConfigTemplates.from_template(
        "basic_vrrp", 
        "VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password"
    )
    print(config.params[0].to_str())
    print()


def example_complete_master():
    """Example: Create a complete MASTER VRRP instance configuration"""
    print("=== Complete MASTER VRRP Instance Template ===")
    config = KeepAlivedConfigTemplates.from_template(
        "complete_vrrp_master",
        "VI_1",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password",
        virtual_ipaddress="192.168.1.100/24"
    )
    print(config.params[0].to_str())
    print()


def example_complete_backup():
    """Example: Create a complete BACKUP VRRP instance configuration"""
    print("=== Complete BACKUP VRRP Instance Template ===")
    config = KeepAlivedConfigTemplates.from_template(
        "complete_vrrp_backup",
        "VI_1",
        interface="eth0",
        virtual_router_id=51,
        priority=90,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password",
        virtual_ipaddress="192.168.1.100/24"
    )
    print(config.params[0].to_str())
    print()


def example_basic_global():
    """Example: Create a basic global definitions configuration"""
    print("=== Basic Global Definitions Template ===")
    config = KeepAlivedConfigTemplates.from_template(
        "basic_global",
        notification_email="admin@example.com",
        notification_email_from="keepalived@example.com",
        smtp_server="smtp.example.com",
        smtp_connect_timeout=30
    )
    print(config.params[0].to_str())
    print()


def example_virtual_server():
    """Example: Create a basic virtual server configuration"""
    print("=== Basic Virtual Server Template ===")
    config = KeepAlivedConfigTemplates.from_template(
        "basic_virtual_server",
        "192.168.1.100 80",
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP",
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        real_server_weight=1,
        health_check_type="TCP_CHECK",
        tcp_connect_timeout=3,
        tcp_delay_before_retry=3
    )
    print(config.params[0].to_str())
    print()


def example_custom_template():
    """Example: Register and use a custom template"""
    print("=== Custom Template Example ===")
    
    # Define a custom template
    custom_template = {
        "type": "custom_block",
        "params": {
            "custom_param1": "{param1}",
            "custom_param2": "{param2}",
            "nested_block": {
                "nested_param": "{nested_value}"
            }
        }
    }
    
    # Register the custom template
    KeepAlivedConfigTemplates.register_template("my_custom_template", custom_template)
    
    # Use the custom template
    config = KeepAlivedConfigTemplates.from_template(
        "my_custom_template",
        param1="value1",
        param2="value2",
        nested_value="nested_value"
    )
    print(config.params[0].to_str())
    print()


def example_list_templates():
    """Example: List all available templates"""
    print("=== Available Templates ===")
    templates = KeepAlivedConfigTemplates.list_templates()
    for template in templates:
        print(f"  - {template}")
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_list_templates()
    example_basic_vrrp()
    example_complete_master()
    example_complete_backup()
    example_basic_global()
    example_virtual_server()
    example_custom_template()
    
    print("All examples completed successfully!")