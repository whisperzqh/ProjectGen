import os
import django
from django.conf import settings

# 手动初始化 Django 配置（无需使用完整项目 settings）
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "rest_framework",
            "rest_framework_simplejwt",
        ],
        SECRET_KEY="dummy_secret_key_for_testing_only",
        USE_TZ=True,
        TIME_ZONE="UTC",
    )
    django.setup()


import pytest
import datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class TestCoreTokenMechanics:
    """Test the core behaviors of token creation, decoding, and validation."""

    def test_basic_token_creation_and_verification(self):
        """Ensure AccessToken encodes and decodes claims correctly."""
        token = AccessToken()
        token["user_id"] = "alpha_user_88"
        token["permissions"] = ["read", "write"]
        token["iat"] = int(timezone.now().timestamp())

        # Decode via UntypedToken should yield same claims
        decoded = UntypedToken(str(token))
        assert decoded["user_id"] == "alpha_user_88"
        assert "permissions" in decoded
        assert decoded["permissions"] == ["read", "write"]

    def test_refresh_access_token_linkage(self):
        """Test RefreshToken can generate linked AccessToken."""
        refresh = RefreshToken()
        refresh["session_id"] = "sess_90210_xyz"
        refresh["origin"] = "mobile_app"

        access = refresh.access_token
        assert isinstance(access, AccessToken)
        assert access["jti"] != refresh["jti"]  # distinct token IDs
        assert access["token_type"] == "access"

    def test_invalid_token_detection(self):
        """Ensure invalid or tampered tokens raise appropriate exceptions."""
        invalid_token_str = "abc.def.ghi"
        with pytest.raises(TokenError):
            UntypedToken(invalid_token_str)

        # Expired token
        expired = AccessToken()
        expired.set_exp(from_time=timezone.now() - datetime.timedelta(days=2))
        # with pytest.raises(InvalidToken):
            # UntypedToken(str(expired))
        with pytest.raises((InvalidToken, TokenError)):
            UntypedToken(str(expired))



