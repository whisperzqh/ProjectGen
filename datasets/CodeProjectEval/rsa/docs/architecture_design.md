# Architecture Design

Below is a text-based representation of the file tree.

``` bash
├── rsa
│   ├── asn1.py
│   ├── cli.py
│   ├── common.py
│   ├── core.py
│   ├── __init__.py
│   ├── key.py
│   ├── parallel.py
│   ├── pem.py
│   ├── pkcs1.py
│   ├── pkcs1_v2.py
│   ├── prime.py
│   ├── py.typed
│   ├── randnum.py
│   ├── transform.py
│   └── util.py
```

`asn1.py` :

- `PubKeyHeader()`: An ASN.1 SEQUENCE representing the algorithm identifier header in an OpenSSL public key structure.

  - The instance attribute `componentType` defines the header as containing an object identifier and null parameters.

- `OpenSSLPubKey()`: An ASN.1 SEQUENCE modeling the full OpenSSL public key format, consisting of a header and a key bitstring encoded as an octet string using an implicit tag.

  - The instance attribute `componentType` defines the structure as containing a `PubKeyHeader` and a tagged octet string for the key data.

- `AsnPubKey()`: An ASN.1 SEQUENCE representing the raw RSA public key in DER encoding, containing the modulus and public exponent.

  - The instance attribute `componentType` defines the structure as containing two integers: the RSA modulus and the public exponent.a

`cli.py` :

- `keygen()`: A command-line utility that generates a new RSA key pair of a specified bit size and optionally saves the public and private keys to files in PEM or DER format.

- `CryptoOperation()`: An abstract base class for command-line cryptographic operations that handle input/output files and key loading. It defines the common workflow for reading keys, processing data, and writing output.

  - The instance attribute `keyname` indicates whether the operation uses a "public" or "private" key.
  - The instance attribute `usage` defines the command-line usage string.
  - The instance attribute `description` provides a brief description of the operation.
  - The instance attribute `operation` names the action (e.g., "encrypt").
  - The instance attribute `operation_past` describes the result (e.g., "encrypted").
  - The instance attribute `operation_progressive` is used in status messages (e.g., "encrypting").
  - The instance attribute `input_help` describes the input file option.
  - The instance attribute `output_help` describes the output file option.
  - The instance attribute `expected_cli_args` specifies the number of required positional command-line arguments.
  - The instance attribute `has_output` indicates whether the operation writes output data.
  - The instance attribute `key_class` specifies the expected key type (`rsa.PublicKey` or `rsa.PrivateKey`).
  - `perform_operation(indata: bytes, key: rsa.key.AbstractKey, cli_args: Indexable) -> typing.Any`: Abstract method that subclasses must implement to define the core cryptographic operation.
  - `__call__()`: Executes the full command-line operation by parsing arguments, loading the key, reading input, performing the operation, and writing output.
  - `parse_cli() -> typing.Tuple[optparse.Values, typing.List[str]]`: Parses command-line options and validates the number of arguments.
  - `read_key(filename: str, keyform: str) -> rsa.key.AbstractKey`: Loads an RSA key from a file in the specified format (PEM or DER).
  - `read_infile(inname: str) -> bytes`: Reads input data from a file or stdin.
  - `write_outfile(outdata: bytes, outname: str) -> None`: Writes output data to a file or stdout.

- `EncryptOperation()`: A concrete `CryptoOperation` subclass that encrypts input data using a public RSA key.

  - `perform_operation(indata: bytes, pub_key: rsa.key.AbstractKey, cli_args: Indexable = ()) -> bytes`: Encrypts the input bytes using the provided public key.

- `DecryptOperation()`: A concrete `CryptoOperation` subclass that decrypts input data using a private RSA key.

  - `perform_operation(indata: bytes, priv_key: rsa.key.AbstractKey, cli_args: Indexable = ()) -> bytes`: Decrypts the input bytes using the provided private key.

- `SignOperation()`: A concrete `CryptoOperation` subclass that creates a digital signature of input data using a private RSA key and a specified hash method.

  - `perform_operation(indata: bytes, priv_key: rsa.key.AbstractKey, cli_args: Indexable) -> bytes`: Signs the input data using the private key and the hash method given as the second command-line argument.

- `VerifyOperation()`: A concrete `CryptoOperation` subclass that verifies a digital signature against input data using a public RSA key.

  - `perform_operation(indata: bytes, pub_key: rsa.key.AbstractKey, cli_args: Indexable) -> None`: Verifies the signature read from the file specified in the second command-line argument; exits with an error if verification fails.

`common.py` :

- `bit_size(num: int) -> int`: Returns the number of bits required to represent the absolute value of an integer, excluding leading zeros. Returns 0 for input 0.

