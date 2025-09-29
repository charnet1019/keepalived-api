class KeepAlivedConfigConstants:
    DEFAULT_PATH = "/etc/keepalived/keepalived.conf"
    INDENT_WIDTH = 4

    @staticmethod
    def get_indent(level: int = 0) -> str:
        return " " * (KeepAlivedConfigConstants.INDENT_WIDTH * level)


class KeepAlivedConfigDefaults:
    """默认配置值常量类"""
    
    # 虚拟服务器默认值
    VIRTUAL_SERVER_DELAY_LOOP = 6
    VIRTUAL_SERVER_LB_ALGO = "rr"
    VIRTUAL_SERVER_LB_KIND = "DR"
    VIRTUAL_SERVER_PROTOCOL = "TCP"
    
    # 真实服务器默认值
    REAL_SERVER_WEIGHT = 1
    REAL_SERVER_HEALTH_CHECK = "TCP_CHECK"
    
    # TCP_CHECK默认值
    TCP_CHECK_CONNECT_TIMEOUT = 3
    TCP_CHECK_DELAY_BEFORE_RETRY = 3
    
    # HTTP_GET默认值
    HTTP_GET_URL = "/"
    
    # UDP_CHECK默认值
    UDP_CHECK_CONNECT_TIMEOUT = 3
    UDP_CHECK_DELAY_BEFORE_RETRY = 3
