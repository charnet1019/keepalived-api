import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_virtual_server import KeepAlivedConfigVirtualServer
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam


def test_create_virtual_server():
    """Test creating a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 验证虚拟服务器已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "virtual_server 192.168.1.100 80"
    
    # 验证配置中包含该虚拟服务器
    assert len(config.params) == 1
    assert config.params[0] == result.data


def test_get_virtual_server():
    """Test getting a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    # 获取虚拟服务器
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "virtual_server 192.168.1.100 80"

    # 尝试获取不存在的虚拟服务器
    result = vs_manager.get_virtual_server("192.168.1.101", 8080)
    assert result.success is False
    assert result.data is None


def test_list_virtual_servers():
    """Test listing virtual servers"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建几个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=443,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    # 列出虚拟服务器
    result = vs_manager.list_virtual_servers()
    assert result.success is True
    assert isinstance(result.data, list)
    assert len(result.data) == 2
    assert "192.168.1.100 80" in result.data
    assert "192.168.1.100 443" in result.data

    # 清空配置后再次列出
    config.params.clear()
    result = vs_manager.list_virtual_servers()
    assert result.success is True
    assert isinstance(result.data, list)
    assert len(result.data) == 0


def test_create_duplicate_virtual_server():
    """Test creating a duplicate virtual server raises VirtualServerExistsError"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建第一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 尝试创建同名虚拟服务器应该抛出VirtualServerExistsError异常
    from keepalived_config.keepalived_config_exceptions import VirtualServerExistsError
    with pytest.raises(VirtualServerExistsError):
        vs_manager.create_virtual_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            delay_loop=10,
            lb_algo="wrr",
            lb_kind="DR",
            protocol="TCP"
        )


def test_remove_virtual_server():
    """Test removing a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 确保虚拟服务器存在
    assert len(config.params) == 1
    
    # 删除虚拟服务器
    result = vs_manager.remove_virtual_server("192.168.1.100", 80)
    assert result.success is True
    assert len(config.params) == 0
    
    # 尝试删除不存在的虚拟服务器应该抛出VirtualServerNotFoundError异常
    from keepalived_config.keepalived_config_exceptions import VirtualServerNotFoundError
    with pytest.raises(VirtualServerNotFoundError):
        vs_manager.remove_virtual_server("192.168.1.101", 8080)


def test_update_virtual_server():
    """Test updating a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    # 更新虚拟服务器
    result = vs_manager.update_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=15,
        lb_algo="lc"
    )
    assert result.success is True

    # 验证更新是否生效
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    vs_block = result.data
    
    delay_loop_param = None
    lb_algo_param = None
    lb_kind_param = None
    for param in vs_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "delay_loop":
            delay_loop_param = param
        elif isinstance(param, KeepAlivedConfigParam) and param.name == "lb_algo":
            lb_algo_param = param
        elif isinstance(param, KeepAlivedConfigParam) and param.name == "lb_kind":
            lb_kind_param = param

    assert delay_loop_param is not None and delay_loop_param.value == "15"
    assert lb_algo_param is not None and lb_algo_param.value == "lc"
    assert lb_kind_param is not None and lb_kind_param.value == "DR"


def test_add_real_server():
    """Test attaching a real server to a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 为虚拟服务器添加真实服务器 (TCP_CHECK)
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
    
    # 验证真实服务器已添加
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "real_server 192.168.1.101 8080"
    
    # 验证TCP_CHECK配置
    tcp_check_block = None
    for param in result.data.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "TCP_CHECK":
            tcp_check_block = param
            break
    
    assert tcp_check_block is not None
    
    # 验证TCP_CHECK参数
    connect_timeout_param = None
    delay_before_retry_param = None
    for param in tcp_check_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "connect_timeout":
            connect_timeout_param = param
        elif isinstance(param, KeepAlivedConfigParam) and param.name == "delay_before_retry":
            delay_before_retry_param = param
    
    assert connect_timeout_param is not None and connect_timeout_param.value == "3"
    assert delay_before_retry_param is not None and delay_before_retry_param.value == "3"
    
    # 验证真实服务器在虚拟服务器中
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    vs_block = result.data
    # 检查真实服务器块是否在虚拟服务器的参数中
    is_found = False
    for param in vs_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "real_server 192.168.1.101 8080":
            is_found = True
            break
    assert is_found


def test_create_virtual_server_from_template():
    """Test creating a virtual server from template"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 先清空配置以确保没有冲突
    config.params.clear()
    
    # 从模板创建虚拟服务器（提供所有必需参数）
    result = vs_manager.create_from_template(
        template_name="basic_virtual_server",
        instance_name="192.168.1.101 8080",
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP",
        real_server_ip="192.168.1.102",
        real_server_port=8081,
        real_server_weight=1
    )
    
    # 验证虚拟服务器已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "virtual_server 192.168.1.101 8080"
    
    # 验证配置中包含该虚拟服务器
    assert len(config.params) == 1
    assert config.params[0] == result.data
    
    # 验证参数是否正确替换
    config_str = result.data.to_str()
    assert "delay_loop 10" in config_str
    assert "lb_algo wrr" in config_str
    assert "lb_kind DR" in config_str
    assert "protocol TCP" in config_str


