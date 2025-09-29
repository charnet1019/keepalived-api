#!/usr/bin/env python3
"""
Keepalived Config Templates Health Check Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates


def example_tcp_check():
    """Example: Virtual server with TCP health check"""
    print("=== Virtual Server with TCP Health Check ===")
    
    # Create a template with TCP_CHECK
    tcp_check_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": 6,
            "lb_algo": "rr",
            "lb_kind": "DR",
            "protocol": "TCP",
            "real_server": {
                "ip": "192.168.1.101",
                "port": 80,
                "weight": 1,
                "health_check": "TCP_CHECK",
                "TCP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                },
                "HTTP_GET": {
                    "url": "/",
                    "digest": "NONE",
                    "status_code": 200
                },
                "UDP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                }
            }
        }
    }
    
    # Register and use the template
    KeepAlivedConfigTemplates.register_template("tcp_check_vs", tcp_check_template)
    config = KeepAlivedConfigTemplates.from_template("tcp_check_vs", "192.168.1.100 80")
    print(config.params[0].to_str())
    print()


def example_http_check():
    """Example: Virtual server with HTTP health check"""
    print("=== Virtual Server with HTTP Health Check ===")
    
    # Create a template with HTTP_GET
    http_check_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": 6,
            "lb_algo": "rr",
            "lb_kind": "DR",
            "protocol": "TCP",
            "real_server": {
                "ip": "192.168.1.101",
                "port": 80,
                "weight": 1,
                "health_check": "HTTP_GET",
                "TCP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                },
                "HTTP_GET": {
                    "url": "/",
                    "digest": "NONE",
                    "status_code": 200
                },
                "UDP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                }
            }
        }
    }
    
    # Register and use the template
    KeepAlivedConfigTemplates.register_template("http_check_vs", http_check_template)
    config = KeepAlivedConfigTemplates.from_template("http_check_vs", "192.168.1.100 80")
    print(config.params[0].to_str())
    print()


def example_udp_check():
    """Example: Virtual server with UDP health check"""
    print("=== Virtual Server with UDP Health Check ===")
    
    # Create a template with UDP_CHECK
    udp_check_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": 6,
            "lb_algo": "rr",
            "lb_kind": "DR",
            "protocol": "UDP",
            "real_server": {
                "ip": "192.168.1.101",
                "port": 53,
                "weight": 1,
                "health_check": "UDP_CHECK",
                "TCP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                },
                "HTTP_GET": {
                    "url": "/",
                    "digest": "NONE",
                    "status_code": 200
                },
                "UDP_CHECK": {
                    "connect_timeout": 3,
                    "delay_before_retry": 3
                }
            }
        }
    }
    
    # Register and use the template
    KeepAlivedConfigTemplates.register_template("udp_check_vs", udp_check_template)
    config = KeepAlivedConfigTemplates.from_template("udp_check_vs", "192.168.1.100 53")
    print(config.params[0].to_str())
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_tcp_check()
    example_http_check()
    example_udp_check()
    
    print("Health check examples completed successfully!")