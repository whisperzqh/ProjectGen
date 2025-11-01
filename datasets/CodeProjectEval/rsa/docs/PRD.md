# PRD Document for rsa

## Introduction

**Python-RSA** is a pure-Python RSA implementation that supports encryption and decryption, signing and verifying signatures, and key generation according to PKCS#1 version 1.5.   
The project's history dates back to 2006 when it started as a student assignment for the University of Amsterdam. Python was chosen primarily for its unlimited precision integer support, which is essential for RSA cryptographic operations.   
Initially, the project was just a module for calculating large primes and performing basic RSA operations with large numbers, including public and private key generation, though it lacked functionality for working with byte sequences at that time.  

## Goals

The primary goal of Python-RSA is to provide a complete RSA cryptographic solution that can be used both as a Python library and from the command line.   
The library aims to be compatible with industry standards and other RSA implementations, particularly through its support of PKCS#1 version 1.5 and version 2.1 (for multiprime encryption).   
Over its evolution, the project has focused on improving security through the introduction of random padding, ensuring compatibility with OpenSSL and other implementations, enhancing key generation to provide the exact number of bits requested while improving generation speed, and adding support for saving and loading keys in PEM and DER formats. 

## Features and Functionalities

The following features and functionalities are provided by the Python-RSA project:

### Key Generation
- Ability to generate RSA key pairs with specified bit size  
- Ability to generate keys with multiprime RSA (more than 2 prime factors) using `nprimes` parameter  
- Ability to use parallel processing to speed up key generation with `poolsize` parameter  
- Ability to control key generation accuracy with `accurate` parameter (exact bit size vs faster generation)  
- Ability to specify custom public exponent (default is 65537)  

### Encryption and Decryption
- Ability to encrypt messages using RSA public key encryption  
- Ability to decrypt messages using RSA private key decryption  
- Ability to encrypt messages with PKCS#1 v1.5 padding for security  
- Ability to perform low-level encryption/decryption operations on integers  

### Digital Signatures
- Ability to create detached signatures for messages using private key  
- Ability to verify signatures using public key  
- Ability to sign and verify file-like objects directly  
- Ability to compute hash and sign separately for remote signing scenarios  
- Support for multiple hash algorithms: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA3-256, SHA3-384, SHA3-512  

### Key Storage and Loading
- Ability to save public keys in PKCS#1 PEM format  
- Ability to save public keys in PKCS#1 DER format  
- Ability to save private keys in PKCS#1 PEM format  
- Ability to save private keys in PKCS#1 DER format  
- Ability to load public keys from PKCS#1 PEM format  
- Ability to load public keys from PKCS#1 DER format  
- Ability to load private keys from PKCS#1 PEM format  
- Ability to load private keys from PKCS#1 DER format  

### Command Line Interface
- `pyrsa-keygen`: Generate new RSA key pairs in PEM or DER format  
- `pyrsa-encrypt`: Encrypt files with RSA public key  
- `pyrsa-decrypt`: Decrypt files with RSA private key  
- `pyrsa-sign`: Create digital signatures for files  
- `pyrsa-verify`: Verify digital signatures with exit status codes  
- `pyrsa-priv2pub`: Extract public key from private key  

### Security Features
- Implementation of PKCS#1 version 1.5 standard for encryption and signing  
- Automatic random padding for encryption with minimum 8 bytes  
- Blinding support to mitigate timing attacks  
- MGF1 (Mask Generation Function) implementation for PKCS#1 v2.1  

### Python Library API
- Pure Python implementation requiring no external dependencies except pyasn1  
- Dictionary-like and attribute access to key components  
- Support for pickling keys for serialization  

## Technical Constraints

- **Python Version**: The repository must support Python 3.8 or higher (up to but not including Python 4.0)  

- **Pure Python Implementation**: The repository must be implemented entirely in pure Python with no C extensions or compiled dependencies  

- **Single Runtime Dependency**: The repository should only depend on `pyasn1` (version 0.1.3 or higher) as its sole runtime dependency  

- **PKCS#1 v1.5 Compliance**: The repository must implement RSA encryption, decryption, signing, and verification according to PKCS#1 version 1.5 standard  

- **Platform Independence**: The repository must be operating system independent and work across different platforms  

- **Python Implementation Support**: The repository must support both CPython and PyPy implementations  

