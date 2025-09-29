import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config_types import VRRPConfig, VirtualServerConfig


def test_vrrp_config_default_values():
    """Test VRRPConfig default values"""
    config = VRRPConfig()
    
    assert config.state == "BACKUP"
    assert config.interface == "eth0"
    assert config.virtual_router_id == 51
    assert config.priority == 100
    assert config.advert_int == 1
    assert config.auth_type == "PASS"
    assert config.auth_pass == ""
    assert config.virtual_ipaddresses == []
    assert config.nopreempt is False
    assert config.preempt_delay is None
    assert config.garp_master_delay is None


def test_vrrp_config_custom_values():
    """Test VRRPConfig with custom values"""
    config = VRRPConfig(
        state="MASTER",
        interface="eth1",
        virtual_router_id=100,
        priority=150,
        advert_int=2,
        auth_type="AH",
        auth_pass="mypassword",
        virtual_ipaddresses=["192.168.1.100/24"],
        nopreempt=True,
        preempt_delay=5,
        garp_master_delay=10,
        # 新增参数
        unicast_src_ip="192.168.1.1",
        unicast_peer=["192.168.1.2", "192.168.1.3"],
        smtp_alert=True,
        notify_master="/path/to/notify_master.sh",
        notify_backup="/path/to/notify_backup.sh",
        notify_fault="/path/to/notify_fault.sh"
    )
    
    assert config.state == "MASTER"
    assert config.interface == "eth1"
    assert config.virtual_router_id == 100
    assert config.priority == 150
    assert config.advert_int == 2
    assert config.auth_type == "AH"
    assert config.auth_pass == "mypassword"
    assert config.virtual_ipaddresses == ["192.168.1.100/24"]
    assert config.nopreempt is True
    assert config.preempt_delay == 5
    assert config.garp_master_delay == 10
    # 新增参数验证
    assert config.unicast_src_ip == "192.168.1.1"
    assert config.unicast_peer == ["192.168.1.2", "192.168.1.3"]
    assert config.smtp_alert is True
    assert config.notify_master == "/path/to/notify_master.sh"
    assert config.notify_backup == "/path/to/notify_backup.sh"
    assert config.notify_fault == "/path/to/notify_fault.sh"


def test_virtual_server_config_default_values():
    """Test VirtualServerConfig default values"""
    config = VirtualServerConfig()
    
    assert config.delay_loop == 6
    assert config.lb_algo == "rr"
    assert config.lb_kind == "DR"
    assert config.protocol == "TCP"
    assert config.persistence_timeout is None
    assert config.persistence_granularity is None
    assert config.virtualhost is None


def test_virtual_server_config_custom_values():
    """Test VirtualServerConfig with custom values"""
    config = VirtualServerConfig(
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="NAT",
        protocol="UDP",
        persistence_timeout=300,
        persistence_granularity="255.255.255.0",
        virtualhost="example.com",
        # 新增参数
        ha_suspend=True,
        alpha=True,
        omega=False,
        quorum=2,
        quorum_up="/path/to/quorum_up.sh",
        quorum_down="/path/to/quorum_down.sh",
        hysteresis=3,
        retry=5
    )
    
    assert config.delay_loop == 10
    assert config.lb_algo == "wrr"
    assert config.lb_kind == "NAT"
    assert config.protocol == "UDP"
    assert config.persistence_timeout == 300
    assert config.persistence_granularity == "255.255.255.0"
    assert config.virtualhost == "example.com"
    # 新增参数验证
    assert config.ha_suspend is True
    assert config.alpha is True
    assert config.omega is False
    assert config.quorum == 2
    assert config.quorum_up == "/path/to/quorum_up.sh"
    assert config.quorum_down == "/path/to/quorum_down.sh"
    assert config.hysteresis == 3
    assert config.retry == 5


if __name__ == "__main__":
    pytest.main([__file__])