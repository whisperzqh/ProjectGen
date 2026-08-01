# -*- coding: utf-8 -*-
from zxcvbn import zxcvbn


def test_unicode_user_inputs():
    """Newly constructed test"""
    input_ = u'张伟محمد田中'
    password = u'密MậtKhẩu123!@#'

    zxcvbn(password, user_inputs=[input_])


def test_invalid_user_inputs():
    """Newly constructed test"""
    invalid_inputs = [42, True, [], {"name": "test"}, 3.14]
    password = u'StrongP@ss!'

    zxcvbn(password, user_inputs=invalid_inputs)


def test_long_password():
    """Newly constructed test"""
    base = "abcdefghijklmnopqrstuvwxyz0123456789!@#$"
    password = (base * 15)[:512]  
    zxcvbn(password, user_inputs=[None])