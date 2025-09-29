#!/usr/bin/env python3
"""
完整的Keepalived配置创建和保存示例
展示如何使用Keepalived Config SDK创建一个完整的keepalived.conf配置文件
"""

import sys
import os

# 添加src目录到路径以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import (
    KeepAlivedConfig,
    KeepAlivedConfigVRRP,
    KeepAlivedConfigVirtualServer,
    KeepAlivedConfigManager,
    VRRPConfig,
    VirtualServerConfig
)
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam


def create_complete_keepalived_configuration():
    """
    创建一个完整的Keepalived配置示例
    包含全局定义、VRRP实例和虚拟服务器配置
    """
    print("=== 创建完整的Keepalived配置 ===")
    
    # 创建配置管理器（这是推荐的统一入口）
    manager = KeepAlivedConfigManager()
    
    # 获取各个配置管理器
    config = manager.config
    vrrp_manager = manager.vrrp
    vs_manager = manager.virtual_server
    
    # 1. 添加全局定义部分
    print("1. 添加全局定义...")
    global_block = KeepAlivedConfigBlock("global_defs")
    global_block.add_param(KeepAlivedConfigParam("notification_email", "admin@company.com"))
    global_block.add_param(KeepAlivedConfigParam("notification_email_from", "keepalived@company.com"))
    global_block.add_param(KeepAlivedConfigParam("smtp_server", "smtp.company.com"))
    global_block.add_param(KeepAlivedConfigParam("smtp_connect_timeout", "30"))
    global_block.add_param(KeepAlivedConfigParam("router_id", "LVS_DEVEL"))
    config.params.append(global_block)
    
    # 2. 创建VRRP实例
    print("2. 创建VRRP实例...")
    
    # 创建MASTER实例
    master_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="1111",
        nopreempt=False
    )
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        config=master_config,
        virtual_ipaddresses=["192.168.200.10/24", "192.168.200.9/24"]
    )
    
    if result:
        print("   MASTER VRRP实例创建成功")
    else:
        print(f"   MASTER VRRP实例创建失败: {result.message}")
    
    # 创建BACKUP实例
    backup_config = VRRPConfig(
        state="BACKUP",
        interface="eth0",
        virtual_router_id=52,
        priority=90,
        advert_int=1,
        auth_type="PASS",
        auth_pass="1111",
        nopreempt=False
    )
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_2",
        config=backup_config,
        virtual_ipaddresses=["192.168.100.10/24"]
    )
    
    if result:
        print("   BACKUP VRRP实例创建成功")
    else:
        print(f"   BACKUP VRRP实例创建失败: {result.message}")
    
    # 3. 创建虚拟服务器
    print("3. 创建虚拟服务器...")
    
    # HTTP虚拟服务器
    http_vs_config = VirtualServerConfig(
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=80,
        config=http_vs_config
    )
    
    if result:
        print("   HTTP虚拟服务器创建成功")
    else:
        print(f"   HTTP虚拟服务器创建失败: {result.message}")
    
    # 为HTTP虚拟服务器添加真实服务器
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=80,
        real_server_ip="192.168.200.20",
        real_server_port=80,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    
    if result:
        print("   HTTP真实服务器1添加成功")
    else:
        print(f"   HTTP真实服务器1添加失败: {result.message}")
    
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=80,
        real_server_ip="192.168.200.21",
        real_server_port=80,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    
    if result:
        print("   HTTP真实服务器2添加成功")
    else:
        print(f"   HTTP真实服务器2添加失败: {result.message}")
    
    # HTTPS虚拟服务器
    https_vs_config = VirtualServerConfig(
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=443,
        config=https_vs_config
    )
    
    if result:
        print("   HTTPS虚拟服务器创建成功")
    else:
        print(f"   HTTPS虚拟服务器创建失败: {result.message}")
    
    # 为HTTPS虚拟服务器添加真实服务器
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=443,
        real_server_ip="192.168.200.20",
        real_server_port=443,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    
    if result:
        print("   HTTPS真实服务器1添加成功")
    else:
        print(f"   HTTPS真实服务器1添加失败: {result.message}")
    
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.200.10",
        virtual_server_port=443,
        real_server_ip="192.168.200.21",
        real_server_port=443,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    
    if result:
        print("   HTTPS真实服务器2添加成功")
    else:
        print(f"   HTTPS真实服务器2添加失败: {result.message}")
    
    # 4. 保存配置到文件
    print("4. 保存配置到文件...")
    
    # 创建输出目录
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # 保存配置文件
    config_file = os.path.join(examples_dir, "keepalived.conf")
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


def load_and_inspect_configuration(config_file):
    """
    加载并检查已保存的配置文件
    """
    print("\n=== 加载并检查配置文件 ===")
    
    # 使用管理器加载配置
    manager = KeepAlivedConfigManager()
    result = manager.load_config(config_file)
    
    if result:
        print("   配置加载成功")
        
        # 显示VRRP实例
        print("   VRRP实例:")
        for instance in manager.vrrp_instances:
            print(f"     - {instance}")
        
        # 显示虚拟服务器
        print("   虚拟服务器:")
        for vs in manager.virtual_servers:
            print(f"     - {vs}")
    else:
        print(f"   配置加载失败: {result.message}")


if __name__ == "__main__":
    # 创建完整配置
    config_file = create_complete_keepalived_configuration()
    
    # 加载并检查配置
    load_and_inspect_configuration(config_file)
    
    print("\n完整Keepalived配置示例完成!")