- **Command-Line Interface**: The repository must provide command-line tools for key generation, encryption, decryption, signing, and verification operations using Python's optparse library  

- **Build System**: The repository must use Poetry as the build backend and dependency management system  

- **Apache 2.0 License**: The repository must be licensed under the Apache License, version 2.0  

## Requirements

### Dependencies

- `python>=3.8, <4` - Python version requirement
- `pyasn1>=0.1.3` - ASN.1 types and DER/BER/CER codecs for Python  

### Development Dependencies

- `coveralls^3.0.0` - Code coverage reporting service integration
- `Sphinx^5.0.0` - Documentation generator
- `pytest^7.2` - Testing framework
- `pytest-cov^4.0` - Test coverage plugin for pytest
- `tox^3.22.0` - Testing automation tool for multiple Python versions
- `mypy^1.2` - Static type checker for Python
- `flake8^3.8.4` - Python linting tool for style guide enforcement  

## Usage

### Installation

Install using pip:  

```bash
pip install rsa
```

### Basic Usage

#### Generating Keys

Generate a new RSA key pair:  

```python
import rsa
(pubkey, privkey) = rsa.newkeys(512)
```

Load keys from a file:  

```python
import rsa
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)
```

#### Encryption and Decryption

Encrypt a message:  

```python
import rsa
(bob_pub, bob_priv) = rsa.newkeys(512)
message = 'hello Bob!'.encode('utf8')
crypto = rsa.encrypt(message, bob_pub)
```

Decrypt a message:  

```python
message = rsa.decrypt(crypto, bob_priv)
print(message.decode('utf8'))
```

#### Signing and Verification

Sign a message:  

```python
(pubkey, privkey) = rsa.newkeys(512)
message = 'Go left at the blue tree'.encode()
signature = rsa.sign(message, privkey, 'SHA-1')
```

Verify a signature:  

```python
message = 'Go left at the blue tree'.encode()
rsa.verify(message, signature, pubkey)
# Returns: 'SHA-1'
```

### Advanced Usage Examples

#### Generate keys with multiple primes:  

```python
import rsa
(pubkey, privkey) = rsa.newkeys(512, nprimes=3)
```

#### Parallel key generation for faster processing:  

```python
(pubkey, privkey) = rsa.newkeys(512, poolsize=8)
```

#### Compute hash and sign separately:  

```python
message = 'Go left at the blue tree'.encode()
hash = rsa.compute_hash(message, 'SHA-1')
signature = rsa.sign_hash(hash, privkey, 'SHA-1')
```

#### Sign and verify files:  

```python
with open('somefile', 'rb') as msgfile:
    signature = rsa.sign(msgfile, privkey, 'SHA-1')

with open('somefile', 'rb') as msgfile:
    rsa.verify(msgfile, signature, pubkey)
```

### Command-Line Interface  

The library also provides command-line tools:

- `pyrsa-keygen` - Generate RSA key pairs
- `pyrsa-encrypt` - Encrypt files
- `pyrsa-decrypt` - Decrypt files
- `pyrsa-sign` - Sign files
- `pyrsa-verify` - Verify signatures
- `pyrsa-priv2pub` - Convert private key to public key

All commands accept `--help` for detailed usage instructions.

## Command Line Configuration Arguments

### 1. pyrsa-keygen  

```
Usage: pyrsa-keygen [options] keysize

  Generates a new RSA key pair of "keysize" bits.

Options:
  --pubout TEXT     Output filename for the public key. The public key is
                    not saved if this option is not present. You can use
                    pyrsa-priv2pub to create the public key file later.
  -o, --out TEXT    Output filename for the private key. The key is
                    written to stdout if this option is not present.
  --form            Key format of the private and public keys - default PEM
                    Choices: (PEM, DER)
```

### 2. pyrsa-encrypt  

```
Usage: pyrsa-encrypt [options] public_key

  Encrypts a file. The file must be shorter than the key length in order
  to be encrypted.

Options:
  -i, --input TEXT   Name of the file to encrypt. Reads from stdin if
                     not specified.
  -o, --output TEXT  Name of the file to write the encrypted file to.
                     Written to stdout if this option is not present.
  --keyform          Key format of the public key - default PEM
                     Choices: (PEM, DER)
```

### 3. pyrsa-decrypt  

