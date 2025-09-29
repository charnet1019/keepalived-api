import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_vrrp import KeepAlivedConfigVRRP
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam


def test_create_vrrp_instance():
    """Test creating a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="secret123",
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    # 验证实例已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "vrrp_instance VI_1"
    
    # 验证配置中包含该实例
    assert len(config.params) == 1
    assert config.params[0] == result.data


def test_get_vrrp_instance():
    """Test getting a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    # 获取实例
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_1")
    assert vrrp_block is not None
    assert isinstance(vrrp_block, KeepAlivedConfigBlock)
    assert vrrp_block.name == "vrrp_instance VI_1"
    
    # 尝试获取不存在的实例
    non_existent = vrrp_manager.get_vrrp_instance("VI_2")
    assert non_existent is None


def test_create_duplicate_vrrp_instance():
    """Test creating a duplicate VRRP instance raises VRRPInstanceExistsError"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建第一个实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    # 尝试创建同名实例应该抛出VRRPInstanceExistsError异常
    from keepalived_config.keepalived_config_exceptions import VRRPInstanceExistsError
    with pytest.raises(VRRPInstanceExistsError):
        vrrp_manager.create_vrrp_instance(
            instance_name="VI_1",
            state="BACKUP",
            interface="eth1",
            virtual_router_id=52,
            priority=90
        )


def test_remove_vrrp_instance():
    """Test removing a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    # 确保实例存在
    assert len(config.params) == 1
    
    # 删除实例
    result = vrrp_manager.remove_vrrp_instance("VI_1")
    assert result.success is True
    assert len(config.params) == 0
    
    # 尝试删除不存在的实例应该抛出VRRPInstanceNotFoundError异常
    from keepalived_config.keepalived_config_exceptions import VRRPInstanceNotFoundError
    with pytest.raises(VRRPInstanceNotFoundError):
        vrrp_manager.remove_vrrp_instance("VI_2")


def test_update_vrrp_instance():
    """Test updating a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1
    )
    
    # 更新实例
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_1",
        state="BACKUP",
        priority=90,
        advert_int=2
    )
    
    assert result.success is True
    
    # 验证更新是否生效
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_1")
    state_param = None
    priority_param = None
    advert_int_param = None
    
    for param in vrrp_block.params:
        if isinstance(param, KeepAlivedConfigParam):
            if param.name == "state":
                state_param = param
            elif param.name == "priority":
                priority_param = param
            elif param.name == "advert_int":
                advert_int_param = param
    
    assert state_param is not None and state_param.value == "BACKUP"
    assert priority_param is not None and priority_param.value == "90"
    assert advert_int_param is not None and advert_int_param.value == "2"


def test_list_vrrp_instances():
    """Test listing VRRP instances"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建多个VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_2",
        state="BACKUP",
        interface="eth1",
        virtual_router_id=52,
        priority=90
    )
    
    # 列出所有实例
    instances = vrrp_manager.list_vrrp_instances()
    assert len(instances) == 2
    assert "VI_1" in instances
    assert "VI_2" in instances


def test_create_vrrp_instance_with_optional_params():
    """Test creating a VRRP instance with optional parameters"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个带可选参数的VRRP实例
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        nopreempt=True,
        preempt_delay=5,
        garp_master_delay=10
    )
    
    # 验证可选参数是否正确添加
    assert result.success is True
    vrrp_block = result.data
    
    nopreempt_param = None
    preempt_delay_param = None
    garp_master_delay_param = None
    
    for param in vrrp_block.params:
        if isinstance(param, KeepAlivedConfigParam):
            if param.name == "nopreempt":
                nopreempt_param = param
            elif param.name == "preempt_delay":
                preempt_delay_param = param
            elif param.name == "garp_master_delay":
                garp_master_delay_param = param
    
    assert nopreempt_param is not None
    assert preempt_delay_param is not None and preempt_delay_param.value == "5"
    assert garp_master_delay_param is not None and garp_master_delay_param.value == "10"


def test_update_vrrp_instance_virtual_ips():
    """Test updating virtual IP addresses of a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    # 更新虚拟IP地址
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_1",
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    
    assert result.success is True
    
    # 验证更新是否生效
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_1")
    vip_block = None
    
    for param in vrrp_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "virtual_ipaddress":
            vip_block = param
            break
    
    assert vip_block is not None
    assert len(vip_block.params) == 2


