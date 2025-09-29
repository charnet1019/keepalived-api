import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config_templates import KeepAlivedConfigTemplates
from keepalived_config.keepalived_config import KeepAlivedConfig


def test_template_registration():
    """Test template registration functionality"""
    # Define a custom template
    custom_template = {
        "type": "test_block",
        "params": {
            "test_param": "{test_value}"
        }
    }
    
    # Register the template
    KeepAlivedConfigTemplates.register_template("test_custom_template", custom_template)
    
    # Verify it's in the list
    templates = KeepAlivedConfigTemplates.list_templates()
    assert "test_custom_template" in templates
    
    # Verify we can create a config from it
    config = KeepAlivedConfigTemplates.from_template("test_custom_template", test_value="actual_value")
    assert isinstance(config, KeepAlivedConfig)
    assert len(config.params) == 1
    
    # Check that parameters were correctly replaced
    config_str = config.params[0].to_str()
    assert "test_param actual_value" in config_str


def test_template_unregistration():
    """Test template unregistration functionality"""
    # Define and register a temporary template
    temp_template = {
        "type": "temp_block",
        "params": {
            "temp_param": "{temp_value}"
        }
    }
    
    KeepAlivedConfigTemplates.register_template("temp_test_template", temp_template)
    
    # Verify it exists
    assert KeepAlivedConfigTemplates.template_exists("temp_test_template")
    
    # Unregister the template
    result = KeepAlivedConfigTemplates.unregister_template("temp_test_template")
    assert result is True
    
    # Verify it no longer exists
    assert not KeepAlivedConfigTemplates.template_exists("temp_test_template")
    
    # Try to unregister again - should return False
    result = KeepAlivedConfigTemplates.unregister_template("temp_test_template")
    assert result is False
    
    # Try to use the unregistered template - should raise an error
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.from_template("temp_test_template", temp_value="test")


def test_get_template():
    """Test getting template definition"""
    # Get an existing template
    template_def = KeepAlivedConfigTemplates.get_template("basic_vrrp")
    assert isinstance(template_def, dict)
    assert "type" in template_def
    assert "params" in template_def
    assert template_def["type"] == "vrrp_instance"
    
    # Try to get a non-existent template
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.get_template("non_existent_template")


def test_update_template():
    """Test updating an existing template"""
    # Create a modified template
    modified_template = {
        "type": "vrrp_instance",
        "params": {
            "state": "{state}",
            "interface": "eth0",  # Fixed value
            "virtual_router_id": "{virtual_router_id}",
            "priority": "{priority}"
        }
    }
    
    # Update the existing template
    KeepAlivedConfigTemplates.update_template("basic_vrrp", modified_template)
    
    # Verify the update by using the template
    config = KeepAlivedConfigTemplates.from_template(
        "basic_vrrp",
        "VI_TEST",
        state="MASTER",
        virtual_router_id=51,
        priority=100
    )
    
    config_str = config.params[0].to_str()
    assert "interface eth0" in config_str  # Should have the fixed value
    
    # Try to update a non-existent template
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.update_template("non_existent_template", modified_template)
    
    # Try to update with invalid definition
    with pytest.raises(ValueError):
        KeepAlivedConfigTemplates.update_template("basic_vrrp", {"invalid": "definition"})


def test_template_exists():
    """Test checking if a template exists"""
    # Check existing template
    assert KeepAlivedConfigTemplates.template_exists("basic_vrrp")
    
    # Check non-existent template
    assert not KeepAlivedConfigTemplates.template_exists("non_existent_template")
    
    # Register a new template and check
    new_template = {
        "type": "test_block",
        "params": {
            "test_param": "test_value"
        }
    }
    
    KeepAlivedConfigTemplates.register_template("new_test_template", new_template)
    assert KeepAlivedConfigTemplates.template_exists("new_test_template")
    
    # Unregister and check again
    KeepAlivedConfigTemplates.unregister_template("new_test_template")
    assert not KeepAlivedConfigTemplates.template_exists("new_test_template")


def test_template_isolation():
    """Test that templates are properly isolated and don't interfere with each other"""
    # Register two different templates
    template1 = {
        "type": "block1",
        "params": {
            "param1": "{value1}"
        }
    }
    
    template2 = {
        "type": "block2",
        "params": {
            "param2": "{value2}"
        }
    }
    
    KeepAlivedConfigTemplates.register_template("template1", template1)
    KeepAlivedConfigTemplates.register_template("template2", template2)
    
    # Use both templates
    config1 = KeepAlivedConfigTemplates.from_template("template1", value1="actual1")
    config2 = KeepAlivedConfigTemplates.from_template("template2", value2="actual2")
    
    # Verify they created different configurations
    str1 = config1.params[0].to_str()
    str2 = config2.params[0].to_str()
    
    assert "block1" in str1
    assert "param1 actual1" in str1
    assert "block2" in str2
    assert "param2 actual2" in str2


if __name__ == "__main__":
    pytest.main([__file__])