#!/usr/bin/env python3
"""
Keepalived Config Extended Templates Usage Examples
展示如何使用扩展的模板系统，包括注册、更新、获取和注销自定义模板
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates
from keepalived_config.keepalived_config import KeepAlivedConfig


def example_template_registration():
    """Example: 模板注册功能"""
    print("=== 模板注册功能示例 ===")
    
    # 定义一个自定义模板
    custom_vrrp_template = {
        "type": "vrrp_instance",
        "params": {
            "state": "{state}",
            "interface": "{interface}",
            "virtual_router_id": "{virtual_router_id}",
            "priority": "{priority}",
            "advert_int": "{advert_int}",
            "authentication": {
                "auth_type": "{auth_type}",
                "auth_pass": "{auth_pass}"
            },
            "virtual_ipaddress": ["{virtual_ipaddress}"],
            "nopreempt": "",
            "preempt_delay": "{preempt_delay}",
            "garp_master_delay": "{garp_master_delay}"
        }
    }
    
    # 注册自定义模板
    KeepAlivedConfigTemplates.register_template("custom_vrrp", custom_vrrp_template)
    print("1. 已注册自定义VRRP模板 'custom_vrrp'")
    
    # 检查模板是否已注册
    if KeepAlivedConfigTemplates.template_exists("custom_vrrp"):
        print("2. 确认模板 'custom_vrrp' 已存在")
    
    # 列出所有模板
    templates = KeepAlivedConfigTemplates.list_templates()
    print("3. 当前所有模板:")
    for template in templates:
        print(f"   - {template}")
    
    # 使用自定义模板
    print("4. 使用自定义模板创建配置:")
    config = KeepAlivedConfigTemplates.from_template(
        "custom_vrrp",
        "VI_CUSTOM",
        state="MASTER",
        interface="eth0",
        virtual_router_id=100,
        priority=150,
        advert_int=1,
        auth_type="PASS",
        auth_pass="custom_password",
        virtual_ipaddress="10.0.0.100/24",
        preempt_delay=5,
        garp_master_delay=10
    )
    print(config.params[0].to_str())
    print()


def example_template_management():
    """Example: 模板管理功能"""
    print("=== 模板管理功能示例 ===")
    
    # 获取模板定义
    try:
        template_def = KeepAlivedConfigTemplates.get_template("basic_vrrp")
        print("1. 获取 'basic_vrrp' 模板定义:")
        print(f"   类型: {template_def['type']}")
        print(f"   参数: {list(template_def['params'].keys())}")
    except ValueError as e:
        print(f"   错误: {e}")
    
    # 尝试获取不存在的模板
    try:
        KeepAlivedConfigTemplates.get_template("non_existent_template")
    except ValueError as e:
        print(f"2. 尝试获取不存在的模板: {e}")
    
    # 更新现有模板
    updated_template = {
        "type": "vrrp_instance",
        "params": {
            "state": "{state}",
            "interface": "{interface}",
            "virtual_router_id": "{virtual_router_id}",
            "priority": "{priority}",
            "advert_int": 2,  # 固定值
            "virtual_ipaddress": ["{virtual_ipaddress}"]
        }
    }
    
    try:
        KeepAlivedConfigTemplates.update_template("basic_vrrp", updated_template)
        print("3. 已更新 'basic_vrrp' 模板，将 advert_int 固定为 2")
        
        # 验证更新
        config = KeepAlivedConfigTemplates.from_template(
            "basic_vrrp",
            "VI_UPDATED",
            state="MASTER",
            interface="eth0",
            virtual_router_id=51,
            priority=100,
            virtual_ipaddress="192.168.1.100/24"
        )
        config_str = config.params[0].to_str()
        if "advert_int 2" in config_str:
            print("4. 验证更新成功，advert_int 被设置为 2")
        else:
            print("4. 验证更新失败")
        print(config.params[0].to_str())
    except ValueError as e:
        print(f"   错误: {e}")
    
    print()


def example_template_unregistration():
    """Example: 模板注销功能"""
    print("=== 模板注销功能示例 ===")
    
    # 注册一个临时模板
    temp_template = {
        "type": "custom_block",
        "params": {
            "custom_param": "{custom_value}"
        }
    }
    
    KeepAlivedConfigTemplates.register_template("temp_template", temp_template)
    print("1. 已注册临时模板 'temp_template'")
    
    # 确认模板存在
    if KeepAlivedConfigTemplates.template_exists("temp_template"):
        print("2. 确认模板 'temp_template' 存在")
    
    # 使用模板
    config = KeepAlivedConfigTemplates.from_template(
        "temp_template",
        custom_value="test_value"
    )
    print("3. 使用临时模板创建配置:")
    print(config.params[0].to_str())
    
    # 注销模板
    if KeepAlivedConfigTemplates.unregister_template("temp_template"):
        print("4. 已注销模板 'temp_template'")
    
    # 确认模板已不存在
    if not KeepAlivedConfigTemplates.template_exists("temp_template"):
        print("5. 确认模板 'temp_template' 已被成功注销")
    
    # 尝试使用已注销的模板
    try:
        KeepAlivedConfigTemplates.from_template("temp_template", custom_value="test")
    except ValueError as e:
        print(f"6. 尝试使用已注销的模板: {e}")
    
    print()


def example_advanced_custom_template():
    """Example: 高级自定义模板"""
    print("=== 高级自定义模板示例 ===")
    
    # 创建一个包含复杂结构的自定义模板
    advanced_template = {
        "type": "virtual_server",
        "params": {
            "delay_loop": "{delay_loop}",
            "lb_algo": "{lb_algo}",
            "lb_kind": "{lb_kind}",
            "protocol": "{protocol}",
            "persistence_timeout": "{persistence_timeout}",
            "real_server": {
                "ip": "{real_server_ip}",
                "port": "{real_server_port}",
                "weight": "{real_server_weight}",
                "health_check": "{health_check_type}",
                "TCP_CHECK": {
                    "connect_timeout": "{tcp_connect_timeout}",
                    "delay_before_retry": "{tcp_delay_before_retry}",
                    "warmup": "{tcp_warmup}",
                    "retry": "{tcp_retry}"
                },
                "HTTP_GET": {
                    "url": "{http_url}",
                    "digest": "{http_digest}",
                    "status_code": "{http_status_code}",
                    "warmup": "{http_warmup}",
                    "retry": "{http_retry}"
                },
                "SSL_GET": {
                    "url": "{ssl_url}",
                    "digest": "{ssl_digest}",
                    "status_code": "{ssl_status_code}",
                    "warmup": "{ssl_warmup}",
                    "retry": "{ssl_retry}",
                    "connect_port": "{ssl_connect_port}",
                    "bindto": "{ssl_bindto}"
                }
            }
        }
    }
    
    # 注册高级模板
    KeepAlivedConfigTemplates.register_template("advanced_virtual_server", advanced_template)
    print("1. 已注册高级虚拟服务器模板 'advanced_virtual_server'")
    
    # 使用模板创建包含SSL健康检查的配置
    config = KeepAlivedConfigTemplates.from_template(
        "advanced_virtual_server",
        "192.168.1.100 443",
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP",
        persistence_timeout=300,
        real_server_ip="192.168.1.101",
        real_server_port=443,
        real_server_weight=2,
        health_check_type="SSL_GET",
        ssl_url="/health",
        ssl_status_code=200,
        ssl_connect_port=443,
        ssl_warmup=5,
        ssl_retry=3
    )
    
    print("2. 使用高级模板创建SSL健康检查配置:")
    print(config.params[0].to_str())
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_template_registration()
    example_template_management()
    example_template_unregistration()
    example_advanced_custom_template()
    
    print("扩展模板系统使用示例完成!")