# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
    ├── main
    │   └── java
    │       └── com
    │           └── warrenstrange
    │               └── googleauth
    │                   ├── GoogleAuthenticatorConfig.java
    │                   ├── GoogleAuthenticatorException.java
    │                   ├── GoogleAuthenticator.java
    │                   ├── GoogleAuthenticatorKey.java
    │                   ├── GoogleAuthenticatorQRGenerator.java
    │                   ├── HmacHashFunction.java
    │                   ├── ICredentialRepository.java
    │                   ├── IGoogleAuthenticator.java
    │                   ├── KeyRepresentation.java
    │                   └── ReseedingSecureRandom.java

```

`GoogleAuthenticatorConfig.java`:

- `GoogleAuthenticatorConfig`: Defines the configuration parameters for the Google Authenticator TOTP generation (e.g., time step, window size, code digits).

  - `getKeyModulus() -> int`: Returns the modulus used for code generation based on the number of digits.
  
  - `getKeyRepresentation() -> KeyRepresentation`: Returns the key representation format (BASE32 or BASE64).
  
  - `getCodeDigits() -> int`: Returns the number of digits in the generated code.
  
  - `getNumberOfScratchCodes() -> int`: Returns the number of scratch codes to generate.
  
  - `getTimeStepSizeInMillis() -> long`: Returns the time step size in milliseconds (default 30s).
  
  - `getWindowSize() -> int`: Returns the validation window size to account for clock skew.
  
  - `getSecretBits() -> int`: Returns the number of bits for the secret key.
  
  - `getHmacHashFunction() -> HmacHashFunction`: Returns the cryptographic hash function used (e.g., SHA1).

- `GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder`: Builder class for creating `GoogleAuthenticatorConfig` instances.

  - `build() -> GoogleAuthenticatorConfig`: Constructs and returns the configuration object.
  
  - `setCodeDigits(codeDigits: int) -> GoogleAuthenticatorConfigBuilder`: Sets the number of digits for the code (must be between 6 and 8).
  
  - `setNumberOfScratchCodes(numberOfScratchCodes: int) -> GoogleAuthenticatorConfigBuilder`: Sets the number of scratch codes to generate (max 1000).
  
  - `setTimeStepSizeInMillis(timeStepSizeInMillis: long) -> GoogleAuthenticatorConfigBuilder`: Sets the time step size in milliseconds.
  
  - `setWindowSize(windowSize: int) -> GoogleAuthenticatorConfigBuilder`: Sets the window size for validation.
  
  - `setSecretBits(secretBits: int) -> GoogleAuthenticatorConfigBuilder`: Sets the number of bits for the secret key (min 128, multiple of 8).
  
  - `setKeyRepresentation(keyRepresentation: KeyRepresentation) -> GoogleAuthenticatorConfigBuilder`: Sets the key representation format.
  
  - `setHmacHashFunction(hmacHashFunction: HmacHashFunction) -> GoogleAuthenticatorConfigBuilder`: Sets the HMAC hash function.

`GoogleAuthenticatorException.java`:

- `GoogleAuthenticatorException`: Runtime exception thrown when an error occurs during the Google Authenticator operations.

  - `Constructor(message: String) -> GoogleAuthenticatorException`: Constructs an exception with a specific message.
  
  - `Constructor(message: String, cause: Throwable) -> GoogleAuthenticatorException`: Constructs an exception with a message and a root cause.

`GoogleAuthenticator.java`:

- `GoogleAuthenticator`: The main class implementing the TOTP algorithm (RFC 6238), providing methods to create credentials and validate code.

  - `Constructor() -> GoogleAuthenticator`: Initializes with default configuration and SecureRandom algorithm.
  
  - `Constructor(config: GoogleAuthenticatorConfig) -> GoogleAuthenticator`: Initializes with a custom configuration.
  
  - `Constructor(randomNumberAlgorithm: String, randomNumberAlgorithmProvider: String) -> GoogleAuthenticator`: Initializes with custom SecureRandom algorithm and default config.
  
  - `Constructor(config: GoogleAuthenticatorConfig, randomNumberAlgorithm: String, randomNumberAlgorithmProvider: String) -> GoogleAuthenticator`: Initializes with custom config and SecureRandom algorithm.
  
  - `getRandomNumberAlgorithm() -> String`: Returns the random number generator algorithm name.
  
  - `getRandomNumberAlgorithmProvider() -> String`: Returns the provider for the random number generator.
  
  - `calculateCode(key: byte[], tm: long) -> int`: Calculates the verification code for a given key and time instant.
  
  - `getTimeWindowFromTime(time: long) -> long`: Converts a time in ms to a time window index based on step size.
  
  - `checkCode(secret: String, code: long, timestamp: long, window: int) -> boolean`: Checks if a code is valid within a specified time window.
  
  - `decodeSecret(secret: String) -> byte[]`: Decodes the secret string (Base32 or Base64) into bytes.
  
  - `createCredentials() -> GoogleAuthenticatorKey`: Generates a new random secret key and associated credentials.
  
  - `createCredentials(userName: String) -> GoogleAuthenticatorKey`: Generates credentials and saves them to the configured repository.
  
  - `calculateScratchCodes() -> List<Integer>`: Generates a list of scratch codes.
  
  - `calculateScratchCode(scratchCodeBuffer: byte[]) -> int`: Calculates a single scratch code from a byte buffer.
  
  - `validateScratchCode(scratchCode: int) -> boolean`: Validates if a scratch code meets format requirements.
  
  - `generateScratchCode() -> int`: Generates a valid random scratch code.
  
  - `calculateValidationCode(secretKey: byte[]) -> int`: Calculates the validation code at time 0.
  
  - `getTotpPassword(secret: String) -> int`: Generates the current TOTP password for a secret.
  
  - `getTotpPassword(secret: String, time: long) -> int`: Generates the TOTP password for a secret at a specific time.
  
  - `getTotpPasswordOfUser(userName: String) -> int`: Generates the current TOTP password for a user using the repository.
  
  - `getTotpPasswordOfUser(userName: String, time: long) -> int`: Generates the TOTP password for a user at a specific time using the repository.
  
  - `calculateSecretKey(secretKey: byte[]) -> String`: Encodes the raw secret key bytes into a string.
  
  - `authorize(secret: String, verificationCode: int) -> boolean`: Checks a verification code against a secret using current time.
  
  - `authorize(secret: String, verificationCode: int, time: long) -> boolean`: Checks a verification code against a secret using a specific time.
  
  - `authorizeUser(userName: String, verificationCode: int) -> boolean`: Validates a code for a user using the repository and current time.
  
  - `authorizeUser(userName: String, verificationCode: int, time: long) -> boolean`: Validates a code for a user using the repository and specific time.
  
  - `getValidCredentialRepository() -> ICredentialRepository`: Retrieves the configured credential repository or throws generic exception if absent.
  
  - `getCredentialRepository() -> ICredentialRepository`: Retrieves the configured or discovered credential repository.
  
  - `setCredentialRepository(repository: ICredentialRepository) -> void`: Sets the credential repository explicitly.

`GoogleAuthenticatorKey.java`:

- `GoogleAuthenticatorKey`: An immutable container for the secret key, configuration, validation code, and scratch codes.

  - `Constructor(config: GoogleAuthenticatorConfig, key: String, verificationCode: int, scratchCodes: List<Integer>) -> GoogleAuthenticatorKey`: Private constructor used by the Builder.
  
  - `getScratchCodes() -> List<Integer>`: Returns the list of scratch codes.
  
  - `getConfig() -> GoogleAuthenticatorConfig`: Returns the configuration associated with this key.
  
  - `getKey() -> String`: Returns the secret key.
  
  - `getVerificationCode() -> int`: Returns the verification code at time 0.

- `GoogleAuthenticatorKey.Builder`: Builder class for `GoogleAuthenticatorKey`.

  - `Constructor(key: String) -> Builder`: Initializes the builder with a secret key.
  
  - `build() -> GoogleAuthenticatorKey`: Constructs the key object.
  
  - `setConfig(config: GoogleAuthenticatorConfig) -> Builder`: Sets the configuration.
  
  - `setKey(key: String) -> Builder`: Sets the secret key.
  
  - `setVerificationCode(verificationCode: int) -> Builder`: Sets the verification code.
  
  - `setScratchCodes(scratchCodes: List<Integer>) -> Builder`: Sets the list of scratch codes.

`GoogleAuthenticatorQRGenerator.java`:

- `GoogleAuthenticatorQRGenerator`: Utility class to generate URLs for QR codes used to provision the Google Authenticator app.

  - `internalURLEncode(s: String) -> String`: Helper to URL-encode strings using UTF-8.
  
  - `formatLabel(issuer: String, accountName: String) -> String`: Formats the label for the OTP URI.
  
  - `getOtpAuthURL(issuer: String, accountName: String, credentials: GoogleAuthenticatorKey) -> String`: Returns a Google Chart API URL to generate the QR code.
  
  - `getOtpAuthTotpURL(issuer: String, accountName: String, credentials: GoogleAuthenticatorKey) -> String`: Returns the raw `otpauth://` URI.
  
  - `getAlgorithmName(hashFunction: HmacHashFunction) -> String`: Maps the hash function enum to its string name.

