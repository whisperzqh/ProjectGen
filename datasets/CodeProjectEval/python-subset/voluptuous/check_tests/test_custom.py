"""Core schema validation tests (version 2, reimagined dataset)."""
'''
import pytest
import re
from voluptuous import (
    Schema,
    In,
    NotIn,
    Contains,
    Remove,
    Equal,
    Range,
    Match,
    MultipleInvalid,
    Invalid,
)
'''

import collections
import copy
import os
import sys
from enum import Enum
import re
import pytest

from voluptuous import (
    ALLOW_EXTRA,
    PREVENT_EXTRA,
    REMOVE_EXTRA,
    All,
    AllInvalid,
    Any,
    Clamp,
    Coerce,
    Contains,
    ContainsInvalid,
    Date,
    Datetime,
    Email,
    EmailInvalid,
    Equal,
    ExactSequence,
    Exclusive,
    Extra,
    FqdnUrl,
    In,
    Inclusive,
    InInvalid,
    Invalid,
    IsDir,
    IsFile,
    Length,
    Literal,
    LiteralInvalid,
    Marker,
    Match,
    MatchInvalid,
    Maybe,
    MultipleInvalid,
    NotIn,
    NotInInvalid,
    Number,
    Object,
    Optional,
    PathExists,
    Range,
    Remove,
    Replace,
    Required,
    Schema,
    Self,
    SomeOf,
    TooManyValid,
    TypeInvalid,
    Union,
    Unordered,
    Url,
    UrlInvalid,
    raises,
    validate,
)
from voluptuous.humanize import humanize_error
from voluptuous.util import Capitalize, Lower, Strip, Title, Upper

# --- 1. In validator ---------------------------------------------------------
def test_in_v2():
    """Verify that 'In' validator works with new color set."""
    schema = Schema({"fruit": In(["apple", "banana", "grape"])})
    assert schema({"fruit": "banana"}) == {"fruit": "banana"}

    with pytest.raises(
        MultipleInvalid,
        match=r"value must be one of \['apple', 'banana', 'grape'\]",
    ):
        schema({"fruit": "orange"})


# --- 2. NotIn validator ------------------------------------------------------
def test_not_in_v2():
    """Verify that 'NotIn' validator correctly rejects forbidden values."""
    schema = Schema({"word": NotIn(["spam", "scam", "fake"])})
    assert schema({"word": "trust"}) == {"word": "trust"}

    with pytest.raises(
        MultipleInvalid,
        match=r"value must not be one of \['fake', 'scam', 'spam'\]",
    ):
        schema({"word": "spam"})


# --- 3. Contains validator ---------------------------------------------------
def test_contains_v2():
    """Verify that 'Contains' validator enforces required numbers in list."""
    schema = Schema({"numbers": Contains(5)})
    assert schema({"numbers": [1, 2, 5, 8]}) == {"numbers": [1, 2, 5, 8]}

    with pytest.raises(MultipleInvalid, match="value is not allowed"):
        schema({"numbers": [1, 2, 3, 4]})


# --- 4. Remove validator -----------------------------------------------------
def test_remove_v2():
    """Verify that 'Remove' properly strips unwanted keys and values."""
    # Remove dictionary keys
    schema = Schema({"id": int, Remove("temp"): str})
    result = schema({"id": 10, "temp": "outdated"})
    assert "temp" not in result and "id" in result

    # Remove unwanted values from list
    schema = Schema([Remove(0), int])
    cleaned = schema([0, 1, 2, 0, 3, 4])
    assert cleaned == [1, 2, 3, 4]


# --- 5. Equal validator ------------------------------------------------------
def test_equal_v2():
    """Ensure Equal validator checks exact match across types."""
    from voluptuous import Equal

    schema = Schema(Equal("HELLO"))
    assert schema("HELLO") == "HELLO"

    #with pytest.raises(Invalid, match=r"not a valid value"):
    with pytest.raises(Invalid, match=re.compile(r"Values are not equal", re.IGNORECASE)):
        schema("hello")  # Case mismatch

    schema = Schema(Equal([10, 20]))
    assert schema([10, 20]) == [10, 20]

    with pytest.raises(Invalid):
        schema([10, 20, 30])


# --- 6. Range validator ------------------------------------------------------
def test_range_v2():
    """Test Range validator with float and negative numbers."""
    schema = Schema(Range(min=-5.0, max=5.0))
    assert schema(0.0) == 0.0
    assert schema(-4.5) == -4.5

    with pytest.raises(MultipleInvalid):
        schema(-6.0)
    with pytest.raises(MultipleInvalid):
        schema(8.0)