def test_create_virtual_server_from_template_invalid_template():
    """Test creating a virtual server from invalid template returns failure"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 从不存在的模板创建虚拟服务器应该返回失败
    result = vs_manager.create_from_template(
        template_name="invalid_template",
        instance_name="192.168.1.100 80"
    )
    
    assert result.success is False
    assert "模板" in result.message


def test_create_duplicate_virtual_server_from_template():
    """Test creating a duplicate virtual server from template returns failure"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 首先创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 尝试从模板创建同名虚拟服务器应该返回失败
    result = vs_manager.create_from_template(
        template_name="basic_virtual_server",
        instance_name="192.168.1.100 80",  # 同名
        delay_loop=10,
        lb_algo="wrr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    assert result.success is False
    assert "已存在" in result.message


def test_add_real_server_with_udp_check():
    """Test attaching a real server with UDP health check to a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=53,
        delay_loop=5,
        lb_algo="rr",
        lb_kind="DR",
        protocol="UDP"
    )

    # 为虚拟服务器添加真实服务器 (UDP_CHECK)
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=53,
        real_server_ip="192.168.1.101",
        real_server_port=53,
        weight=1,
        health_check="UDP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )

    # 验证真实服务器已添加
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "real_server 192.168.1.101 53"

    # 验证UDP_CHECK配置
    udp_check_block = None
    for param in result.data.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "UDP_CHECK":
            udp_check_block = param
            break

    assert udp_check_block is not None

    # 验证UDP_CHECK参数
    connect_timeout_param = None
    delay_before_retry_param = None
    for param in udp_check_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "connect_timeout":
            connect_timeout_param = param
        elif isinstance(param, KeepAlivedConfigParam) and param.name == "delay_before_retry":
            delay_before_retry_param = param

    assert connect_timeout_param is not None and connect_timeout_param.value == "3"
    assert delay_before_retry_param is not None and delay_before_retry_param.value == "3"

    # 验证真实服务器在虚拟服务器中
    result = vs_manager.get_virtual_server("192.168.1.100", 53)
    assert result.success is True
    vs_block = result.data
    # 检查真实服务器块是否在虚拟服务器的参数中
    is_found = False
    for param in vs_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "real_server 192.168.1.101 53":
            is_found = True
            break
    assert is_found


def test_update_real_server_with_udp_check():
    """Test updating a real server with UDP health check parameters"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=53,
        delay_loop=5,
        lb_algo="rr",
        lb_kind="DR",
        protocol="UDP"
    )

    # 为虚拟服务器添加真实服务器 (UDP_CHECK)
    vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=53,
        real_server_ip="192.168.1.101",
        real_server_port=53,
        weight=1,
        health_check="UDP_CHECK",
        health_check_params={
            "connect_timeout": 3,
            "delay_before_retry": 3
        }
    )

    # 更新UDP_CHECK参数
    result = vs_manager.update_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=53,
        real_server_ip="192.168.1.101",
        real_server_port=53,
        health_check_params={
            "connect_timeout": 5,
            "delay_before_retry": 5
        }
    )

    assert result.success is True

    # 验证更新是否生效
    result = vs_manager.get_real_server("192.168.1.100", 53, "192.168.1.101", 53)
    assert result.success is True
    rs_block = result.data
    
    # 验证UDP_CHECK参数更新
    udp_check_block = None
    for param in rs_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "UDP_CHECK":
            udp_check_block = param
            break

    assert udp_check_block is not None

    connect_timeout_param = None
    delay_before_retry_param = None
    for param in udp_check_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "connect_timeout":
            connect_timeout_param = param
        elif isinstance(param, KeepAlivedConfigParam) and param.name == "delay_before_retry":
            delay_before_retry_param = param

    assert connect_timeout_param is not None and connect_timeout_param.value == "5"
    assert delay_before_retry_param is not None and delay_before_retry_param.value == "5"


