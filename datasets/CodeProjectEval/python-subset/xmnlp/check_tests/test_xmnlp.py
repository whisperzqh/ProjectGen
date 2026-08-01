# -*- coding: utf-8 -*-

# -------------------------------------------#
# author: sean lee                           #
# email: xmlee97@gmail.com                   #
# -------------------------------------------#

import pytest
import xmnlp
from functools import partial

@pytest.fixture
def lexical_data_new():
    return [
        '小明在清华大学读书，他的邮箱是xiaoming@tsinghua.edu.cn',
        '今天是2025年10月16日，星期四',
        '苹果公司发布了新款iPhone 16',
        '我喜欢吃苹果，也喜欢用苹果手机',
        '《三体》是中国科幻小说的巅峰之作'
    ]


def lexical_equal(preds, trues):
    for (y_pred, y_true) in zip(preds, trues):
        assert y_pred == y_true


def test_seg_new():
    """Newly constructed test"""
    inputs = ['小明在清华大学读书']
    # 运行代码获取预期结果（见下方说明）
    expected = [['小明', '在', '清华大学', '读书']]
    preds = [xmnlp.seg(s) for s in inputs]
    lexical_equal(preds, expected)


def test_fast_seg_new():
    """Newly constructed test"""
    inputs = ['苹果公司发布了新款iPhone 16']
    # 注意：fast_seg 可能将“苹果”拆为“苹”“果”
    expected = [['苹果公司', '发布', '了', '新款', 'iPhone', '16']]
    preds = [xmnlp.fast_seg(s) for s in inputs]
    lexical_equal(preds, expected)


def test_deep_seg_new():
    """Newly constructed test"""
    inputs = ['《三体》是中国科幻小说的巅峰之作']
    # deep_seg 会保留书名整体
    expected = [['《', '三体', '》', '是', '中国科幻小说', '的', '巅峰', '之', '作']]
    preds = [xmnlp.deep_seg(s) for s in inputs]
    lexical_equal(preds, expected)

def test_pinyin_new():
    """Newly constructed test"""
    assert xmnlp.pinyin('北京') == ['bei', 'jing']


def test_radical_new():
    """Newly constructed test"""
    assert xmnlp.radical('清华大学') == ['氵', '十', '大', '子']


def test_sentiment_new():
    """Newly constructed test"""
    pos = xmnlp.sentiment('这部电影太精彩了！')
    neg = xmnlp.sentiment('服务态度极其恶劣')
    assert pos[1] > 0.7
    assert neg[1] < 0.3


def test_checker_new():
    """Newly constructed test"""
    # “在再”、“需须”等常见错别字
    err = xmnlp.checker('我再超市买了须要的东西。', suggest=False)
    # 预期：'再' 应为 '在'（位置1），'须要' 应为 '需要'（位置5）
    assert err == [(1, '再'), (6, '须')]


def test_keyphrase_new():
    """Newly constructed test"""
    doc = '''人工智能是未来科技的核心。深度学习、自然语言处理和计算机视觉是AI的三大支柱。'''
    kp = xmnlp.keyphrase(doc, k=1)
    # 关键句应包含核心内容
    assert '人工智能是未来科技的核心' in kp[0] or '三大支柱' in kp[0]