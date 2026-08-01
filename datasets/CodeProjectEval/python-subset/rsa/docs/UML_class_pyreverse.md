## UML Class Diagram

```mermaid
classDiagram
  class AsnPubKey {
    componentType
  }
  class OpenSSLPubKey {
    componentType
  }
  class PubKeyHeader {
    componentType
  }
  class CryptoOperation {
    description : str
    expected_cli_args : int
    has_output : bool
    input_help : str
    key_class
    keyname : str
    operation : str
    operation_past : str
    operation_progressive : str
    output_help : str
    usage : str
    parse_cli() typing.Tuple[optparse.Values, typing.List[str]]
    perform_operation(indata: bytes, key: rsa.key.AbstractKey, cli_args: Indexable)* typing.Any
    read_infile(inname: str) bytes
    read_key(filename: str, keyform: str) rsa.key.AbstractKey
    write_outfile(outdata: bytes, outname: str) None
  }
  class DecryptOperation {
    description : str
    key_class
    keyname : str
    operation : str
    operation_past : str
    operation_progressive : str
    perform_operation(indata: bytes, priv_key: rsa.key.AbstractKey, cli_args: Indexable) bytes
  }
  class EncryptOperation {
    description : str
    keyname : str
    operation : str
    operation_past : str
    operation_progressive : str
    perform_operation(indata: bytes, pub_key: rsa.key.AbstractKey, cli_args: Indexable) bytes
  }
  class SignOperation {
    description : str
    expected_cli_args : int
    key_class
    keyname : str
    operation : str
    operation_past : str
    operation_progressive : str
    output_help : str
    usage : str
    perform_operation(indata: bytes, priv_key: rsa.key.AbstractKey, cli_args: Indexable) bytes
  }
  class VerifyOperation {
    description : str
    expected_cli_args : int
    has_output : bool
    key_class
    keyname : str
    operation : str
    operation_past : str
    operation_progressive : str
    usage : str
    perform_operation(indata: bytes, pub_key: rsa.key.AbstractKey, cli_args: Indexable) None
  }
  class NotRelativePrimeError {
    a : int
    b : int
    d : int
  }
  class AbstractKey {
    blindfac : int
    blindfac_inverse : int
    e : int
    mutex : lock
    n : int
    blind(message: int) typing.Tuple[int, int]
    load_pkcs1(keyfile: bytes, format: str) T
    save_pkcs1(format: str) bytes
    unblind(blinded: int, blindfac_inverse: int) int
  }
  class AsnPrivKey {
    componentType
  }
  class PrivateKey {
    coef : int
    d : int
    ds : list
    e
    exp1 : int
    exp2 : int
    n
    p : int
    q : int
    rs : list, typing.Optional[typing.List[int]]
    ts : list
    blinded_decrypt(encrypted: int) int
  }
  class PublicKey {
    e
    n
    load_pkcs1_openssl_der(keyfile: bytes) 'PublicKey'
    load_pkcs1_openssl_pem(keyfile: bytes) 'PublicKey'
  }
  class CryptoError {
  }
  class DecryptionError {
  }
  class VerificationError {
  }
  DecryptOperation --|> CryptoOperation
  EncryptOperation --|> CryptoOperation
  SignOperation --|> CryptoOperation
  VerifyOperation --|> CryptoOperation
  PrivateKey --|> AbstractKey
  PublicKey --|> AbstractKey
  DecryptionError --|> CryptoError
  VerificationError --|> CryptoError
  DecryptOperation --> PrivateKey : key_class
  SignOperation --> PrivateKey : key_class
  CryptoOperation --> PublicKey : key_class
  VerifyOperation --> PublicKey : key_class

```
## UML Package Diagram

```mermaid
classDiagram
  class rsa {
  }
  class asn1 {
  }
  class cli {
  }
  class common {
  }
  class core {
  }
  class key {
  }
  class parallel {
  }
  class pem {
  }
  class pkcs1 {
  }
  class pkcs1_v2 {
  }
  class prime {
  }
  class randnum {
  }
  class transform {
  }
  class util {
  }
  rsa --> key
  rsa --> pkcs1
  cli --> rsa
  key --> rsa
  key --> asn1
  key --> parallel
  key --> prime
  parallel --> prime
  pkcs1_v2 --> rsa
  pkcs1_v2 --> common
  pkcs1_v2 --> pkcs1
  pkcs1_v2 --> transform
  prime --> common
  randnum --> rsa
  randnum --> common
  randnum --> transform
  util --> key
```

