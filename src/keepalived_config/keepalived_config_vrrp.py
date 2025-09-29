from typing import Optional, List, Dict, Any, Union
from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam
from keepalived_config.keepalived_config_comment import (
    KeepAlivedConfigComment,
    KeepAlivedConfigCommentTypes,
)
from keepalived_config.keepalived_config_constants import KeepAlivedConfigDefaults
from keepalived_config.keepalived_config_result import OperationResult
from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates
from keepalived_config.keepalived_config_types import VRRPConfig
from keepalived_config.keepalived_config_exceptions import (
    KeepAlivedConfigTypeError,
    VRRPInstanceExistsError,
    VRRPInstanceNotFoundError,
    VRRPParameterError
)
from keepalived_config.keepalived_config_base import KeepAlivedConfigBase
from keepalived_config.keepalived_config_validator import KeepAlivedConfigValidator


class KeepAlivedConfigVRRP(KeepAlivedConfigBase):
    """
    VRRP实例管理器，负责对Keepalived配置中的VRRP实例进行增删改查（CRUD）和配置管理。
    
    该类提供了以下核心功能：
    - 创建新的VRRP实例 (create_vrrp_instance)
    - 获取指定的VRRP实例 (get_vrrp_instance)
    - 删除现有的VRRP实例 (remove_vrrp_instance)
    - 更新VRRP实例的配置参数 (update_vrrp_instance)
    - 列出所有存在的VRRP实例 (list_vrrp_instances)
    - 从模板创建VRRP实例 (create_from_template)
    """

    def __init__(self, config: KeepAlivedConfig):
        """
        初始化VRRP管理器
        
        Args:
            config (KeepAlivedConfig): Keepalived配置对象
        """
        super().__init__()
        self.config = config

    def __enter__(self):
        """
        上下文管理器入口
        
        Returns:
            KeepAlivedConfigVRRP: VRRP管理器实例
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出
        
        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯信息
        """
        # VRRP管理器本身不处理自动保存，因为配置保存由KeepAlivedConfig处理
        pass

    def create_vrrp_instance(
        self, 
        instance_name: str,
        state: str = None,
        interface: str = None,
        virtual_router_id: int = None,
        priority: int = None,
        advert_int: int = None,
        auth_type: str = None,
        auth_pass: str = None,
        virtual_ipaddresses: List[str] = None,
        nopreempt: bool = None,
        preempt_delay: int = None,
        garp_master_delay: int = None,
        unicast_src_ip: str = None,
        unicast_peer: List[str] = None,
        smtp_alert: bool = None,
        notify_master: str = None,
        notify_backup: str = None,
        notify_fault: str = None,
        comments: List[KeepAlivedConfigComment] = None,
        config: VRRPConfig = None,
        **kwargs
    ) -> OperationResult:
        """
        创建VRRP实例
        
        Args:
            instance_name (str): 实例名称
            state (str): 状态 (MASTER/BACKUP)
            interface (str): 网络接口
            virtual_router_id (int): 虚拟路由器ID (0-255)
            priority (int): 优先级 (0-255)
            advert_int (int): 广播间隔（秒）
            auth_type (str): 认证类型 (PASS/AH)
            auth_pass (str): 认证密码
            virtual_ipaddresses (List[str]): 虚拟IP地址列表
            nopreempt (bool): 是否禁用抢占
            preempt_delay (int): 抢占延迟（秒）
            garp_master_delay (int): GARP主延迟（秒）
            unicast_src_ip (str): 单播源IP地址
            unicast_peer (List[str]): 单播对端IP地址列表
            smtp_alert (bool): 是否启用SMTP告警
            notify_master (str): 切换到MASTER状态时执行的脚本
            notify_backup (str): 切换到BACKUP状态时执行的脚本
            notify_fault (str): 发生故障时执行的脚本
            comments (List[KeepAlivedConfigComment]): 注释列表
            config (VRRPConfig): VRRP配置对象
            **kwargs: 其他参数，用于向后兼容
            
        Returns:
            OperationResult: 操作结果对象，包含创建的VRRP实例块
            
        Example:
            ```python
            # 使用传统方式创建VRRP实例
            result = vrrp_manager.create_vrrp_instance(
                instance_name="VI_1",
                state="MASTER",
                interface="eth0",
                virtual_router_id=51,
                priority=100,
                virtual_ipaddresses=["192.168.1.100/24"]
            )
            
            # 使用配置对象创建VRRP实例
            vrrp_config = VRRPConfig(
                state="MASTER",
                interface="eth0",
                virtual_router_id=51,
                priority=100
            )
            result = vrrp_manager.create_vrrp_instance(
                instance_name="VI_1",
                config=vrrp_config,
                virtual_ipaddresses=["192.168.1.100/24"]
            )
            
            if result:
                print(f"VRRP实例创建成功: {result.data.name}")
            else:
                print(f"创建失败: {result.message}")
            ```
            
        Raises:
            ValueError: 当参数无效时
            TypeError: 当参数类型错误时
            VRRPInstanceExistsError: 当VRRP实例已存在时
        """
        # 如果提供了配置对象，则使用配置对象的值作为默认值
        if config is not None:
            # 使用配置对象的值作为默认值
            state = state if state is not None else config.state
            interface = interface if interface is not None else config.interface
            virtual_router_id = virtual_router_id if virtual_router_id is not None else config.virtual_router_id
            priority = priority if priority is not None else config.priority
            advert_int = advert_int if advert_int is not None else config.advert_int
            auth_type = auth_type if auth_type is not None else config.auth_type
            auth_pass = auth_pass if auth_pass is not None else config.auth_pass
            virtual_ipaddresses = virtual_ipaddresses if virtual_ipaddresses is not None else config.virtual_ipaddresses
            nopreempt = nopreempt if nopreempt is not None else config.nopreempt
            preempt_delay = preempt_delay if preempt_delay is not None else config.preempt_delay
            garp_master_delay = garp_master_delay if garp_master_delay is not None else config.garp_master_delay
            # 新增参数
            unicast_src_ip = unicast_src_ip if unicast_src_ip is not None else config.unicast_src_ip
            unicast_peer = unicast_peer if unicast_peer is not None else config.unicast_peer
            smtp_alert = smtp_alert if smtp_alert is not None else config.smtp_alert
            notify_master = notify_master if notify_master is not None else config.notify_master
            notify_backup = notify_backup if notify_backup is not None else config.notify_backup
            notify_fault = notify_fault if notify_fault is not None else config.notify_fault
        
        # 如果没有提供配置对象，使用默认值
        if config is None:
            # 设置默认值
            state = state if state is not None else "BACKUP"
            interface = interface if interface is not None else "eth0"
            virtual_router_id = virtual_router_id if virtual_router_id is not None else 51
            priority = priority if priority is not None else 100
            advert_int = advert_int if advert_int is not None else 1
            auth_type = auth_type if auth_type is not None else "PASS"
            virtual_ipaddresses = virtual_ipaddresses if virtual_ipaddresses is not None else []
            nopreempt = nopreempt if nopreempt is not None else False
        
        # 参数验证
        try:
            KeepAlivedConfigValidator.validate_string(instance_name, "实例名称", allow_empty=False)
        except (KeepAlivedConfigTypeError, VRRPParameterError) as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_choice(state, "状态", ["MASTER", "BACKUP"])
        except VRRPParameterError as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_string(interface, "网络接口", allow_empty=False)
        except (KeepAlivedConfigTypeError, VRRPParameterError) as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_integer_in_range(virtual_router_id, "虚拟路由器ID", 0, 255)
        except VRRPParameterError as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_integer_in_range(priority, "优先级", 0, 255)
        except VRRPParameterError as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_positive_integer(advert_int, "广播间隔")
        except VRRPParameterError as e:
            return OperationResult.fail(str(e))
            
        if auth_type not in ["PASS", "AH"]:
            return OperationResult.fail("认证类型必须是 'PASS' 或 'AH'")
            
        if virtual_ipaddresses is None:
            virtual_ipaddresses = []
            
        # 检查是否已存在同名实例
        if self.get_vrrp_instance(instance_name) is not None:
            raise VRRPInstanceExistsError(f"VRRP实例 '{instance_name}' 已存在")
            
        # 创建VRRP实例块
        vrrp_block = KeepAlivedConfigBlock("vrrp_instance", instance_name, comments or [])
        
        # 添加基本参数
        vrrp_block.add_param(KeepAlivedConfigParam("state", state))
        vrrp_block.add_param(KeepAlivedConfigParam("interface", interface))
        vrrp_block.add_param(KeepAlivedConfigParam("virtual_router_id", str(virtual_router_id)))
        vrrp_block.add_param(KeepAlivedConfigParam("priority", str(priority)))
        vrrp_block.add_param(KeepAlivedConfigParam("advert_int", str(advert_int)))
        
        # 添加认证配置
        if auth_pass:
            auth_block = KeepAlivedConfigBlock("authentication")
            auth_block.add_param(KeepAlivedConfigParam("auth_type", auth_type))
            auth_block.add_param(KeepAlivedConfigParam("auth_pass", auth_pass))
            vrrp_block.add_param(auth_block)
        
        # 添加虚拟IP地址
        if virtual_ipaddresses:
            vip_block = KeepAlivedConfigBlock("virtual_ipaddress")
            for vip in virtual_ipaddresses:
                vip_block.add_param(KeepAlivedConfigParam("", vip))
            vrrp_block.add_param(vip_block)
            
        # 添加可选参数
        if nopreempt:
            vrrp_block.add_param(KeepAlivedConfigParam("nopreempt"))
            
        if preempt_delay is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("preempt_delay", str(preempt_delay)))
            
        if garp_master_delay is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("garp_master_delay", str(garp_master_delay)))
            
        # 添加新增参数
        if unicast_src_ip is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("unicast_src_ip", unicast_src_ip))
            
        if unicast_peer is not None:
            unicast_peer_block = KeepAlivedConfigBlock("unicast_peer")
            for peer in unicast_peer:
                unicast_peer_block.add_param(KeepAlivedConfigParam("", peer))
            vrrp_block.add_param(unicast_peer_block)
            
        if smtp_alert is not None:
            smtp_alert_param = "smtp_alert" if smtp_alert else "no_smtp_alert"
            vrrp_block.add_param(KeepAlivedConfigParam(smtp_alert_param))
            
        if notify_master is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("notify_master", notify_master))
            
        if notify_backup is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("notify_backup", notify_backup))
            
        if notify_fault is not None:
            vrrp_block.add_param(KeepAlivedConfigParam("notify_fault", notify_fault))
        
        # 添加到配置中
        self.config.params.append(vrrp_block)
        
        return OperationResult.ok(f"VRRP实例 '{instance_name}' 创建成功", vrrp_block)

    def create_from_template(self, template_name: str, instance_name: str, config: VRRPConfig = None, **kwargs) -> OperationResult:
        """
        从模板创建VRRP实例
        
        Args:
            template_name (str): 模板名称
            instance_name (str): 实例名称
            config (VRRPConfig): VRRP配置对象
            **kwargs: 模板参数
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 从模板创建VRRP实例
            vrrp_config = VRRPConfig(
                state="MASTER",
                interface="eth0",
                virtual_router_id=51,
                priority=100
            )
            result = vrrp_manager.create_from_template(
                "basic_vrrp",
                "VI_1",
                config=vrrp_config
            )
            
            # 或者直接传递参数
            result = vrrp_manager.create_from_template(
                "basic_vrrp",
                "VI_1",
                state="MASTER",
                interface="eth0",
                virtual_router_id=51,
                priority=100
            )
            
            if result:
                print("VRRP实例创建成功")
            else:
                print(f"创建失败: {result.message}")
            ```
        """
        # 如果提供了配置对象，将其属性转换为kwargs
        if config is not None:
            # 将配置对象的属性添加到kwargs中
            for attr_name, attr_value in config.__dict__.items():
                if attr_name not in kwargs:  # 只有在kwargs中没有时才添加
                    kwargs[attr_name] = attr_value
        
        try:
            # 使用模板创建VRRP实例配置
            template_config = KeepAlivedConfigTemplates.from_template(template_name, instance_name, **kwargs)
            
            # 检查是否已存在同名实例
            if self.get_vrrp_instance(instance_name) is not None:
                return OperationResult.fail(f"VRRP实例 '{instance_name}' 已存在")
            
            # 获取模板生成的VRRP块
            if template_config.params and isinstance(template_config.params[0], KeepAlivedConfigBlock):
                vrrp_block = template_config.params[0]
                # 添加到当前配置中
                self.config.params.append(vrrp_block)
                return OperationResult.ok(f"VRRP实例 '{instance_name}' 从模板 '{template_name}' 创建成功", vrrp_block)
            else:
                return OperationResult.fail("模板未生成有效的VRRP实例配置")
        except Exception as e:
            return OperationResult.fail(f"从模板创建VRRP实例失败: {str(e)}", e)

    def get_vrrp_instance(self, instance_name: str) -> Optional[KeepAlivedConfigBlock]:
        """
        获取指定名称的VRRP实例
        
        Args:
            instance_name (str): 实例名称
            
        Returns:
            Optional[KeepAlivedConfigBlock]: VRRP实例块，如果不存在则返回None
            
        Raises:
            KeepAlivedConfigTypeError: 当实例名称不是字符串时
        """
        if not isinstance(instance_name, str):
            raise KeepAlivedConfigTypeError(f"Instance name must be a string, got {type(instance_name)}")
            
        for param in self.config.params:
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("vrrp_instance") and \
               param.name.endswith(instance_name):
                return param
                
        return None

    def remove_vrrp_instance(self, instance_name: str) -> OperationResult:
        """
        删除指定名称的VRRP实例
        
        Args:
            instance_name (str): 实例名称
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 删除VRRP实例
            result = vrrp_manager.remove_vrrp_instance("VI_1")
            if result:
                print("VRRP实例删除成功")
            else:
                print(f"删除失败: {result.message}")
            ```
            
        Raises:
            KeepAlivedConfigTypeError: 当实例名称不是字符串时
            VRRPInstanceNotFoundError: 当VRRP实例不存在时
        """
        if not isinstance(instance_name, str):
            raise KeepAlivedConfigTypeError("实例名称必须是字符串")
            
        for i, param in enumerate(self.config.params):
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("vrrp_instance") and \
               param.name.endswith(instance_name):
                self.config.params.pop(i)
                return OperationResult.ok(f"VRRP实例 '{instance_name}' 删除成功")
                
        raise VRRPInstanceNotFoundError(f"VRRP实例 '{instance_name}' 不存在")

    def update_vrrp_instance(
        self,
        instance_name: str,
        state: str = None,
        interface: str = None,
        virtual_router_id: int = None,
        priority: int = None,
        advert_int: int = None,
        auth_type: str = None,
        auth_pass: str = None,
        virtual_ipaddresses: List[str] = None,
        nopreempt: bool = None,
        preempt_delay: int = None,
        garp_master_delay: int = None,
        unicast_src_ip: str = None,
        unicast_peer: List[str] = None,
        smtp_alert: bool = None,
        notify_master: str = None,
        notify_backup: str = None,
        notify_fault: str = None
    ) -> OperationResult:
        """
        更新VRRP实例配置
        
        Args:
            instance_name (str): 实例名称
            state (str): 状态 (MASTER/BACKUP)
            interface (str): 网络接口
            virtual_router_id (int): 虚拟路由器ID (0-255)
            priority (int): 优先级 (0-255)
            advert_int (int): 广播间隔（秒）
            auth_type (str): 认证类型 (PASS/AH)
            auth_pass (str): 认证密码
            virtual_ipaddresses (List[str]): 虚拟IP地址列表
            nopreempt (bool): 是否禁用抢占
            preempt_delay (int): 抢占延迟（秒）
            garp_master_delay (int): GARP主延迟（秒）
            unicast_src_ip (str): 单播源IP地址
            unicast_peer (List[str]): 单播对端IP地址列表
            smtp_alert (bool): 是否启用SMTP告警
            notify_master (str): 切换到MASTER状态时执行的脚本
            notify_backup (str): 切换到BACKUP状态时执行的脚本
            notify_fault (str): 发生故障时执行的脚本
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 更新VRRP实例
            result = vrrp_manager.update_vrrp_instance(
                instance_name="VI_1",
                priority=150,
                advert_int=2
            )
            if result:
                print("VRRP实例更新成功")
            else:
                print(f"更新失败: {result.message}")
            ```
            
        Raises:
            ValueError: 当参数无效时
            TypeError: 当参数类型错误时
            VRRPInstanceNotFoundError: 当VRRP实例不存在时
        """
        # 获取现有的VRRP实例
        vrrp_block = self.get_vrrp_instance(instance_name)
        if vrrp_block is None:
            raise VRRPInstanceNotFoundError(f"VRRP实例 '{instance_name}' 不存在")
            
        # 参数验证
        if state is not None and state not in ["MASTER", "BACKUP"]:
            return OperationResult.fail("状态必须是 'MASTER' 或 'BACKUP'")
            
        if virtual_router_id is not None and not (0 <= virtual_router_id <= 255):
            return OperationResult.fail("虚拟路由器ID必须是0到255之间的整数")
            
        if priority is not None and not (0 <= priority <= 255):
            return OperationResult.fail("优先级必须是0到255之间的整数")
            
        if advert_int is not None and advert_int <= 0:
            return OperationResult.fail("广播间隔必须是正整数")
            
        if auth_type is not None and auth_type not in ["PASS", "AH"]:
            return OperationResult.fail("认证类型必须是 'PASS' 或 'AH'")
            
        # 更新参数
        if state is not None:
            self._update_param(vrrp_block, "state", state)
            
        if interface is not None:
            self._update_param(vrrp_block, "interface", interface)
            
        if virtual_router_id is not None:
            self._update_param(vrrp_block, "virtual_router_id", str(virtual_router_id))
            
        if priority is not None:
            self._update_param(vrrp_block, "priority", str(priority))
            
        if advert_int is not None:
            self._update_param(vrrp_block, "advert_int", str(advert_int))
            
        # 更新认证配置
        if auth_type is not None or auth_pass is not None:
            auth_block = self._get_sub_block(vrrp_block, "authentication")
            if auth_block is None:
                auth_block = KeepAlivedConfigBlock("authentication")
                vrrp_block.add_param(auth_block)
                
            if auth_type is not None:
                self._update_param(auth_block, "auth_type", auth_type)
                
            if auth_pass is not None:
                self._update_param(auth_block, "auth_pass", auth_pass)
                
        # 更新虚拟IP地址
        if virtual_ipaddresses is not None:
            # 移除现有的virtual_ipaddress块
            vip_block = self._get_sub_block(vrrp_block, "virtual_ipaddress")
            if vip_block:
                vrrp_block.params.remove(vip_block)
                
            # 添加新的virtual_ipaddress块
            if virtual_ipaddresses:
                vip_block = KeepAlivedConfigBlock("virtual_ipaddress")
                for vip in virtual_ipaddresses:
                    vip_block.add_param(KeepAlivedConfigParam("", vip))
                vrrp_block.add_param(vip_block)
                
        # 更新可选参数
        if nopreempt is not None:
            nopreempt_param = self._get_param(vrrp_block, "nopreempt")
            if nopreempt and nopreempt_param is None:
                vrrp_block.add_param(KeepAlivedConfigParam("nopreempt"))
            elif not nopreempt and nopreempt_param is not None:
                vrrp_block.params.remove(nopreempt_param)
                
        if preempt_delay is not None:
            self._update_param(vrrp_block, "preempt_delay", str(preempt_delay))
            
        if garp_master_delay is not None:
            self._update_param(vrrp_block, "garp_master_delay", str(garp_master_delay))
            
        # 更新新增参数
        if unicast_src_ip is not None:
            self._update_param(vrrp_block, "unicast_src_ip", unicast_src_ip)
            
        if unicast_peer is not None:
            # 移除现有的unicast_peer块
            unicast_peer_block = self._get_sub_block(vrrp_block, "unicast_peer")
            if unicast_peer_block:
                vrrp_block.params.remove(unicast_peer_block)
                
            # 添加新的unicast_peer块
            if unicast_peer:
                unicast_peer_block = KeepAlivedConfigBlock("unicast_peer")
                for peer in unicast_peer:
                    unicast_peer_block.add_param(KeepAlivedConfigParam("", peer))
                vrrp_block.add_param(unicast_peer_block)
                
        if smtp_alert is not None:
            # 先移除可能存在的参数
            smtp_params = ["smtp_alert", "no_smtp_alert"]
            for param_name in smtp_params:
                smtp_param = self._get_param(vrrp_block, param_name)
                if smtp_param is not None:
                    vrrp_block.params.remove(smtp_param)
            # 添加新参数
            smtp_alert_param = "smtp_alert" if smtp_alert else "no_smtp_alert"
            vrrp_block.add_param(KeepAlivedConfigParam(smtp_alert_param))
            
        if notify_master is not None:
            self._update_param(vrrp_block, "notify_master", notify_master)
            
        if notify_backup is not None:
            self._update_param(vrrp_block, "notify_backup", notify_backup)
            
        if notify_fault is not None:
            self._update_param(vrrp_block, "notify_fault", notify_fault)
            
        return OperationResult.ok(f"VRRP实例 '{instance_name}' 更新成功")

    def list_vrrp_instances(self) -> List[str]:
        """
        列出所有VRRP实例名称
        
        Returns:
            List[str]: VRRP实例名称列表
        """
        instances = []
        for param in self.config.params:
            if isinstance(param, KeepAlivedConfigBlock) and param.name.startswith("vrrp_instance"):
                # 提取实例名称 (格式: "vrrp_instance INSTANCE_NAME")
                parts = param.name.split(" ", 1)
                if len(parts) == 2:
                    instances.append(parts[1])
        return instances

    def _get_param(self, block: KeepAlivedConfigBlock, param_name: str) -> Optional[KeepAlivedConfigParam]:
        """
        在块中查找指定名称的参数
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            param_name (str): 参数名称
            
        Returns:
            Optional[KeepAlivedConfigParam]: 参数对象，如果不存在则返回None
        """
        # 使用基类方法
        return super()._get_param(block, param_name)

    def _update_param(self, block: KeepAlivedConfigBlock, param_name: str, param_value: str):
        """
        更新块中的参数值
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            param_name (str): 参数名称
            param_value (str): 参数值
        """
        # 使用基类方法
        super()._update_param(block, param_name, param_value)

    def _get_sub_block(self, block: KeepAlivedConfigBlock, block_name: str) -> Optional[KeepAlivedConfigBlock]:
        """
        在块中查找指定名称的子块
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            block_name (str): 子块名称
            
        Returns:
            Optional[KeepAlivedConfigBlock]: 子块对象，如果不存在则返回None
        """
        # 使用基类方法
        return super()._get_sub_block(block, block_name)