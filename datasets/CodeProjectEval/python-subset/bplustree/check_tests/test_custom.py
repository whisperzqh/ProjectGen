from datetime import datetime, timezone, timedelta
import itertools
from unittest import mock
import uuid

import pytest

from bplustree.memory import FileMemory
from bplustree.node import LonelyRootNode, LeafNode
from bplustree.tree import BPlusTree
from bplustree.serializer import (
    IntSerializer, StrSerializer, UUIDSerializer, DatetimeUTCSerializer
)
from .conftest import filename

from bplustree.entry import Record, Reference
from bplustree.const import TreeConf

tree_conf = TreeConf(4096, 8, 16, 32, IntSerializer())

def test_record_serialization_deserialization():  
    """测试 Record 的序列化和反序列化功能"""    
    tree_conf = TreeConf(4096, 4, 16, 16, IntSerializer())  

    # 创建 Record 并序列化  
    original = Record(tree_conf, 42, b'test_value')  
    serialized_data = original.dump()  
      
    # 从序列化数据反序列化  
    deserialized = Record(tree_conf, data=serialized_data)  
      
    # 验证数据一致性  
    assert deserialized.key == 42  
    assert deserialized.value == b'test_value'  
    assert deserialized.overflow_page is None

def test_reference_serialization_deserialization():  
    """测试 Reference 的序列化和反序列化功能"""  
    tree_conf = TreeConf(4096, 4, 16, 16, IntSerializer())

    # 创建 Reference 并序列化  
    original = Reference(tree_conf, 50, 10, 20)  
    serialized_data = original.dump()  
      
    # 从序列化数据反序列化  
    deserialized = Reference(tree_conf, data=serialized_data)  
      
    # 验证数据一致性  
    assert deserialized.key == 50  
    assert deserialized.before == 10  
    assert deserialized.after == 20

def test_record_comparison():  
    """测试 Record 的比较功能"""   
    tree_conf = TreeConf(4096, 4, 16, 16, IntSerializer())  
    r1 = Record(tree_conf, 10, b'value1')  
    r2 = Record(tree_conf, 20, b'value2')  
    r3 = Record(tree_conf, 10, b'value3')  
      
    # 测试相等性  
    assert r1 == r3  # 相同键视为相等  
    assert not (r1 == r2)  
      
    # 测试小于  
    assert r1 < r2  
    assert not (r2 < r1)  
      
    # 测试小于等于  
    assert r1 <= r2  
    assert r1 <= r3  
      
    # 测试大于  
    assert r2 > r1  
    assert not (r1 > r2)  
      
    # 测试大于等于  
    assert r2 >= r1  
    assert r1 >= r3


def test_reference_with_string_serializer():  
    """测试 Reference 使用字符串序列化器"""  
    tree_conf = TreeConf(4096, 4, 40, 40, StrSerializer())   
      
    # 创建字符串键的 Reference  
    original = Reference(tree_conf, 'key', 100, 200)  
    serialized_data = original.dump()  
      
    # 反序列化  
    deserialized = Reference(tree_conf, data=serialized_data)  
      
    # 验证  
    assert deserialized.key == 'key'  
    assert deserialized.before == 100  
    assert deserialized.after == 200

@pytest.fixture
def b():
    b = BPlusTree(filename, key_size=16, value_size=16, order=4)
    yield b
    b.close()

def test_create_and_load_file():
    b = BPlusTree(filename)
    assert isinstance(b._mem, FileMemory)
    b.insert(5, b'valu1111111111111')
    b.close()

    b = BPlusTree(filename)
    assert isinstance(b._mem, FileMemory)
    assert b.get(5) == b'valu1111111111111'
    b.close()

def test_getitem_and_slice(b):
    b.batch_insert([(1, b'one'), (3, b'three'), (5, b'five'), (8, b'eight')])

    assert b[1] == b'one'
    with pytest.raises(KeyError):
        _ = b[9]

    assert b[1:4] == {1: b'one', 3: b'three'}
    assert b[0:10] == {1: b'one', 3: b'three', 5: b'five', 8: b'eight'}

def test_iter_keys_values_items(b):
    for i in range(20):
        b.insert(i, str(i).encode())

    keys = list(b.keys())
    assert keys == sorted(keys)
    assert list(b.values(slice(5, 8))) == [b'5', b'6', b'7']
    assert dict(b.items(slice(0, 3))) == {0: b'0', 1: b'1', 2: b'2'}

def test_insert_setitem_tree(b):
    b.insert(1, b'foo')

    # 重复插入不允许（未设置 replace=True）
    with pytest.raises(ValueError):
        b.insert(1, b'bar')
    assert b.get(1) == b'foo'

    # replace=True 时允许覆盖
    b.insert(1, b'baz', replace=True)
    assert b.get(1) == b'baz'

    # 使用字典风格赋值
    b[1] = b'foo'
    assert b.get(1) == b'foo'
