import copy
from keepalived_config.keepalived_config_constants import KeepAlivedConfigConstants
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_comment import (
    KeepAlivedConfigComment,
    KeepAlivedConfigCommentTypes,
)
from keepalived_config.keepalived_config import KeepAlivedConfig


class KeepAlivedConfigTemplates:
    # Common configuration templates
    _templates = {
        "basic_vrrp": {
            "type": "vrrp_instance",
            "params": {
                "state": "{state}",
                "interface": "{interface}",
                "virtual_router_id": "{virtual_router_id}",
                "priority": "{priority}",
                "advert_int": "{advert_int}",
                "authentication": {
                    "auth_type": "{auth_type}",
                    "auth_pass": "{auth_pass}"
                },
                "virtual_ipaddress": ["{virtual_ipaddress}"]
            }
        },
        "basic_global": {
            "type": "global_defs",
            "params": {
                "notification_email": ["{notification_email}"],
                "notification_email_from": "{notification_email_from}",
                "smtp_server": "{smtp_server}",
                "smtp_connect_timeout": "{smtp_connect_timeout}"
            }
        },
        "complete_vrrp_master": {
            "type": "vrrp_instance",
            "params": {
                "state": "MASTER",
                "interface": "{interface}",
                "virtual_router_id": "{virtual_router_id}",
                "priority": "{priority}",
                "advert_int": "{advert_int}",
                "authentication": {
                    "auth_type": "{auth_type}",
                    "auth_pass": "{auth_pass}"
                },
                "virtual_ipaddress": ["{virtual_ipaddress}"],
                "nopreempt": ""
            }
        },
        "complete_vrrp_backup": {
            "type": "vrrp_instance",
            "params": {
                "state": "BACKUP",
                "interface": "{interface}",
                "virtual_router_id": "{virtual_router_id}",
                "priority": "{priority}",
                "advert_int": "{advert_int}",
                "authentication": {
                    "auth_type": "{auth_type}",
                    "auth_pass": "{auth_pass}"
                },
                "virtual_ipaddress": ["{virtual_ipaddress}"]
            }
        },
        "basic_virtual_server": {
            "type": "virtual_server",
            "params": {
                "delay_loop": "{delay_loop}",
                "lb_algo": "{lb_algo}",
                "lb_kind": "{lb_kind}",
                "protocol": "{protocol}",
                "real_server": {
                    "ip": "{real_server_ip}",
                    "port": "{real_server_port}",
                    "weight": "{real_server_weight}",
                    "health_check": "{health_check_type}",  # TCP_CHECK or HTTP_GET or UDP_CHECK
                    "TCP_CHECK": {
                        "connect_timeout": "{tcp_connect_timeout}",
                        "delay_before_retry": "{tcp_delay_before_retry}"
                    },
                    "HTTP_GET": {
                        "url": "{http_url}",
                        "digest": "{http_digest}",
                        "status_code": "{http_status_code}"
                    },
                    "UDP_CHECK": {
                        "connect_timeout": "{udp_connect_timeout}",
                        "delay_before_retry": "{udp_delay_before_retry}"
                    }
                }
            }
        }
    }

    @classmethod
    def from_template(cls, template_name: str, instance_name: str = None, config_class=None, **kwargs) -> "KeepAlivedConfig":
        """
        Create configuration from template
        
        Args:
            template_name (str): Template name
            instance_name (str): Instance name (required for VRRP templates)
            config_class: The KeepAlivedConfig class to create instance from
            **kwargs: Template parameters for dynamic replacement
            
        Returns:
            KeepAlivedConfig: Configuration object created based on template
        """
        if template_name not in cls._templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(cls._templates.keys())}")
            
        if config_class is None:
            config_class = KeepAlivedConfig
            
        template = cls._templates[template_name]
        config = config_class()
        
        # Special handling for virtual_server template
        if template_name == "basic_virtual_server":
            block = KeepAlivedConfigBlock(template["type"], instance_name or "{virtual_server_ip} {virtual_server_port}")
            
            # Add basic parameters
            for param_name, param_value in template["params"].items():
                if param_name == "real_server":
                    # Process real_server using the helper method
                    real_server_block = cls._process_real_server(param_value, kwargs)
                    block.add_param(real_server_block)
                else:
                    block.add_param(KeepAlivedConfigParam(param_name, cls._replace_placeholders(str(param_value), kwargs)))
            config.params.append(block)
            return config
            
        # Handle VRRP templates
        if template["type"] == "vrrp_instance":
            if not instance_name:
                raise ValueError("Instance name is required for VRRP instance templates")
            block = KeepAlivedConfigBlock(template["type"], instance_name)
        else:
            block = KeepAlivedConfigBlock(template["type"])
        
        # Add parameters from template
        for param_name, param_value in template["params"].items():
            if isinstance(param_value, dict):
                # Nested blocks
                if param_name == "real_server":
                    # Special handling for real_server using the helper method
                    real_server_block = cls._process_real_server(param_value, kwargs)
                    block.add_param(real_server_block)
                else:
                    sub_block = KeepAlivedConfigBlock(param_name)
                    for sub_param_name, sub_param_value in param_value.items():
                        # Handle authentication password
                        if param_name == "authentication" and sub_param_name == "auth_pass":
                            if sub_param_value == "{auth_pass}":
                                # Use provided password or generate secure one
                                password = kwargs.get("auth_pass", "CHANGEME")
                                sub_block.add_param(KeepAlivedConfigParam(sub_param_name, password))
                            else:
                                sub_block.add_param(KeepAlivedConfigParam(sub_param_name, cls._replace_placeholders(str(sub_param_value), kwargs)))
                        else:
                            sub_block.add_param(KeepAlivedConfigParam(sub_param_name, cls._replace_placeholders(str(sub_param_value), kwargs)))
                    block.add_param(sub_block)
            elif isinstance(param_value, list):
                # List parameters
                if param_name == "virtual_ipaddress":
                    if "{virtual_ipaddress}" in param_value:
                        # Use provided virtual IP address
                        vip = kwargs.get("virtual_ipaddress", "192.168.1.100/24")
                        sub_block = KeepAlivedConfigBlock(param_name)
                        sub_block.add_param(KeepAlivedConfigParam("", vip))
                        block.add_param(sub_block)
                    else:
                        sub_block = KeepAlivedConfigBlock(param_name)
                        for ip in param_value:
                            sub_block.add_param(KeepAlivedConfigParam("", cls._replace_placeholders(str(ip), kwargs)))
                        block.add_param(sub_block)
                elif param_name == "notification_email":
                    if "{notification_email}" in param_value:
                        # Use provided notification email
                        email = kwargs.get("notification_email", "admin@example.com")
                        sub_block = KeepAlivedConfigBlock(param_name)
                        sub_block.add_param(KeepAlivedConfigParam("", email))
                        block.add_param(sub_block)
                    else:
                        sub_block = KeepAlivedConfigBlock(param_name)
                        for email in param_value:
                            sub_block.add_param(KeepAlivedConfigParam("", cls._replace_placeholders(str(email), kwargs)))
                        block.add_param(sub_block)
            else:
                # Simple parameters
                if param_value == "":
                    block.add_param(KeepAlivedConfigParam(param_name))
                else:
                    # Replace placeholders with provided values or defaults
                    replaced_value = cls._replace_placeholders(str(param_value), kwargs)
                    block.add_param(KeepAlivedConfigParam(param_name, replaced_value))
        
        config.params.append(block)
        return config

    @staticmethod
    def _process_real_server(real_server_config, template_params):
        """
        Process real_server configuration and create the corresponding block
        
        Args:
            real_server_config (dict): Real server configuration
            template_params (dict): Template parameters for dynamic replacement
            
        Returns:
            KeepAlivedConfigBlock: Real server block
        """
        # Get real server IP and port with defaults
        rs_ip = template_params.get("real_server_ip", real_server_config.get("ip", "192.168.1.101"))
        rs_port = template_params.get("real_server_port", real_server_config.get("port", "80"))
        
        real_server_block = KeepAlivedConfigBlock("real_server", f"{rs_ip} {rs_port}")
        
        # Get weight with default
        weight = template_params.get("real_server_weight", real_server_config.get("weight", "1"))
        real_server_block.add_param(KeepAlivedConfigParam("weight", str(weight)))
        
        # Add health check block based on health_check type
        health_check_type = template_params.get("health_check_type", real_server_config.get("health_check", "TCP_CHECK"))
        if health_check_type == "tcp_check" or health_check_type == "TCP_CHECK":
            # Add TCP_CHECK block
            tcp_check_block = KeepAlivedConfigBlock("TCP_CHECK")
            tcp_check_params = real_server_config["TCP_CHECK"]
            
            # Get TCP check parameters with defaults
            connect_timeout = template_params.get("tcp_connect_timeout", tcp_check_params.get("connect_timeout", "3"))
            delay_before_retry = template_params.get("tcp_delay_before_retry", tcp_check_params.get("delay_before_retry", "3"))
            
            tcp_check_block.add_param(KeepAlivedConfigParam("connect_timeout", str(connect_timeout)))
            tcp_check_block.add_param(KeepAlivedConfigParam("delay_before_retry", str(delay_before_retry)))
            real_server_block.add_param(tcp_check_block)
        elif health_check_type == "http_check" or health_check_type == "HTTP_GET":
            # Add HTTP_GET block
            http_check_block = KeepAlivedConfigBlock("HTTP_GET")
            http_check_params = real_server_config["HTTP_GET"]
            
            # Get HTTP check parameters with defaults
            url = template_params.get("http_url", http_check_params.get("url", "/"))
            digest = template_params.get("http_digest", http_check_params.get("digest"))
            status_code = template_params.get("http_status_code", http_check_params.get("status_code"))
            
            http_check_block.add_param(KeepAlivedConfigParam("url", str(url)))
            if digest is not None:
                http_check_block.add_param(KeepAlivedConfigParam("digest", str(digest)))
            if status_code is not None:
                http_check_block.add_param(KeepAlivedConfigParam("status_code", str(status_code)))
            real_server_block.add_param(http_check_block)
        elif health_check_type == "UDP_CHECK":
            # Add UDP_CHECK block
            udp_check_block = KeepAlivedConfigBlock("UDP_CHECK")
            udp_check_params = real_server_config["UDP_CHECK"]
            
            # Get UDP check parameters with defaults
            connect_timeout = template_params.get("udp_connect_timeout", udp_check_params.get("connect_timeout", "3"))
            delay_before_retry = template_params.get("udp_delay_before_retry", udp_check_params.get("delay_before_retry", "3"))
            
            udp_check_block.add_param(KeepAlivedConfigParam("connect_timeout", str(connect_timeout)))
            udp_check_block.add_param(KeepAlivedConfigParam("delay_before_retry", str(delay_before_retry)))
            real_server_block.add_param(udp_check_block)
            
        return real_server_block

    @classmethod
    def register_template(cls, template_name: str, template_definition: dict):
        """
        Register a new template or override an existing one
        
        Args:
            template_name (str): Name of the template
            template_definition (dict): Template definition with type and params
        """
        if not isinstance(template_definition, dict):
            raise ValueError("Template definition must be a dictionary")
            
        if "type" not in template_definition or "params" not in template_definition:
            raise ValueError("Template definition must contain 'type' and 'params' keys")
            
        cls._templates[template_name] = template_definition

    @classmethod
    def unregister_template(cls, template_name: str):
        """
        Unregister a template
        
        Args:
            template_name (str): Name of the template to unregister
            
        Returns:
            bool: True if template was unregistered, False if it didn't exist
        """
        if template_name in cls._templates:
            del cls._templates[template_name]
            return True
        return False

    @classmethod
    def get_template(cls, template_name: str) -> dict:
        """
        Get a template definition
        
        Args:
            template_name (str): Name of the template
            
        Returns:
            dict: Template definition
            
        Raises:
            ValueError: If template doesn't exist
        """
        if template_name not in cls._templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(cls._templates.keys())}")
        return cls._templates[template_name].copy()  # Return a copy to prevent modification of the original

    @classmethod
    def update_template(cls, template_name: str, template_definition: dict):
        """
        Update an existing template
        
        Args:
            template_name (str): Name of the template to update
            template_definition (dict): New template definition
            
        Raises:
            ValueError: If template doesn't exist or definition is invalid
        """
        if template_name not in cls._templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(cls._templates.keys())}")
            
        if not isinstance(template_definition, dict):
            raise ValueError("Template definition must be a dictionary")
            
        if "type" not in template_definition or "params" not in template_definition:
            raise ValueError("Template definition must contain 'type' and 'params' keys")
            
        cls._templates[template_name] = template_definition

    @classmethod
    def template_exists(cls, template_name: str) -> bool:
        """
        Check if a template exists
        
        Args:
            template_name (str): Name of the template
            
        Returns:
            bool: True if template exists, False otherwise
        """
        return template_name in cls._templates

    @classmethod
    def list_templates(cls) -> list:
        """
        List all available templates
        
        Returns:
            list: List of template names
        """
        return list(cls._templates.keys())
        
    @staticmethod
    def _replace_placeholders(text: str, template_params: dict) -> str:
        """
        Replace placeholders in text with provided values
        
        Args:
            text (str): Text with placeholders
            template_params (dict): Template parameters for replacement
            
        Returns:
            str: Text with placeholders replaced
        """
        result = text
        for key, value in template_params.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result