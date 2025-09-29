#!/usr/bin/env python3
"""
Keepalived Config Manager Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config import KeepAlivedConfigManager, KeepAlivedConfigTemplates


def example_unified_management():
    """Example: 使用统一管理器进行配置管理"""
    print("=== 使用统一管理器进行配置管理 ===")
    
    # 创建配置管理器
    manager = KeepAlivedConfigManager()
    
    # 使用管理器创建VRRP实例
    print("1. 创建VRRP实例...")
    result = manager.vrrp.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secure_password",
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    if result:
        print(f"   VRRP实例创建成功: {result.data.name}")
    else:
        print(f"   VRRP实例创建失败: {result.message}")
    
    # 使用管理器从模板创建VRRP实例
    print("2. 从模板创建VRRP实例...")
    result = manager.vrrp.create_from_template(
        "complete_vrrp_backup",
        "VI_2",
        interface="eth1",
        virtual_router_id=52,
        priority=90,
        advert_int=2,
        auth_type="PASS",
        auth_pass="backup_password",
        virtual_ipaddress="192.168.2.100/24"
    )
    if result:
        print(f"   从模板创建VRRP实例成功: {result.data.name}")
    else:
        print(f"   从模板创建VRRP实例失败: {result.message}")
    
    # 使用管理器创建虚拟服务器
    print("3. 创建虚拟服务器...")
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
    
    # 使用管理器从模板创建虚拟服务器
    print("4. 从模板创建虚拟服务器...")
    result = manager.virtual_server.create_from_template(
        "basic_virtual_server",
        "192.168.1.100 443",
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP",
        real_server_ip="192.168.1.101",
        real_server_port=443,
        real_server_weight=1,
        health_check_type="TCP_CHECK",
        tcp_connect_timeout=3,
        tcp_delay_before_retry=3
    )
    if result:
        print(f"   从模板创建虚拟服务器成功: {result.data.name}")
    else:
        print(f"   从模板创建虚拟服务器失败: {result.message}")
    
    # 列出所有VRRP实例
    print("5. 所有VRRP实例:")
    for instance in manager.vrrp_instances:
        print(f"   - {instance}")
    
    # 列出所有虚拟服务器
    print("6. 所有虚拟服务器:")
    for vs in manager.virtual_servers:
        print(f"   - {vs}")
    
    # 验证配置
    print("7. 验证配置...")
    result = manager.validate()
    if result:
        print("   配置验证通过")
    else:
        print("   配置验证发现问题:")
        for issue in result.data:
            print(f"     - {issue}")
    
    # 保存配置
    print("8. 保存配置...")
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    config_file = os.path.join(examples_dir, "managed_config.conf")
    
    result = manager.save_config(config_file)
    if result:
        print(f"   配置保存成功: {config_file}")
    else:
        print(f"   配置保存失败: {result.message}")
    
    print()


def example_template_integration():
    """Example: 模板与管理器的集成使用"""
    print("=== 模板与管理器的集成使用 ===")
    
    # 创建配置管理器
    manager = KeepAlivedConfigManager()
    
    # 直接使用模板系统创建配置
    print("1. 直接使用模板系统创建配置...")
    template_config = KeepAlivedConfigTemplates.from_template(
        "basic_vrrp",
        "VI_TEMPLATE",
        state="MASTER",
        interface="eth0",
        virtual_router_id=100,
        priority=150,
        advert_int=1,
        auth_type="PASS",
        auth_pass="template_password",
        virtual_ipaddress="10.0.0.100/24"
    )
    
    # 将模板配置合并到管理器中
    if template_config.params:
        manager.config.params.append(template_config.params[0])
        print("   模板配置已合并到管理器中")
    
    # 现在可以通过管理器管理这个实例
    vrrp_instance = manager.vrrp.get_vrrp_instance("VI_TEMPLATE")
    if vrrp_instance:
        print(f"   通过管理器访问模板创建的实例: {vrrp_instance.name}")
    
    print()


if __name__ == "__main__":
    # Run all examples
    example_unified_management()
    example_template_integration()
    
    print("配置管理器使用示例完成!")