`HmacHashFunction.java`:

- `HmacHashFunction`: Enum representing supported HMAC hash functions.

  - `HmacSHA1`: SHA1 algorithm.
  
  - `HmacSHA256`: SHA256 algorithm.
  
  - `HmacSHA512`: SHA512 algorithm.

`ICredentialRepository.java`:

- `ICredentialRepository`: Interface for a storage mechanism to save and retrieve user credentials.

  - `getSecretKey(userName: String) -> String`: Retrieves the secret key for a given user.
  
  - `saveUserCredentials(userName: String, secretKey: String, validationCode: int, scratchCodes: List<Integer>) -> void`: Saves the credentials for a user.

`IGoogleAuthenticator.java`:

- `IGoogleAuthenticator`: Interface defining the contract for the Google Authenticator library service.

  - `createCredentials() -> GoogleAuthenticatorKey`: Generates a new set of credentials.
  
  - `createCredentials(userName: String) -> GoogleAuthenticatorKey`: Generates and saves credentials for a user.
  
  - `getTotpPassword(secret: String) -> int`: Generates the current TOTP password.
  
  - `getTotpPassword(secret: String, time: long) -> int`: Generates the TOTP password at a specific time.
  
  - `getTotpPasswordOfUser(userName: String) -> int`: Generates the current TOTP password for a user.
  
  - `getTotpPasswordOfUser(userName: String, time: long) -> int`: Generates the TOTP password for a user at a specific time.
  
  - `authorize(secret: String, verificationCode: int) -> boolean`: Validates a code against a secret.
  
  - `authorize(secret: String, verificationCode: int, time: long) -> boolean`: Validates a code against a secret at a specific time.
  
  - `authorizeUser(userName: String, verificationCode: int) -> boolean`: Validates a code for a user.
  
  - `authorizeUser(userName: String, verificationCode: int, time: long) -> boolean`: Validates a code for a user at a specific time.
  
  - `getCredentialRepository() -> ICredentialRepository`: Gets the current credential repository.
  
  - `setCredentialRepository(repository: ICredentialRepository) -> void`: Sets the credential repository.

`KeyRepresentation.java`:

- `KeyRepresentation`: Enum representing the encoding format of the secret key.

  - `BASE32`: Base32 encoding.
  
  - `BASE64`: Base64 encoding.

`ReseedingSecureRandom.java`:

- `ReseedingSecureRandom`: A wrapper around `SecureRandom` that automatically reseeds itself after a certain number of operations (package-private).

  - `Constructor() -> ReseedingSecureRandom`: Initializes with default algorithm.
  
  - `Constructor(algorithm: String) -> ReseedingSecureRandom`: Initializes with specific algorithm.
  
  - `Constructor(algorithm: String, provider: String) -> ReseedingSecureRandom`: Initializes with specific algorithm and provider.
  
  - `buildSecureRandom() -> void`: Creates the underlying `SecureRandom` instance.
  
  - `nextBytes(bytes: byte[]) -> void`: Generates random bytes, reseeding the generator if the operation count threshold is reached.
