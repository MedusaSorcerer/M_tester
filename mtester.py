#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import re
import unittest

from medusa import get_dict_key

results_dict = {
    'Login': {
        'POST': {
            'response': {
                'identity': 1,
                'name': 'MedusaSorcerer'
            },
            'request': {
                'username': 'medusasorcerer',
                'password': 'medusasorcerer'
            }
        }
    }
}


def get_result_dict(keys):
    """ [title].[method].[request|response] """

    def _list_handler(_v):
        _value = list()
        for _i in _v:
            if isinstance(_i, list):
                _value.append(_list_handler(_i))
            elif isinstance(_i, dict):
                _value.append(_dict_handler(_i))
            elif isinstance(_i, str):
                _value.append(_str_handler(_i))
            else:
                _value.append(_i)
        return _value

    def _str_handler(_v):
        _regex = re.match(r'^(.*)\.(GET|POST|PUT|DELETE)\.(request|response)(\.(.*))?', _v)
        if _regex:
            return get_dict_key(results_dict[_regex.group(1)][_regex.group(2)][_regex.group(3)], _regex.group(5))
        return _v

    def _dict_handler(_v):
        _value = dict()
        for _k, _ in _v.items():
            if isinstance(_, str):
                _ = _str_handler(_)
            elif isinstance(_, list):
                _ = _list_handler(_)
            elif isinstance(_, dict):
                _ = _dict_handler(_)
            _value[_k] = _
        return _value

    if isinstance(keys, dict):
        return _dict_handler(keys)
    if isinstance(keys, list):
        return _list_handler(keys)
    if isinstance(keys, str):
        return _str_handler(keys)
    return keys


class MTester(unittest.TestCase):

    def test_01(self):
        keys = {'a': {'b': {'c': 1}}}
        self.assertEqual(get_result_dict(keys), {'a': {'b': {'c': 1}}})

    def test_02(self):
        keys = {'a': {'b': {'c': 'Login.POST.response.identity'}}}
        self.assertEqual(get_result_dict(keys), {'a': {'b': {'c': 1}}})

    def test_03(self):
        keys = 'Login.POST.response'
        self.assertEqual(get_result_dict(keys), {'identity': 1, 'name': 'MedusaSorcerer'})

    def test_04(self):
        keys = ['Login.POST.response.identity']
        self.assertEqual(get_result_dict(keys), [1])

    def test_05(self):
        keys = [{'a': 'Login.POST.response.identity'}, {'b': 'Login.POST.response.identity'}]
        self.assertEqual(get_result_dict(keys), [{'a': 1}, {'b': 1}])


if __name__ == '__main__':
    unittest.main()
