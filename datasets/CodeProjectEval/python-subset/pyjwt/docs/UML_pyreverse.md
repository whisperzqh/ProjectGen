## UML Class Diagram

```mermaid
classDiagram
  class Algorithm {
    check_crypto_key_type(key: PublicKeyTypes | PrivateKeyTypes)
    compute_hash_digest(bytestr: bytes) bytes
    from_jwk(jwk: str | JWKDict)* Any
    prepare_key(key: Any)* Any
    sign(msg: bytes, key: Any)* bytes
    to_jwk(key_obj, as_dict: Literal[True])* JWKDict
    verify(msg: bytes, key: Any, sig: bytes)* bool
  }
  class ECAlgorithm {
    SHA256 : ClassVar[type[hashes.HashAlgorithm]]
    SHA384 : ClassVar[type[hashes.HashAlgorithm]]
    SHA512 : ClassVar[type[hashes.HashAlgorithm]]
    hash_alg : type[hashes.HashAlgorithm]
    from_jwk(jwk: str | JWKDict) AllowedECKeys
    prepare_key(key: AllowedECKeys | str | bytes) AllowedECKeys
    sign(msg: bytes, key: EllipticCurvePrivateKey) bytes
    to_jwk(key_obj: AllowedECKeys, as_dict: Literal[True]) JWKDict
    verify(msg: bytes, key: AllowedECKeys, sig: bytes) bool
  }
  class HMACAlgorithm {
    SHA256 : ClassVar[HashlibHash]
    SHA384 : ClassVar[HashlibHash]
    SHA512 : ClassVar[HashlibHash]
    hash_alg : Callable
    from_jwk(jwk: str | JWKDict) bytes
    prepare_key(key: str | bytes) bytes
    sign(msg: bytes, key: bytes) bytes
    to_jwk(key_obj: str | bytes, as_dict: Literal[True]) JWKDict
    verify(msg: bytes, key: bytes, sig: bytes) bool
  }
  class NoneAlgorithm {
    from_jwk(jwk: str | JWKDict)* NoReturn
    prepare_key(key: str | None) None
    sign(msg: bytes, key: None) bytes
    to_jwk(key_obj: Any, as_dict: bool)* NoReturn
    verify(msg: bytes, key: None, sig: bytes) bool
  }
  class OKPAlgorithm {
    from_jwk(jwk: str | JWKDict) AllowedOKPKeys
    prepare_key(key: AllowedOKPKeys | str | bytes) AllowedOKPKeys
    sign(msg: str | bytes, key: Ed25519PrivateKey | Ed448PrivateKey) bytes
    to_jwk(key: AllowedOKPKeys, as_dict: Literal[True]) JWKDict
    verify(msg: str | bytes, key: AllowedOKPKeys, sig: str | bytes) bool
  }
  class RSAAlgorithm {
    SHA256 : ClassVar[type[hashes.HashAlgorithm]]
    SHA384 : ClassVar[type[hashes.HashAlgorithm]]
    SHA512 : ClassVar[type[hashes.HashAlgorithm]]
    hash_alg : type[hashes.HashAlgorithm]
    from_jwk(jwk: str | JWKDict) AllowedRSAKeys
    prepare_key(key: AllowedRSAKeys | str | bytes) AllowedRSAKeys
    sign(msg: bytes, key: RSAPrivateKey) bytes
    to_jwk(key_obj: AllowedRSAKeys, as_dict: Literal[True]) JWKDict
    verify(msg: bytes, key: RSAPublicKey, sig: bytes) bool
  }
  class RSAPSSAlgorithm {
    sign(msg: bytes, key: RSAPrivateKey) bytes
    verify(msg: bytes, key: RSAPublicKey, sig: bytes) bool
  }
  class PyJWK {
    Algorithm
    algorithm_name : str | None
    key
    key_id : str | None
    key_type : str | None
    public_key_use : str | None
    from_dict(obj: JWKDict, algorithm: str | None) PyJWK
    from_json(data: str, algorithm: None) PyJWK
  }
  class PyJWKSet {
    keys : list
    from_dict(obj: dict[str, Any]) PyJWKSet
    from_json(data: str) PyJWKSet
  }
  class PyJWTSetWithTimestamp {
    jwk_set
    timestamp
    get_jwk_set() PyJWKSet
    get_timestamp() float
  }
  class PyJWS {
    header_typ : str
    options
    decode(jwt: str | bytes, key: AllowedPublicKeys | PyJWK | str | bytes, algorithms: Sequence[str] | None, options: SigOptions | None, detached_payload: bytes | None) Any
    decode_complete(jwt: str | bytes, key: AllowedPublicKeys | PyJWK | str | bytes, algorithms: Sequence[str] | None, options: SigOptions | None, detached_payload: bytes | None) dict[str, Any]
    encode(payload: bytes, key: AllowedPrivateKeys | PyJWK | str | bytes, algorithm: str | None, headers: dict[str, Any] | None, json_encoder: type[json.JSONEncoder] | None, is_payload_detached: bool, sort_headers: bool) str
    get_algorithm_by_name(alg_name: str) Algorithm
    get_algorithms() list[str]
    get_unverified_header(jwt: str | bytes) dict[str, Any]
    register_algorithm(alg_id: str, alg_obj: Algorithm) None
    unregister_algorithm(alg_id: str) None
  }
  class PyJWT {
    options : dict
    decode(jwt: str | bytes, key: AllowedPublicKeys | PyJWK | str | bytes, algorithms: Sequence[str] | None, options: Options | None, verify: bool | None, detached_payload: bytes | None, audience: str | Iterable[str] | None, subject: str | None, issuer: str | Container[str] | None, leeway: float | timedelta) dict[str, Any]
    decode_complete(jwt: str | bytes, key: AllowedPublicKeyTypes, algorithms: Sequence[str] | None, options: Options | None, verify: bool | None, detached_payload: bytes | None, audience: str | Iterable[str] | None, issuer: str | Container[str] | None, subject: str | None, leeway: float | timedelta) dict[str, Any]
    encode(payload: dict[str, Any], key: AllowedPrivateKeyTypes, algorithm: str | None, headers: dict[str, Any] | None, json_encoder: type[json.JSONEncoder] | None, sort_headers: bool) str
  }
  class DecodeError {
  }
  class ExpiredSignatureError {
  }
  class ImmatureSignatureError {
  }
  class InvalidAlgorithmError {
  }
  class InvalidAudienceError {
  }
  class InvalidIssuedAtError {
  }
  class InvalidIssuerError {
  }
  class InvalidJTIError {
  }
  class InvalidKeyError {
  }
  class InvalidSignatureError {
  }
  class InvalidSubjectError {
  }
  class InvalidTokenError {
  }
  class MissingCryptographyError {
  }
  class MissingRequiredClaimError {
    claim : str
  }
  class PyJWKClientConnectionError {
  }
  class PyJWKClientError {
  }
  class PyJWKError {
  }
  class PyJWKSetError {
  }
  class PyJWTError {
  }
  class JWKSetCache {
    jwk_set_with_timestamp : NoneType, Optional[PyJWTSetWithTimestamp]
    lifespan : float
    get() Optional[PyJWKSet]
    is_expired() bool
    put(jwk_set: PyJWKSet) None
  }
  class PyJWKClient {
    get_signing_key
    headers : Optional[Dict[str, Any]]
    jwk_set_cache : NoneType, Optional[JWKSetCache]
    ssl_context : Optional[SSLContext]
    timeout : float
    uri : str
    fetch_data() Any
    get_jwk_set(refresh: bool) PyJWKSet
    get_signing_key(kid: str) PyJWK
    get_signing_key_from_jwt(token: str | bytes) PyJWK
    get_signing_keys(refresh: bool) List[PyJWK]
    match_kid(signing_keys: List[PyJWK], kid: str) Optional[PyJWK]
  }
  class FullOptions {
    require : list[str]
    strict_aud : bool
    verify_aud : bool
    verify_exp : bool
    verify_iat : bool
    verify_iss : bool
    verify_jti : bool
    verify_nbf : bool
    verify_signature : bool
    verify_sub : bool
  }
  class Options {
    require : list[str]
    strict_aud : bool
    verify_aud : bool
    verify_exp : bool
    verify_iat : bool
    verify_iss : bool
    verify_jti : bool
    verify_nbf : bool
    verify_signature : bool
    verify_sub : bool
  }
  class SigOptions {
    verify_signature : bool
  }
  class RemovedInPyjwt3Warning {
  }
  ECAlgorithm --|> Algorithm
  HMACAlgorithm --|> Algorithm
  NoneAlgorithm --|> Algorithm
  OKPAlgorithm --|> Algorithm
  RSAAlgorithm --|> Algorithm
  RSAPSSAlgorithm --|> RSAAlgorithm
  DecodeError --|> InvalidTokenError
  ExpiredSignatureError --|> InvalidTokenError
  ImmatureSignatureError --|> InvalidTokenError
  InvalidAlgorithmError --|> InvalidTokenError
  InvalidAudienceError --|> InvalidTokenError
  InvalidIssuedAtError --|> InvalidTokenError
  InvalidIssuerError --|> InvalidTokenError
  InvalidJTIError --|> InvalidTokenError
  InvalidKeyError --|> PyJWTError
  InvalidSignatureError --|> DecodeError
  InvalidSubjectError --|> InvalidTokenError
  InvalidTokenError --|> PyJWTError
  MissingCryptographyError --|> PyJWKError
  MissingRequiredClaimError --|> InvalidTokenError
  PyJWKClientConnectionError --|> PyJWKClientError
  PyJWKClientError --|> PyJWTError
  PyJWKError --|> PyJWTError
  PyJWKSetError --|> PyJWTError
  PyJWTSetWithTimestamp --* JWKSetCache : jwk_set_with_timestamp
  JWKSetCache --* PyJWKClient : jwk_set_cache
  SigOptions --* PyJWS : options
  PyJWKSet --o PyJWTSetWithTimestamp : jwk_set
```

## UML Package Diagram

```mermaid
classDiagram
  class jwt {
  }
  class algorithms {
  }
  class api_jwk {
  }
  class api_jws {
  }
  class api_jwt {
  }
  class exceptions {
  }
  class help {
  }
  class jwk_set_cache {
  }
  class jwks_client {
  }
  class types {
  }
  class utils {
  }
  class warnings {
  }
  jwt --> api_jwk
  jwt --> api_jws
  jwt --> api_jwt
  jwt --> exceptions
  jwt --> jwks_client
  algorithms --> exceptions
  algorithms --> types
  algorithms --> utils
  api_jwk --> algorithms
  api_jwk --> exceptions
  api_jwk --> types
  api_jws --> algorithms
  api_jws --> api_jwk
  api_jws --> exceptions
  api_jws --> utils
  api_jws --> warnings
  api_jws --> warnings
  api_jwt --> algorithms
  api_jwt --> api_jwk
  api_jwt --> exceptions
  api_jwt --> types
  api_jwt --> warnings
  api_jwt --> warnings
  jwk_set_cache --> api_jwk
  jwks_client --> api_jwk
  jwks_client --> api_jwt
  jwks_client --> exceptions
  jwks_client --> jwk_set_cache
  api_jws ..> types
```