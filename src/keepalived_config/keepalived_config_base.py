from typing import Optional, List, Dict, Any, Union
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam
from keepalived_config.keepalived_config_comment import (
    KeepAlivedConfigComment,
    KeepAlivedConfigCommentTypes,
)


class KeepAlivedConfigBase:
    """
    Keepalived配置管理基类，提供通用的配置操作方法
    """

    def _get_param(self, block: KeepAlivedConfigBlock, param_name: str) -> Optional[KeepAlivedConfigParam]:
        """
        在块中查找指定名称的参数
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            param_name (str): 参数名称
            
        Returns:
            Optional[KeepAlivedConfigParam]: 参数对象，如果不存在则返回None
        """
        for param in block.params:
            if isinstance(param, KeepAlivedConfigParam) and param.name == param_name:
                return param
        return None

    def _update_param(self, block: KeepAlivedConfigBlock, param_name: str, param_value: str):
        """
        更新块中的参数值
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            param_name (str): 参数名称
            param_value (str): 参数值
        """
        param = self._get_param(block, param_name)
        if param is not None:
            param.value = param_value
        else:
            block.add_param(KeepAlivedConfigParam(param_name, param_value))

    def _get_sub_block(self, block: KeepAlivedConfigBlock, block_name: str) -> Optional[KeepAlivedConfigBlock]:
        """
        在块中查找指定名称的子块
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            block_name (str): 子块名称
            
        Returns:
            Optional[KeepAlivedConfigBlock]: 子块对象，如果不存在则返回None
        """
        for param in block.params:
            if isinstance(param, KeepAlivedConfigBlock) and param.name == block_name:
                return param
        return None

    def _add_comment(self, block: KeepAlivedConfigBlock, comment: str, inline: bool = False):
        """
        为块添加注释
        
        Args:
            block (KeepAlivedConfigBlock): 配置块
            comment (str): 注释内容
            inline (bool): 是否为行内注释
        """
        comment_type = KeepAlivedConfigCommentTypes.INLINE if inline else KeepAlivedConfigCommentTypes.GENERIC
        block.add_param(KeepAlivedConfigComment(comment, type=comment_type))

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
        if comment:
            self._add_comment(block, comment)
            
        param = KeepAlivedConfigParam(param_name, param_value)
        
        if inline_comment:
            param.add_comment(KeepAlivedConfigComment(inline_comment, type=KeepAlivedConfigCommentTypes.INLINE))
            
        block.add_param(param)