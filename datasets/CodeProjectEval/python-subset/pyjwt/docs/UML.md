## UML Class Diagram

```mermaid
classDiagram
    class PyJWT {
        +options: FullOptions
        +encode(payload, key, algorithm, headers) str
        +decode(jwt, key, algorithms, options) dict
        +decode_complete(jwt, key, algorithms, options) dict
        -_validate_claims(payload, options)
        -_encode_payload(payload, headers, json_encoder)
    }
    
    class PyJWS {
        +options: SigOptions
        +encode(payload, key, algorithm, headers) str
        +decode(jwt, key, algorithms, options) bytes
        +decode_complete(jwt, key, algorithms, options) dict
        +get_unverified_header(jwt) dict
        -_verify_signature(signing_input, header, signature, key, algorithms)
        -_load(jwt)
    }
    
    class PyJWKClient {
        +uri: str
        +headers: Dict
        +timeout: int
        +ssl_context: SSLContext
        +jwk_set_cache: JWKSetCache
        +fetch_data() Any
        +get_jwk_set(refresh) PyJWKSet
        +get_signing_keys(refresh) List~PyJWK~
        +get_signing_key(kid) PyJWK
        +get_signing_key_from_jwt(token) PyJWK
        +match_kid(signing_keys, kid) PyJWK
    }
    
    class JWKSetCache {
        +lifespan: int
        +jwk_set_with_timestamp: tuple
        +put(jwk_set)
        +get() dict
        +is_expired() bool
    }
    
    class PyJWKSet {
        +keys: List~PyJWK~
        +from_dict(jwk_set_dict) PyJWKSet
        +from_json(jwk_set_string) PyJWKSet
    }
    
    class PyJWK {
        +key: Any
        +key_id: str
        +key_type: str
        +algorithm_name: str
        +Algorithm: Algorithm
        +public_key_use: str
    }
    
    class Algorithm {
        <<abstract>>
        +prepare_key(key) Any
        +sign(msg, key) bytes
        +verify(msg, key, sig) bool
        +to_jwk(key_obj, as_dict) str|JWKDict
        +from_jwk(jwk) Any
        +compute_hash_digest(bytestr) bytes
    }
    
    class HMACAlgorithm {
        +hash_alg
        +prepare_key(key) bytes
        +sign(msg, key) bytes
        +verify(msg, key, sig) bool
    }
    
    class RSAAlgorithm {
        +hash_alg
        +prepare_key(key) RSAPublicKey|RSAPrivateKey
        +sign(msg, key) bytes
        +verify(msg, key, sig) bool
    }
    
    class ECAlgorithm {
        +hash_alg
        +prepare_key(key) EllipticCurvePublicKey|EllipticCurvePrivateKey
        +sign(msg, key) bytes
        +verify(msg, key, sig) bool
    }
    
    class OKPAlgorithm {
        +prepare_key(key) Ed25519PublicKey|Ed25519PrivateKey
        +sign(msg, key) bytes
        +verify(msg, key, sig) bool
    }
    
    PyJWT --|> PyJWS : inherits
    PyJWKClient --> JWKSetCache : uses
    PyJWKClient --> PyJWKSet : manages
    PyJWKSet --> PyJWK : contains
    PyJWK --> Algorithm : uses
    Algorithm <|-- HMACAlgorithm : implements
    Algorithm <|-- RSAAlgorithm : implements
    Algorithm <|-- ECAlgorithm : implements
    Algorithm <|-- OKPAlgorithm : implements
    PyJWS --> Algorithm : uses
```

## UML Package Diagram

```mermaid
graph TD
    A["jwt (main package)"] --> B["api_jwt (PyJWT class)"]
    A --> C["api_jws (PyJWS class)"]
    A --> D["algorithms (Algorithm implementations)"]
    A --> E["api_jwk (PyJWK, PyJWKSet)"]
    A --> F["jwks_client (PyJWKClient)"]
    A --> G["jwk_set_cache (JWKSetCache)"]
    A --> H["exceptions (Error classes)"]
    A --> I["types (Type definitions)"]
    A --> J["utils (Utility functions)"]
    
    B --> C
    B --> H
    B --> I
    C --> D
    C --> E
    C --> H
    F --> E
    F --> G
    F --> C
    E --> D
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant App as "Application"
    participant JWT as "PyJWT"
    participant Client as "PyJWKClient"
    participant Cache as "JWKSetCache"
    participant Remote as "JWKS Endpoint"
    participant Algo as "Algorithm"
    
    App->>Client: get_signing_key_from_jwt(token)
    Client->>JWT: decode_complete(token, verify_signature=False)
    JWT-->>Client: {"header": {"kid": "..."}, ...}
    
    Client->>Client: get_signing_key(kid)
    Client->>Client: get_signing_keys()
    Client->>Client: get_jwk_set()
    
    alt Cache exists and not expired
        Client->>Cache: get()
        Cache-->>Client: cached JWK set
    else Cache expired or missing
        Client->>Remote: HTTP GET (fetch_data)
        Remote-->>Client: JWK set JSON
        Client->>Cache: put(jwk_set)
    end
    
    Client->>Client: PyJWKSet.from_dict(data)
    Client->>Client: Filter signing keys
    Client->>Client: match_kid(signing_keys, kid)
    
    alt Key found
        Client-->>App: PyJWK
    else Key not found
        Client->>Remote: Refresh JWK set
        Remote-->>Client: Updated JWK set
        Client->>Client: match_kid again
        alt Key found after refresh
            Client-->>App: PyJWK
        else Still not found
            Client-->>App: PyJWKClientError
        end
    end
    
    App->>JWT: decode(token, signing_key.key, algorithms)
    JWT->>Algo: verify(signing_input, key, signature)
    Algo-->>JWT: verification result
    JWT-->>App: decoded payload
```