def test_get_real_server():
    """Test getting a real server from a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 为虚拟服务器添加真实服务器
    vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1
    )
    
    # 获取真实服务器
    result = vs_manager.get_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "real_server 192.168.1.101 8080"

    # 尝试获取不存在的虚拟服务器中的真实服务器
    result = vs_manager.get_real_server("192.168.1.101", 8080, "192.168.1.101", 8080)
    assert result.success is False
    assert result.data is None

    # 尝试获取不存在的真实服务器
    result = vs_manager.get_real_server("192.168.1.100", 80, "192.168.1.102", 8080)
    assert result.success is False
    assert result.data is None


def test_list_real_servers():
    """Test listing real servers in a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    # 为虚拟服务器添加几个真实服务器
    vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1
    )

    vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.102",
        real_server_port=8080,
        weight=2
    )

    # 列出真实服务器
    result = vs_manager.list_real_servers("192.168.1.100", 80)
    assert result.success is True
    assert isinstance(result.data, list)
    assert len(result.data) == 2
    assert "192.168.1.101 8080" in result.data
    assert "192.168.1.102 8080" in result.data

    # 尝试列出不存在的虚拟服务器中的真实服务器
    result = vs_manager.list_real_servers("192.168.1.101", 8080)
    assert result.success is False
    assert result.data is None

    # 清空虚拟服务器中的真实服务器后再次列出
    vs_manager.remove_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
    vs_manager.remove_real_server("192.168.1.100", 80, "192.168.1.102", 8080)
    result = vs_manager.list_real_servers("192.168.1.100", 80)
    assert result.success is True
    assert isinstance(result.data, list)
    assert len(result.data) == 0


def test_attach_duplicate_real_server():
    """Test attaching a duplicate real server raises RealServerExistsError"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)

    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )

    # 添加第一个真实服务器
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1
    )
    assert result.success is True

    # 尝试添加同名真实服务器应该抛出RealServerExistsError异常
    from keepalived_config.keepalived_config_exceptions import RealServerExistsError
    with pytest.raises(RealServerExistsError):
        vs_manager.add_real_server(
            virtual_server_ip="192.168.1.100",
            virtual_server_port=80,
            real_server_ip="192.168.1.101",
            real_server_port=8080,
            weight=2
        )


def test_remove_real_server():
    """Test detaching a real server from a virtual server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 为虚拟服务器添加真实服务器
    vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1
    )
    
    # 确保真实服务器存在
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    vs_block = result.data
    initial_count = len(vs_block.params)
    
    # 删除真实服务器
    result = vs_manager.remove_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
    assert result.success is True
    
    # 验证真实服务器已删除
    result = vs_manager.get_virtual_server("192.168.1.100", 80)
    assert result.success is True
    vs_block = result.data
    assert len(vs_block.params) == initial_count - 1
    
    # 尝试删除不存在的真实服务器应该抛出RealServerNotFoundError异常
    from keepalived_config.keepalived_config_exceptions import RealServerNotFoundError
    with pytest.raises(RealServerNotFoundError):
        vs_manager.remove_real_server("192.168.1.100", 80, "192.168.1.102", 8080)


