import pytest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import (
    KeepAlivedConfig,
    KeepAlivedConfigVRRP,
    KeepAlivedConfigVirtualServer
)
from keepalived_config.keepalived_config_exceptions import (
    VRRPInstanceNotFoundError,
    VirtualServerNotFoundError,
    RealServerNotFoundError
)


def test_update_nonexistent_vrrp_instance():
    """Test that updating a non-existent VRRP instance raises VRRPInstanceNotFoundError"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    with pytest.raises(VRRPInstanceNotFoundError):
        vrrp_manager.update_vrrp_instance(
            instance_name="NON_EXISTENT",
            priority=100
        )


def test_update_nonexistent_virtual_server():
    """Test that updating a non-existent virtual server raises VirtualServerNotFoundError"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    with pytest.raises(VirtualServerNotFoundError):
        vs_manager.update_virtual_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            delay_loop=10
        )


def test_update_nonexistent_real_server():
    """Test that updating a non-existent real server raises RealServerNotFoundError"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 先创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    with pytest.raises(RealServerNotFoundError):
        vs_manager.update_real_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            real_server_ip="192.168.1.101",
            real_server_port=8080,
            weight=2
        )


if __name__ == "__main__":
    pytest.main([__file__])