# --- 7. Phone number format validation --------------------------------------
def test_phone_format_v2():
    """Validate phone numbers using regex match."""
    schema = Schema({"phone": Match(r"^\+?\d{10,15}$")})
    assert schema({"phone": "+8613800138000"}) == {"phone": "+8613800138000"}

    with pytest.raises(MultipleInvalid, match=r"does not match regular expression"):
        schema({"phone": "123-abc"})


# --- 8. URL-like validation --------------------------------------------------
def test_url_format_v2():
    """Validate URLs with correct protocol and domain format."""
    schema = Schema({"url": Match(r"^https?://[a-z0-9.-]+\.[a-z]{2,}$")})
    assert schema({"url": "https://openai.com"}) == {"url": "https://openai.com"}

    with pytest.raises(MultipleInvalid, match=r"does not match regular expression"):
        schema({"url": "ftp://openai.com"})

    with pytest.raises(MultipleInvalid, match=r"does not match regular expression"):
        schema({"url": "http://example"})

# --- 9. Combined test to ensure all schema types interact correctly ----------
def test_combined_schema_v2():
    """Integration test combining multiple validators in one schema."""
    schema = Schema(
        {
            "name": In(["Alice", "Bob", "Charlie"]),
            "age": Range(min=0, max=120),
            "tags": Contains("member"),
            "email": Match(r"^[\w\.-]+@[\w\.-]+\.\w+$"),
        }
    )

    valid = {"name": "Alice", "age": 25, "tags": ["member", "active"], "email": "alice@example.com"}
    assert schema(valid) == valid

    with pytest.raises(MultipleInvalid):
        schema({"name": "Eve", "age": -5, "tags": [], "email": "invalid@"})


def test_humanize_error_rewritten():
    """
    重写 test_humanize_error:
    使用一个包含 Email 和嵌套字典（包含布尔值）的新 schema。
    """
    # 新的数据和 schema
    data = {'user': 'not-an-email', 'config': {'active': 'yes', 'level': 10}}
    schema = Schema({'user': Email(), 'config': {'active': bool, 'level': str}})

    with pytest.raises(MultipleInvalid) as ctx:
        schema(data)

    # 验证新 schema 产生了两个错误
    assert len(ctx.value.errors) == 3

    # 生成预期的人性化错误字符串
    # 注意：错误的顺序取决于字典迭代，在现代 Python 中是可预测的
    expected_error_str = (
        "expected an email address for dictionary value @ data['user']. Got 'not-an-email'\n"
        "expected bool for dictionary value @ data['config']['active']. Got 'yes'\n"
        "expected str for dictionary value @ data['config']['level']. Got 10"
    )

    # 由于字典迭代顺序可能在不同测试运行中（理论上）变化，我们检查两种可能的顺序
    # （尽管在 Python 3.7+ 中，字典顺序是稳定的）
    # 更新：实际上有三个错误，让我们检查所有三个

    actual_error = humanize_error(data, ctx.value)

    # 为确保测试稳定性，我们只检查所有预期的错误信息是否都存在
    assert "expected an email address for dictionary value @ data['user']. Got 'not-an-email'" in actual_error
    assert "expected bool for dictionary value @ data['config']['active']. Got 'yes'" in actual_error
    assert "expected str for dictionary value @ data['config']['level']. Got 10" in actual_error


def test_validate_with_humanized_errors_failure_rewritten():
    """
    重写 test_validate_with_humanized_errors_failure:
    使用一个包含 Range 和 Length 校验的新 schema。
    """
    # 导入 'Error' 和 'validate_with_humanized_errors'
    from voluptuous.humanize import Error, validate_with_humanized_errors

    # 新 schema，使用 Range 和 Length
    schema = Schema({
        'id': All(int, Range(min=1000)),
        'code': Length(min=8, max=10)
    })

    # 违反新 schema 的数据
    data = {'id': 99, 'code': 'short'}

    with pytest.raises(Error) as ctx:
        validate_with_humanized_errors(data, schema)

    error_message = str(ctx.value)

    # 检查新 schema 产生的新错误信息
    assert "value must be at least 1000 for dictionary value @ data['id']" in error_message
    assert "length of value must be at least 8 for dictionary value @ data['code']" in error_message

    # 检查 'Got' 部分是否包含了不正确的数据
    assert "Got 99" in error_message
    assert "Got 'short'" in error_message
