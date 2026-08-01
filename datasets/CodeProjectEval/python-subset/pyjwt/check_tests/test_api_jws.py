import pytest

from jwt.api_jws import PyJWS

try:
    from cryptography.hazmat.primitives.serialization import (
        load_pem_private_key,
        load_pem_public_key,
        load_ssh_public_key,
    )
except ModuleNotFoundError:
    pass


@pytest.fixture
def jws():
    return PyJWS()


@pytest.fixture
def payload():
    """Creates a sample jws claimset for use as a payload during tests"""
    return b"hello world"


class TestJWS:
    """Original test"""

    def test_load_verify_valid_jws(self, jws, payload):
        """Original test"""

        example_secret = "secret"
        example_jws = (
            b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            b"aGVsbG8gd29ybGQ."
            b"SIr03zM64awWRdPrAM_61QWsZchAtgDV3pphfHPPWkI"
        )

        decoded_payload = jws.decode(
            example_jws, key=example_secret, algorithms=["HS256"]
        )
        assert decoded_payload == payload

    