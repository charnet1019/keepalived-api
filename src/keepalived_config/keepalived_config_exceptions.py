class KeepAlivedConfigError(Exception):
    """Keepalived配置基础异常类"""
    pass


class KeepAlivedConfigValueError(KeepAlivedConfigError, ValueError):
    """配置值错误异常"""
    pass


class KeepAlivedConfigTypeError(KeepAlivedConfigError, TypeError):
    """配置类型错误异常"""
    pass


class VRRPInstanceExistsError(KeepAlivedConfigError):
    """VRRP实例已存在异常"""
    pass


class VRRPInstanceNotFoundError(KeepAlivedConfigError):
    """VRRP实例未找到异常"""
    pass


class VRRPParameterError(KeepAlivedConfigError):
    """VRRP参数错误异常"""
    pass


class VirtualServerError(KeepAlivedConfigError):
    """虚拟服务器错误异常"""
    pass


class VirtualServerExistsError(VirtualServerError):
    """虚拟服务器已存在异常"""
    pass


class VirtualServerNotFoundError(VirtualServerError):
    """虚拟服务器未找到异常"""
    pass


class VirtualServerParameterError(VirtualServerError):
    """虚拟服务器参数错误异常"""
    pass


class RealServerError(VirtualServerError):
    """真实服务器错误异常"""
    pass


class RealServerExistsError(RealServerError):
    """真实服务器已存在异常"""
    pass


class RealServerNotFoundError(RealServerError):
    """真实服务器未找到异常"""
    pass


class TemplateError(KeepAlivedConfigError):
    """模板错误异常"""
    pass


class TemplateNotFoundError(TemplateError):
    """模板未找到异常"""
    pass


class ConfigParseError(KeepAlivedConfigError):
    """配置解析错误异常"""
    pass


class ConfigSaveError(KeepAlivedConfigError):
    """配置保存错误异常"""
    pass


class ConfigValidationError(KeepAlivedConfigError):
    """配置验证错误异常"""
    pass