import json

import pytest

from jwt.algorithms import has_crypto
from jwt.api_jwk import PyJWK

from .utils import crypto_required, key_path

if has_crypto:
    from jwt.algorithms import RSAAlgorithm


class TestPyJWK:
    """Original test"""
    
    @crypto_required
    def test_should_load_key_from_jwk_data_dict(self):
        """Original test"""

        algo = RSAAlgorithm(RSAAlgorithm.SHA256)

        with open(key_path("jwk_rsa_pub.json")) as keyfile:
            pub_key = algo.from_jwk(keyfile.read())

        key_data_str = algo.to_jwk(pub_key)
        key_data = json.loads(key_data_str)

        key_data["alg"] = "RS256"
        key_data["use"] = "sig"
        key_data["kid"] = "keyid-abc123"

        jwk = PyJWK.from_dict(key_data)

        assert jwk.key_type == "RSA"
        assert jwk.key_id == "keyid-abc123"
        assert jwk.public_key_use == "sig"

    @crypto_required
    def test_should_load_key_without_alg_from_dict(self):
        """Original test"""

        with open(key_path("jwk_rsa_pub.json")) as keyfile:
            key_data = json.loads(keyfile.read())

        jwk = PyJWK.from_dict(key_data)

        assert jwk.key_type == "RSA"
        assert isinstance(jwk.Algorithm, RSAAlgorithm)
        assert jwk.Algorithm.hash_alg == RSAAlgorithm.SHA256
        assert jwk.algorithm_name == "RS256"

    