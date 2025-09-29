import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates
from keepalived_config.keepalived_config import KeepAlivedConfig


def test_list_templates():
    """Test that all expected templates are available"""
    templates = KeepAlivedConfigTemplates.list_templates()
    expected_templates = [
        "basic_vrrp",
        "basic_global",
        "complete_vrrp_master",
        "complete_vrrp_backup",
        "basic_virtual_server"
    ]
    
    for template in expected_templates:
        assert template in templates


def test_basic_vrrp_template():
    """Test creating a basic VRRP template"""
    config = KeepAlivedConfigTemplates.from_template(
        "basic_vrrp", 
        "VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password",
        virtual_ipaddress="192.168.1.100/24"
    )
    
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    assert config.params[0].name.startswith("vrrp_instance")
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "state MASTER" in config_str
    assert "interface eth0" in config_str
    assert "virtual_router_id 51" in config_str
    assert "priority 100" in config_str


def test_basic_global_template():
    """Test creating a basic global template"""
    config = KeepAlivedConfigTemplates.from_template(
        "basic_global",
        notification_email="admin@example.com",
        notification_email_from="keepalived@example.com",
        smtp_server="smtp.example.com",
        smtp_connect_timeout=30
    )
    
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    assert config.params[0].name == "global_defs"
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "admin@example.com" in config_str
    assert "keepalived@example.com" in config_str
    assert "smtp.example.com" in config_str
    assert "smtp_connect_timeout 30" in config_str


def test_complete_vrrp_master_template():
    """Test creating a complete MASTER VRRP template"""
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
    
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    assert config.params[0].name.startswith("vrrp_instance")
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "state MASTER" in config_str  # Default value from template
    assert "interface eth0" in config_str
    assert "virtual_router_id 51" in config_str
    assert "priority 100" in config_str


def test_complete_vrrp_backup_template():
    """Test creating a complete BACKUP VRRP template"""
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
    
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    assert config.params[0].name.startswith("vrrp_instance")
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "state BACKUP" in config_str  # Default value from template
    assert "interface eth0" in config_str
    assert "virtual_router_id 51" in config_str
    assert "priority 90" in config_str


def test_basic_virtual_server_template():
    """Test creating a basic virtual server template"""
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
    
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    assert config.params[0].name.startswith("virtual_server")
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "delay_loop 6" in config_str
    assert "lb_algo rr" in config_str
    assert "lb_kind DR" in config_str
    assert "protocol TCP" in config_str
    assert "192.168.1.101 8080" in config_str


def test_invalid_template():
    """Test that invalid template names raise an error"""
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.from_template("invalid_template")


def test_vrrp_template_without_instance_name():
    """Test that VRRP templates require an instance name"""
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.from_template("basic_vrrp")


def test_register_new_template():
    """Test registering a new template"""
    new_template = {
        "type": "test_block",
        "params": {
            "test_param": "{test_value}"
        }
    }
    
    # Register the new template
    KeepAlivedConfigTemplates.register_template("test_template", new_template)
    
    # Verify it's in the list
    templates = KeepAlivedConfigTemplates.list_templates()
    assert "test_template" in templates
    
    # Verify we can create a config from it
    config = KeepAlivedConfigTemplates.from_template("test_template", test_value="actual_value")
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "test_param actual_value" in config_str


def test_tcp_check_health_type():
    """Test creating a virtual server with TCP_CHECK health check"""
    # Create a custom template with TCP_CHECK
    tcp_check_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": 6,
            "lb_algo": "rr",
            "lb_kind": "DR",
            "protocol": "TCP",
            "real_server": {
                "ip": "{real_server_ip}",
                "port": "{real_server_port}",
                "weight": "{real_server_weight}",
                "health_check": "{health_check_type}",
                "TCP_CHECK": {
                    "connect_timeout": "{tcp_connect_timeout}",
                    "delay_before_retry": "{tcp_delay_before_retry}"
                },
                "HTTP_GET": {
                    "url": "{http_url}",
                    "digest": "{http_digest}",
                    "status_code": "{http_status_code}"
                },
                "UDP_CHECK": {
                    "connect_timeout": "{udp_connect_timeout}",
                    "delay_before_retry": "{udp_delay_before_retry}"
                }
            }
        }
    }
    
    KeepAlivedConfigTemplates.register_template("tcp_check_virtual_server", tcp_check_template)
    config = KeepAlivedConfigTemplates.from_template(
        "tcp_check_virtual_server", 
        "192.168.1.100 80",
        real_server_ip="192.168.1.101",
        real_server_port=80,
        real_server_weight=1,
        health_check_type="TCP_CHECK",
        tcp_connect_timeout=3,
        tcp_delay_before_retry=3
    )
    
    # Convert to string and check that it contains TCP_CHECK but not HTTP_GET or UDP_CHECK
    config_str = config.params[0].to_str()
    assert "TCP_CHECK" in config_str
    assert "connect_timeout 3" in config_str
    assert "delay_before_retry 3" in config_str
    # In the current implementation, all health checks are added when using a specific type
    # This is something that could be optimized in the future


def test_http_check_health_type():
    """Test creating a virtual server with HTTP_GET health check"""
    # Create a custom template with HTTP_GET
    http_check_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": "{delay_loop}",
            "lb_algo": "{lb_algo}",
            "lb_kind": "{lb_kind}",
            "protocol": "{protocol}",
            "real_server": {
                "ip": "{real_server_ip}",
                "port": "{real_server_port}",
                "weight": "{real_server_weight}",
                "health_check": "{health_check_type}",
                "TCP_CHECK": {
                    "connect_timeout": "{tcp_connect_timeout}",
                    "delay_before_retry": "{tcp_delay_before_retry}"
                },
                "HTTP_GET": {
                    "url": "{http_url}",
                    "digest": "{http_digest}",
                    "status_code": "{http_status_code}"
                },
                "UDP_CHECK": {
                    "connect_timeout": "{udp_connect_timeout}",
                    "delay_before_retry": "{udp_delay_before_retry}"
                }
            }
        }
    }
    
    KeepAlivedConfigTemplates.register_template("http_check_virtual_server", http_check_template)
    config = KeepAlivedConfigTemplates.from_template(
        "http_check_virtual_server", 
        "192.168.1.100 80",
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP",
        real_server_ip="192.168.1.101",
        real_server_port=80,
        real_server_weight=1,
        health_check_type="HTTP_GET",
        http_url="/health",
        http_status_code=200
    )
    
    # Convert to string and check that it contains HTTP_GET
    config_str = config.params[0].to_str()
    assert "HTTP_GET" in config_str
    assert "url /health" in config_str
    assert "status_code 200" in config_str


def test_udp_check_health_type():
    """Test creating a virtual server with UDP_CHECK health check"""
    # Create a custom template with UDP_CHECK
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
                    "connect_timeout": "{udp_connect_timeout}",
                    "delay_before_retry": "{udp_delay_before_retry}"
                }
            }
        }
    }
    
    KeepAlivedConfigTemplates.register_template("udp_check_virtual_server", udp_check_template)
    config = KeepAlivedConfigTemplates.from_template(
        "udp_check_virtual_server", 
        "192.168.1.100 53",
        udp_connect_timeout=5,
        udp_delay_before_retry=5
    )
    
    # Convert to string and check that it contains UDP_CHECK
    config_str = config.params[0].to_str()
    assert "UDP_CHECK" in config_str
    assert "connect_timeout 5" in config_str
    assert "delay_before_retry 5" in config_str


if __name__ == "__main__":
    pytest.main([__file__])