#!/usr/bin/env python3
"""
Keepalived Config Exception Handling Usage Examples
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
    VRRPInstanceExistsError,
    VRRPInstanceNotFoundError,
    VirtualServerExistsError,
    VirtualServerNotFoundError,
    RealServerExistsError,
    RealServerNotFoundError,
    ConfigParseError,
    ConfigSaveError
)


def example_vrrp_exceptions():
    """Example: VRRP异常处理"""
    print("=== VRRP异常处理示例 ===")
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    print("1. 创建VRRP实例...")
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_EXCEPTION",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    if result:
        print("   VRRP实例创建成功")
    
    # 尝试创建同名实例（应该抛出VRRPInstanceExistsError异常）
    print("2. 尝试创建同名VRRP实例（应该抛出异常）...")
    try:
        vrrp_manager.create_vrrp_instance(
            instance_name="VI_EXCEPTION",
            state="BACKUP",
            interface="eth1",
            virtual_router_id=52,
            priority=90
        )
        print("   意外：没有抛出异常")
    except VRRPInstanceExistsError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    # 尝试删除不存在的实例（应该抛出VRRPInstanceNotFoundError异常）
    print("3. 尝试删除不存在的VRRP实例（应该抛出异常）...")
    try:
        vrrp_manager.remove_vrrp_instance("NON_EXISTENT")
        print("   意外：没有抛出异常")
    except VRRPInstanceNotFoundError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    print()


def example_virtual_server_exceptions():
    """Example: 虚拟服务器异常处理"""
    print("=== 虚拟服务器异常处理示例 ===")
    
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    print("1. 创建虚拟服务器...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    if result:
        print("   虚拟服务器创建成功")
    
    # 尝试创建同名虚拟服务器（应该抛出VirtualServerExistsError异常）
    print("2. 尝试创建同名虚拟服务器（应该抛出异常）...")
    try:
        vs_manager.create_virtual_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            delay_loop=10,
            lb_algo="wrr",
            lb_kind="DR",
            protocol="TCP"
        )
        print("   意外：没有抛出异常")
    except VirtualServerExistsError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    # 尝试删除不存在的虚拟服务器（应该抛出VirtualServerNotFoundError异常）
    print("3. 尝试删除不存在的虚拟服务器（应该抛出异常）...")
    try:
        vs_manager.remove_virtual_server("192.168.1.101", 8080)
        print("   意外：没有抛出异常")
    except VirtualServerNotFoundError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    print()


def example_real_server_exceptions():
    """Example: 真实服务器异常处理"""
    print("=== 真实服务器异常处理示例 ===")
    
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.2.100",
        virtual_server_port=443,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 为虚拟服务器添加真实服务器
    print("1. 为虚拟服务器添加真实服务器...")
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.2.100",
        virtual_server_port=443,
        real_server_ip="192.168.2.101",
        real_server_port=8443,
        weight=1
    )
    if result:
        print("   真实服务器添加成功")
    
    # 尝试添加同名真实服务器（应该抛出RealServerExistsError异常）
    print("2. 尝试添加同名真实服务器（应该抛出异常）...")
    try:
        vs_manager.add_real_server(
            virtual_server_ip="192.168.2.100",
            virtual_server_port=443,
            real_server_ip="192.168.2.101",
            real_server_port=8443,
            weight=2
        )
        print("   意外：没有抛出异常")
    except RealServerExistsError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    # 尝试删除不存在的真实服务器（应该抛出RealServerNotFoundError异常）
    print("3. 尝试删除不存在的真实服务器（应该抛出异常）...")
    try:
        vs_manager.remove_real_server(
            "192.168.2.100", 443,
            "192.168.2.102", 8444
        )
        print("   意外：没有抛出异常")
    except RealServerNotFoundError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    print()


def example_config_exceptions():
    """Example: 配置异常处理"""
    print("=== 配置异常处理示例 ===")
    
    # 创建输出目录
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # 测试配置管理器异常处理
    manager = KeepAlivedConfigManager()
    
    # 尝试加载不存在的配置文件（应该抛出ConfigParseError异常）
    print("1. 尝试加载不存在的配置文件...")
    try:
        manager.load_config("/non/existent/config.conf")
        print("   意外：没有抛出异常")
    except ConfigParseError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    # 尝试保存到无效路径（应该抛出ConfigSaveError异常）
    print("2. 尝试保存到无效路径...")
    try:
        manager.save_config("/invalid/path/config.conf")
        print("   意外：没有抛出异常")
    except ConfigSaveError as e:
        print(f"   正确捕获异常: {e}")
    except Exception as e:
        print(f"   意外异常: {e}")
    
    print()


def example_exception_inheritance():
    """Example: 异常继承关系"""
    print("=== 异常继承关系示例 ===")
    
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.3.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 演示异常继承关系
    print("1. 演示异常继承关系...")
    try:
        vs_manager.remove_virtual_server("192.168.3.101", 8080)
    except VirtualServerNotFoundError:
        print("   捕获到 VirtualServerNotFoundError")
    except Exception:
        print("   意外：没有捕获到正确的异常")
    
    # 使用基类捕获异常
    try:
        vs_manager.remove_virtual_server("192.168.3.101", 8080)
    except VirtualServerNotFoundError as e:
        print(f"   使用基类捕获异常: {type(e).__name__}")
    
    print()


if __name__ == "__main__":
    # Run all examples
    example_vrrp_exceptions()
    example_virtual_server_exceptions()
    example_real_server_exceptions()
    example_config_exceptions()
    example_exception_inheritance()
    
    print("异常处理示例完成!")