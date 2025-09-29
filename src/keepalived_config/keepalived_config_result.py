from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class OperationResult:
    """
    操作结果类，提供详细的操作执行信息
    """
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[Exception] = None

    def __bool__(self):
        """使对象可以直接用于布尔判断"""
        return self.success

    @classmethod
    def ok(cls, message: str = "", data: Optional[Any] = None) -> "OperationResult":
        """创建成功的操作结果"""
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str = "", error: Optional[Exception] = None) -> "OperationResult":
        """创建失败的操作结果"""
        return cls(success=False, message=message, error=error)