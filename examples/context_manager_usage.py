#!/usr/bin/env python3
"""
Keepalived Config Context Manager Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import (
    KeepAlivedConfig,
    KeepAlivedConfigManager,
    KeepAlivedConfigVRRP,
    KeepAlivedConfigVirtualServer,
    VRRPConfig,
    VirtualServerConfig
)


def example_manager_context_manager():
    """Example: 使用配置管理器的上下文管理器"""
    print("=== 使用配置管理器的上下文管理器 ===")
    
    # 创建输出目录
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    config_file = os.path.join(examples_dir, "context_managed_config.conf")
    
    # 使用上下文管理器自动保存配置
    with KeepAlivedConfigManager(auto_save_path=config_file) as manager:
        # 创建VRRP实例
        print("1. 创建VRRP实例...")
        result = manager.vrrp.create_vrrp_instance(
            instance_name="VI_CTX_1",
            state="MASTER",
            interface="eth0",
            virtual_router_id=51,
            priority=100,
            advert_int=1,
            auth_type="PASS",
            auth_pass="context_password",
            virtual_ipaddresses=["192.168.1.100/24"]
        )
        if result:
            print(f"   VRRP实例创建成功: {result.data.name}")
        else:
            print(f"   VRRP实例创建失败: {result.message}")
        
        # 创建虚拟服务器
        print("2. 创建虚拟服务器...")
        result = manager.virtual_server.create_virtual_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            delay_loop=6,
            lb_algo="rr",
            lb_kind="DR",
            protocol="TCP"
        )
        if result:
            print(f"   虚拟服务器创建成功: {result.data.name}")
        else:
            print(f"   虚拟服务器创建失败: {result.message}")
        
        # 为虚拟服务器添加真实服务器
        print("3. 为虚拟服务器添加真实服务器...")
        result = manager.virtual_server.add_real_server(
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
        
        print("4. 配置将在上下文管理器退出时自动保存...")
    
    # 验证配置是否已保存
    if os.path.exists(config_file):
        print(f"5. 配置已成功保存到: {config_file}")
        with open(config_file, 'r') as f:
            print("   配置内容:")
            print(f.read())
    else:
        print("5. 配置保存失败")
    
    print()


def example_vrrp_context_manager():
    """Example: 使用VRRP管理器的上下文管理器"""
    print("=== 使用VRRP管理器的上下文管理器 ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 使用VRRP管理器的上下文管理器（主要用于确保资源正确处理）
    with vrrp_manager as vrrp:
        print("1. 在上下文管理器中创建VRRP实例...")
        result = vrrp.create_vrrp_instance(
            instance_name="VI_CTX_2",
            state="BACKUP",
            interface="eth1",
            virtual_router_id=52,
            priority=90
        )
        if result:
            print(f"   VRRP实例创建成功: {result.data.name}")
        else:
            print(f"   VRRP实例创建失败: {result.message}")
    
    print("2. VRRP上下文管理器使用完成")
    print()


def example_virtual_server_context_manager():
    """Example: 使用虚拟服务器管理器的上下文管理器"""
    print("=== 使用虚拟服务器管理器的上下文管理器 ===")
    
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 使用虚拟服务器管理器的上下文管理器
    with vs_manager as vs:
        print("1. 在上下文管理器中创建虚拟服务器...")
        result = vs.create_virtual_server(
            virtual_server_ip="192.168.2.100",
            virtual_server_port=443,
            delay_loop=10,
            lb_algo="wrr",
            lb_kind="DR",
            protocol="TCP"
        )
        if result:
            print(f"   虚拟服务器创建成功: {result.data.name}")
        else:
            print(f"   虚拟服务器创建失败: {result.message}")
    
    print("2. 虚拟服务器上下文管理器使用完成")
    print()


def example_combined_context_managers():
    """Example: 组合使用多个上下文管理器"""
    print("=== 组合使用多个上下文管理器 ===")
    
    # 创建输出文件
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    config_file = os.path.join(examples_dir, "combined_context_config.conf")
    
    # 创建配置对象
    config = KeepAlivedConfig()
    
    # 组合使用多个上下文管理器
    with KeepAlivedConfigManager(config, auto_save_path=config_file) as manager:
        print("1. 使用管理器上下文创建配置...")
        
        # 使用配置对象创建VRRP管理器并使用其上下文管理器
        with KeepAlivedConfigVRRP(config) as vrrp:
            result = vrrp.create_vrrp_instance(
                instance_name="VI_COMBINED",
                state="MASTER",
                interface="eth0",
                virtual_router_id=100,
                priority=150
            )
            if result:
                print(f"   VRRP实例创建成功: {result.data.name}")
            else:
                print(f"   VRRP实例创建失败: {result.message}")
        
        # 使用配置对象创建虚拟服务器管理器并使用其上下文管理器
        with KeepAlivedConfigVirtualServer(config) as vs:
            result = vs.create_virtual_server(
                virtual_server_ip="10.0.0.100",
                virtual_server_port=80,
                delay_loop=6,
                lb_algo="rr",
                lb_kind="DR",
                protocol="TCP"
            )
            if result:
                print(f"   虚拟服务器创建成功: {result.data.name}")
            else:
                print(f"   虚拟服务器创建失败: {result.message}")
    
    # 验证配置是否已保存
    if os.path.exists(config_file):
        print(f"2. 配置已成功保存到: {config_file}")
    else:
        print("2. 配置保存失败")
    
    print()


if __name__ == "__main__":
    # Run all examples
    example_manager_context_manager()
    example_vrrp_context_manager()
    example_virtual_server_context_manager()
    example_combined_context_managers()
    
    print("上下文管理器使用示例完成!")