def test_update_real_server():
    """Test updating a real server"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建一个虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 为虚拟服务器添加真实服务器
    vs_manager.add_real_server(
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
    
    # 更新真实服务器
    result = vs_manager.update_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=2,
        health_check_params={
            "connect_timeout": 5
        }
    )
    
    assert result.success is True
    
    # 验证更新是否生效
    result = vs_manager.get_real_server("192.168.1.100", 80, "192.168.1.101", 8080)
    assert result.success is True
    rs_block = result.data
    
    weight_param = None
    for param in rs_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "weight":
            weight_param = param
            break
    
    assert weight_param is not None and weight_param.value == "2"
    
    # 验证TCP_CHECK参数更新
    tcp_check_block = None
    for param in rs_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "TCP_CHECK":
            tcp_check_block = param
            break
    
    assert tcp_check_block is not None
    
    connect_timeout_param = None
    for param in tcp_check_block.params:
        if isinstance(param, KeepAlivedConfigParam) and param.name == "connect_timeout":
            connect_timeout_param = param
            break
    
    assert connect_timeout_param is not None and connect_timeout_param.value == "5"


def test_invalid_parameters():
    """Test that invalid parameters return appropriate failure results"""
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 测试无效的负载均衡算法
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="invalid",  # 无效算法
        lb_kind="DR",
        protocol="TCP"
    )
    
    assert result.success is False
    assert "负载均衡算法" in result.message
    
    # 测试无效的负载均衡类型
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="invalid",  # 无效类型
        protocol="TCP"
    )
    
    assert result.success is False
    assert "负载均衡类型" in result.message
    
    # 测试无效的健康检查类型
    # 首先创建虚拟服务器
    vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        delay_loop=6,
        lb_algo="rr",
        lb_kind="DR",
        protocol="TCP"
    )
    
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=1,
        health_check="INVALID_CHECK"  # 无效健康检查
    )
    
    assert result.success is False
    assert "健康检查类型" in result.message
    
    # 测试无效的真实服务器权重
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="192.168.1.101",
        real_server_port=8080,
        weight=-1  # 无效权重
    )
    assert result.success is False
    assert "权重" in result.message

    # 测试无效的真实服务器IP
    result = vs_manager.add_real_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        real_server_ip="",  # 无效IP
        real_server_port=8080,
        weight=1
    )
    assert result.success is False
    assert "真实服务器IP" in result.message

    # 测试不存在的虚拟服务器
    from keepalived_config.keepalived_config_exceptions import VirtualServerNotFoundError
    with pytest.raises(VirtualServerNotFoundError):
        vs_manager.add_real_server(
            virtual_server_ip="192.168.1.101",  # 不存在的虚拟服务器
            virtual_server_port=80,
            real_server_ip="192.168.1.101",
            real_server_port=8080,
            weight=1
        )


def test_create_virtual_server_with_config_object():
    """Test creating a virtual server with config object"""
    from keepalived_config.keepalived_config_types import VirtualServerConfig
    
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
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=80,
        config=vs_config,
        persistence_timeout=300
    )
    
    # 验证虚拟服务器已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "virtual_server 192.168.1.100 80"
    
    # 验证配置中包含该虚拟服务器
    assert len(config.params) == 1
    assert config.params[0] == result.data
    
    # 验证参数是否正确设置
    config_str = result.data.to_str()
    assert "delay_loop 10" in config_str
    assert "lb_algo wrr" in config_str
    assert "lb_kind DR" in config_str
    assert "protocol TCP" in config_str
    assert "persistence_timeout 300" in config_str


def test_create_virtual_server_with_config_object_and_override():
    """Test creating a virtual server with config object and override parameters"""
    from keepalived_config.keepalived_config_types import VirtualServerConfig
    
    config = KeepAlivedConfig()
    vs_manager = KeepAlivedConfigVirtualServer(config)
    
    # 创建虚拟服务器配置对象
    vs_config = VirtualServerConfig(
        delay_loop=6,
        lb_algo="rr",
        lb_kind="NAT",
        protocol="UDP"
    )
    
    # 使用配置对象创建虚拟服务器，并覆盖部分参数
    result = vs_manager.create_virtual_server(
        virtual_server_ip="192.168.1.100",
        virtual_server_port=443,
        config=vs_config,
        # 覆盖配置对象中的值
        lb_kind="DR",
        protocol="TCP"
    )
    
    # 验证虚拟服务器已创建
    assert result.success is True
    
    # 验证覆盖的参数是否生效
    config_str = result.data.to_str()
    assert "delay_loop 6" in config_str  # 来自配置对象
    assert "lb_algo rr" in config_str  # 来自配置对象
    assert "lb_kind DR" in config_str  # 被覆盖
    assert "protocol TCP" in config_str  # 被覆盖


if __name__ == "__main__":
    pytest.main([__file__])