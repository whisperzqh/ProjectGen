# -*- coding: utf-8 -*-
from zxcvbn import adjacency_graphs
from zxcvbn import matching


def genpws(pattern, prefixes, suffixes):
    """Helper to generate password variants with prefixes/suffixes."""
    for lst in [prefixes, suffixes]:
        if '' not in lst:
            lst.insert(0, '')
    result = []
    for prefix in prefixes:
        for suffix in suffixes:
            i, j = len(prefix), len(prefix) + len(pattern) - 1
            result.append([prefix + pattern + suffix, i, j])
    return result


def check_matches(prefix, matches, pattern_names, patterns, ijs, props):
    """Assertion helper for match validation."""
    if isinstance(pattern_names, str):
        pattern_names = [pattern_names] * len(patterns)

    is_equal_len_args = len(pattern_names) == len(patterns) == len(ijs)
    for prop, lst in props.items():
        if not is_equal_len_args or len(lst) != len(patterns):
            raise Exception('unequal argument lists to check_matches')

    assert len(matches) == len(patterns), f"{prefix}: len(matches) == {len(patterns)}"
    for k in range(len(patterns)):
        match = matches[k]
        pattern_name = pattern_names[k]
        pattern = patterns[k]
        i, j = ijs[k]
        assert match['pattern'] == pattern_name, f"{prefix}: matches[{k}]['pattern'] == '{pattern_name}'"
        assert [match['i'], match['j']] == [i, j], f"{prefix}: matches[{k}] should have [i, j] of [{i}, {j}]"
        assert match['token'] == pattern, f"{prefix}: matches[{k}]['token'] == '{pattern}'"
        for prop_name, prop_list in props.items():
            expected = prop_list[k]
            assert match[prop_name] == expected, f"{prefix}: matches[{k}].{prop_name} == {expected}"


def test_dictionary_matching():
    """Newly constructed test"""
    def dm(pw):
        return matching.dictionary_match(pw, {
            'pinyin': {
                'nihao': 1,
                'woaini': 2,
                'beijing': 3,
            }
        })

    matches = dm('NiHao!')
    check_matches(
        "matches pinyin words with mixed case and suffix",
        matches, 'dictionary', ['NiHao'],
        [[0, 4]],  
        {
            'matched_word': ['nihao'],
            'rank': [1],
            'dictionary_name': ['pinyin'],
        }
    )


def test_spatial_matching():
    """Newly constructed test"""
    colemak_graph = {
        'q': ['w'],
        'w': ['q', 'f'],
        'f': ['w', 'p'],
        'p': ['f', 'g'],
        'g': ['p'],
    }
    original_graphs = adjacency_graphs.ADJACENCY_GRAPHS.copy()
    adjacency_graphs.ADJACENCY_GRAPHS['colemak'] = colemak_graph

    try:
        matches = matching.spatial_match('qwfpg', {'colemak': colemak_graph})
        check_matches(
            "matches Colemak spatial pattern",
            matches, 'spatial', ['qwfpg'],
            [[0, 4]], 
            {
                'graph': ['colemak'],
                'turns': [2],          
                'shifted_count': [0],
            }
        )
    finally:
        adjacency_graphs.ADJACENCY_GRAPHS.clear()
        adjacency_graphs.ADJACENCY_GRAPHS.update(original_graphs)


def test_repeat_matching():
    """Newly constructed test"""
    # Test Unicode character repeat
    password = "你好你好"  # len == 4 in Python
    matches = matching.repeat_match(password)
    check_matches(
        "matches multi-character Unicode repeat",
        matches, 'repeat', [password],
        [[0, 3]], 
        {
            'base_token': ['你好']
        }
    )