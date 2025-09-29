from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class VRRPConfig:
    """
    VRRP实例配置类，用于简化参数传递
    """
    state: str = "BACKUP"
    interface: str = "eth0"
    virtual_router_id: int = 51
    priority: int = 100
    advert_int: int = 1
    auth_type: str = "PASS"
    auth_pass: str = ""
    virtual_ipaddresses: Optional[List[str]] = None
    nopreempt: bool = False
    preempt_delay: Optional[int] = None
    garp_master_delay: Optional[int] = None
    # 扩展更多参数
    unicast_src_ip: Optional[str] = None
    unicast_peer: Optional[List[str]] = None
    smtp_alert: Optional[bool] = None
    notify_master: Optional[str] = None
    notify_backup: Optional[str] = None
    notify_fault: Optional[str] = None

    def __post_init__(self):
        if self.virtual_ipaddresses is None:
            self.virtual_ipaddresses = []


@dataclass
class VirtualServerConfig:
    """
    虚拟服务器配置类，用于简化参数传递
    """
    delay_loop: int = 6
    lb_algo: str = "rr"
    lb_kind: str = "DR"
    protocol: str = "TCP"
    persistence_timeout: Optional[int] = None
    persistence_granularity: Optional[str] = None
    virtualhost: Optional[str] = None
    # 扩展更多参数
    ha_suspend: Optional[bool] = None
    alpha: Optional[bool] = None
    omega: Optional[bool] = None
    quorum: Optional[int] = None
    quorum_up: Optional[str] = None
    quorum_down: Optional[str] = None
    hysteresis: Optional[int] = None
    retry: Optional[int] = None