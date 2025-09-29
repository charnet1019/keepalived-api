from typing import Optional
from keepalived_config.keepalived_config import KeepAlivedConfig
from keepalived_config.keepalived_config_vrrp import KeepAlivedConfigVRRP
from keepalived_config.keepalived_config_virtual_server import KeepAlivedConfigVirtualServer
from keepalived_config.keepalived_config_parser import KeepAlivedConfigParser
from keepalived_config.keepalived_config_result import OperationResult
from keepalived_config.keepalived_config_exceptions import (
    ConfigParseError,
    ConfigSaveError,
    ConfigValidationError
)


class KeepAlivedConfigManager:
    """
    KeepAlived配置管理器，提供统一的配置管理入口
    
    该类整合了所有KeepAlived配置管理功能，包括：
    - VRRP实例管理
    - 虚拟服务器管理
    - 配置文件解析
    - 配置保存
    """

    def __init__(self, config: Optional[KeepAlivedConfig] = None, auto_save_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config (Optional[KeepAlivedConfig]): KeepAlived配置对象，如果未提供则创建新的
            auto_save_path (Optional[str]): 自动保存路径，如果提供则在上下文管理器退出时自动保存
        """
        self.config = config or KeepAlivedConfig()
        self.vrrp = KeepAlivedConfigVRRP(self.config)
        self.virtual_server = KeepAlivedConfigVirtualServer(self.config)
        self._auto_save_path = auto_save_path

    def __enter__(self):
        """
        上下文管理器入口
        
        Returns:
            KeepAlivedConfigManager: 配置管理器实例
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出，如果设置了自动保存路径则自动保存配置
        
        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯信息
        """
        if self._auto_save_path is not None and exc_type is None:
            # 只有在没有异常的情况下才自动保存
            self.save_config(self._auto_save_path)
        # 返回None表示不抑制异常

    def load_config(self, config_file: str) -> OperationResult:
        """
        从文件加载配置
        
        Args:
            config_file (str): 配置文件路径
            
        Returns:
            OperationResult: 操作结果
            
        Raises:
            ConfigParseError: 当配置解析失败时
        """
        try:
            parser = KeepAlivedConfigParser()
            self.config = parser.parse_file(config_file)
            # 重新初始化管理器以使用新的配置
            self.vrrp = KeepAlivedConfigVRRP(self.config)
            self.virtual_server = KeepAlivedConfigVirtualServer(self.config)
            return OperationResult.ok(f"配置文件 '{config_file}' 加载成功")
        except Exception as e:
            raise ConfigParseError(f"加载配置文件失败: {str(e)}") from e

    def save_config(self, file_path: Optional[str] = None) -> OperationResult:
        """
        保存配置到文件
        
        Args:
            file_path (Optional[str]): 保存文件路径，如果未提供则使用配置对象的默认路径
            
        Returns:
            OperationResult: 操作结果
            
        Raises:
            ConfigSaveError: 当配置保存失败时
        """
        try:
            self.config.save(file_path)
            path = file_path or self.config.config_file or "default location"
            return OperationResult.ok(f"配置保存成功到 '{path}'")
        except Exception as e:
            raise ConfigSaveError(f"保存配置失败: {str(e)}") from e

    def validate(self) -> OperationResult:
        """
        验证配置完整性
        
        Returns:
            OperationResult: 操作结果，数据部分包含验证问题列表
            
        Raises:
            ConfigValidationError: 当配置验证失败时
        """
        try:
            issues = []
            
            # 验证VRRP实例
            vrrp_instances = self.vrrp.list_vrrp_instances()
            for instance_name in vrrp_instances:
                vrrp_block = self.vrrp.get_vrrp_instance(instance_name)
                if vrrp_block:
                    # 检查必需参数
                    required_params = ["state", "interface", "virtual_router_id", "priority"]
                    for param_name in required_params:
                        param = self.vrrp._get_param(vrrp_block, param_name)
                        if not param or not param.value:
                            issues.append(f"VRRP实例 '{instance_name}' 缺少必需参数 '{param_name}'")
            
            # 验证虚拟服务器
            result = self.virtual_server.list_virtual_servers()
            if result:
                virtual_servers = result.data
                for vs_name in virtual_servers:
                    # 解析IP和端口
                    parts = vs_name.split(" ", 1)
                    if len(parts) == 2:
                        ip, port = parts
                        result = self.virtual_server.get_virtual_server(ip, port)
                        if result:
                            vs_block = result.data
                            # 检查必需参数
                            required_params = ["delay_loop", "lb_algo", "lb_kind", "protocol"]
                            for param_name in required_params:
                                param = self.virtual_server._get_param(vs_block, param_name)
                                if not param or not param.value:
                                    issues.append(f"虚拟服务器 '{vs_name}' 缺少必需参数 '{param_name}'")
            
            if issues:
                return OperationResult.fail("配置验证发现问题", issues)
            else:
                return OperationResult.ok("配置验证通过")
        except Exception as e:
            raise ConfigValidationError(f"配置验证失败: {str(e)}") from e

    @property
    def vrrp_instances(self) -> list:
        """
        获取所有VRRP实例名称
        
        Returns:
            list: VRRP实例名称列表
        """
        return self.vrrp.list_vrrp_instances()

    @property
    def virtual_servers(self) -> list:
        """
        获取所有虚拟服务器名称
        
        Returns:
            list: 虚拟服务器名称列表
        """
        result = self.virtual_server.list_virtual_servers()
        return result.data if result else []
