#!/usr/bin/env python3
"""
Keepalived Config VRRP Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_vrrp import KeepAlivedConfigVRRP
from keepalived_config.keepalived_config_exceptions import (
    VRRPInstanceExistsError,
    VRRPInstanceNotFoundError
)


def example_basic_vrrp_operations():
    """Example: Basic VRRP instance operations"""
    print("=== Basic VRRP Instance Operations ===")
    
    # 创建配置和VRRP管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建MASTER实例
    print("1. Creating MASTER VRRP instance...")
    master_result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secret123",
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    if master_result:
        print(f"   Created: {master_result.data.name}")
    else:
        print(f"   Failed to create: {master_result.message}")
    
    # 创建BACKUP实例
    print("2. Creating BACKUP VRRP instance...")
    backup_result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_2",
        state="BACKUP",
        interface="eth1",
        virtual_router_id=52,
        priority=90,
        nopreempt=True,
        preempt_delay=5
    )
    if backup_result:
        print(f"   Created: {backup_result.data.name}")
    else:
        print(f"   Failed to create: {backup_result.message}")
    
    # 列出所有实例
    print("3. Listing all VRRP instances:")
    instances = vrrp_manager.list_vrrp_instances()
    for instance in instances:
        print(f"   - {instance}")
    
    # 获取特定实例
    print("4. Getting specific VRRP instance:")
    vi1 = vrrp_manager.get_vrrp_instance("VI_1")
    if vi1:
        print(f"   Found: {vi1.name}")
        print("   Configuration:")
        print(vi1.to_str(1))  # 使用缩进以便查看
    
    # 更新实例
    print("5. Updating VRRP instance...")
    update_result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_2",
        priority=95,
        advert_int=2
    )
    if update_result:
        print("   Successfully updated VI_2")
    else:
        print(f"   Failed to update: {update_result.message}")
    
    # 显示更新后的配置
    vi2 = vrrp_manager.get_vrrp_instance("VI_2")
    if vi2:
        print("   Updated configuration:")
        print(vi2.to_str(1))
    
    # 删除实例
    print("6. Removing VRRP instance...")
    remove_result = vrrp_manager.remove_vrrp_instance("VI_2")
    if remove_result:
        print("   Successfully removed VI_2")
    else:
        print(f"   Failed to remove: {remove_result.message}")
    
    # 验证删除
    instances = vrrp_manager.list_vrrp_instances()
    print("7. Remaining VRRP instances:")
    for instance in instances:
        print(f"   - {instance}")
    
    print()


def example_advanced_vrrp_features():
    """Example: Advanced VRRP features"""
    print("=== Advanced VRRP Features ===")
    
    # 创建配置和VRRP管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建带高级选项的实例
    print("1. Creating VRRP instance with advanced options...")
    advanced_result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_ADVANCED",
        state="MASTER",
        interface="eth0",
        virtual_router_id=100,
        priority=150,
        advert_int=1,
        auth_type="PASS",
        auth_pass="ultrasecret",
        virtual_ipaddresses=["10.0.0.100/24"],
        nopreempt=False,
        preempt_delay=3,
        garp_master_delay=5
    )
    if advanced_result:
        print(f"   Created: {advanced_result.data.name}")
        print("   Configuration:")
        print(advanced_result.data.to_str(1))
    else:
        print(f"   Failed to create: {advanced_result.message}")
    
    # 动态更新虚拟IP地址
    print("2. Updating virtual IP addresses...")
    update_result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_ADVANCED",
        virtual_ipaddresses=["10.0.0.100/24", "10.0.1.100/24", "10.0.2.100/24"]
    )
    
    if update_result:
        print("   Successfully updated virtual IP addresses")
    else:
        print(f"   Failed to update: {update_result.message}")
    
    # 查看更新后的配置
    updated_block = vrrp_manager.get_vrrp_instance("VI_ADVANCED")
    if updated_block:
        print("   Updated configuration:")
        print(updated_block.to_str(1))
    
    print()


def example_error_handling():
    """Example: Error handling"""
    print("=== Error Handling ===")
    
    # 创建配置和VRRP管理器
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    print("1. Created VI_1 instance")
    
    # 尝试创建同名实例（应该失败）
    try:
        vrrp_manager.create_vrrp_instance(
            instance_name="VI_1",  # 同名
            state="BACKUP",
            interface="eth1",
            virtual_router_id=52,
            priority=90
        )
        print("2. Unexpected: No exception was thrown")
    except VRRPInstanceExistsError as e:
        print(f"2. Correctly caught error: {e}")
    
    # 尝试更新不存在的实例（应该抛出异常）
    try:
        vrrp_manager.update_vrrp_instance(
            instance_name="NON_EXISTENT",
            priority=100
        )
        print("3. Unexpected: No exception was thrown")
    except VRRPInstanceNotFoundError as e:
        print(f"3. Correctly caught error: {e}")
    
    # 尝试删除不存在的实例（应该返回失败结果）
    try:
        result = vrrp_manager.remove_vrrp_instance("NON_EXISTENT")
        print(f"4. Unexpected: No exception was thrown, result: {result.success}")
    except VRRPInstanceNotFoundError as e:
        print(f"4. Correctly caught error: {e}")
    
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_basic_vrrp_operations()
    example_advanced_vrrp_features()
    example_error_handling()
    
    print("VRRP usage examples completed successfully!")