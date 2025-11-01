# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── jwt
│   ├── algorithms.py
│   ├── api_jwk.py
│   ├── api_jws.py
│   ├── api_jwt.py
│   ├── exceptions.py
│   ├── help.py
│   ├── __init__.py
│   ├── jwks_client.py
│   ├── jwk_set_cache.py
│   ├── py.typed
│   ├── types.py
│   ├── utils.py
│   └── warnings.py
```

`algorithms.py`:

- `Algorithm(ABC)`:
    - `compute_hash_digest(self, bytestr: bytes) -> bytes`:  
      Compute a hash digest using the specified algorithm's hash algorithm. If there is no hash algorithm, raises a `NotImplementedError`.

    - `check_crypto_key_type(self, key: PublicKeyTypes | PrivateKeyTypes)`:  
      Check that the key belongs to the right cryptographic family. Only works when `cryptography` is installed. Raises `ValueError` if cryptography is not available or if called by a non-cryptography algorithm; raises `InvalidKeyError` if the key type is incorrect.

    - `prepare_key(self, key: Any) -> Any`:  
      Performs necessary validation and conversions on the key and returns the key value in the proper format for `sign()` and `verify()`.

    - `sign(self, msg: bytes, key: Any) -> bytes`:  
      Returns a digital signature for the specified message using the specified key value.

    - `verify(self, msg: bytes, key: Any, sig: bytes) -> bool`:  
      Verifies that the specified digital signature is valid for the specified message and key values.

    - `to_jwk(key_obj, as_dict: bool = False) -> JWKDict | str`:  
      Serializes a given key into a JSON Web Key (JWK). If `as_dict` is `True`, returns a dictionary; otherwise, returns a JSON string.

    - `from_jwk(jwk: str | JWKDict) -> Any`:  
      Deserializes a given key from JWK format back into a key object.

- `NoneAlgorithm(Algorithm)`:
    - `prepare_key(self, key: str | None) -> None`:  
      Validates that the key is `None` when algorithm is `"none"`. Raises `InvalidKeyError` if a non-`None` key is provided.

    - `sign(self, msg: bytes, key: None) -> bytes`:  
      Returns an empty byte string as the signature (no signing is performed).

    - `verify(self, msg: bytes, key: None, sig: bytes) -> bool`:  
      Always returns `False` since verification is not supported for the `"none"` algorithm.

    - `to_jwk(key_obj: Any, as_dict: bool = False) -> NoReturn`:  
      Not implemented; raises `NotImplementedError`.

    - `from_jwk(jwk: str | JWKDict) -> NoReturn`:  
      Not implemented; raises `NotImplementedError`.

- `HMACAlgorithm(Algorithm)`:
    - `prepare_key(self, key: str | bytes) -> bytes`:  
      Converts the key to bytes and ensures it is not a PEM or SSH-formatted asymmetric key or certificate, which are invalid for HMAC.

    - `to_jwk(key_obj: str | bytes, as_dict: bool = False) -> JWKDict | str`:  
      Serializes an HMAC key into a JWK with key type `"oct"`.

    - `from_jwk(jwk: str | JWKDict) -> bytes`:  
      Deserializes a JWK of type `"oct"` back into raw bytes for use as an HMAC key.

    - `sign(self, msg: bytes, key: bytes) -> bytes`:  
      Computes an HMAC signature of the message using the provided key and the algorithm’s hash function.

    - `verify(self, msg: bytes, key: bytes, sig: bytes) -> bool`:  
      Verifies the HMAC signature using a constant-time comparison to prevent timing attacks.

- `RSAAlgorithm(Algorithm)` (requires `cryptography`):
    - `prepare_key(self, key: AllowedRSAKeys | str | bytes) -> AllowedRSAKeys`:  
      Loads and validates an RSA key from PEM or SSH public key format, or accepts an already-loaded `cryptography` key object.

    - `to_jwk(key_obj: AllowedRSAKeys, as_dict: bool = False) -> JWKDict | str`:  
      Serializes an RSA public or private key into a JWK representation.

    - `from_jwk(jwk: str | JWKDict) -> AllowedRSAKeys`:  
      Deserializes an RSA JWK into a `cryptography` RSA public or private key object.

    - `sign(self, msg: bytes, key: RSAPrivateKey) -> bytes`:  
      Signs a message using RSASSA-PKCS1-v1_5 with the specified hash algorithm.

    - `verify(self, msg: bytes, key: RSAPublicKey, sig: bytes) -> bool`:  
      Verifies an RSASSA-PKCS1-v1_5 signature using the public key and hash algorithm.

- `ECAlgorithm(Algorithm)` (requires `cryptography`):
    - `prepare_key(self, key: AllowedECKeys | str | bytes) -> AllowedECKeys`:  
      Loads and validates an Elliptic Curve key from PEM format or accepts an already-loaded `cryptography` key object.

    - `sign(self, msg: bytes, key: EllipticCurvePrivateKey) -> bytes`:  
      Signs a message using ECDSA and converts the DER-encoded signature to raw (IEEE P1363) format.

    - `verify(self, msg: bytes, key: AllowedECKeys, sig: bytes) -> bool`:  
      Converts the raw signature to DER format and verifies it using ECDSA.

    - `to_jwk(key_obj: AllowedECKeys, as_dict: bool = False) -> JWKDict | str`:  
      Serializes an EC public or private key into a JWK, including curve identifier and coordinates.

    - `from_jwk(jwk: str | JWKDict) -> AllowedECKeys`:  
      Deserializes an EC JWK into a `cryptography` EC public or private key object, validating curve and coordinate lengths.

- `RSAPSSAlgorithm(RSAAlgorithm)` (requires `cryptography`):
    - `sign(self, msg: bytes, key: RSAPrivateKey) -> bytes`:  
      Signs a message using RSASSA-PSS with MGF1 and a salt length equal to the hash digest size.

    - `verify(self, msg: bytes, key: RSAPublicKey, sig: bytes) -> bool`:  
      Verifies an RSASSA-PSS signature using MGF1 and the same salt length as the hash digest size.

- `OKPAlgorithm(Algorithm)` (requires `cryptography`):
    - `prepare_key(self, key: AllowedOKPKeys | str | bytes) -> AllowedOKPKeys`:  
      Loads and validates an EdDSA key (Ed25519 or Ed448) from PEM or SSH public key format.

    - `sign(self, msg: str | bytes, key: Ed25519PrivateKey | Ed448PrivateKey) -> bytes`:  
      Signs a message using EdDSA (Ed25519 or Ed448).

    - `verify(self, msg: str | bytes, key: AllowedOKPKeys, sig: str | bytes) -> bool`:  
      Verifies an EdDSA signature using the corresponding public key.

    - `to_jwk(key: AllowedOKPKeys, as_dict: bool = False) -> JWKDict | str`:  
      Serializes an OKP (Octet Key Pair) public or private key into a JWK with `"kty": "OKP"` and appropriate curve.

    - `from_jwk(jwk: str | JWKDict) -> AllowedOKPKeys`:  
      Deserializes an OKP JWK into a `cryptography` Ed25519 or Ed448 key object.

- `get_default_algorithms() -> dict[str, Algorithm]`:  
  Returns a dictionary mapping algorithm names (e.g., `"HS256"`, `"RS256"`) to their corresponding `Algorithm` instances. Includes all supported algorithms based on whether `cryptography` is installed.

- `requires_cryptography`:  
  A set containing the names of algorithms that require the `cryptography` library (e.g., RSA, EC, EdDSA, and RSASSA-PSS variants).

`api_jwk.py`:

- `PyJWK`:
    - `__init__(self, jwk_data: JWKDict, algorithm: str | None = None)`:  
      A class that represents a JSON Web Key (JWK) as defined in RFC 7517. Initializes the key by determining the appropriate algorithm based on the JWK’s `kty`, `crv`, and optionally `alg` fields. Validates key type and curve support, ensures required dependencies (e.g., `cryptography`) are available, and deserializes the JWK into a usable key object.

    - `from_dict(obj: JWKDict, algorithm: str | None = None) -> PyJWK`:  
      Creates a `PyJWK` object from a JSON-like dictionary. Implicitly calls the constructor with the provided dictionary and optional algorithm.

    - `from_json(data: str, algorithm: str | None = None) -> PyJWK`:  
      Creates a `PyJWK` object from a JSON string by first parsing it into a dictionary and then calling `from_dict()`.

    - `key_type(self) -> str | None`:  
      Returns the `"kty"` (key type) parameter from the JWK (e.g., `"RSA"`, `"EC"`, `"oct"`, `"OKP"`).

    - `key_id(self) -> str | None`:  
      Returns the `"kid"` (key ID) parameter from the JWK, used to identify the key within a set.

    - `public_key_use(self) -> str | None`:  
      Returns the `"use"` (public key use) parameter from the JWK, indicating intended use such as `"sig"` (signature) or `"enc"` (encryption).

- `PyJWKSet`:
    - `__init__(self, keys: list[JWKDict])`:  
      Represents a JSON Web Key Set (JWKS) as defined in RFC 7517. Initializes a list of `PyJWK` objects from the provided list of JWK dictionaries. Skips keys that cannot be loaded (e.g., due to unsupported algorithms) unless the failure is due to a missing `cryptography` dependency, which is re-raised. Raises an error if no usable keys remain.

    - `from_dict(obj: dict[str, Any]) -> PyJWKSet`:  
      Constructs a `PyJWKSet` from a dictionary expected to contain a `"keys"` array of JWKs.

    - `from_json(data: str) -> PyJWKSet`:  
      Constructs a `PyJWKSet` by parsing a JSON string and delegating to `from_dict()`.

    - `__getitem__(self, kid: str) -> PyJWK`:  
      Retrieves a `PyJWK` from the set by matching the given key ID (`kid`). Raises `KeyError` if no key with that `kid` exists.

    - `__iter__(self) -> Iterator[PyJWK]`:  
      Returns an iterator over all usable `PyJWK` objects in the set.

- `PyJWTSetWithTimestamp`:
    - `__init__(self, jwk_set: PyJWKSet)`:  
      Wraps a `PyJWKSet` along with a timestamp (using `time.monotonic()`) to track when the set was created or last refreshed.

    - `get_jwk_set(self) -> PyJWKSet`:  
      Returns the wrapped `PyJWKSet`.

    - `get_timestamp(self) -> float`:  
      Returns the monotonic timestamp associated with the creation of this object.

`api_jws.py`:

- `PyJWS`:
    - `__init__(self, algorithms: Sequence[str] | None = None, options: SigOptions | None = None)`:  
      Initializes a `PyJWS` instance with a set of allowed signing algorithms and verification options. If `algorithms` is not provided, all default algorithms are allowed. The `options` dictionary controls behavior such as signature verification.

    - `_get_default_options() -> SigOptions`:  
      Returns the default signature verification options, currently `{"verify_signature": True}`.

    - `register_algorithm(self, alg_id: str, alg_obj: Algorithm)`:  
      Registers a new algorithm for use when creating and verifying tokens. Raises `ValueError` if an algorithm with the same ID is already registered, or `TypeError` if `alg_obj` is not an instance of `Algorithm`.

    - `unregister_algorithm(self, alg_id: str)`:  
      Unregisters an algorithm by its ID. Raises `KeyError` if the algorithm is not currently registered.

    - `get_algorithms(self) -> list[str]`:  
      Returns a list of algorithm names currently allowed for use.

    - `get_algorithm_by_name(self, alg_name: str) -> Algorithm`:  
      Retrieves the `Algorithm` object corresponding to the given algorithm name. Raises `NotImplementedError` if the algorithm is unsupported or requires `cryptography` but it is not installed.

    - `encode(self, payload: bytes, key: AllowedPrivateKeys | PyJWK | str | bytes, algorithm: str | None = "HS256", headers: dict[str, Any] | None = None, json_encoder: type[json.JSONEncoder] | None = None, is_payload_detached: bool = False, sort_headers: bool = True) -> str`:  
      Encodes a JWS token from the given payload and signing key. Supports detached payloads (when `b64: false` per RFC 7797) and custom headers. The resulting token is a compact JWS string.

    - `decode_complete(self, jwt: str | bytes, key: AllowedPublicKeys | PyJWK | str | bytes = "", algorithms: Sequence[str] | None = None, options: SigOptions | None = None, detached_payload: bytes | None = None, **kwargs) -> dict[str, Any]`:  
      Decodes and verifies a JWS token, returning a dictionary containing the `payload`, `header`, and `signature`. If `b64` is `false` in the header, a `detached_payload` must be provided. Signature verification is controlled by the `verify_signature` option.

    - `decode(self, jwt: str | bytes, key: AllowedPublicKeys | PyJWK | str | bytes = "", algorithms: Sequence[str] | None = None, options: SigOptions | None = None, detached_payload: bytes | None = None, **kwargs) -> Any`:  
      Decodes a JWS token and returns only the payload. Internally calls `decode_complete()` and extracts the payload. Signature verification is performed unless disabled via options.

    - `get_unverified_header(self, jwt: str | bytes) -> dict[str, Any]`:  
      Returns the header of a JWS token without verifying the signature. **Note**: The header should not be trusted until the signature is verified.

    - `_load(self, jwt: str | bytes) -> tuple[bytes, bytes, dict[str, Any], bytes]`:  
      Parses a JWS token into its components: payload (possibly empty if detached), signing input, header (as a dict), and raw signature bytes. Validates structure and base64url encoding.

    - `_verify_signature(self, signing_input: bytes, header: dict[str, Any], signature: bytes, key: AllowedPublicKeys | PyJWK | str | bytes = "", algorithms: Sequence[str] | None = None)`:  
      Verifies the JWS signature using the specified key and allowed algorithms. Ensures the `alg` header is present and permitted, prepares the key, and delegates to the algorithm’s `verify()` method. Raises `InvalidSignatureError` on failure.

    - `_validate_headers(self, headers: dict[str, Any])`:  
      Validates known JWS header parameters. Currently validates the `kid` (Key ID) parameter.

    - `_validate_kid(self, kid: Any)`:  
      Ensures the `kid` header parameter is a string. Raises `InvalidTokenError` if not.

- `encode(payload: bytes, key: ..., algorithm: str | None = "HS256", headers: dict | None = None, json_encoder: type[json.JSONEncoder] | None = None, is_payload_detached: bool = False, sort_headers: bool = True) -> str`:  
  Global convenience function that delegates to the default `PyJWS` instance’s `encode()` method to create a JWS token.

- `decode_complete(jwt: str | bytes, key: ..., algorithms: Sequence[str] | None = None, options: SigOptions | None = None, detached_payload: bytes | None = None, **kwargs) -> dict[str, Any]`:  
  Global convenience function that delegates to the default `PyJWS` instance’s `decode_complete()` method to fully decode and verify a JWS token.

- `decode(jwt: str | bytes, key: ..., algorithms: Sequence[str] | None = None, options: SigOptions | None = None, detached_payload: bytes | None = None, **kwargs) -> Any`:  
  Global convenience function that delegates to the default `PyJWS` instance’s `decode()` method to return only the payload of a verified JWS token.

- `register_algorithm(alg_id: str, alg_obj: Algorithm)`:  
  Global convenience function to register a new algorithm with the default `PyJWS` instance.

- `unregister_algorithm(alg_id: str)`:  
  Global convenience function to unregister an algorithm from the default `PyJWS` instance.

- `get_algorithm_by_name(alg_name: str) -> Algorithm`:  
  Global convenience function to retrieve an algorithm by name from the default `PyJWS` instance.

- `get_unverified_header(jwt: str | bytes) -> dict[str, Any]`:  
  Global convenience function to extract the unverified header from a JWS token using the default `PyJWS` instance.

`api_jwt.py`:

- `PyJWT`:
    - `__init__(self, options: Options | None = None)`: Initializes a PyJWT instance with optional validation options.

    - `_get_default_options()`: Returns the default validation options used by the decoder.

    - `_merge_options(self, options: Options | None = None)`: Merges provided options with defaults, applying logic such as disabling claim validation when signature verification is off.

    - `encode(self, payload: dict[str, Any], key: AllowedPrivateKeyTypes, algorithm: str | None = "HS256", headers: dict[str, Any] | None = None, json_encoder: type[json.JSONEncoder] | None = None, sort_headers: bool = True)`: Encode the `payload` as a JSON Web Token. Raises `TypeError` if `payload` is not a dictionary.

    - `_encode_payload(self, payload: dict[str, Any], headers: dict[str, Any] | None = None, json_encoder: type[json.JSONEncoder] | None = None)`: Encodes the payload into UTF-8 JSON bytes. Intended to be overridden for custom payload encoding (e.g., compression).

    - `decode_complete(self, jwt: str | bytes, key: AllowedPublicKeyTypes = "", algorithms: Sequence[str] | None = None, options: Options | None = None, verify: bool | None = None, detached_payload: bytes | None = None, audience: str | Iterable[str] | None = None, issuer: str | Container[str] | None = None, subject: str | None = None, leeway: float | timedelta = 0, **kwargs: Any)`: Decodes a JWT and returns a dictionary containing the header, payload, and signature. Validates claims according to provided options and parameters.

    - `_decode_payload(self, decoded: dict[str, Any])`: Parses the payload from a JWS structure as a JSON object. Intended to be overridden for custom payload decoding (e.g., decompression).

    - `decode(self, jwt: str | bytes, key: AllowedPublicKeyTypes = "", algorithms: Sequence[str] | None = None, options: Options | None = None, verify: bool | None = None, detached_payload: bytes | None = None, audience: str | Iterable[str] | None = None, subject: str | None = None, issuer: str | Container[str] | None = None, leeway: float | timedelta = 0, **kwargs: Any)`: Verifies the JWT signature and returns only the claims (payload).

    - `_validate_claims(self, payload: dict[str, Any], options: FullOptions, audience: Iterable[str] | str | None = None, issuer: Container[str] | str | None = None, subject: str | None = None, leeway: float | timedelta = 0)`: Validates standard JWT claims (`exp`, `nbf`, `iat`, `iss`, `aud`, `sub`, `jti`) according to the merged options and provided parameters.

    - `_validate_required_claims(self, payload: dict[str, Any], claims: Iterable[str])`: Ensures that all claims listed in `claims` are present in the payload.

    - `_validate_sub(self, payload: dict[str, Any], subject: str | None = None)`: Validates the "sub" (subject) claim if present, ensuring it is a string and matches the expected value if provided.

    - `_validate_jti(self, payload: dict[str, Any])`: Validates the "jti" (JWT ID) claim if present, ensuring it is a string.

    - `_validate_iat(self, payload: dict[str, Any], now: float, leeway: float)`: Validates the "iat" (issued at) claim, ensuring it is an integer and not in the future beyond the allowed leeway.

    - `_validate_nbf(self, payload: dict[str, Any], now: float, leeway: float)`: Validates the "nbf" (not before) claim, ensuring it is an integer and not in the future beyond the allowed leeway.

    - `_validate_exp(self, payload: dict[str, Any], now: float, leeway: float)`: Validates the "exp" (expiration time) claim, ensuring it is an integer and not in the past beyond the allowed leeway.

    - `_validate_aud(self, payload: dict[str, Any], audience: str | Iterable[str] | None, *, strict: bool = False)`: Validates the "aud" (audience) claim, supporting both strict (exact string match) and relaxed (list inclusion) modes.

    - `_validate_iss(self, payload: dict[str, Any], issuer: Container[str] | str | None)`: Validates the "iss" (issuer) claim, ensuring it is a string and matches the expected issuer(s) if provided.

- `encode(payload: dict[str, Any], key: AllowedPrivateKeyTypes, algorithm: str | None = "HS256", headers: dict[str, Any] | None = None, json_encoder: type[json.JSONEncoder] | None = None, sort_headers: bool = True)`: Convenience wrapper around `PyJWT.encode()` using a global instance.

- `decode_complete(jwt: str | bytes, key: AllowedPublicKeyTypes = "", algorithms: Sequence[str] | None = None, options: Options | None = None, verify: bool | None = None, detached_payload: bytes | None = None, audience: str | Iterable[str] | None = None, issuer: str | Container[str] | None = None, subject: str | None = None, leeway: float | timedelta = 0, **kwargs: Any)`: Convenience wrapper around `PyJWT.decode_complete()` using a global instance.

- `decode(jwt: str | bytes, key: AllowedPublicKeyTypes = "", algorithms: Sequence[str] | None = None, options: Options | None = None, verify: bool | None = None, detached_payload: bytes | None = None, audience: str | Iterable[str] | None = None, subject: str | None = None, issuer: str | Container[str] | None = None, leeway: float | timedelta = 0, **kwargs: Any)`: Convenience wrapper around `PyJWT.decode()` using a global instance.

`exceptions.py`:

- `PyJWTError(Exception)`: Base class for all exceptions raised by PyJWT.

- `InvalidTokenError(PyJWTError)`: Base exception raised when `decode()` fails on a token.

- `DecodeError(InvalidTokenError)`: Raised when a token cannot be decoded because it failed validation.

- `InvalidSignatureError(DecodeError)`: Raised when a token's signature doesn't match the one provided as part of the token.

- `ExpiredSignatureError(InvalidTokenError)`: Raised when a token's `exp` claim indicates that it has expired.

- `InvalidAudienceError(InvalidTokenError)`: Raised when a token's `aud` claim does not match one of the expected audience values.

- `InvalidIssuerError(InvalidTokenError)`: Raised when a token's `iss` claim does not match the expected issuer.

- `InvalidIssuedAtError(InvalidTokenError)`: Raised when a token's `iat` claim is non-numeric.

- `ImmatureSignatureError(InvalidTokenError)`: Raised when a token's `nbf` or `iat` claims represent a time in the future.

- `InvalidKeyError(PyJWTError)`: Raised when the specified key is not in the proper format.

- `InvalidAlgorithmError(InvalidTokenError)`: Raised when the specified algorithm is not recognized by PyJWT.

- `MissingRequiredClaimError(InvalidTokenError)`: Raised when a claim that is required to be present is not contained in the claimset.

    - `__init__(self, claim: str)`: Initializes the exception with the name of the missing claim.

    - `__str__(self)`: Returns a human-readable message indicating which claim is missing.

- `PyJWKError(PyJWTError)`: Base class for exceptions related to JSON Web Keys (JWK).

- `MissingCryptographyError(PyJWKError)`: Raised if the algorithm requires the `cryptography` library to be installed and it is not available.

- `PyJWKSetError(PyJWTError)`: Base class for exceptions related to JSON Web Key Sets (JWKS).

- `PyJWKClientError(PyJWTError)`: Base class for exceptions related to the PyJWK client.

- `PyJWKClientConnectionError(PyJWKClientError)`: Raised when there is a connection error while fetching a JWKS from a remote endpoint.

- `InvalidSubjectError(InvalidTokenError)`: Raised when a token's `sub` claim is not a string or doesn't match the expected `subject`.

- `InvalidJTIError(InvalidTokenError)`: Raised when a token's `jti` claim is not a string.

`help.py`:

- `info() -> Dict[str, Dict[str, str]]`:  
  Generate information for a bug report. Based on the requests package help utility module. Returns a dictionary containing details about the platform, Python implementation, cryptography library version (if available), and PyJWT version.

- `main() -> None`:  
  Pretty-print the bug information as JSON. This function calls `info()` and outputs the result to stdout using `json.dumps()` with sorted keys and indentation for readability.

`__init__.py`:

`jwks_client.py`:

- `PyJWKClient`:
    - `__init__(self, uri: str, cache_keys: bool = False, max_cached_keys: int = 16, cache_jwk_set: bool = True, lifespan: float = 300, headers: Optional[Dict[str, Any]] = None, timeout: float = 30, ssl_context: Optional[SSLContext] = None)`: Initializes a PyJWKClient instance with a JWKS URI and optional caching, network, and SSL settings. If `cache_jwk_set` is enabled, a `JWKSetCache` is created with the specified `lifespan`. If `cache_keys` is enabled, the `get_signing_key` method is wrapped with `functools.lru_cache`.

    - `fetch_data(self) -> Any`: Fetches the JWKS data from the configured URI using `urllib.request.urlopen`, applying custom headers, timeout, and SSL context. On success, returns the parsed JSON response. On network errors (`URLError`, `TimeoutError`), raises `PyJWKClientConnectionError`. Regardless of success or failure, attempts to store the fetched (or failed) data in the JWK set cache if caching is enabled.

    - `get_jwk_set(self, refresh: bool = False) -> PyJWKSet`: Retrieves a `PyJWKSet` instance. If caching is enabled and `refresh` is `False`, attempts to return a cached version. Otherwise, fetches fresh data via `fetch_data()`. Validates that the returned data is a dictionary before constructing the `PyJWKSet`.

    - `get_signing_keys(self, refresh: bool = False) -> List[PyJWK]`: Returns a list of signing keys from the JWKS where `public_key_use` is `"sig"` (or `None`) and a `key_id` is present. If no such keys exist, raises `PyJWKClientError`. Optionally forces a refresh of the JWKS if `refresh=True`.

    - `get_signing_key(self, kid: str) -> PyJWK`: Retrieves the signing key matching the given key ID (`kid`). First attempts with the current JWKS; if no match is found, retries after refreshing the JWKS. Raises `PyJWKClientError` if no matching key is found after refresh.

    - `get_signing_key_from_jwt(self, token: str | bytes) -> PyJWK`: Extracts the `kid` from the header of an unverified JWT (using `decode_complete` with signature verification disabled) and delegates to `get_signing_key` to retrieve the corresponding signing key.

    - `match_kid(signing_keys: List[PyJWK], kid: str) -> Optional[PyJWK]`: Static helper method that searches a list of `PyJWK` objects for one whose `key_id` matches the provided `kid`. Returns the first match or `None` if no match is found.

`jwk_set_cache.py`:

- `JWKSetCache`:
    - `__init__(self, lifespan: float) -> None`: Initializes a cache for a `PyJWKSet` with a specified `lifespan` in seconds. The cached entry includes a timestamp to support expiration logic.

    - `put(self, jwk_set: PyJWKSet) -> None`: Stores the given `PyJWKSet` in the cache wrapped in a `PyJWTSetWithTimestamp`. If `jwk_set` is `None`, clears the cache by setting the internal reference to `None`.

    - `get(self) -> Optional[PyJWKSet]`: Retrieves the cached `PyJWKSet` if it exists and has not expired. Returns `None` if the cache is empty or the entry has expired.

    - `is_expired(self) -> bool`: Determines whether the currently cached `PyJWKSet` has expired by comparing the current monotonic time with the stored timestamp plus the configured `lifespan`. Returns `True` if expired or if no entry is cached; otherwise `False`.

`types.py`:

- `SigOptions(TypedDict)`: A `TypedDict` specifying options used by the `PyJWS` class for signature handling. It is a minimal subset of the full decoding options.

- `Options(TypedDict, total=False)`: A `TypedDict` specifying decoding options for the `jwt.decode()` and `jwt.api_jwt.decode_complete()` functions. All keys are optional (`total=False`).

- `FullOptions(TypedDict)`: `TypedDict` identical in structure to `Options`, but with all keys required (`total=True` by default). Used internally where a complete set of option values is guaranteed to be present.

`utils.py`:

- `force_bytes(value: Union[bytes, str]) -> bytes`: Converts a string to UTF-8 encoded bytes; returns bytes as-is. Raises `TypeError` if the input is neither a string nor bytes.

- `base64url_decode(input: Union[bytes, str]) -> bytes`: Decodes a Base64URL-encoded string or bytes into raw bytes, automatically padding the input if necessary to satisfy Base64 length requirements.

- `base64url_encode(input: bytes) -> bytes`: Encodes raw bytes into a Base64URL-encoded byte string with padding characters (`=`) removed.

- `to_base64url_uint(val: int, *, bit_length: Optional[int] = None) -> bytes`: Encodes a positive integer as a big-endian byte string with optional fixed bit length, then Base64URL-encodes the result. Raises `ValueError` if the input is negative.

- `from_base64url_uint(val: Union[bytes, str]) -> int`: Decodes a Base64URL-encoded string or bytes into a positive integer by interpreting the decoded bytes as a big-endian unsigned integer.

- `number_to_bytes(num: int, num_bytes: int) -> bytes`: Converts an integer to a fixed-length big-endian byte string of exactly `num_bytes` length, zero-padded if necessary.

- `bytes_to_number(string: bytes) -> int`: Converts a byte string into an integer by interpreting it as a hexadecimal number.

- `bytes_from_int(val: int, *, bit_length: Optional[int] = None) -> bytes`: Converts a non-negative integer to its minimal big-endian byte representation. If `bit_length` is provided, the output is padded to that bit length.

- `der_to_raw_signature(der_sig: bytes, curve: "EllipticCurve") -> bytes`: Converts a DER-encoded ECDSA signature into a raw concatenated (r, s) signature format, each component padded to the key size of the given elliptic curve.

- `raw_to_der_signature(raw_sig: bytes, curve: "EllipticCurve") -> bytes`: Converts a raw concatenated (r, s) ECDSA signature into DER-encoded format, using the key size of the given elliptic curve to validate input length.

- `is_pem_format(key: bytes) -> bool`: Determines whether the given byte string matches the PEM format for any of the supported PEM object types (e.g., certificates, private keys). Uses a regular expression derived from the `pem` library.

- `is_ssh_key(key: bytes) -> bool`: Checks whether the given byte string starts with a known SSH public key format identifier (e.g., `ssh-rsa`, `ecdsa-sha2-nistp256`). Based on logic from the `cryptography` library.

`warnings.py`:

- `RemovedInPyjwt3Warning(DeprecationWarning)`: A custom deprecation warning class indicating features that will be removed in PyJWT version 3.0. Inherits from Python’s built-in `DeprecationWarning`.