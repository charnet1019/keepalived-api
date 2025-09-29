#!/usr/bin/env python3
"""
Keepalived Config Object Usage Examples
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


def example_vrrp_config_object():
    """Example: 使用VRRP配置对象"""
    print("=== 使用VRRP配置对象 ===")
    
    # 创建配置和VRRP管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建VRRP配置对象
    vrrp_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password"
    )
    
    # 使用配置对象创建VRRP实例
    print("1. 使用配置对象创建VRRP实例...")
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_CONFIG",
        config=vrrp_config,
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    
    if result:
        print(f"   VRRP实例创建成功: {result.data.name}")
        print("   配置内容:")
        print(result.data.to_str(1))
    else:
        print(f"   VRRP实例创建失败: {result.message}")
    
    # 使用配置对象和额外参数创建另一个实例
    print("2. 使用配置对象和额外参数创建VRRP实例...")
    vrrp_config_2 = VRRPConfig(
        state="BACKUP",
        interface="eth1",
        virtual_router_id=52,
        priority=90
    )
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_CONFIG_2",
        config=vrrp_config_2,
        # 覆盖配置对象中的值
        advert_int=2,
        nopreempt=True,
        preempt_delay=5
    )
    
    if result:
        print(f"   VRRP实例创建成功: {result.data.name}")
        print("   配置内容:")
        print(result.data.to_str(1))
    else:
        print(f"   VRRP实例创建失败: {result.message}")
    
    print()


def example_virtual_server_config_object():
    """Example: 使用虚拟服务器配置对象"""
    print("=== 使用虚拟服务器配置对象 ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建虚拟服务器配置对象
    vs_config = VirtualServerConfig(
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 使用配置对象创建虚拟服务器
    print("1. 使用配置对象创建虚拟服务器...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        config=vs_config,
        persistence_timeout=300
    )
    
    if result:
        print(f"   虚拟服务器创建成功: {result.data.name}")
        print("   配置内容:")
        print(result.data.to_str(1))
    else:
        print(f"   虚拟服务器创建失败: {result.message}")
    
    # 为虚拟服务器添加真实服务器
    print("2. 为虚拟服务器添加真实服务器...")
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    
    if result:
        print("   真实服务器添加成功")
    else:
        print(f"   真实服务器添加失败: {result.message}")
    
    print()


def example_combined_usage():
    """Example: 综合使用配置对象"""
    print("=== 综合使用配置对象 ===")
    
    # 创建配置和管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建多个VRRP实例
    print("1. 创建多个VRRP实例...")
    
    # MASTER实例
    master_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_MASTER",
        config=master_config,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    if result:
        print("   MASTER实例创建成功")
    else:
        print(f"   MASTER实例创建失败: {result.message}")
    
    # BACKUP实例
    backup_config = VRRPConfig(
        state="BACKUP",
        interface="eth1",
        virtual_router_id=52,
        priority=90
    )
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_BACKUP",
        config=backup_config,
        virtual_ipaddresses=["192.168.2.100/24"]
    )
    
    if result:
        print("   BACKUP实例创建成功")
    else:
        print(f"   BACKUP实例创建失败: {result.message}")
    
    # 创建虚拟服务器
    print("2. 创建虚拟服务器...")
    vs_config = VirtualServerConfig(
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        config=vs_config
    )
    
    if result:
        print("   虚拟服务器创建成功")
    else:
        print(f"   虚拟服务器创建失败: {result.message}")
    
    # 显示完整配置
    print("3. 完整配置:")
    for item in config.params:
        print(item.to_str())
    
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_vrrp_config_object()
    example_virtual_server_config_object()
    example_combined_usage()
    
    print("配置对象使用示例完成!")