- `byte_size(number: int) -> int`: Computes the number of bytes required to hold a non-negative integer, rounding up to the nearest whole byte.

- `ceil_div(num: int, div: int) -> int`: Returns the ceiling of the division of `num` by `div`, i.e., the smallest integer greater than or equal to the exact quotient.

- `extended_gcd(a: int, b: int) -> typing.Tuple[int, int, int]`: Computes the greatest common divisor (gcd) of two integers `a` and `b`, along with Bézout coefficients `i` and `j` such that `gcd(a, b) = i*a + j*b`.

- `inverse(x: int, n: int) -> int`: Returns the multiplicative inverse of `x` modulo `n`, i.e., an integer `inv` such that `(x * inv) % n == 1`. Raises `NotRelativePrimeError` if `x` and `n` are not coprime.

- `crt(a_values: typing.Iterable[int], modulo_values: typing.Iterable[int]) -> int`: Solves a system of simultaneous congruences using the Chinese Remainder Theorem, returning the smallest non-negative integer `x` satisfying `x ≡ a[i] (mod m[i])` for all `i`.

- `NotRelativePrimeError(a: int, b: int, d: int, msg: str = "")`: An exception raised when two integers are not relatively prime (i.e., their greatest common divisor is not 1), typically in modular arithmetic contexts.

  - The instance attribute `a` stores the first integer involved in the failed coprimality check.
  - The instance attribute `b` stores the second integer involved.
  - The instance attribute `d` stores the actual greatest common divisor of `a` and `b`.

`core.py` :

- `assert_int(var: int, name: str)`: Raises a `TypeError` if the given `var` is not an integer, used for input validation in RSA operations.

- `encrypt_int(message: int, ekey: int, n: int) -> int`: Encrypts a non-negative integer `message` using RSA public exponent `ekey` and modulus `n`, ensuring the message is smaller than `n`.

- `decrypt_int(cyphertext: int, dkey: int, n: int) -> int`: Decrypts an RSA ciphertext integer using the private exponent `dkey` and modulus `n` via modular exponentiation.

- `decrypt_int_fast(cyphertext: int, rs: typing.List[int], ds: typing.List[int], ts: typing.List[int]) -> int`: Efficiently decrypts an RSA ciphertext using the Chinese Remainder Theorem (CRT), given prime factors, exponents, and precomputed coefficients.

`key.py` :

- `find_primes(nbits: int, getprime_func: typing.Callable[[int], int] = rsa.prime.getprime, accurate: bool = True, nprimes: int = 2) -> typing.List[int]`: Returns a list of distinct primes whose total bit length sums to `nbits`, distributed evenly (or as evenly as possible) among them.

- `find_p_q(nbits: int, getprime_func: typing.Callable[[int], int] = rsa.prime.getprime, accurate: bool = True) -> typing.Tuple[int, int]`: Generates two distinct primes `p` and `q`, each approximately `nbits` long, ensuring their product has the desired total bit length when `accurate=True`.

- `calculate_keys_custom_exponent(p: int, q: int, exponent: int, rs: typing.Optional[typing.List[int]] = None) -> typing.Tuple[int, int]`: Computes the public exponent `e` (as provided) and private exponent `d` using Euler’s totient of the modulus formed from primes `p`, `q`, and optionally additional primes `rs`.

- `calculate_keys(p: int, q: int) -> typing.Tuple[int, int]`: Calculates the standard RSA key pair exponents (`e`, `d`) using the default public exponent (65537) and given primes `p` and `q`.

- `gen_keys(nbits: int, getprime_func: typing.Callable[[int], int], accurate: bool = True, exponent: int = DEFAULT_EXPONENT, nprimes: int = 2) -> typing.Tuple`: Generates RSA key components (`p`, `q`, `e`, `d`, and optionally `rs`) for a modulus of `nbits` bits, retrying until valid keys are found.

- `newkeys(nbits: int, accurate: bool = True, poolsize: int = 1, exponent: int = DEFAULT_EXPONENT, nprimes: int = 2) -> typing.Tuple[PublicKey, PrivateKey]`: Creates and returns a new RSA public/private key pair with a modulus of `nbits` bits, supporting multi-prime RSA and optional parallel prime generation.

