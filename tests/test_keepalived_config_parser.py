import os
import sys
import pytest

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)

from keepalived_config.keepalived_config_parser import KeepAlivedConfigParser
from keepalived_config.keepalived_config_exceptions import ConfigParseError, KeepAlivedConfigValueError


def test_invalid_parse_string():
    invalid_items = [
        None,
        123,
        0.3,
        True,
        {"a": "b"},
        ["a", "b"],
    ]

    def verify_invalid_parse_string(item):
        with pytest.raises(TypeError):
            KeepAlivedConfigParser().parse_string(item)

    for item in invalid_items:
        verify_invalid_parse_string(item)

    with pytest.raises(KeepAlivedConfigValueError):
        KeepAlivedConfigParser().parse_string("")

    # test with valid string but syntax error
    with pytest.raises(ConfigParseError):
        KeepAlivedConfigParser().parse_string("global_defs {")


def test_valid_parse_string():
    valid_strings = [
        " ",
        "\n",
        "param value",
        "param value\n",
        "param value\nparam2 value2",
        "block {\n}",
        "block {\nparam value\n}",
        "# comment",
        "! comment",
        "param value # inline comment",
    ]

    def verify_valid_parse_string(string):
        config = KeepAlivedConfigParser().parse_string(string)        
        assert config is not None

    for string in valid_strings:
        verify_valid_parse_string(string)
        
    # 测试空字符串应该抛出异常
    from keepalived_config.keepalived_config_exceptions import KeepAlivedConfigValueError
    with pytest.raises(KeepAlivedConfigValueError):
        KeepAlivedConfigParser().parse_string("")


def test_invalid_parse_file():
    with pytest.raises(FileNotFoundError):
        KeepAlivedConfigParser().parse_file("/non/existent/file.conf")


def test_valid_parse_file():
    # Create a temporary file
    temp_file = os.path.join(os.path.dirname(__file__), "temp_config.conf")
    try:
        with open(temp_file, "w") as f:
            f.write("global_defs {\nparam value\n}")

        config = KeepAlivedConfigParser().parse_file(temp_file)
        assert config is not None
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])