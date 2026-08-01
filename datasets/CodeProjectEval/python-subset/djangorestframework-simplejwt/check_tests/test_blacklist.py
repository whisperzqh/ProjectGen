import os
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        SECRET_KEY='dummy',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'rest_framework',
            'rest_framework_simplejwt.token_blacklist',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
        TIME_ZONE='UTC',
        REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES": []},
    )

django.setup()

import random
import string
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import aware_utcnow
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken



# from .utils import MigrationTestCase, override_api_settings

class MigrationTestCase:
    """
    A minimal stub of MigrationTestCase for testing without Django migrations.
    """
    migrate_from = None
    migrate_to = None

    # def setUp(self):
        # pass

    def setUp(self):
        # Create a fake apps registry for migration tests
        from django.apps import apps as django_apps
        super.setUp()
        self.apps = django_apps
        super().setUp()

    def setUpBeforeMigration(self, apps):
        pass


def override_api_settings(**kwargs):
    """
    Dummy decorator to mock override_api_settings in tests.
    """
    def decorator(func):
        return func
    return decorator


def rand_str(prefix="", length=6):
    return prefix + "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# ---------------------------------------------------------
# 1️⃣ 核心黑名单拦截逻辑
# ---------------------------------------------------------
class TestTokenBlacklistCore(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username=rand_str("usr_"),
            password=rand_str("pwd_"),
        )

    def test_token_will_not_validate_if_blacklisted(self):
        """验证：黑名单中的Token无法再次验证"""
        token = RefreshToken.for_user(self.user)
        outstanding_token = OutstandingToken.objects.first()

        # 初始可用
        RefreshToken(str(token))

        # 加入黑名单
        BlacklistedToken.objects.create(token=outstanding_token)

        # 应该抛出 TokenError
        with self.assertRaises(TokenError) as e:
            RefreshToken(str(token))
            self.assertIn("blacklisted", e.exception.args[0])


# ---------------------------------------------------------
# 2️⃣ 手动黑名单逻辑 + 重复创建检测
# ---------------------------------------------------------
class TestManualBlacklistBehavior(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username=rand_str("user_"),
            password=rand_str("pw_"),
        )

    def test_tokens_can_be_manually_blacklisted(self):
        """验证：Token可被手动加入黑名单并检测重复添加"""
        token = RefreshToken.for_user(self.user)
        RefreshToken(str(token))

        # 第一次加入黑名单
        blacklisted_token, created = token.blacklist()
        self.assertTrue(created)
        self.assertEqual(blacklisted_token.token.jti, token["jti"])

        # 第二次添加不应重复创建
        blacklisted_token, created = token.blacklist()
        self.assertFalse(created)

        # 新token应被正常加入
        new_token = RefreshToken()
        new_blacklisted, created = new_token.blacklist()
        self.assertTrue(created)
        self.assertEqual(new_blacklisted.token.jti, new_token["jti"])


# ---------------------------------------------------------
# 3️⃣ 清理过期Token命令
# ---------------------------------------------------------
class TestFlushExpiredTokens(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username=rand_str("usr_"),
            password=rand_str("pwd_"),
        )

    def test_it_should_delete_any_expired_tokens(self):
        """验证：flushexpiredtokens命令能删除过期的Token"""
        not_expired_1 = RefreshToken.for_user(self.user)
        not_expired_2 = RefreshToken.for_user(self.user)
        not_expired_3 = RefreshToken()

        not_expired_2.blacklist()
        not_expired_3.blacklist()

        fake_now = aware_utcnow() - api_settings.REFRESH_TOKEN_LIFETIME

        with patch("rest_framework_simplejwt.tokens.aware_utcnow") as fake_time:
            fake_time.return_value = fake_now
            expired_1 = RefreshToken.for_user(self.user)
            expired_2 = RefreshToken()

        expired_1.blacklist()
        expired_2.blacklist()

        not_expired_4 = RefreshToken.for_user(self.user)

        self.assertEqual(OutstandingToken.objects.count(), 6)
        self.assertEqual(BlacklistedToken.objects.count(), 4)

        call_command("flushexpiredtokens")

        # 确认删除后数量正确
        self.assertEqual(OutstandingToken.objects.count(), 4)
        self.assertEqual(BlacklistedToken.objects.count(), 2)

User = get_user_model()
AuthToken = api_settings.AUTH_TOKEN_CLASSES[0]


class TestJWTAuthentication(TestCase):
    def setUp(self):
        self.backend = authentication.JWTAuthentication()

    def test_get_validated_token(self):
        """验证：无效或过期 Token 应触发 InvalidToken 异常，正常 Token 可被验证"""
        token = AuthToken()
        token.set_exp(lifetime=-timedelta(days=1))  # 过期
        with self.assertRaises(InvalidToken):
            self.backend.get_validated_token(str(token))

        # 再生成一个有效 token
        token.set_exp()
        validated = self.backend.get_validated_token(str(token))
        self.assertEqual(validated.payload, token.payload)

    def test_get_user(self):
        """验证：用户不存在、非激活状态和正常登录的处理逻辑"""
        payload = {"some_other_id": "foo"}

        # 缺少用户识别字段，应抛 InvalidToken
        with self.assertRaises(InvalidToken):
            self.backend.get_user(payload)

        # 用户不存在
        payload[api_settings.USER_ID_CLAIM] = 99999
        with self.assertRaises(AuthenticationFailed):
            self.backend.get_user(payload)

        # 创建用户但设为非激活
        user = User.objects.create_user(username="random_user")
        user.is_active = False
        user.save()
        payload[api_settings.USER_ID_CLAIM] = getattr(user, api_settings.USER_ID_FIELD)

        with self.assertRaises(AuthenticationFailed):
            self.backend.get_user(payload)

        # 激活用户应正常返回
        user.is_active = True
        user.save()
        auth_user = self.backend.get_user(payload)
        self.assertEqual(auth_user.id, user.id)