- `AbstractKey(metaclass=abc.ABCMeta)`: Abstract base class for RSA public and private keys, providing shared functionality including blinding support for side-channel attack mitigation.

  - `blind(self, message: int) -> typing.Tuple[int, int]`: Blinds the input message using a random blinding factor to prevent timing or other side-channel attacks during cryptographic operations.
  
  - `unblind(self, blinded: int, blindfac_inverse: int) -> int`: Unblinds a previously blinded message using the inverse of the blinding factor to recover the original result.
  
  - `load_pkcs1(cls, keyfile: bytes, format: str = "PEM") -> T`: Loads a key from PKCS#1-encoded data in either PEM or DER format.
  
  - `save_pkcs1(self, format: str = "PEM") -> bytes`: Serializes the key to PKCS#1 format, either PEM or DER.

- `PublicKey(AbstractKey)`: Represents an RSA public key (encryption key), containing the modulus `n` and public exponent `e`.

  - The instance attribute `n` is the RSA modulus.
  - The instance attribute `e` is the public exponent.
  - Supports dictionary-like access (e.g., `key['n']`) and pickling.
  
  - `_load_pkcs1_pem(cls, keyfile: bytes) -> "PublicKey"`: Parses a PEM-encoded PKCS#1 RSA public key.
  
  - `_load_pkcs1_der(cls, keyfile: bytes) -> "PublicKey"`: Parses a DER-encoded PKCS#1 RSA public key.
  
  - `_save_pkcs1_pem(self) -> bytes`: Serializes the public key to PEM-encoded PKCS#1 format.
  
  - `_save_pkcs1_der(self) -> bytes`: Serializes the public key to DER-encoded PKCS#1 format.
  
  - `load_pkcs1_openssl_pem(cls, keyfile: bytes) -> "PublicKey"`: Loads a public key from OpenSSL’s PEM format (starting with "-----BEGIN PUBLIC KEY-----").
  
  - `load_pkcs1_openssl_der(cls, keyfile: bytes) -> "PublicKey"`: Loads a public key from OpenSSL’s DER format (which includes an OID identifying RSA).

- `PrivateKey(AbstractKey)`: Represents an RSA private key (decryption key), containing the modulus `n`, public exponent `e`, private exponent `d`, prime factors `p` and `q`, and CRT optimization parameters.

  - The instance attribute `n` is the RSA modulus.
  - The instance attribute `e` is the public exponent.
  - The instance attribute `d` is the private exponent.
  - The instance attributes `p` and `q` are the prime factors of `n`.
  - The instance attributes `exp1`, `exp2`, and `coef` are used for Chinese Remainder Theorem (CRT) optimizations.
  - The instance attributes `rs`, `ds`, and `ts` support multi-prime RSA (additional primes and related parameters).
  - Supports dictionary-like access and secure pickling (with warnings about untrusted sources).
  
  - `blinded_decrypt(self, encrypted: int) -> int`: Decrypts a ciphertext using blinding to protect against side-channel attacks, leveraging CRT-based fast decryption internally.
  
  - `_load_pkcs1_pem(cls, keyfile: bytes) -> "PrivateKey"`: Parses a PEM-encoded PKCS#1 RSA private key.
  
  - `_load_pkcs1_der(cls, keyfile: bytes) -> "PrivateKey"`: Parses a DER-encoded PKCS#1 RSA private key, including optional multi-prime fields.
  
  - `_save_pkcs1_pem(self) -> bytes`: Serializes the private key to PEM-encoded PKCS#1 format.
  
  - `_save_pkcs1_der(self) -> bytes`: Serializes the private key to DER-encoded PKCS#1 format, including multi-prime extensions if present.

`parallel.py` :

- `getprime(nbits: int, poolsize: int) -> int`: Generates a prime number that fits in `nbits` bits by using `poolsize` parallel processes to search concurrently, significantly speeding up prime generation on multi-core systems.

`pem.py` :

- `load_pem(contents: FlexiText, pem_marker: FlexiText) -> bytes`: Parses PEM-encoded input (given as either a string or bytes) and extracts the binary data located between the PEM start and end markers corresponding to `pem_marker` (e.g., `'RSA PRIVATE KEY'`), returning the base64-decoded content as bytes. Raises `ValueError` if the expected markers are missing or malformed.

- `save_pem(contents: bytes, pem_marker: FlexiText) -> bytes`: Encodes binary data into PEM format by wrapping it with standard PEM header and footer lines based on `pem_marker` (e.g., `'RSA PUBLIC KEY'`), applying base64 encoding, and formatting the output with 64-character line breaks followed by a final newline.

`pkcs1_v2.py` :