def test_create_vrrp_instance_without_virtual_ips():
    """Test creating a VRRP instance without virtual IP addresses"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个没有虚拟IP地址的VRRP实例
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_NO_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=53,
        priority=100
        # 不提供virtual_ipaddresses参数
    )
    
    # 验证实例已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "vrrp_instance VI_NO_VIP"
    
    # 验证没有virtual_ipaddress块
    vip_block = None
    for param in result.data.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "virtual_ipaddress":
            vip_block = param
            break
    
    # 应该没有virtual_ipaddress块
    assert vip_block is None


def test_create_vrrp_instance_with_multiple_virtual_ips():
    """Test creating a VRRP instance with multiple virtual IP addresses"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个带多个虚拟IP地址的VRRP实例
    virtual_ips = [
        "192.168.1.100/24",
        "192.168.2.100/24",
        "10.0.0.100/24",
        "172.16.1.100/24"
    ]
    
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_MULTI_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=54,
        priority=100,
        virtual_ipaddresses=virtual_ips
    )
    
    # 验证实例已创建
    assert result.success is True
    
    # 查找virtual_ipaddress块
    vip_block = None
    for param in result.data.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "virtual_ipaddress":
            vip_block = param
            break
    
    # 验证virtual_ipaddress块存在
    assert vip_block is not None
    assert len(vip_block.params) == len(virtual_ips)
    
    # 验证每个IP地址都正确添加
    for i, expected_ip in enumerate(virtual_ips):
        assert isinstance(vip_block.params[i], KeepAlivedConfigParam)
        assert vip_block.params[i].value == expected_ip


def test_update_vrrp_instance_remove_all_virtual_ips():
    """Test updating a VRRP instance to remove all virtual IP addresses"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个带虚拟IP地址的VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_REMOVE_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=55,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    
    # 更新为不包含虚拟IP地址
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_REMOVE_VIP",
        virtual_ipaddresses=[]  # 空列表应该移除virtual_ipaddress块
    )
    
    assert result.success is True
    
    # 验证virtual_ipaddress块已被移除
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_REMOVE_VIP")
    vip_block = None
    
    for param in vrrp_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "virtual_ipaddress":
            vip_block = param
            break
    
    # 应该没有virtual_ipaddress块
    assert vip_block is None


def test_update_vrrp_instance_change_virtual_ips_completely():
    """Test completely changing virtual IP addresses of a VRRP instance"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建一个带初始虚拟IP地址的VRRP实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_CHANGE_VIP",
        state="MASTER",
        interface="eth0",
        virtual_router_id=56,
        priority=100,
        virtual_ipaddresses=["192.168.1.100/24", "192.168.2.100/24"]
    )
    
    # 完全更换为新的虚拟IP地址集合
    new_virtual_ips = ["10.0.0.100/24", "10.0.1.100/24", "10.0.2.100/24"]
    result = vrrp_manager.update_vrrp_instance(
        instance_name="VI_CHANGE_VIP",
        virtual_ipaddresses=new_virtual_ips
    )
    
    assert result.success is True
    
    # 验证更新是否生效
    vrrp_block = vrrp_manager.get_vrrp_instance("VI_CHANGE_VIP")
    vip_block = None
    
    for param in vrrp_block.params:
        if isinstance(param, KeepAlivedConfigBlock) and param.name == "virtual_ipaddress":
            vip_block = param
            break
    
    assert vip_block is not None
    assert len(vip_block.params) == len(new_virtual_ips)
    
    # 验证新的IP地址都正确添加
    for i, expected_ip in enumerate(new_virtual_ips):
        assert isinstance(vip_block.params[i], KeepAlivedConfigParam)
        assert vip_block.params[i].value == expected_ip


