import os

from keepalived_config.keepalived_config_constants import KeepAlivedConfigConstants
from keepalived_config.keepalived_config_param import KeepAlivedConfigParam
from keepalived_config.keepalived_config_block import KeepAlivedConfigBlock
from keepalived_config.keepalived_config_comment import (
    KeepAlivedConfigComment,
    KeepAlivedConfigCommentTypes,
)
from keepalived_config.keepalived_config_exceptions import (
    KeepAlivedConfigTypeError,
    ConfigSaveError
)


class KeepAlivedConfig:

    def __init__(self, params: list = None, config_file=None):
        self._config_file = None
        self._params: list[KeepAlivedConfigBlock | KeepAlivedConfigParam] = []

        if config_file:
            self.config_file = config_file

        if params:
            self.set_params(params)

    @property
    def params(self):
        return self._params

    # 设置配置参数列表，验证参数类型
    def set_params(self, params: list):
        """
        设置配置参数列表，验证参数类型
        
        Args:
            params (list): 参数列表
            
        Raises:
            KeepAlivedConfigTypeError: 当参数类型错误时
            ValueError: 当参数列表包含无效参数时
        """
        if not isinstance(params, list):
            raise KeepAlivedConfigTypeError(f"Invalid params type '{type(params)}'! Expected 'list'")

        if list(
            filter(
                lambda c: not isinstance(c, KeepAlivedConfigParam)
                and not isinstance(c, KeepAlivedConfigBlock),
                params,
            )
        ):
            raise ValueError(
                f"Invalid params list! Expected list of {KeepAlivedConfigParam.__class__.__name__}' or {KeepAlivedConfigBlock.__class__.__name__}"
            )

        self._params = params

    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, config_file: str):
        """
        设置配置文件路径
        
        Args:
            config_file (str): 配置文件路径
            
        Raises:
            KeepAlivedConfigTypeError: 当配置文件路径类型错误时
            FileNotFoundError: 当配置文件不存在时
        """
        if not isinstance(config_file, str):
            raise KeepAlivedConfigTypeError(
                f"Invalid config_file type '{type(config_file)}'! Expected 'str'"
            )

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found!")

        self._config_file = config_file

    # 将配置保存到文件
    def save(self, file=None):
        """
        将配置保存到文件
        
        Args:
            file (str, optional): 保存文件路径
            
        Raises:
            ConfigSaveError: 当配置保存失败时
        """
        try:
            if not file:
                file = self.config_file

            with open(file, "w") as f:
                for item in self._params:
                    f.write(item.to_str() + "\n")
        except Exception as e:
            raise ConfigSaveError(f"保存配置失败: {str(e)}") from e