- `mgf1(seed: bytes, length: int, hasher: str = "SHA-1") -> bytes`: Implements the MGF1 (Mask Generation Function 1) as defined in RFC 2437 (PKCS#1 v2.0). It generates a pseudorandom mask of specified `length` from a given `seed` using a hash function (default: SHA-1). Used primarily in OAEP padding for RSA encryption. Raises `ValueError` for unsupported hashers and `OverflowError` if the requested length exceeds the allowed limit (2³² × hash output size).

`pkcs1.py` :

- `encrypt(message: bytes, pub_key: key.PublicKey) -> bytes`: Encrypts a message using PKCS#1 v1.5 padding with the given RSA public key. Raises `OverflowError` if the message is too long for the key size.

- `decrypt(crypto: bytes, priv_key: key.PrivateKey) -> bytes`: Decrypts a PKCS#1 v1.5–padded ciphertext using the given RSA private key. Raises `DecryptionError` if the padding is invalid or malformed.

- `sign(message: bytes, priv_key: key.PrivateKey, hash_method: str) -> bytes`: Computes a PKCS#1 v1.5 signature over the message by first hashing it with the specified algorithm and then signing the hash with the private key.

- `sign_hash(hash_value: bytes, priv_key: key.PrivateKey, hash_method: str) -> bytes`: Signs a precomputed hash value using PKCS#1 v1.5 padding and the given private key, embedding the hash method identifier in the signature.

- `verify(message: bytes, signature: bytes, pub_key: key.PublicKey) -> str`: Verifies a PKCS#1 v1.5 signature against the message using the public key, automatically detecting the hash algorithm used. Returns the name of the hash method on success or raises `VerificationError` on failure.

- `find_signature_hash(signature: bytes, pub_key: key.PublicKey) -> str`: Extracts and returns the name of the hash algorithm embedded in a PKCS#1 v1.5 signature without verifying the message.

- `compute_hash(message: typing.Union[bytes, typing.BinaryIO], method_name: str) -> bytes`: Computes the digest of a message (either bytes or a file-like object) using the specified hash algorithm.

- `yield_fixedblocks(infile: typing.BinaryIO, blocksize: int) -> typing.Iterator[bytes]`: A generator that reads a binary file in fixed-size blocks and yields each block until EOF.

- `CryptoError`: Base exception class for all cryptographic errors in this module.

- `DecryptionError`: Raised when PKCS#1 v1.5 decryption fails due to invalid padding or formatting.

- `VerificationError`: Raised when a PKCS#1 v1.5 signature verification fails due to mismatched hash or invalid structure.

`prime.py`:

- `gcd(p: int, q: int) -> int`: Computes the greatest common divisor of two integers using the Euclidean algorithm.

- `get_primality_testing_rounds(number: int) -> int`: Determines the number of Miller–Rabin primality test rounds required based on the bit size of the input number, following NIST FIPS 186-4 recommendations for a 2⁻¹⁰⁰ error probability.

- `miller_rabin_primality_testing(n: int, k: int) -> bool`: Performs the Miller–Rabin probabilistic primality test on an integer `n` using `k` random witnesses; returns `True` if `n` is probably prime, `False` if it is definitely composite.

- `is_prime(number: int) -> bool`: Checks whether a given integer is prime by first handling small and even numbers directly, then applying the Miller–Rabin test with a security parameter derived from the number’s bit size.

- `getprime(nbits: int) -> int`: Generates a random prime number that fits in exactly `nbits` bits by repeatedly sampling random odd integers and testing them for primality.

- `are_relatively_prime(a: int, b: int) -> bool`: Returns `True` if two integers are coprime (i.e., their greatest common divisor is 1), otherwise `False`.

`randnum.py` :

- `read_random_bits(nbits: int) -> bytes`: Generates a byte string containing `nbits` of cryptographically secure random data, padding with an extra partial byte if `nbits` is not divisible by 8.

- `read_random_int(nbits: int) -> int`: Returns a random integer that uses approximately `nbits` bits, ensuring the most significant bit is set so the result has the full bit length.

- `read_random_odd_int(nbits: int) -> int`: Returns a random odd integer of approximately `nbits` bits by setting the least significant bit of a random integer generated via `read_random_int`.

- `randint(maxvalue: int) -> int`: Returns a uniformly random integer `x` such that `1 <= x <= maxvalue`, using rejection sampling with adaptive bit size to improve efficiency.

`transform.py` :

- `bytes2int(raw_bytes: bytes) -> int`: Converts a byte string to an unsigned integer using big-endian byte order. Intended for raw binary data, not Unicode strings.

- `int2bytes(number: int, fill_size: int = 0) -> bytes`: Converts a non-negative integer to its big-endian byte representation. If `fill_size` is specified, the result is padded with leading zero bytes to match the given length; raises `OverflowError` if the number requires more bytes than `fill_size`.

`util.py` :

- `private_to_public() -> None`: A command-line utility function that reads an RSA private key from a file or standard input (in PEM or DER format), extracts the corresponding public key, and writes it to a file or standard output in the specified format.
  