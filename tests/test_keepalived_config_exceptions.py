import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config_exceptions import (
    KeepAlivedConfigError,
    KeepAlivedConfigValueError,
    KeepAlivedConfigTypeError,
    VRRPInstanceExistsError,
    VRRPInstanceNotFoundError,
    VRRPParameterError,
    VirtualServerError,
    VirtualServerExistsError,
    VirtualServerNotFoundError,
    VirtualServerParameterError,
    RealServerError,
    RealServerExistsError,
    RealServerNotFoundError,
    TemplateError,
    TemplateNotFoundError,
    ConfigParseError,
    ConfigSaveError,
    ConfigValidationError
)


def test_base_exceptions():
    """Test base exception classes"""
    # Test KeepAlivedConfigError
    with pytest.raises(KeepAlivedConfigError):
        raise KeepAlivedConfigError("Base error")
    
    # Test KeepAlivedConfigValueError
    with pytest.raises(KeepAlivedConfigValueError):
        raise KeepAlivedConfigValueError("Value error")
    
    # Test that KeepAlivedConfigValueError is also a ValueError
    with pytest.raises(ValueError):
        raise KeepAlivedConfigValueError("Value error")
    
    # Test KeepAlivedConfigTypeError
    with pytest.raises(KeepAlivedConfigTypeError):
        raise KeepAlivedConfigTypeError("Type error")
    
    # Test that KeepAlivedConfigTypeError is also a TypeError
    with pytest.raises(TypeError):
        raise KeepAlivedConfigTypeError("Type error")


def test_vrrp_exceptions():
    """Test VRRP exception classes"""
    # Test VRRPInstanceExistsError
    with pytest.raises(VRRPInstanceExistsError):
        raise VRRPInstanceExistsError("VRRP instance already exists")
    
    # Test VRRPInstanceNotFoundError
    with pytest.raises(VRRPInstanceNotFoundError):
        raise VRRPInstanceNotFoundError("VRRP instance not found")
    
    # Test VRRPParameterError
    with pytest.raises(VRRPParameterError):
        raise VRRPParameterError("VRRP parameter error")


def test_virtual_server_exceptions():
    """Test virtual server exception classes"""
    # Test VirtualServerError
    with pytest.raises(VirtualServerError):
        raise VirtualServerError("Virtual server error")
    
    # Test VirtualServerExistsError
    with pytest.raises(VirtualServerExistsError):
        raise VirtualServerExistsError("Virtual server already exists")
    
    # Test that VirtualServerExistsError is also a VirtualServerError
    with pytest.raises(VirtualServerError):
        raise VirtualServerExistsError("Virtual server already exists")
    
    # Test VirtualServerNotFoundError
    with pytest.raises(VirtualServerNotFoundError):
        raise VirtualServerNotFoundError("Virtual server not found")
    
    # Test that VirtualServerNotFoundError is also a VirtualServerError
    with pytest.raises(VirtualServerError):
        raise VirtualServerNotFoundError("Virtual server not found")
    
    # Test VirtualServerParameterError
    with pytest.raises(VirtualServerParameterError):
        raise VirtualServerParameterError("Virtual server parameter error")
    
    # Test that VirtualServerParameterError is also a VirtualServerError
    with pytest.raises(VirtualServerError):
        raise VirtualServerParameterError("Virtual server parameter error")


def test_real_server_exceptions():
    """Test real server exception classes"""
    # Test RealServerError
    with pytest.raises(RealServerError):
        raise RealServerError("Real server error")
    
    # Test that RealServerError is also a VirtualServerError
    with pytest.raises(VirtualServerError):
        raise RealServerError("Real server error")
    
    # Test RealServerExistsError
    with pytest.raises(RealServerExistsError):
        raise RealServerExistsError("Real server already exists")
    
    # Test that RealServerExistsError is also a RealServerError
    with pytest.raises(RealServerError):
        raise RealServerExistsError("Real server already exists")
    
    # Test RealServerNotFoundError
    with pytest.raises(RealServerNotFoundError):
        raise RealServerNotFoundError("Real server not found")
    
    # Test that RealServerNotFoundError is also a RealServerError
    with pytest.raises(RealServerError):
        raise RealServerNotFoundError("Real server not found")


def test_template_exceptions():
    """Test template exception classes"""
    # Test TemplateError
    with pytest.raises(TemplateError):
        raise TemplateError("Template error")
    
    # Test TemplateNotFoundError
    with pytest.raises(TemplateNotFoundError):
        raise TemplateNotFoundError("Template not found")
    
    # Test that TemplateNotFoundError is also a TemplateError
    with pytest.raises(TemplateError):
        raise TemplateNotFoundError("Template not found")


def test_config_exceptions():
    """Test config exception classes"""
    # Test ConfigParseError
    with pytest.raises(ConfigParseError):
        raise ConfigParseError("Config parse error")
    
    # Test ConfigSaveError
    with pytest.raises(ConfigSaveError):
        raise ConfigSaveError("Config save error")
    
    # Test ConfigValidationError
    with pytest.raises(ConfigValidationError):
        raise ConfigValidationError("Config validation error")


if __name__ == "__main__":
    pytest.main([__file__])