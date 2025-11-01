import pytest

from jwt.api_jwt import PyJWT


@pytest.fixture
def jwt():
    return PyJWT()


class TestJWTExtracted:
    """Newly constructed test"""

    def test_decodes_valid_jwt(self, jwt):
        """Newly constructed test"""

        example_payload = {"user_id": 98765, "role": "admin", "active": True}
        example_secret = "my_super_secret_key_2025"

        example_jwt = jwt.encode(example_payload, example_secret, algorithm="HS256")
        decoded_payload = jwt.decode(example_jwt, example_secret, algorithms=["HS256"])

        assert decoded_payload == example_payload

    def test_decodes_complete_valid_jwt(self, jwt):
        """Newly constructed test"""

        example_payload = {"session_id": "sess_abc123xyz", "device": "mobile"}
        example_secret = "another_secret_!@#"
        example_jwt = jwt.encode(example_payload, example_secret, algorithm="HS256")
        decoded = jwt.decode_complete(example_jwt, example_secret, algorithms=["HS256"])

        assert decoded["header"] == {"alg": "HS256", "typ": "JWT"}
        assert decoded["payload"] == example_payload
        assert isinstance(decoded["signature"], bytes)
        assert len(decoded["signature"]) > 0