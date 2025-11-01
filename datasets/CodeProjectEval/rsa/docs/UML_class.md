## UML Class Diagram

```mermaid
classDiagram
    class AbstractKey {
        <<abstract>>
        +int n
        +int e
        +int blindfac
        +int blindfac_inverse
        +Lock mutex
        +__init__(n, e)
        +blind(message) Tuple~int, int~
        +unblind(blinded, blindfac_inverse) int
        +load_pkcs1(keyfile, format)* T
        +save_pkcs1(format) bytes
        +_load_pkcs1_pem(keyfile)* T
        +_load_pkcs1_der(keyfile)* T
        +_save_pkcs1_pem()* bytes
        +_save_pkcs1_der()* bytes
    }

    class PublicKey {
        +__init__(n, e)
        +__getitem__(key) int
        +__repr__() str
        +__eq__(other) bool
        +__hash__() int
        +_load_pkcs1_der(keyfile) PublicKey
        +_load_pkcs1_pem(keyfile) PublicKey
        +_save_pkcs1_der() bytes
        +_save_pkcs1_pem() bytes
        +load_pkcs1_openssl_pem(keyfile) PublicKey
        +load_pkcs1_openssl_der(keyfile) PublicKey
    }

    class PrivateKey {
        +int d
        +int p
        +int q
        +int exp1
        +int exp2
        +int coef
        +List~int~ rs
        +List~int~ ds
        +List~int~ ts
        +__init__(n, e, d, p, q, rs)
        +__getitem__(key) int
        +__repr__() str
        +__eq__(other) bool
        +__hash__() int
        +blinded_decrypt(encrypted) int
        +_load_pkcs1_der(keyfile) PrivateKey
        +_load_pkcs1_pem(keyfile) PrivateKey
        +_save_pkcs1_der() bytes
        +_save_pkcs1_pem() bytes
    }

    class CryptoError {
        <<exception>>
    }

    class DecryptionError {
        <<exception>>
    }

    class VerificationError {
        <<exception>>
    }

    class NotRelativePrimeError {
        <<exception>>
        +int a
        +int b
        +int d
        +__init__(a, b, d, msg)
    }

    class AsnPubKey {
        <<pyasn1>>
        +componentType
    }

    class OpenSSLPubKey {
        <<pyasn1>>
        +componentType
    }

    class PubKeyHeader {
        <<pyasn1>>
        +componentType
    }

    AbstractKey <|-- PublicKey
    AbstractKey <|-- PrivateKey
    CryptoError <|-- DecryptionError
    CryptoError <|-- VerificationError
    ValueError <|-- NotRelativePrimeError
    OpenSSLPubKey *-- PubKeyHeader
```  

## UML Package Diagram

```mermaid
graph TD
    rsa["rsa (main package)"]
    key["rsa.key"]
    pkcs1["rsa.pkcs1"]
    core["rsa.core"]
    common["rsa.common"]
    transform["rsa.transform"]
    prime["rsa.prime"]
    randnum["rsa.randnum"]
    pem["rsa.pem"]
    asn1["rsa.asn1"]
    cli["rsa.cli"]
    parallel["rsa.parallel"]
    pkcs1_v2["rsa.pkcs1_v2"]
    util["rsa.util"]

    rsa --> key
    rsa --> pkcs1
    
    key --> prime
    key --> pem
    key --> common
    key --> randnum
    key --> core
    key --> asn1
    
    pkcs1 --> common
    pkcs1 --> transform
    pkcs1 --> core
    pkcs1 --> key
    
    prime --> common
    prime --> randnum
    
    randnum --> common
    randnum --> transform
    
    cli --> key
    cli --> pkcs1
    
    parallel --> prime
    
    pem -.-> base64
    asn1 -.-> pyasn1
    
    style rsa fill:#e1f5ff
    style key fill:#fff3e0
    style pkcs1 fill:#fff3e0
    style core fill:#f3e5f5
    style common fill:#f3e5f5
    style transform fill:#f3e5f5
```  
