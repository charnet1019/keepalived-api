from typing import Union, List, Any
from keepalived_config.keepalived_config_exceptions import (
    KeepAlivedConfigTypeError,
    VRRPParameterError,
    VirtualServerParameterError
)


class KeepAlivedConfigValidator:
    """
    Keepalived配置参数验证工具类
    集中管理所有参数验证逻辑，减少代码重复
    """

    @staticmethod
    def validate_string(value: Any, name: str, allow_empty: bool = False) -> str:
        """
        验证字符串参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            allow_empty: 是否允许空字符串
            
        Returns:
            str: 验证通过的字符串值
            
        Raises:
            KeepAlivedConfigTypeError: 当值不是字符串类型时
            VirtualServerParameterError: 当值为空字符串且不允许时
        """
        if not isinstance(value, str):
            raise KeepAlivedConfigTypeError(f"{name}必须是字符串, got {type(value)}")
            
        if not allow_empty and not value:
            raise VirtualServerParameterError(f"{name}不能为空字符串")
            
        return value

    @staticmethod
    def validate_port(value: Any, name: str) -> Union[int, str]:
        """
        验证端口参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            
        Returns:
            Union[int, str]: 验证通过的端口值
            
        Raises:
            KeepAlivedConfigTypeError: 当值不是整数或字符串类型时
        """
        if not isinstance(value, (int, str)):
            raise KeepAlivedConfigTypeError(f"{name}必须是整数或字符串, got {type(value)}")
            
        return value

    @staticmethod
    def validate_positive_integer(value: Any, name: str) -> int:
        """
        验证正整数参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            
        Returns:
            int: 验证通过的正整数
            
        Raises:
            VirtualServerParameterError: 当值不是正整数时
            VRRPParameterError: 当VRRP参数不是正整数时
        """
        if not isinstance(value, int) or value <= 0:
            # 根据参数名称判断应该抛出哪种异常
            if "虚拟路由器" in name or "优先级" in name or "广播间隔" in name:
                from keepalived_config.keepalived_config_exceptions import VRRPParameterError
                raise VRRPParameterError(f"{name}必须是正整数")
            else:
                raise VirtualServerParameterError(f"{name}必须是正整数")
            
        return value

    @staticmethod
    def validate_non_negative_integer(value: Any, name: str) -> int:
        """
        验证非负整数参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            
        Returns:
            int: 验证通过的非负整数
            
        Raises:
            VirtualServerParameterError: 当值不是非负整数时
        """
        if not isinstance(value, int) or value < 0:
            raise VirtualServerParameterError(f"{name}必须是非负整数")
            
        return value

    @staticmethod
    def validate_integer_in_range(value: Any, name: str, min_val: int, max_val: int) -> int:
        """
        验证范围内的整数参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            int: 验证通过的整数
            
        Raises:
            VirtualServerParameterError: 当值不在指定范围内时
            VRRPParameterError: 当VRRP参数不在指定范围内时
        """
        if not isinstance(value, int) or not (min_val <= value <= max_val):
            # 根据参数名称判断应该抛出哪种异常
            if "虚拟路由器" in name or "优先级" in name:
                from keepalived_config.keepalived_config_exceptions import VRRPParameterError
                raise VRRPParameterError(f"{name}必须是{min_val}到{max_val}之间的整数")
            else:
                raise VirtualServerParameterError(f"{name}必须是{min_val}到{max_val}之间的整数")
            
        return value

    @staticmethod
    def validate_choice(value: Any, name: str, choices: List[str]) -> str:
        """
        验证选项参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            choices: 可选值列表
            
        Returns:
            str: 验证通过的选项值
            
        Raises:
            VirtualServerParameterError: 当值不在可选列表中时
            VRRPParameterError: 当VRRP参数不在可选列表中时
        """
        if value not in choices:
            # 根据参数名称判断应该抛出哪种异常
            if "状态" in name or "协议" in name or "认证类型" in name:
                from keepalived_config.keepalived_config_exceptions import VRRPParameterError
                raise VRRPParameterError(f"{name}必须是以下之一: {', '.join(choices)}")
            elif "负载均衡" in name:
                raise VirtualServerParameterError(f"{name}必须是以下之一: {', '.join(choices)}")
            else:
                raise VirtualServerParameterError(f"{name}必须是以下之一: {', '.join(choices)}")
            
        return value

    @staticmethod
    def validate_bool(value: Any, name: str) -> bool:
        """
        验证布尔参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            
        Returns:
            bool: 验证通过的布尔值
            
        Raises:
            KeepAlivedConfigTypeError: 当值不是布尔类型时
        """
        if not isinstance(value, bool):
            raise KeepAlivedConfigTypeError(f"{name}必须是布尔值, got {type(value)}")
            
        return value

    @staticmethod
    def validate_list(value: Any, name: str) -> list:
        """
        验证列表参数
        
        Args:
            value: 待验证的值
            name: 参数名称
            
        Returns:
            list: 验证通过的列表
            
        Raises:
            KeepAlivedConfigTypeError: 当值不是列表类型时
        """
        if not isinstance(value, list):
            raise KeepAlivedConfigTypeError(f"{name}必须是列表, got {type(value)}")
            
        return value