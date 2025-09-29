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
from keepalived_config.keepalived_config_types import VirtualServerConfig
from keepalived_config.keepalived_config_exceptions import (
    KeepAlivedConfigTypeError,
    VirtualServerExistsError,
    VirtualServerNotFoundError,
    VirtualServerParameterError,
    RealServerExistsError,
    RealServerNotFoundError
)
from keepalived_config.keepalived_config_base import KeepAlivedConfigBase
from keepalived_config.keepalived_config_validator import KeepAlivedConfigValidator


class KeepAlivedConfigVirtualServer(KeepAlivedConfigBase):
    """
    虚拟服务器管理类，提供虚拟服务器和真实服务器的增删改查功能
    """

    def __init__(self, config: KeepAlivedConfig):
        """
        初始化虚拟服务器管理器
        
        Args:
            config (KeepAlivedConfig): Keepalived配置对象
        """
        super().__init__()
        self.config = config

    def __enter__(self):
        """
        上下文管理器入口
        
        Returns:
            KeepAlivedConfigVirtualServer: 虚拟服务器管理器实例
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
        # 虚拟服务器管理器本身不处理自动保存，因为配置保存由KeepAlivedConfig处理
        pass

    def create_virtual_server(
        self,
        virtual_server_ip: str,
        virtual_server_port: Union[int, str],
        delay_loop: int = None,
        lb_algo: str = None,
        lb_kind: str = None,
        protocol: str = None,
        persistence_timeout: int = None,
        persistence_granularity: str = None,
        virtualhost: str = None,
        ha_suspend: bool = None,
        alpha: bool = None,
        omega: bool = None,
        quorum: int = None,
        quorum_up: str = None,
        quorum_down: str = None,
        hysteresis: int = None,
        retry: int = None,
        comments: List[KeepAlivedConfigComment] = None,
        config: VirtualServerConfig = None,
        **kwargs
    ) -> OperationResult:
        """
        创建虚拟服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            delay_loop (int): 健康检查间隔（秒），默认值为6
            lb_algo (str): 负载均衡算法 (rr|wrr|lc|wlc|lblc|sh|dh)，默认值为"rr"
            lb_kind (str): 负载均衡类型 (NAT|DR|TUN)，默认值为"DR"
            protocol (str): 协议 (TCP|UDP|SCTP)，默认值为"TCP"
            persistence_timeout (int): 会话保持超时时间
            persistence_granularity (str): 会话保持粒度
            virtualhost (str): 虚拟主机
            ha_suspend (bool): 是否启用HA暂停
            alpha (bool): 是否在启动时运行健康检查
            omega (bool): 是否在关闭时运行健康检查
            quorum (int): 最小真实服务器数量
            quorum_up (str): 达到quorum时执行的脚本
            quorum_down (str): 低于quorum时执行的脚本
            hysteresis (int): 迟滞值
            retry (int): 重试次数
            comments (List[KeepAlivedConfigComment]): 注释列表
            config (VirtualServerConfig): 虚拟服务器配置对象
            **kwargs: 其他参数，用于向后兼容
            
        Returns:
            OperationResult: 操作结果对象，包含创建的虚拟服务器块
            
        Example:
            ```python
            # 使用传统方式创建虚拟服务器
            result = vs_manager.create_virtual_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                lb_kind="DR",
                protocol="TCP"
            )
            
            # 使用配置对象创建虚拟服务器
            vs_config = VirtualServerConfig(
                lb_kind="DR",
                protocol="TCP"
            )
            result = vs_manager.create_virtual_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                config=vs_config
            )
            
            if result:
                print(f"虚拟服务器创建成功: {result.data.name}")
            else:
                print(f"创建失败: {result.message}")
            ```
            
        Raises:
            VirtualServerExistsError: 当虚拟服务器已存在时
        """
        # 如果提供了配置对象，则使用配置对象的值作为默认值
        if config is not None:
            # 使用配置对象的值作为默认值
            delay_loop = delay_loop if delay_loop is not None else config.delay_loop
            lb_algo = lb_algo if lb_algo is not None else config.lb_algo
            lb_kind = lb_kind if lb_kind is not None else config.lb_kind
            protocol = protocol if protocol is not None else config.protocol
            persistence_timeout = persistence_timeout if persistence_timeout is not None else config.persistence_timeout
            persistence_granularity = persistence_granularity if persistence_granularity is not None else config.persistence_granularity
            virtualhost = virtualhost if virtualhost is not None else config.virtualhost
            # 新增参数
            ha_suspend = ha_suspend if ha_suspend is not None else config.ha_suspend
            alpha = alpha if alpha is not None else config.alpha
            omega = omega if omega is not None else config.omega
            quorum = quorum if quorum is not None else config.quorum
            quorum_up = quorum_up if quorum_up is not None else config.quorum_up
            quorum_down = quorum_down if quorum_down is not None else config.quorum_down
            hysteresis = hysteresis if hysteresis is not None else config.hysteresis
            retry = retry if retry is not None else config.retry
        
        # 如果没有提供配置对象，使用默认值
        if config is None:
            # 设置默认值
            delay_loop = delay_loop if delay_loop is not None else KeepAlivedConfigDefaults.VIRTUAL_SERVER_DELAY_LOOP
            lb_algo = lb_algo if lb_algo is not None else KeepAlivedConfigDefaults.VIRTUAL_SERVER_LB_ALGO
            lb_kind = lb_kind if lb_kind is not None else KeepAlivedConfigDefaults.VIRTUAL_SERVER_LB_KIND
            protocol = protocol if protocol is not None else KeepAlivedConfigDefaults.VIRTUAL_SERVER_PROTOCOL
        
        # 参数验证
        if delay_loop is not None:
            try:
                KeepAlivedConfigValidator.validate_positive_integer(delay_loop, "健康检查间隔")
            except VirtualServerParameterError as e:
                return OperationResult.fail(str(e))
            
        if lb_algo is not None:
            try:
                KeepAlivedConfigValidator.validate_choice(lb_algo, "负载均衡算法", ["rr", "wrr", "lc", "wlc", "lblc", "sh", "dh"])
            except VirtualServerParameterError as e:
                return OperationResult.fail(str(e))
            
        if lb_kind is not None:
            try:
                KeepAlivedConfigValidator.validate_choice(lb_kind, "负载均衡类型", ["NAT", "DR", "TUN"])
            except VirtualServerParameterError as e:
                return OperationResult.fail(str(e))
            
        if protocol is not None:
            try:
                KeepAlivedConfigValidator.validate_choice(protocol, "协议", ["TCP", "UDP", "SCTP"])
            except VirtualServerParameterError as e:
                return OperationResult.fail(str(e))
            
        # 检查是否已存在相同IP和端口的虚拟服务器
        vs_name = f"{virtual_server_ip} {virtual_server_port}"
        if self._get_virtual_server_internal(virtual_server_ip, virtual_server_port) is not None:
            raise VirtualServerExistsError(f"虚拟服务器 '{vs_name}' 已存在")
            
        # 创建虚拟服务器块
        vs_block = KeepAlivedConfigBlock("virtual_server", vs_name, comments or [])
        
        # 添加基本参数
        vs_block.add_param(KeepAlivedConfigParam("delay_loop", str(delay_loop)))
        vs_block.add_param(KeepAlivedConfigParam("lb_algo", lb_algo))
        vs_block.add_param(KeepAlivedConfigParam("lb_kind", lb_kind))
        vs_block.add_param(KeepAlivedConfigParam("protocol", protocol))
        
        # 添加可选参数
        if persistence_timeout is not None:
            vs_block.add_param(KeepAlivedConfigParam("persistence_timeout", str(persistence_timeout)))
            
        if persistence_granularity is not None:
            vs_block.add_param(KeepAlivedConfigParam("persistence_granularity", persistence_granularity))
            
        if virtualhost is not None:
            vs_block.add_param(KeepAlivedConfigParam("virtualhost", virtualhost))
            
        # 添加新增参数
        if ha_suspend is not None:
            ha_suspend_param = "ha_suspend" if ha_suspend else "no_ha_suspend"
            vs_block.add_param(KeepAlivedConfigParam(ha_suspend_param))
            
        if alpha is not None:
            alpha_param = "alpha" if alpha else "no_alpha"
            vs_block.add_param(KeepAlivedConfigParam(alpha_param))
            
        if omega is not None:
            omega_param = "omega" if omega else "no_omega"
            vs_block.add_param(KeepAlivedConfigParam(omega_param))
            
        if quorum is not None:
            vs_block.add_param(KeepAlivedConfigParam("quorum", str(quorum)))
            
        if quorum_up is not None:
            vs_block.add_param(KeepAlivedConfigParam("quorum_up", quorum_up))
            
        if quorum_down is not None:
            vs_block.add_param(KeepAlivedConfigParam("quorum_down", quorum_down))
            
        if hysteresis is not None:
            vs_block.add_param(KeepAlivedConfigParam("hysteresis", str(hysteresis)))
            
        if retry is not None:
            vs_block.add_param(KeepAlivedConfigParam("retry", str(retry)))
        
        # 添加到配置中
        self.config.params.append(vs_block)
        
        return OperationResult.ok(f"虚拟服务器 '{vs_name}' 创建成功", vs_block)

    def create_from_template(self, template_name: str, instance_name: str, config: VirtualServerConfig = None, **kwargs) -> OperationResult:
        """
        从模板创建虚拟服务器
        
        Args:
            template_name (str): 模板名称
            instance_name (str): 实例名称（格式: "IP PORT"）
            config (VirtualServerConfig): 虚拟服务器配置对象
            **kwargs: 模板参数
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 从模板创建虚拟服务器
            vs_config = VirtualServerConfig(
                delay_loop=10,
                lb_algo="wrr",
                lb_kind="DR",
                protocol="TCP"
            )
            result = vs_manager.create_from_template(
                "basic_virtual_server",
                "192.168.1.100 80",
                config=vs_config
            )
            
            # 或者直接传递参数
            result = vs_manager.create_from_template(
                "basic_virtual_server",
                "192.168.1.100 80",
                delay_loop=10,
                lb_algo="wrr",
                lb_kind="DR",
                protocol="TCP"
            )
            
            if result:
                print("虚拟服务器创建成功")
            else:
                print(f"创建失败: {result.message}")
            ```
        """
        try:
            # 使用模板创建虚拟服务器配置
            template_config = KeepAlivedConfigTemplates.from_template(template_name, instance_name, **kwargs)
            
            # 检查是否已存在相同IP和端口的虚拟服务器
            result = self.get_virtual_server_by_name(instance_name)
            if result.success:
                return OperationResult.fail(f"虚拟服务器 '{instance_name}' 已存在")
            
            # 获取模板生成的虚拟服务器块
            if template_config.params and isinstance(template_config.params[0], KeepAlivedConfigBlock):
                vs_block = template_config.params[0]
                # 添加到当前配置中
                self.config.params.append(vs_block)
                return OperationResult.ok(f"虚拟服务器 '{instance_name}' 从模板 '{template_name}' 创建成功", vs_block)
            else:
                return OperationResult.fail("模板未生成有效的虚拟服务器配置")
        except Exception as e:
            return OperationResult.fail(f"从模板创建虚拟服务器失败: {str(e)}", e)

    def get_virtual_server(self, virtual_server_ip: str, virtual_server_port: Union[int, str]) -> OperationResult:
        """
        获取指定IP和端口的虚拟服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            
        Returns:
            OperationResult: 操作结果对象，数据部分包含虚拟服务器块，如果不存在则返回失败结果
            
        Example:
            ```python
            # 获取虚拟服务器
            result = vs_manager.get_virtual_server("192.168.1.100", 80)
            if result:
                print(f"找到虚拟服务器: {result.data.name}")
            else:
                print("虚拟服务器不存在")
            ```
            
        Raises:
            KeepAlivedConfigTypeError: 当IP或端口类型错误时
        """
        if not isinstance(virtual_server_ip, str):
            raise KeepAlivedConfigTypeError(f"IP必须是字符串, got {type(virtual_server_ip)}")
            
        if not isinstance(virtual_server_port, (int, str)):
            raise KeepAlivedConfigTypeError(f"端口必须是整数或字符串, got {type(virtual_server_port)}")
            
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is not None:
            return OperationResult.ok(f"成功获取虚拟服务器 '{virtual_server_ip} {virtual_server_port}'", vs_block)
        else:
            return OperationResult.fail(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")

    def get_virtual_server_by_name(self, name: str) -> OperationResult:
        """
        根据名称获取虚拟服务器
        
        Args:
            name (str): 虚拟服务器名称（格式: "IP PORT"）
            
        Returns:
            OperationResult: 操作结果对象，数据部分包含虚拟服务器块，如果不存在则返回失败结果
            
        Raises:
            KeepAlivedConfigTypeError: 当名称不是字符串时
        """
        if not isinstance(name, str):
            raise KeepAlivedConfigTypeError(f"名称必须是字符串, got {type(name)}")
            
        for param in self.config.params:
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("virtual_server") and \
               param.name.endswith(name):
                return OperationResult.ok(f"成功获取虚拟服务器 '{name}'", param)
        return OperationResult.fail(f"虚拟服务器 '{name}' 不存在")

    def list_virtual_servers(self) -> OperationResult:
        """
        列出所有虚拟服务器
        
        Returns:
            OperationResult: 操作结果对象，数据部分包含虚拟服务器列表，格式为 "IP PORT"
            
        Example:
            ```python
            # 列出所有虚拟服务器
            result = vs_manager.list_virtual_servers()
            if result:
                for vs in result.data:
                    print(f"虚拟服务器: {vs}")
            ```
        """
        virtual_servers = []
        for param in self.config.params:
            if isinstance(param, KeepAlivedConfigBlock) and param.name.startswith("virtual_server"):
                # 提取虚拟服务器名称 (格式: "virtual_server IP PORT")
                parts = param.name.split(" ", 1)
                if len(parts) == 2:
                    virtual_servers.append(parts[1])
        return OperationResult.ok("成功获取虚拟服务器列表", virtual_servers)

    def remove_virtual_server(self, virtual_server_ip: str, virtual_server_port: Union[int, str]) -> OperationResult:
        """
        删除指定IP和端口的虚拟服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 删除虚拟服务器
            result = vs_manager.remove_virtual_server("192.168.1.100", 80)
            if result:
                print("虚拟服务器删除成功")
            else:
                print(f"删除失败: {result.message}")
            ```
            
        Raises:
            KeepAlivedConfigTypeError: 当IP或端口类型错误时
            VirtualServerNotFoundError: 当虚拟服务器不存在时
        """
        if not isinstance(virtual_server_ip, str):
            raise KeepAlivedConfigTypeError("IP必须是字符串")
            
        if not isinstance(virtual_server_port, (int, str)):
            raise KeepAlivedConfigTypeError("端口必须是整数或字符串")
            
        # 参数验证
        try:
            KeepAlivedConfigValidator.validate_port(virtual_server_port, "端口")
        except KeepAlivedConfigTypeError as e:
            raise KeepAlivedConfigTypeError(str(e))
            
        vs_name = f"{virtual_server_ip} {virtual_server_port}"
        for i, param in enumerate(self.config.params):
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("virtual_server") and \
               param.name.endswith(vs_name):
                self.config.params.pop(i)
                return OperationResult.ok(f"虚拟服务器 '{vs_name}' 删除成功")
                
        raise VirtualServerNotFoundError(f"虚拟服务器 '{vs_name}' 不存在")

    def update_virtual_server(
        self,
        virtual_server_ip: str,
        virtual_server_port: Union[int, str],
        delay_loop: int = None,
        lb_algo: str = None,
        lb_kind: str = None,
        protocol: str = None,
        persistence_timeout: int = None,
        persistence_granularity: str = None,
        virtualhost: str = None,
        ha_suspend: bool = None,
        alpha: bool = None,
        omega: bool = None,
        quorum: int = None,
        quorum_up: str = None,
        quorum_down: str = None,
        hysteresis: int = None,
        retry: int = None
    ) -> OperationResult:
        """
        更新虚拟服务器配置
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            delay_loop (int): 健康检查间隔（秒）
            lb_algo (str): 负载均衡算法 (rr|wrr|lc|wlc|lblc|sh|dh)
            lb_kind (str): 负载均衡类型 (NAT|DR|TUN)
            protocol (str): 协议 (TCP|UDP|SCTP)
            persistence_timeout (int): 会话保持超时时间
            persistence_granularity (str): 会话保持粒度
            virtualhost (str): 虚拟主机
            ha_suspend (bool): 是否启用HA暂停
            alpha (bool): 是否在启动时运行健康检查
            omega (bool): 是否在关闭时运行健康检查
            quorum (int): 最小真实服务器数量
            quorum_up (str): 达到quorum时执行的脚本
            quorum_down (str): 低于quorum时执行的脚本
            hysteresis (int): 迟滞值
            retry (int): 重试次数
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 更新虚拟服务器配置
            result = vs_manager.update_virtual_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                delay_loop=10,
                lb_algo="wrr"
            )
            if result:
                print("虚拟服务器更新成功")
            else:
                print(f"更新失败: {result.message}")
            ```
            
        Raises:
            VirtualServerNotFoundError: 当虚拟服务器不存在时
        """
        # 获取现有的虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            raise VirtualServerNotFoundError(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")
            
        # 参数验证
        if delay_loop is not None and (not isinstance(delay_loop, int) or delay_loop <= 0):
            return OperationResult.fail("健康检查间隔必须是正整数")
            
        if lb_algo is not None and lb_algo not in ["rr", "wrr", "lc", "wlc", "lblc", "sh", "dh"]:
            return OperationResult.fail("负载均衡算法必须是以下之一: rr, wrr, lc, wlc, lblc, sh, dh")
            
        if lb_kind is not None and lb_kind not in ["NAT", "DR", "TUN"]:
            return OperationResult.fail("负载均衡类型必须是以下之一: NAT, DR, TUN")
            
        if protocol is not None and protocol not in ["TCP", "UDP", "SCTP"]:
            return OperationResult.fail("协议必须是以下之一: TCP, UDP, SCTP")
            
        # 更新参数
        if delay_loop is not None:
            self._update_param(vs_block, "delay_loop", str(delay_loop))
            
        if lb_algo is not None:
            self._update_param(vs_block, "lb_algo", lb_algo)
            
        if lb_kind is not None:
            self._update_param(vs_block, "lb_kind", lb_kind)
            
        if protocol is not None:
            self._update_param(vs_block, "protocol", protocol)
            
        if persistence_timeout is not None:
            self._update_param(vs_block, "persistence_timeout", str(persistence_timeout))
            
        if persistence_granularity is not None:
            self._update_param(vs_block, "persistence_granularity", persistence_granularity)
            
        if virtualhost is not None:
            self._update_param(vs_block, "virtualhost", virtualhost)
            
        # 更新新增参数
        if ha_suspend is not None:
            ha_suspend_param = "ha_suspend" if ha_suspend else "no_ha_suspend"
            # 先移除可能存在的参数
            ha_params = ["ha_suspend", "no_ha_suspend"]
            for param_name in ha_params:
                ha_param = self._get_param(vs_block, param_name)
                if ha_param is not None:
                    vs_block.params.remove(ha_param)
            # 添加新参数
            vs_block.add_param(KeepAlivedConfigParam(ha_suspend_param))
            
        if alpha is not None:
            alpha_param = "alpha" if alpha else "no_alpha"
            # 先移除可能存在的参数
            alpha_params = ["alpha", "no_alpha"]
            for param_name in alpha_params:
                alpha_param_obj = self._get_param(vs_block, param_name)
                if alpha_param_obj is not None:
                    vs_block.params.remove(alpha_param_obj)
            # 添加新参数
            vs_block.add_param(KeepAlivedConfigParam(alpha_param))
            
        if omega is not None:
            omega_param = "omega" if omega else "no_omega"
            # 先移除可能存在的参数
            omega_params = ["omega", "no_omega"]
            for param_name in omega_params:
                omega_param_obj = self._get_param(vs_block, param_name)
                if omega_param_obj is not None:
                    vs_block.params.remove(omega_param_obj)
            # 添加新参数
            vs_block.add_param(KeepAlivedConfigParam(omega_param))
            
        if quorum is not None:
            self._update_param(vs_block, "quorum", str(quorum))
            
        if quorum_up is not None:
            self._update_param(vs_block, "quorum_up", quorum_up)
            
        if quorum_down is not None:
            self._update_param(vs_block, "quorum_down", quorum_down)
            
        if hysteresis is not None:
            self._update_param(vs_block, "hysteresis", str(hysteresis))
            
        if retry is not None:
            self._update_param(vs_block, "retry", str(retry))
            
        return OperationResult.ok(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 更新成功")

    def add_real_server(
        self,
        virtual_server_ip: str,
        virtual_server_port: Union[int, str],
        real_server_ip: str,
        real_server_port: Union[int, str],
        weight: int = KeepAlivedConfigDefaults.REAL_SERVER_WEIGHT,
        health_check: str = KeepAlivedConfigDefaults.REAL_SERVER_HEALTH_CHECK,
        health_check_params: Dict[str, Any] = None,
        comments: List[KeepAlivedConfigComment] = None
    ) -> OperationResult:
        """
        为虚拟服务器添加真实服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            real_server_ip (str): 真实服务器IP地址
            real_server_port (Union[int, str]): 真实服务器端口
            weight (int): 权重，默认值为1
            health_check (str): 健康检查类型 (TCP_CHECK|HTTP_GET|SSL_GET|DNS_CHECK|MISC_CHECK|UDP_CHECK)，默认值为"TCP_CHECK"
            health_check_params (Dict[str, Any]): 健康检查参数
                - TCP_CHECK: {"connect_timeout": 3, "delay_before_retry": 3}
                - HTTP_GET: {"url": "/", "digest": None, "status_code": None}
                - UDP_CHECK: {"connect_timeout": 3, "delay_before_retry": 3}
            comments (List[KeepAlivedConfigComment]): 注释列表
            
        Returns:
            OperationResult: 操作结果对象，包含创建的真实服务器块
            
        Example:
            ```python
            # 添加使用TCP健康检查的真实服务器
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
            
            # 添加使用HTTP健康检查的真实服务器
            result = vs_manager.add_real_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                real_server_ip="192.168.1.101",
                real_server_port=8080,
                weight=1,
                health_check="HTTP_GET",
                health_check_params={
                    "url": "/health",
                    "status_code": 200
                }
            )
            ```
            
        Raises:
            RealServerExistsError: 当真实服务器已存在时
            VirtualServerNotFoundError: 当虚拟服务器不存在时
        """
        # 参数验证
        try:
            KeepAlivedConfigValidator.validate_string(real_server_ip, "真实服务器IP", allow_empty=False)
        except (KeepAlivedConfigTypeError, VirtualServerParameterError) as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_port(real_server_port, "真实服务器端口")
        except KeepAlivedConfigTypeError as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_non_negative_integer(weight, "权重")
        except VirtualServerParameterError as e:
            return OperationResult.fail(str(e))
            
        try:
            KeepAlivedConfigValidator.validate_choice(health_check, "健康检查类型", 
                                                    ["TCP_CHECK", "HTTP_GET", "SSL_GET", "DNS_CHECK", "MISC_CHECK", "UDP_CHECK"])
        except VirtualServerParameterError as e:
            return OperationResult.fail(str(e))
            
        # 获取虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            raise VirtualServerNotFoundError(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")
            
        # 检查是否已存在相同IP和端口的真实服务器
        rs_name = f"{real_server_ip} {real_server_port}"
        if self._get_real_server_internal(virtual_server_ip, virtual_server_port, real_server_ip, real_server_port) is not None:
            raise RealServerExistsError(f"真实服务器 '{rs_name}' 已存在于虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中")
            
        # 创建真实服务器块
        rs_block = KeepAlivedConfigBlock("real_server", rs_name, comments or [])
        
        # 添加权重参数
        rs_block.add_param(KeepAlivedConfigParam("weight", str(weight)))
        
        # 处理健康检查参数默认值
        if health_check_params is None:
            health_check_params = {}
        
        # 添加健康检查配置
        if health_check == "TCP_CHECK":
            health_check_block = KeepAlivedConfigBlock("TCP_CHECK")
            connect_timeout = health_check_params.get("connect_timeout", KeepAlivedConfigDefaults.TCP_CHECK_CONNECT_TIMEOUT)
            delay_before_retry = health_check_params.get("delay_before_retry", KeepAlivedConfigDefaults.TCP_CHECK_DELAY_BEFORE_RETRY)
            health_check_block.add_param(KeepAlivedConfigParam("connect_timeout", str(connect_timeout)))
            health_check_block.add_param(KeepAlivedConfigParam("delay_before_retry", str(delay_before_retry)))
            rs_block.add_param(health_check_block)
            
        elif health_check == "HTTP_GET":
            health_check_block = KeepAlivedConfigBlock("HTTP_GET")
            url = health_check_params.get("url", KeepAlivedConfigDefaults.HTTP_GET_URL)
            digest = health_check_params.get("digest")
            status_code = health_check_params.get("status_code")
            
            health_check_block.add_param(KeepAlivedConfigParam("url", url))
            if digest is not None:
                health_check_block.add_param(KeepAlivedConfigParam("digest", digest))
            if status_code is not None:
                health_check_block.add_param(KeepAlivedConfigParam("status_code", str(status_code)))
            rs_block.add_param(health_check_block)
            
        elif health_check == "UDP_CHECK":
            health_check_block = KeepAlivedConfigBlock("UDP_CHECK")
            connect_timeout = health_check_params.get("connect_timeout", KeepAlivedConfigDefaults.UDP_CHECK_CONNECT_TIMEOUT)
            delay_before_retry = health_check_params.get("delay_before_retry", KeepAlivedConfigDefaults.UDP_CHECK_DELAY_BEFORE_RETRY)
            health_check_block.add_param(KeepAlivedConfigParam("connect_timeout", str(connect_timeout)))
            health_check_block.add_param(KeepAlivedConfigParam("delay_before_retry", str(delay_before_retry)))
            rs_block.add_param(health_check_block)
            
        # 可以继续添加其他健康检查类型...
        
        # 添加到虚拟服务器中
        vs_block.add_param(rs_block)
        
        return OperationResult.ok(f"真实服务器 '{rs_name}' 添加成功", rs_block)

    def get_real_server(
        self, 
        virtual_server_ip: str, 
        virtual_server_port: Union[int, str], 
        real_server_ip: str, 
        real_server_port: Union[int, str]
    ) -> OperationResult:
        """
        获取虚拟服务器中的指定真实服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            real_server_ip (str): 真实服务器IP地址
            real_server_port (Union[int, str]): 真实服务器端口
            
        Returns:
            OperationResult: 操作结果对象，数据部分包含真实服务器块，如果不存在则返回失败结果
            
        Example:
            ```python
            # 获取真实服务器
            result = vs_manager.get_real_server(
                "192.168.1.100", 80, 
                "192.168.1.101", 8080
            )
            if result:
                print(f"找到真实服务器: {result.data.name}")
            else:
                print("真实服务器不存在")
            ```
            
        Raises:
            VirtualServerNotFoundError: 当虚拟服务器不存在时
        """
        # 获取虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            return OperationResult.fail(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")
            
        rs_block = self._get_real_server_internal(virtual_server_ip, virtual_server_port, real_server_ip, real_server_port)
        if rs_block is not None:
            return OperationResult.ok(f"成功获取真实服务器 '{real_server_ip} {real_server_port}'", rs_block)
        else:
            return OperationResult.fail(f"真实服务器 '{real_server_ip} {real_server_port}' 在虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中不存在")

    def list_real_servers(self, virtual_server_ip: str, virtual_server_port: Union[int, str]) -> OperationResult:
        """
        列出虚拟服务器中的所有真实服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            
        Returns:
            OperationResult: 操作结果对象，数据部分包含真实服务器列表，格式为 "IP PORT"
            
        Example:
            ```python
            # 列出虚拟服务器中的所有真实服务器
            result = vs_manager.list_real_servers("192.168.1.100", 80)
            if result:
                for rs in result.data:
                    print(f"真实服务器: {rs}")
            ```
            
        Raises:
            VirtualServerNotFoundError: 当虚拟服务器不存在时
        """
        # 获取虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            return OperationResult.fail(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")
            
        real_servers = []
        for param in vs_block.params:
            if isinstance(param, KeepAlivedConfigBlock) and param.name.startswith("real_server"):
                # 提取真实服务器名称 (格式: "real_server IP PORT")
                parts = param.name.split(" ", 1)
                if len(parts) == 2:
                    real_servers.append(parts[1])
        return OperationResult.ok(f"成功获取虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中的真实服务器列表", real_servers)

    def remove_real_server(
        self, 
        virtual_server_ip: str, 
        virtual_server_port: Union[int, str], 
        real_server_ip: str, 
        real_server_port: Union[int, str]
    ) -> OperationResult:
        """
        从虚拟服务器中删除指定的真实服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            real_server_ip (str): 真实服务器IP地址
            real_server_port (Union[int, str]): 真实服务器端口
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 删除真实服务器
            result = vs_manager.remove_real_server(
                "192.168.1.100", 80, 
                "192.168.1.101", 8080
            )
            if result:
                print("真实服务器删除成功")
            else:
                print(f"删除失败: {result.message}")
            ```
            
        Raises:
            VirtualServerNotFoundError: 当虚拟服务器不存在时
            RealServerNotFoundError: 当真实服务器不存在时
        """
        # 获取虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            raise VirtualServerNotFoundError(f"虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 不存在")
            
        rs_name = f"{real_server_ip} {real_server_port}"
        for i, param in enumerate(vs_block.params):
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("real_server") and \
               param.name.endswith(rs_name):
                vs_block.params.pop(i)
                return OperationResult.ok(f"真实服务器 '{rs_name}' 从虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中删除成功")
                
        raise RealServerNotFoundError(f"真实服务器 '{rs_name}' 在虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中不存在")

    def update_real_server(
        self,
        virtual_server_ip: str,
        virtual_server_port: Union[int, str],
        real_server_ip: str,
        real_server_port: Union[int, str],
        weight: int = None,
        health_check_params: Dict[str, Any] = None
    ) -> OperationResult:
        """
        更新真实服务器配置
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            real_server_ip (str): 真实服务器IP地址
            real_server_port (Union[int, str]): 真实服务器端口
            weight (int): 权重
            health_check_params (Dict[str, Any]): 健康检查参数更新
                - TCP_CHECK: {"connect_timeout": 3, "delay_before_retry": 3}
                - HTTP_GET: {"url": "/", "digest": None, "status_code": None}
                - UDP_CHECK: {"connect_timeout": 3, "delay_before_retry": 3}
            
        Returns:
            OperationResult: 操作结果对象
            
        Example:
            ```python
            # 更新真实服务器权重和健康检查参数
            result = vs_manager.update_real_server(
                virtual_server_ip="192.168.1.100",
                virtual_server_port=80,
                real_server_ip="192.168.1.101",
                real_server_port=8080,
                weight=2,
                health_check_params={
                    "connect_timeout": 5,
                    "delay_before_retry": 5
                }
            )
            if result:
                print("真实服务器更新成功")
            else:
                print(f"更新失败: {result.message}")
            ```
            
        Raises:
            RealServerNotFoundError: 当真实服务器不存在时
        """
        # 获取真实服务器
        rs_block = self._get_real_server_internal(virtual_server_ip, virtual_server_port, real_server_ip, real_server_port)
        if rs_block is None:
            raise RealServerNotFoundError(f"真实服务器 '{real_server_ip} {real_server_port}' 在虚拟服务器 '{virtual_server_ip} {virtual_server_port}' 中不存在")
            
        # 参数验证
        if weight is not None:
            try:
                KeepAlivedConfigValidator.validate_non_negative_integer(weight, "权重")
            except VirtualServerParameterError as e:
                return OperationResult.fail(str(e))
            
        # 更新权重
        if weight is not None:
            self._update_param(rs_block, "weight", str(weight))
            
        # 更新健康检查配置
        if health_check_params is not None:
            # 更新TCP_CHECK参数
            if "connect_timeout" in health_check_params:
                tcp_check_block = self._get_sub_block(rs_block, "TCP_CHECK")
                if tcp_check_block:
                    self._update_param(tcp_check_block, "connect_timeout", str(health_check_params["connect_timeout"]))
                    
            if "delay_before_retry" in health_check_params:
                tcp_check_block = self._get_sub_block(rs_block, "TCP_CHECK")
                if tcp_check_block:
                    self._update_param(tcp_check_block, "delay_before_retry", str(health_check_params["delay_before_retry"]))
                    
            # 更新UDP_CHECK参数
            if "connect_timeout" in health_check_params:
                udp_check_block = self._get_sub_block(rs_block, "UDP_CHECK")
                if udp_check_block:
                    self._update_param(udp_check_block, "connect_timeout", str(health_check_params["connect_timeout"]))
                    
            if "delay_before_retry" in health_check_params:
                udp_check_block = self._get_sub_block(rs_block, "UDP_CHECK")
                if udp_check_block:
                    self._update_param(udp_check_block, "delay_before_retry", str(health_check_params["delay_before_retry"]))
                    
            # 更新HTTP_GET参数
            if "url" in health_check_params:
                http_get_block = self._get_sub_block(rs_block, "HTTP_GET")
                if http_get_block:
                    self._update_param(http_get_block, "url", health_check_params["url"])
                    
            if "digest" in health_check_params:
                http_get_block = self._get_sub_block(rs_block, "HTTP_GET")
                if http_get_block:
                    self._update_param(http_get_block, "digest", health_check_params["digest"])
                    
            if "status_code" in health_check_params:
                http_get_block = self._get_sub_block(rs_block, "HTTP_GET")
                if http_get_block:
                    self._update_param(http_get_block, "status_code", str(health_check_params["status_code"]))
            
        return OperationResult.ok(f"真实服务器 '{real_server_ip} {real_server_port}' 更新成功")

    def validate_configuration(self) -> OperationResult:
        """
        验证配置的一致性和完整性
        
        Returns:
            OperationResult: 操作结果对象，数据部分包含验证问题列表
            
        Example:
            ```python
            # 验证配置
            result = vs_manager.validate_configuration()
            if result:
                print("配置验证通过")
            else:
                print("配置验证发现问题:")
                for issue in result.data:
                    print(f"  - {issue}")
            ```
        """
        issues = []
        
        # 验证每个虚拟服务器
        for vs_name in self.list_virtual_servers():
            ip, port = vs_name.split(" ", 1)
            vs_block = self._get_virtual_server_internal(ip, port)
            
            # 获取虚拟服务器协议
            protocol_param = self._get_param(vs_block, "protocol")
            vs_protocol = protocol_param.value if protocol_param else "TCP"  # 默认TCP
            
            # 验证真实服务器与虚拟服务器协议匹配
            for rs_name in self.list_real_servers(ip, port):
                rs_ip, rs_port = rs_name.split(" ", 1)
                # 这里可以添加更多验证逻辑
                
        if issues:
            return OperationResult.fail("配置验证发现问题", issues)
        else:
            return OperationResult.ok("配置验证通过")

    def _get_virtual_server_internal(self, virtual_server_ip: str, virtual_server_port: Union[int, str]) -> Optional[KeepAlivedConfigBlock]:
        """
        内部方法：获取指定IP和端口的虚拟服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            
        Returns:
            Optional[KeepAlivedConfigBlock]: 虚拟服务器块，如果不存在则返回None
        """
        vs_name = f"{virtual_server_ip} {virtual_server_port}"
        for param in self.config.params:
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("virtual_server") and \
               param.name.endswith(vs_name):
                return param
        return None

    def _get_real_server_internal(
        self, 
        virtual_server_ip: str, 
        virtual_server_port: Union[int, str], 
        real_server_ip: str, 
        real_server_port: Union[int, str]
    ) -> Optional[KeepAlivedConfigBlock]:
        """
        内部方法：获取虚拟服务器中的指定真实服务器
        
        Args:
            virtual_server_ip (str): 虚拟服务器IP地址
            virtual_server_port (Union[int, str]): 虚拟服务器端口
            real_server_ip (str): 真实服务器IP地址
            real_server_port (Union[int, str]): 真实服务器端口
            
        Returns:
            Optional[KeepAlivedConfigBlock]: 真实服务器块，如果不存在则返回None
        """
        # 获取虚拟服务器
        vs_block = self._get_virtual_server_internal(virtual_server_ip, virtual_server_port)
        if vs_block is None:
            return None
            
        rs_name = f"{real_server_ip} {real_server_port}"
        for param in vs_block.params:
            if isinstance(param, KeepAlivedConfigBlock) and \
               param.name.startswith("real_server") and \
               param.name.endswith(rs_name):
                return param
                
        return None

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

    def _add_comment(self, block: KeepAlivedConfigBlock, comment: str, inline: bool = False):
        """
        为块添加注释
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            comment (str): 注释内容
            inline (bool): 是否为行内注释
        """
        # 使用基类方法
        super()._add_comment(block, comment, inline)

    def _set_param_with_comment(
        self, 
        block: KeepAlivedConfigBlock, 
        param_name: str, 
        param_value: str, 
        comment: str = None,
        inline_comment: str = None
    ):
        """
        设置参数并添加注释
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            param_name (str): 参数名称
            param_value (str): 参数值
            comment (str): 块级注释
            inline_comment (str): 行内注释
        """
        # 使用基类方法
        super()._set_param_with_comment(block, param_name, param_value, comment, inline_comment)