def test_invalid_parameters():
    """Test that invalid parameters return appropriate failure results"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 测试无效的状态
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="INVALID",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    assert result.success is False
    assert "状态" in result.message
    
    # 测试无效的虚拟路由器ID
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=300,  # 超出范围
        priority=100
    )
    
    assert result.success is False
    assert "虚拟路由器ID" in result.message


def test_create_vrrp_instance_from_template():
    """Test creating a VRRP instance from template"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 从模板创建VRRP实例
    result = vrrp_manager.create_from_template(
        template_name="basic_vrrp",
        instance_name="VI_TEMPLATE",
        state="MASTER",
        interface="eth0",
        virtual_router_id=100,
        priority=150,
        advert_int=1,
        auth_type="PASS",
        auth_pass="template_password",
        virtual_ipaddress="10.0.0.100/24"
    )
    
    # 验证实例已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "vrrp_instance VI_TEMPLATE"
    
    # 验证配置中包含该实例
    assert len(config.params) == 1
    assert config.params[0] == result.data
    
    # 验证参数是否正确替换
    config_str = result.data.to_str()
    assert "state MASTER" in config_str
    assert "interface eth0" in config_str
    assert "virtual_router_id 100" in config_str
    assert "priority 150" in config_str


def test_create_vrrp_instance_from_template_invalid_template():
    """Test creating a VRRP instance from invalid template returns failure"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 从不存在的模板创建VRRP实例应该返回失败
    result = vrrp_manager.create_from_template(
        template_name="invalid_template",
        instance_name="VI_INVALID"
    )
    
    assert result.success is False
    assert "模板" in result.message


def test_create_duplicate_vrrp_instance_from_template():
    """Test creating a duplicate VRRP instance from template returns failure"""
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 首先创建一个实例
    vrrp_manager.create_vrrp_instance(
        instance_name="VI_1",
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100
    )
    
    # 尝试从模板创建同名实例应该返回失败
    result = vrrp_manager.create_from_template(
        template_name="basic_vrrp",
        instance_name="VI_1",  # 同名
        state="BACKUP",
        interface="eth1",
        virtual_router_id=52,
        priority=90
    )
    
    assert result.success is False
    assert "已存在" in result.message


def test_create_vrrp_instance_with_config_object():
    """Test creating a VRRP instance with config object"""
    from keepalived_config.keepalived_config_types import VRRPConfig
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建VRRP配置对象
    vrrp_config = VRRPConfig(
        state="MASTER",
        interface="eth0",
        virtual_router_id=51,
        priority=100,
        advert_int=1,
        auth_type="PASS",
        auth_pass="config_password"
    )
    
    # 使用配置对象创建VRRP实例
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_CONFIG",
        config=vrrp_config,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    # 验证实例已创建
    assert result.success is True
    assert isinstance(result.data, KeepAlivedConfigBlock)
    assert result.data.name == "vrrp_instance VI_CONFIG"
    
    # 验证配置中包含该实例
    assert len(config.params) == 1
    assert config.params[0] == result.data
    
    # 验证参数是否正确设置
    config_str = result.data.to_str()
    assert "state MASTER" in config_str
    assert "interface eth0" in config_str
    assert "virtual_router_id 51" in config_str
    assert "priority 100" in config_str
    assert "auth_pass config_password" in config_str


def test_create_vrrp_instance_with_config_object_and_override():
    """Test creating a VRRP instance with config object and override parameters"""
    from keepalived_config.keepalived_config_types import VRRPConfig
    
    config = KeepAlivedConfig()
    vrrp_manager = KeepAlivedConfigVRRP(config)
    
    # 创建VRRP配置对象
    vrrp_config = VRRPConfig(
        state="BACKUP",
        interface="eth0",
        virtual_router_id=51,
        priority=90
    )
    
    # 使用配置对象创建VRRP实例，并覆盖部分参数
    result = vrrp_manager.create_vrrp_instance(
        instance_name="VI_OVERRIDE",
        config=vrrp_config,
        # 覆盖配置对象中的值
        state="MASTER",
        priority=100,
        advert_int=2,
        virtual_ipaddresses=["192.168.1.100/24"]
    )
    
    # 验证实例已创建
    assert result.success is True
    
    # 验证覆盖的参数是否生效
    config_str = result.data.to_str()
    assert "state MASTER" in config_str  # 被覆盖
    assert "interface eth0" in config_str  # 来自配置对象
    assert "virtual_router_id 51" in config_str  # 来自配置对象
    assert "priority 100" in config_str  # 被覆盖
    assert "advert_int 2" in config_str  # 被覆盖


if __name__ == "__main__":
    pytest.main([__file__])