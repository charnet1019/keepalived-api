#!/usr/bin/env python3
"""
简单的Keepalived配置创建和保存示例
展示如何使用Keepalived Config SDK创建一个基本的keepalived.conf配置文件
"""

import sys
import os

# 添加src目录到路径以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import (
    KeepAlivedConfigManager,
    VRRPConfig,
    VirtualServerConfig
)


def create_simple_keepalived_configuration():
    """
    创建一个简单的Keepalived配置示例
    """
    print("=== 创建简单的Keepalived配置 ===")
    
    # 1. 创建配置管理器（推荐的统一入口）
    manager = KeepAlivedConfigManager()
    
    # 2. 创建VRRP实例（高可用配置）
    print("1. 创建VRRP实例...")
    
    # 使用配置对象创建MASTER实例
    master_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    result = manager.vrrp.create_vrrp_instance(
        instance_name="VI_1",
        config=master_config,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    if result:
        print("   MASTER VRRP实例创建成功")
    else:
        print(f"   MASTER VRRP实例创建失败: {result.message}")
    
    # 3. 创建虚拟服务器（负载均衡配置）
    print("2. 创建虚拟服务器...")
    
    # 使用配置对象创建HTTP虚拟服务器
    http_vs_config = VirtualServerConfig(
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    result = manager.virtual_server.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        config=http_vs_config
    )
    
    if result:
        print("   HTTP虚拟服务器创建成功")
    else:
        print(f"   HTTP虚拟服务器创建失败: {result.message}")
    
    # 为虚拟服务器添加真实服务器
    result = manager.virtual_server.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.10",
        real_server_port=80,
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
    
    # 4. 保存配置到文件
    print("3. 保存配置到文件...")
    
    # 创建输出目录
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # 保存配置文件
    config_file = os.path.join(examples_dir, "simple_keepalived.conf")
    result = manager.save_config(config_file)
    
    if result:
        print(f"   配置保存成功: {config_file}")
        # 显示配置内容
        print("\n生成的配置内容:")
        print("=" * 50)
        with open(config_file, 'r', encoding='utf-8') as f:
            print(f.read())
        print("=" * 50)
    else:
        print(f"   配置保存失败: {result.message}")
    
    return config_file


if __name__ == "__main__":
    # 创建简单配置
    config_file = create_simple_keepalived_configuration()
    print("\n简单Keepalived配置示例完成!")