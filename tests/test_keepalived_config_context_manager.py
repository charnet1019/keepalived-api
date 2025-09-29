import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_manager import KeepAlivedConfigManager
from keepalived_config.keepalived_config_vrrp import KeepAlivedConfigVRRP
from keepalived_config.keepalived_config_virtual_server import KeepAlivedConfigVirtualServer


def test_manager_context_manager():
    """Test KeepAlivedConfigManager context manager"""
    # 创建临时文件路径
    temp_config_file = os.path.join(os.path.dirname(__file__), "temp_config.conf")
    
    # 确保临时文件不存在
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)
    
    try:
        # 测试上下文管理器
        with KeepAlivedConfigManager(auto_save_path=temp_config_file) as manager:
            # 创建VRRP实例
            result = manager.vrrp.create_vrrp_instance(
                instance_name="VI_CTX_TEST",
                state="MASTER",
                interface="eth0",
                virtual_router_id=51,
                priority=100
            )
            assert result.success is True
            
            # 创建虚拟服务器
            result = manager.virtual_server.create_virtual_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                delay_loop=6,
                lb_algo="rr",
                lb_kind="DR",
                protocol="TCP"
            )
            assert result.success is True
        
        # 验证配置是否已自动保存
        assert os.path.exists(temp_config_file) is True
        
        # 验证保存的配置内容
        with open(temp_config_file, 'r') as f:
            content = f.read()
            assert "vrrp_instance VI_CTX_TEST" in content
            assert "virtual_server 192.168.1.100 80" in content
            
    finally:
        # 清理临时文件
        if os.path.exists(temp_config_file):
            os.remove(temp_config_file)


def test_manager_context_manager_without_auto_save():
    """Test KeepAlivedConfigManager context manager without auto save"""
    # 测试不设置自动保存路径的上下文管理器
    with KeepAlivedConfigManager() as manager:
        # 创建VRRP实例
        result = manager.vrrp.create_vrrp_instance(
            instance_name="VI_CTX_TEST2",
            state="BACKUP",
            interface="eth1",
            virtual_router_id=52,
            priority=90
        )
        assert result.success is True


def test_vrrp_context_manager():
    """Test KeepAlivedConfigVRRP context manager"""
    config = KeepAlivedConfig()
    
    with KeepAlivedConfigVRRP(config) as vrrp_manager:
        # 创建VRRP实例
        result = vrrp_manager.create_vrrp_instance(
            instance_name="VI_VRRP_CTX",
            state="MASTER",
            interface="eth0",
            virtual_router_id=53,
            priority=100
        )
        assert result.success is True
        
        # 验证实例已创建
        vrrp_instance = vrrp_manager.get_vrrp_instance("VI_VRRP_CTX")
        assert vrrp_instance is not None


def test_virtual_server_context_manager():
    """Test KeepAlivedConfigVirtualServer context manager"""
    config = KeepAlivedConfig()
    
    with KeepAlivedConfigVirtualServer(config) as vs_manager:
        # 创建虚拟服务器
        result = vs_manager.create_virtual_server(
            virtual_server_ip="192.168.2.100",
            virtual_server_port=443,
            delay_loop=10,
            lb_algo="wrr",
            lb_kind="DR",
            protocol="TCP"
        )
        assert result.success is True
        
        # 验证虚拟服务器已创建
        vs_instance = vs_manager.get_virtual_server("192.168.2.100", 443)
        assert vs_instance is not None


def test_combined_context_managers():
    """Test combined usage of multiple context managers"""
    config = KeepAlivedConfig()
    temp_config_file = os.path.join(os.path.dirname(__file__), "temp_combined_config.conf")
    
    # 确保临时文件不存在
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)
    
    try:
        # 组合使用多个上下文管理器
        with KeepAlivedConfigManager(config, auto_save_path=temp_config_file) as manager:
            with KeepAlivedConfigVRRP(config) as vrrp:
                result = vrrp.create_vrrp_instance(
                    instance_name="VI_COMBINED_CTX",
                    state="MASTER",
                    interface="eth0",
                    virtual_router_id=54,
                    priority=150
                )
                assert result.success is True
            
            with KeepAlivedConfigVirtualServer(config) as vs:
                result = vs.create_virtual_server(
                    virtual_server_ip="192.168.3.100",
                    virtual_server_port=8080,
                    delay_loop=6,
                    lb_algo="rr",
                    lb_kind="DR",
                    protocol="TCP"
                )
                assert result.success is True
        
        # 验证配置是否已保存
        assert os.path.exists(temp_config_file) is True
        
        # 验证保存的配置内容
        with open(temp_config_file, 'r') as f:
            content = f.read()
            assert "vrrp_instance VI_COMBINED_CTX" in content
            assert "virtual_server 192.168.3.100 8080" in content
            
    finally:
        # 清理临时文件
        if os.path.exists(temp_config_file):
            os.remove(temp_config_file)


if __name__ == "__main__":
    pytest.main([__file__])