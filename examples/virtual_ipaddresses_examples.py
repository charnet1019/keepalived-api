#!/usr/bin/env python3
"""
Keepalived Config VRRP Virtual IP Addresses Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_vrrp import KeepAlivedConfigVRRP


def example_add_vrrp_without_virtual_ips():
    """Example: Add VRRP instance without virtual IP addresses"""
    print("=== Add VRRP Instance Without Virtual IP Addresses ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 添加一个不带虚拟IP地址的VRRP实例
    vrrp_block = vrrp_manager.add_vrrp_instance(
        instance_name="VI_NO_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
        # 注意：没有提供virtual_ipaddresses参数
    )
    
    print("Added VRRP instance without virtual IP addresses:")
    print(vrrp_block.to_str(1))
    print()


def example_add_vrrp_with_multiple_virtual_ips():
    """Example: Add VRRP instance with multiple virtual IP addresses"""
    print("=== Add VRRP Instance With Multiple Virtual IP Addresses ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 添加一个带多个虚拟IP地址的VRRP实例
    virtual_ips = [
        "192.168.1.100/24",
        "192.168.2.100/24",
        "10.0.0.100/24",
        "172.16.1.100/24"
    ]
    
    vrrp_block = vrrp_manager.add_vrrp_instance(
        instance_name="VI_MULTI_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=52,
        priority=100,
        virtual_ipaddresses=virtual_ips
    )
    
    print("Added VRRP instance with multiple virtual IP addresses:")
    print(vrrp_block.to_str(1))
    print()


def example_update_virtual_ips():
    """Example: Update virtual IP addresses of existing VRRP instance"""
    print("=== Update Virtual IP Addresses of Existing VRRP Instance ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 首先添加一个带初始虚拟IP地址的VRRP实例
    vrrp_manager.add_vrrp_instance(
        instance_name="VI_UPDATE_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=53,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    
    print("Initial configuration:")
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_UPDATE_VIP")
    print(vrrp_block.to_str(1))
    
    # 更新虚拟IP地址
    new_virtual_ips = ["10.0.0.100/24", "10.0.1.100/24", "10.0.2.100/24"]
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_UPDATE_VIP",
        virtual_ipaddresses=new_virtual_ips
    )
    
    if result:
        print("Updated virtual IP addresses:")
        vrrp_block = vrrp_manager.get_vrrp_instance("VI_UPDATE_VIP")
        print(vrrp_block.to_str(1))
    print()


def example_remove_all_virtual_ips():
    """Example: Remove all virtual IP addresses from VRRP instance"""
    print("=== Remove All Virtual IP Addresses From VRRP Instance ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 首先添加一个带虚拟IP地址的VRRP实例
    vrrp_manager.add_vrrp_instance(
        instance_name="VI_REMOVE_ALL_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=54,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24", "192.168.3.100/24"]
    )
    
    print("Initial configuration with virtual IP addresses:")
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_REMOVE_ALL_VIP")
    print(vrrp_block.to_str(1))
    
    # 移除所有虚拟IP地址
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_REMOVE_ALL_VIP",
        virtual_ipaddresses=[]  # 空列表表示移除所有
    )
    
    if result:
        print("Configuration after removing all virtual IP addresses:")
        vrrp_block = vrrp_manager.get_vrrp_instance("VI_REMOVE_ALL_VIP")
        print(vrrp_block.to_str(1))
    print()


def example_complex_virtual_ip_scenario():
    """Example: Complex virtual IP address management scenario"""
    print("=== Complex Virtual IP Address Management Scenario ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 添加多个VRRP实例，每个有不同的虚拟IP配置
    print("1. Adding multiple VRRP instances with different virtual IP configurations:")
    
    # MASTER实例，单个虚拟IP
    vrrp_manager.add_vrrp_instance(
        instance_name="VI_MASTER_SINGLE",
        state="MASTER",
        interface="eth0",
        virtual_router_id=61,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    # BACKUP实例，多个虚拟IP
    vrrp_manager.add_vrrp_instance(
        instance_name="VI_BACKUP_MULTI",
        state="BACKUP",
        interface="eth1",
        virtual_router_id=62,
        priority=90,
        virtual_ipaddresses=["192.168.10.100/24", "192.168.11.100/24", "192.168.12.100/24"]
    )
    
    # 实例，无初始虚拟IP
    vrrp_manager.add_vrrp_instance(
        instance_name="VI_NO_INITIAL_VIP",
        state="BACKUP",
        interface="eth2",
        virtual_router_id=63,
        priority=80
    )
    
    # 显示所有实例
    instances = vrrp_manager.list_vrrp_instances()
    for instance_name in instances:
        print(f"\nInstance: {instance_name}")
        vrrp_block = vrrp_manager.get_vrrp_instance(instance_name)
        print(vrrp_block.to_str(1))
    
    # 为无初始虚拟IP的实例添加虚拟IP
    print("\n2. Adding virtual IP addresses to instance that initially had none:")
    vrrp_manager.update_vrrp_instance(
        instance_name="VI_NO_INITIAL_VIP",
        virtual_ipaddresses=["10.0.0.100/24", "10.0.1.100/24"]
    )
    
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_NO_INITIAL_VIP")
    print(vrrp_block.to_str(1))
    
    # 修改MASTER实例的虚拟IP
    print("\n3. Changing virtual IP addresses of MASTER instance:")
    vrrp_manager.update_vrrp_instance(
        instance_name="VI_MASTER_SINGLE",
        virtual_ipaddresses=["192.168.1.200/24", "192.168.2.200/24"]
    )
    
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_MASTER_SINGLE")
    print(vrrp_block.to_str(1))
    
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_add_vrrp_without_virtual_ips()
    example_add_vrrp_with_multiple_virtual_ips()
    example_update_virtual_ips()
    example_remove_all_virtual_ips()
    example_complex_virtual_ip_scenario()
    
    print("Virtual IP addresses examples completed successfully!")