#!/usr/bin/env python3
"""
Keepalived Config Virtual Server Usage Examples
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_virtual_server import KeepAlivedConfigVirtualServer


def example_basic_virtual_server_operations():
    """Example: Basic virtual server operations"""
    print("=== Basic Virtual Server Operations ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建虚拟服务器
    print("1. Creating virtual servers...")
    result1 = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    if result1:
        print(f"   Created: {result1.data.name}")
    else:
        print(f"   Failed to create virtual server: {result1.message}")
    
    result2 = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=443,
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="NAT",
        protocol="TCP",
        persistence_timeout=300
    )
    if result2:
        print(f"   Created: {result2.data.name}")
    else:
        print(f"   Failed to create virtual server: {result2.message}")
    
    # 列出所有虚拟服务器
    print("2. Listing all virtual servers:")
    result = vs_manager.list_virtual_servers()
    if result:
        virtual_servers = result.data
        for vs in virtual_servers:
            print(f"   - {vs}")
    
    # 获取特定虚拟服务器
    print("3. Getting specific virtual server:")
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    if result:
        vs = result.data
        print(f"   Found: {vs.name}")
        print("   Configuration:")
        print(vs.to_str(1))
    else:
        print(f"   {result.message}")

    # 更新虚拟服务器
    print("4. Updating virtual server...")
    try:
        vs_manager.update_virtual_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            delay_loop=15,
            lb_algo="lc"
        )
        print("   Successfully updated virtual server")
        # 显示更新后的配置
        result = vs_manager.get_virtual_server("192.168.1.100", 80)
        if result:
            vs = result.data
            print("   Updated configuration:")
            print(vs.to_str(1))
    except VirtualServerNotFoundError as e:
        print(f"   Failed to update virtual server: {e}")

    # 删除虚拟服务器
    print("5. Removing virtual server...")
    result = vs_manager.remove_virtual_server("192.168.1.100", 443)
    if result:
        print("   Successfully removed virtual server")
    else:
        print(f"   Failed to remove virtual server: {result.message}")

    # 列出剩余的虚拟服务器
    print("6. Remaining virtual servers:")
    result = vs_manager.list_virtual_servers()
    if result:
        virtual_servers = result.data
        for vs in virtual_servers:
            print(f"   - {vs}")

    print()


def example_real_server_operations():
    """Example: Real server operations"""
    print("=== Real Server Operations ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建虚拟服务器
    print("1. Creating virtual server...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    if result:
        print("   Created virtual server: 192.168.1.100:80")
    else:
        print(f"   Failed to create virtual server: {result.message}")
        return
    
    # 为虚拟服务器添加真实服务器
    print("2. Attaching real servers to virtual server...")
    result1 = vs_manager.add_real_server(
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
    if result1:
        print(f"   Attached real server: {result1.data.name}")
    else:
        print(f"   Failed to attach real server: {result1.message}")
    
    result2 = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.102",
        real_server_port=8080,
        weight=2,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 5,
            "delay_before_retry": 5
        }
    )
    if result2:
        print(f"   Attached real server: {result2.data.name}")
    else:
        print(f"   Failed to attach real server: {result2.message}")
    
    # 列出虚拟服务器中的所有真实服务器
    print("3. Listing real servers in virtual server:")
    result = vs_manager.list_real_servers("192.168.1.100", 80)
    if result:
        real_servers = result.data
        for rs in real_servers:
            print(f"   - {rs}")
    
    # 获取特定的真实服务器
    print("4. Getting specific real server:")
    result = vs_manager.get_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
    if result:
        rs = result.data
        print(f"   Found: {rs.name}")
        print("   Configuration:")
        print(rs.to_str(2))
    else:
        print(f"   {result.message}")
    
    # 更新真实服务器
    print("5. Updating real server...")
    try:
        vs_manager.update_real_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            real_server_ip="192.168.1.101",
            real_server_port=8080,
            weight=3,
            health_check_params={
                "connect_timeout": 10
            }
        )
        print("   Successfully updated real server")
        # 显示更新后的配置
        result = vs_manager.get_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
        if result:
            print("   Updated configuration:")
            print(result.data.to_str(2))
    except RealServerNotFoundError as e:
        print(f"   Failed to update real server: {e}")
    
    # 删除真实服务器
    print("6. Detaching real server...")
    result = vs_manager.remove_real_server("192.168.1.100", 80, "192.168.1.102", 8080)
    if result:
        print("   Successfully detached real server")
    else:
        print(f"   Failed to detach real server: {result.message}")
    
    # 列出剩余的真实服务器
    print("7. Remaining real servers:")
    result = vs_manager.list_real_servers("192.168.1.100", 80)
    if result:
        real_servers = result.data
        for rs in real_servers:
            print(f"   - {rs}")

    print()


def example_http_health_check():
    """Example: HTTP health check configuration"""
    print("=== HTTP Health Check Configuration ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建虚拟服务器
    print("1. Creating virtual server...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.200",
        virtual_server_port=80,
        delay_loop=10,
        lb_algo="wlc",
        lb_kind="DR",
        protocol="TCP"
    )
    if result:
        print("   Created virtual server: 192.168.1.200:80")
    else:
        print(f"   Failed to create virtual server: {result.message}")
        return
    
    # 添加使用HTTP健康检查的真实服务器
    print("2. Attaching real server with HTTP health check...")
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.200",
        virtual_server_port=80,
        real_server_ip="192.168.1.201",
        real_server_port=80,
        weight=1,
        health_check="HTTP_GET",
        health_check_params={
            "url": "/health",
            "status_code": 200
        }
    )
    if result:
        print(f"   Attached real server with HTTP health check: {result.data.name}")
        print("   Configuration:")
        print(result.data.to_str(2))
    else:
        print(f"   Failed to attach real server: {result.message}")
    
    print()


def example_udp_health_check():
    """Example: UDP health check configuration"""
    print("=== UDP Health Check Configuration ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建UDP虚拟服务器
    print("1. Creating UDP virtual server...")
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.210",
        virtual_server_port=53,
        delay_loop=5,
        lb_algo="rr",
        lb_kind="DR",
        protocol="UDP"
    )
    if result:
        print("   Created DNS virtual server: 192.168.1.210:53")
    else:
        print(f"   Failed to create virtual server: {result.message}")
        return
    
    # 添加使用UDP健康检查的真实服务器
    print("2. Attaching real server with UDP health check...")
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.210",
        virtual_server_port=53,
        real_server_ip="192.168.1.211",
        real_server_port=53,
        weight=1,
        health_check="UDP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )
    if result:
        print(f"   Attached real server with UDP health check: {result.data.name}")
        print("   Configuration:")
        print(result.data.to_str(2))
    else:
        print(f"   Failed to attach real server: {result.message}")
    
    print()


def example_complex_scenario():
    """Example: Complex scenario with multiple virtual servers and real servers"""
    print("=== Complex Scenario ===")
    
    # 创建配置和虚拟服务器管理器
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建多个虚拟服务器
    print("1. Creating multiple virtual servers...")
    # HTTP虚拟服务器
    result = vs_manager.create_virtual_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP",
        persistence_timeout=300
    )
    if result:
        print("   Created HTTP virtual server: 10.0.0.100:80")
    else:
        print(f"   Failed to create HTTP virtual server: {result.message}")
    
    # HTTPS虚拟服务器
    result = vs_manager.create_virtual_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=443,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    if result:
        print("   Created HTTPS virtual server: 10.0.0.100:443")
    else:
        print(f"   Failed to create HTTPS virtual server: {result.message}")
    
    # DNS虚拟服务器
    result = vs_manager.create_virtual_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=53,
        delay_loop=5,
        lb_algo="lc",
        lb_kind="DR",
        protocol="UDP"
    )
    if result:
        print("   Created DNS virtual server: 10.0.0.100:53")
    else:
        print(f"   Failed to create DNS virtual server: {result.message}")
    
    # 为HTTP虚拟服务器添加真实服务器
    print("2. Attaching real servers to HTTP virtual server...")
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=80,
        real_server_ip="10.0.1.101",
        real_server_port=80,
        weight=1,
        health_check="HTTP_GET",
        health_check_params={
            "url": "/",
            "status_code": 200
        }
    )
    
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=80,
        real_server_ip="10.0.1.102",
        real_server_port=80,
        weight=2,
        health_check="HTTP_GET",
        health_check_params={
            "url": "/",
            "status_code": 200
        }
    )
    
    # 为HTTPS虚拟服务器添加真实服务器
    print("3. Attaching real servers to HTTPS virtual server...")
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=443,
        real_server_ip="10.0.1.101",
        real_server_port=443,
        weight=1,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3
        }
    )
    
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=443,
        real_server_ip="10.0.1.102",
        real_server_port=443,
        weight=2,
        health_check="TCP_CHECK",
        health_check_params={
            "connect_timeout": 3
        }
    )
    
    # 为DNS虚拟服务器添加真实服务器（使用UDP_CHECK）
    print("4. Attaching real servers to DNS virtual server...")
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=53,
        real_server_ip="10.0.1.101",
        real_server_port=53,
        weight=1,
        health_check="UDP_CHECK",
        health_check_params={
            "connect_timeout": 2,
            "delay_before_retry": 3
        }
    )
    
    vs_manager.add_real_server(
        virtual_server_ip="10.0.0.100",
        virtual_server_port=53,
        real_server_ip="10.0.1.102",
        real_server_port=53,
        weight=2,
        health_check="UDP_CHECK",
        health_check_params={
            "connect_timeout": 2,
            "delay_before_retry": 3
        }
    )
    
    # 显示完整配置
    print("5. Complete configuration:")
    result = vs_manager.list_virtual_servers()
    if result:
        for vs_name in result.data:
            ip, port = vs_name.split(" ", 1)
            result = vs_manager.get_virtual_server(ip, port)
            if result:
                vs_block = result.data
                print(f"\nvirtual_server {ip} {port}:")
                print(vs_block.to_str(1))
    
    print()


if __name__ == "__main__":
    # Create examples directory if it doesn't exist
    examples_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(examples_dir, exist_ok=True)
    
    # Run all examples
    example_basic_virtual_server_operations()
    example_real_server_operations()
    example_http_health_check()
    example_udp_health_check()
    example_complex_scenario()
    
    print("Virtual server usage examples completed successfully!")