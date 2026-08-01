import base64
from typing import cast

import pytest

from jwt.algorithms import HMACAlgorithm, has_crypto

from .utils import crypto_required, key_path

if has_crypto:
    from cryptography.hazmat.primitives.asymmetric.ec import (
        EllipticCurvePrivateKey,
        EllipticCurvePublicKey,
    )
    from cryptography.hazmat.primitives.asymmetric.ed448 import (
        Ed448PrivateKey,
        Ed448PublicKey,
    )
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives.asymmetric.rsa import (
        RSAPrivateKey,
        RSAPublicKey,
    )

    from jwt.algorithms import OKPAlgorithm, RSAAlgorithm


class TestAlgorithms:
    """Original test"""

    def test_hmac_jwk_should_parse_and_verify(self):
        """Original test"""

        algo = HMACAlgorithm(HMACAlgorithm.SHA256)

        with open(key_path("jwk_hmac.json")) as keyfile:
            key = algo.from_jwk(keyfile.read())

        signature = algo.sign(b"Hello World!", key)
        assert algo.verify(b"Hello World!", key, signature)

    @crypto_required
    def test_rsa_jwk_public_and_private_keys_should_parse_and_verify(self):
        """Original test"""

        algo = RSAAlgorithm(RSAAlgorithm.SHA256)

        with open(key_path("jwk_rsa_pub.json")) as keyfile:
            pub_key = cast(RSAPublicKey, algo.from_jwk(keyfile.read()))

        with open(key_path("jwk_rsa_key.json")) as keyfile:
            priv_key = cast(RSAPrivateKey, algo.from_jwk(keyfile.read()))

        signature = algo.sign(b"Hello World!", priv_key)
        assert algo.verify(b"Hello World!", pub_key, signature)

    @crypto_required
    def test_rsa_private_key_to_jwk_works_with_from_jwk(self):
        """Original test"""

        algo = RSAAlgorithm(RSAAlgorithm.SHA256)

        with open(key_path("testkey_rsa.priv")) as rsa_key:
            orig_key = cast(RSAPrivateKey, algo.prepare_key(rsa_key.read()))

        parsed_key = cast(RSAPrivateKey, algo.from_jwk(algo.to_jwk(orig_key)))
        assert parsed_key.private_numbers() == orig_key.private_numbers()
        assert (
            parsed_key.private_numbers().public_numbers
            == orig_key.private_numbers().public_numbers
        )


@crypto_required
class TestOKPAlgorithms:
    """Original test"""

    hello_world_sig = b"Qxa47mk/azzUgmY2StAOguAd4P7YBLpyCfU3JdbaiWnXM4o4WibXwmIHvNYgN3frtE2fcyd8OYEaOiD/KiwkCg=="
    hello_world_sig_pem = b"9ueQE7PT8uudHIQb2zZZ7tB7k1X3jeTnIfOVvGCINZejrqQbru1EXPeuMlGcQEZrGkLVcfMmr99W/+byxfppAg=="
    hello_world = b"Hello World!"

    @pytest.mark.parametrize(
        "private_key_file,public_key_file,sig_attr",
        [
            ("testkey_ed25519", "testkey_ed25519.pub", "hello_world_sig"),
            ("testkey_ed25519.pem", "testkey_ed25519.pub.pem", "hello_world_sig_pem"),
        ],
    )
    def test_okp_ed25519_sign_should_generate_correct_signature_value(
        self, private_key_file, public_key_file, sig_attr
    ):
        """Original test"""

        algo = OKPAlgorithm()

        jwt_message = self.hello_world

        expected_sig = base64.b64decode(getattr(self, sig_attr))

        with open(key_path(private_key_file)) as keyfile:
            jwt_key = cast(Ed25519PrivateKey, algo.prepare_key(keyfile.read()))

        with open(key_path(public_key_file)) as keyfile:
            jwt_pub_key = cast(Ed25519PublicKey, algo.prepare_key(keyfile.read()))

        algo.sign(jwt_message, jwt_key)
        result = algo.verify(jwt_message, jwt_pub_key, expected_sig)
        assert result
