import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_manager import KeepAlivedConfigManager
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock


def test_create_manager_with_default_config():
    """Test creating manager with default config"""
    manager = KeepAlivedConfigManager()
    
    assert manager.config is not None
    assert isinstance(manager.config, KeepAlivedConfig)
    assert manager.vrrp is not None
    assert manager.virtual_server is not None


def test_create_manager_with_custom_config():
    """Test creating manager with custom config"""
    custom_config = KeepAlivedConfig()
    manager = KeepAlivedConfigManager(custom_config)
    
    assert manager.config == custom_config
    assert manager.vrrp is not None
    assert manager.virtual_server is not None


def test_vrrp_operations_through_manager():
    """Test VRRP operations through manager"""
    manager = KeepAlivedConfigManager()
    
    # 通过管理器创建VRRP实例
    result = manager.vrrp.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    assert result.success is True
    
    # 通过管理器列出VRRP实例
    instances = manager.vrrp_instances
    assert len(instances) == 1
    assert "VI_1" in instances
    
    # 通过管理器获取VRRP实例
    vrrp_block = manager.vrrp.get_vrrp_instance("VI_1")
    assert vrrp_block is not None
    assert isinstance(vrrp_block, KeepAlivedConfigBlock)


def test_virtual_server_operations_through_manager():
    """Test virtual server operations through manager"""
    manager = KeepAlivedConfigManager()

    # 通过管理器创建虚拟服务器
    result = manager.virtual_server.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    assert result.success is True

    # 通过管理器列出虚拟服务器
    virtual_servers = manager.virtual_servers
    assert len(virtual_servers) == 1
    assert "192.168.1.100 80" in virtual_servers

    # 通过管理器获取虚拟服务器
    result = manager.virtual_server.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    vs_block = result.data
    assert isinstance(vs_block, KeepAlivedConfigBlock)


def test_validate_configuration():
    """Test configuration validation"""
    manager = KeepAlivedConfigManager()
    
    # 创建一个有效的VRRP实例
    manager.vrrp.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    # 创建一个有效的虚拟服务器
    manager.virtual_server.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 验证配置
    result = manager.validate()
    assert result.success is True


def test_vrrp_from_template_through_manager():
    """Test creating VRRP instance from template through manager"""
    manager = KeepAlivedConfigManager()
    
    # 通过管理器从模板创建VRRP实例
    result = manager.vrrp.create_from_template(
        template_name="basic_vrrp",
        instance_name="VI_TEMPLATE",
        state="MASTER",
        interface="eth0",
        virtual_router_id=100,
        priority=150
    )
    
    assert result.success is True
    
    # 验证实例已创建
    instances = manager.vrrp_instances
    assert len(instances) == 1
    assert "VI_TEMPLATE" in instances


def test_virtual_server_from_template_through_manager():
    """Test creating virtual server from template through manager"""
    manager = KeepAlivedConfigManager()
    
    # 通过管理器从模板创建虚拟服务器
    result = manager.virtual_server.create_from_template(
        template_name="basic_virtual_server",
        instance_name="192.168.1.100 80",
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    assert result.success is True
    
    # 验证虚拟服务器已创建
    virtual_servers = manager.virtual_servers
    assert len(virtual_servers) == 1
    assert "192.168.1.100 80" in virtual_servers


if __name__ == "__main__":
    pytest.main([__file__])