```
Usage: pyrsa-decrypt [options] private_key

  Decrypts a file. The original file must be shorter than the key length
  in order to have been encrypted.

Options:
  -i, --input TEXT   Name of the file to decrypt. Reads from stdin if
                     not specified.
  -o, --output TEXT  Name of the file to write the decrypted file to.
                     Written to stdout if this option is not present.
  --keyform          Key format of the private key - default PEM
                     Choices: (PEM, DER)
```

### 4. pyrsa-sign  

```
Usage: pyrsa-sign [options] private_key hash_method

  Signs a file, outputs the signature. Choose the hash method from
  MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512

Options:
  -i, --input TEXT   Name of the file to sign. Reads from stdin if
                     not specified.
  -o, --output TEXT  Name of the file to write the signature to.
                     Written to stdout if this option is not present.
  --keyform          Key format of the private key - default PEM
                     Choices: (PEM, DER)
```

### 5. pyrsa-verify  

```
Usage: pyrsa-verify [options] public_key signature_file

  Verifies a signature, exits with status 0 upon success, prints an
  error message and exits with status 1 upon error.

Options:
  -i, --input TEXT   Name of the file to verify. Reads from stdin if
                     not specified.
  --keyform          Key format of the public key - default PEM
                     Choices: (PEM, DER)
```

### 6. pyrsa-priv2pub  

```
Usage: pyrsa-priv2pub [options]

  Reads a private key and outputs the corresponding public key. Both
  private and public keys use the format described in PKCS#1 v1.5

Options:
  -i, --input TEXT   Input filename. Reads from stdin if not specified
  -o, --output TEXT  Output filename. Writes to stdout if not specified
  --inform           Key format of input - default PEM
                     Choices: (PEM, DER)
  --outform          Key format of output - default PEM
                     Choices: (PEM, DER)
```

## Terms/Concepts Explanation

**RSA (Rivest-Shamir-Adleman)**: A public-key cryptographic algorithm that supports encryption and decryption, signing and verifying signatures. This library is a pure-Python implementation of RSA.  

**Public Key / Private Key**: An asymmetric key pair where the public key is used for encrypting messages (encryption key) that can only be decrypted by the owner of the corresponding private key (decryption key). The private key is also used for signing messages.  

**PKCS#1 (Public-Key Cryptography Standards #1)**: A standard for RSA encryption and signing. This library implements PKCS#1 version 1.5 for encryption, decryption, signing, and verification, and version 2.1 for multiprime encryption.  

**PEM (Privacy-Enhanced Mail)**: A Base64-encoded format for storing cryptographic keys and certificates, typically enclosed between "-----BEGIN-----" and "-----END-----" markers.  

**DER (Distinguished Encoding Rules)**: A binary encoding format for storing cryptographic keys and certificates, used as an alternative to PEM format.  

**ASN.1 (Abstract Syntax Notation One)**: A standard interface description language for defining data structures that can be serialized and deserialized in a cross-platform way, used for encoding RSA keys.  

**Digital Signature**: A cryptographic value created by signing a message with a private key, which can be verified using the corresponding public key to ensure the message was signed by the key owner and hasn't been modified.  

**Prime Number**: A fundamental building block of RSA encryption. The algorithm relies on the difficulty of factoring the product of two large prime numbers.  

**Miller-Rabin Primality Testing**: A probabilistic algorithm used to test whether a number is prime or composite, used during RSA key generation to find suitable prime numbers.  

**Chinese Remainder Theorem (CRT)**: A mathematical theorem used to perform faster decryption operations by breaking down the computation into smaller operations modulo the prime factors.  

**Random Padding**: Random data added to messages before encryption to increase security and prevent certain types of attacks. PKCS#1 v1.5 uses at least 8 bytes of random padding.  

**Hash Function**: A cryptographic function (such as SHA-1, SHA-256, SHA-512) that creates a fixed-size digest of a message, used in digital signature operations.  

**Modular Arithmetic**: Mathematical operations performed with a modulus, forming the mathematical foundation of RSA encryption and decryption. The core RSA operations work on integers modulo n.  

**Timing Attack**: A security vulnerability where an attacker can deduce information about cryptographic keys by measuring the time it takes to perform operations. This pure-Python implementation is susceptible to timing attacks due to how Python stores numbers internally.  

**Blinding**: A technique used to protect against certain types of attacks by multiplying the ciphertext with a random blinding factor before decryption, then removing the factor afterward.  


