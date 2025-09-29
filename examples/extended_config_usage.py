#!/usr/bin/env python3
"""
Keepalived Config Extended Parameters Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import (
    KeepAlivedConfig,
    KeepAlivedConfigVRRP,
    KeepAlivedConfigVirtualServer,
    VRRPConfig,
    VirtualServerConfig
)
from keepalived_config.keepalived_config_exceptions import VirtualServerNotFoundError


def example_extended_vrrp_config():
    """Example: 使用扩展的VRRP配置参数"""
    print("=== 使用扩展的VRRP配置参数 ===")
    
    # 创建配置和VRRP管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建带有扩展参数的VRRP配置对象
    vrrp_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password",
        # 扩展参数
        unicast_src_ip="192.168.1.1",
        unicast_peer=["192.168.1.2"],
        smtp_alert=True,
        notify_master="/etc/keepalived/scripts/notify_master.sh",
        notify_backup="/etc/keepalived/scripts/notify_backup.sh",
        notify_fault="/etc/keepalived/scripts/notify_fault.sh"
    )
    
    # 使用配置对象创建VRRP实例
    print("1. 使用扩展配置对象创建VRRP实例...")
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_EXTENDED",
        config=vrrp_config,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    if result:
        print(f"   VRRP实例创建成功: {result.data.name}")
        print("   配置内容:")
        print(result.data.to_str(1))
    else:
        print(f"   VRRP实例创建失败: {result.message}")
    
    print()


def example_extended_virtual_server_config():
    """Example: 使用扩展的虚拟服务器配置参数"""
    print("=== 使用扩展的虚拟服务器配置参数 ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建带有扩展参数的虚拟服务器配置对象
    vs_config = VirtualServerConfig(
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP",
        # 扩展参数
        ha_suspend=True,
        alpha=True,
        omega=True,
        quorum=2,
        quorum_up="/etc/keepalived/scripts/quorum_up.sh",
        quorum_down="/etc/keepalived/scripts/quorum_down.sh",
        hysteresis=3,
        retry=5
    )
    
    # 使用配置对象创建虚拟服务器
    print("1. 使用扩展配置对象创建虚拟服务器...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        config=vs_config
    )
    
    if result:
        print(f"   虚拟服务器创建成功: {result.data.name}")
        print("   配置内容:")
        print(result.data.to_str(1))
    else:
        print(f"   虚拟服务器创建失败: {result.message}")
    
    print()


def example_update_with_extended_parameters():
    """Example: 使用扩展参数更新配置"""
    print("=== 使用扩展参数更新配置 ===")
    
    # 创建配置和管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建基础VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_UPDATE_TEST",
        state="BACKUP",
        interface="eth0",
        virtual_router_id=52,
        priority=90
    )
    
    # 使用扩展参数更新VRRP实例
    print("1. 使用扩展参数更新VRRP实例...")
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_UPDATE_TEST",
        state="MASTER",
        priority=110,
        # 扩展参数
        unicast_src_ip="192.168.2.1",
        unicast_peer=["192.168.2.2", "192.168.2.3"],
        smtp_alert=True,
        notify_master="/etc/keepalived/scripts/master_changed.sh"
    )
    
    if result:
        print("   VRRP实例更新成功")
        vrrp_block = vrrp_manager.get_vrrp_instance("VI_UPDATE_TEST")
        print("   更新后的配置:")
        print(vrrp_block.to_str(1))
    else:
        print(f"   VRRP实例更新失败: {result.message}")
    
    # 创建基础虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.2.100",
        virtual_server_port=443,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 使用扩展参数更新虚拟服务器
    print("2. 使用扩展参数更新虚拟服务器...")
    try:
        vs_manager.update_virtual_server(
            virtual_server_ip="192.168.2.100",
            virtual_server_port=443,
            delay_loop=15,
            # 扩展参数
            ha_suspend=True,
            quorum=3,
            quorum_up="/etc/keepalived/scripts/vs_quorum_up.sh"
        )
        
        print("   虚拟服务器更新成功")
        result = vs_manager.get_virtual_server("192.168.2.100", 443)
        if result:
            vs_block = result.data
            print("   更新后的配置:")
            print(vs_block.to_str(1))
        else:
            print(f"   获取虚拟服务器配置失败: {result.message}")
    except VirtualServerNotFoundError as e:
        print(f"   虚拟服务器更新失败: {e}")
    
    # 获取虚拟服务器配置块
    result = vs_manager.get_virtual_server("192.168.2.100", 443)
    if result:
        vs_block = result.data
        print("   虚拟服务器配置块已获取")
        print("   配置内容:")
        print(vs_block.to_str(1))
    else:
        print(f"   获取虚拟服务器配置块失败: {result.message}")
    
    print()


if __name__ == "__main__":
    example_extended_vrrp_config()
    example_extended_virtual_server_config()
    example_update_with_extended_parameters()
    print("扩展配置参数使用示例完成!")