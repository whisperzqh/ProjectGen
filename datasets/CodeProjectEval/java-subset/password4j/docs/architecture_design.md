# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
    ├── main
    │   └── java
    │       └── com
    │           └── password4j
    │               ├── AbstractHashingFunction.java
    │               ├── AlgorithmFinder.java
    │               ├── Argon2Function.java
    │               ├── BadParametersException.java
    │               ├── BalloonHashingFunction.java
    │               ├── BcryptFunction.java
    │               ├── BenchmarkResult.java
    │               ├── Blake2b.java
    │               ├── CompressedPBKDF2Function.java
    │               ├── HashBuilder.java
    │               ├── HashChecker.java
    │               ├── HashingFunction.java
    │               ├── Hash.java
    │               ├── HashUpdate.java
    │               ├── HashUpdater.java
    │               ├── MessageDigestFunction.java
    │               ├── Password.java
    │               ├── PBKDF2Function.java
    │               ├── PepperGenerator.java
    │               ├── PropertyReader.java
    │               ├── SaltGenerator.java
    │               ├── SaltOption.java
    │               ├── ScryptFunction.java
    │               ├── SecureString.java
    │               ├── SystemChecker.java
    │               ├── types
    │               │   ├── Argon2.java
    │               │   ├── Bcrypt.java
    │               │   └── Hmac.java
    │               └── Utils.java
```

`AbstractHashingFunction.java`:

- `AbstractHashingFunction`: Abstract base class implementing common logic for hashing functions to avoid code duplication.

  - `slowEquals(a: CharSequence, b: CharSequence) -> boolean`: Compares two CharSequences in length-constant time to prevent timing attacks.
  
  - `slowEquals(a: byte[], b: byte[]) -> boolean`: Compares two byte arrays in length-constant time to prevent timing attacks.
  
  - `hash(plainTextPassword: CharSequence, salt: String, pepper: CharSequence) -> Hash`: Hashes a password using the provided salt and pepper.
  
  - `hash(plainTextPassword: byte[], salt: byte[], pepper: CharSequence) -> Hash`: Hashes a byte array password using the provided salt and pepper.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Verifies a password against a hash and salt.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[]) -> boolean`: Verifies a byte array password against a hash and salt.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String, pepper: CharSequence) -> boolean`: Verifies a password against a hash, salt, and pepper.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[], pepper: CharSequence) -> boolean`: Verifies a byte array password against a hash, salt, and pepper.


`AlgorithmFinder.java`:

- `AlgorithmFinder`: Utility class to retrieve singleton instances of hashing algorithms configured via environment or properties file.

  - `AlgorithmFinder() -> AlgorithmFinder`: Private constructor to prevent instantiation.
  
  - `getSecureRandom() -> SecureRandom`: Returns a singleton thread-safe SecureRandom instance.
  
  - `getPBKDF2Instance() -> PBKDF2Function`: Creates or returns a configured singleton PBKDF2Function instance.
  
  - `getCompressedPBKDF2Instance() -> CompressedPBKDF2Function`: Creates or returns a configured singleton CompressedPBKDF2Function instance.
  
  - `internalGetProperties() -> Param`: internal method to read properties for PBKDF2 configuration.
  
  - `getBcryptInstance() -> BcryptFunction`: Creates or returns a configured singleton BcryptFunction instance.
  
  - `getScryptInstance() -> ScryptFunction`: Creates or returns a configured singleton ScryptFunction instance.
  
  - `getMessageDigestInstance() -> MessageDigestFunction`: Creates or returns a configured singleton MessageDigestFunction instance.
  
  - `getArgon2Instance() -> Argon2Function`: Creates or returns a configured singleton Argon2Function instance.
  
  - `getBalloonHashingInstance() -> BalloonHashingFunction`: Creates or returns a configured singleton BalloonHashingFunction instance.
  
  - `getAllPBKDF2Variants() -> List<String>`: Lists all supported PBKDF2 algorithm variants provided by the environment.
  
  - `getAllMessageDigests() -> Set<String>`: Lists all supported Message Digest algorithms.
  
  - `useStrongRandom() -> boolean`: Checks if strong random generation is configured.
  
  - `initialize() -> void`: Initializes the SecureRandom instance.


`Argon2Function.java`:

- `Argon2Function`: Implementation of the Argon2 password hashing function.

  - `Argon2Function(memory: int, iterations: int, parallelism: int, outputLength: int, variant: Argon2, version: int) -> Argon2Function`: Package-private constructor to initialize parameters and memory blocks.
  
  - `getInstance(memory: int, iterations: int, parallelism: int, outputLength: int, type: Argon2) -> Argon2Function`: Factory method for obtaining an Argon2Function instance.
  
  - `getInstance(memory: int, iterations: int, parallelism: int, outputLength: int, type: Argon2, version: int) -> Argon2Function`: Factory method with version specification.
  
  - `getInstanceFromHash(hashed: String) -> Argon2Function`: Creates an instance configured based on parameters extracted from a hash string.
  
  - `getUID(memory: int, iterations: int, parallelism: int, outputLength: int, type: Argon2, version: int) -> String`: Generates a unique identifier string for the configuration.
  
  - `getInitialHashLong(initialHash: byte[], appendix: byte[]) -> byte[]`: Helper method to construct the initial hash.
  
  - `updateWithLength(blake2b: Blake2b, input: byte[]) -> void`: Updates the Blake2b digest with input length and data.
  
  - `getStartingIndex(pass: int, slice: int) -> int`: Determines the starting index for processing.
  
  - `nextAddresses(zeroBlock: long[], inputBlock: long[], addressBlock: long[]) -> void`: Computes the next addresses for Argon2 processing.
  
  - `fillBlock(x: long[], y: long[], currentBlock: long[], withXor: boolean) -> void`: Fills a memory block using the compression function.
  
  - `roundFunction(block: long[], ...) -> void`: Performs the Argon2 round function on a block.
  
  - `f(block: long[], a: int, b: int, c: int, d: int) -> void`: Core transformation function.
  
  - `fBlaMka(block: long[], x: int, y: int) -> void`: BlaMka mixing function.
  
  - `rotr64(block: long[], v: int, w: int, c: long) -> void`: 64-bit right rotation.
  
  - `decodeHash(hash: String) -> Object[]`: Parses an Argon2 hash string to extract parameters.
  
  - `toString(memory: int, iterations: int, parallelism: int, outputLength: int, type: Argon2, version: int) -> String`: Returns a string representation of the parameters.
  
  - `remove(source: String, remove: String) -> String`: Utility to remove a prefix string.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes a password with a generated salt.
  
  - `hash(plainTextPassword: byte[]) -> Hash`: Hashes a byte array password with a generated salt.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes a password with a provided salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Hashes a byte array password with a provided salt.
  
  - `hash(plainTextPassword: CharSequence, salt: String, pepper: CharSequence) -> Hash`: Hashes a password with salt and pepper.
  
  - `hash(plainTextPassword: byte[], salt: byte[], pepper: CharSequence) -> Hash`: Hashes a byte array password with salt and pepper.
  
  - `internalHash(plainTextPassword: byte[], salt: byte[], pepper: CharSequence) -> Hash`: Internal method performing the core Argon2 hashing logic.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks a password against a hash.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks a byte array password against a hash.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String, pepper: CharSequence) -> boolean`: Checks a password against a hash with salt and pepper.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[], pepper: CharSequence) -> boolean`: Checks a byte array password against a hash with salt and pepper.
  
  - `getMemory() -> int`: Returns memory parameter.
  
  - `getIterations() -> int`: Returns iterations parameter.
  
  - `getParallelism() -> int`: Returns parallelism parameter.
  
  - `getOutputLength() -> int`: Returns output length parameter.
  
  - `getVariant() -> Argon2`: Returns the Argon2 variant.
  
  - `getVersion() -> int`: Returns the algorithm version.
  
  - `initialize(plainTextPassword: byte[], salt: byte[], secret: byte[], additional: byte[], blockMemory: long[][]) -> void`: Initializes the Argon2 memory blocks.
  
  - `blake2bLong(input: byte[], outputLength: int) -> byte[]`: Generates a Blake2b hash of arbitrary length.
  
  - `simpleBlake2b(input: byte[], outlenBytes: byte[], outputLength: int) -> byte[]`: Helper for simple Blake2b hashing.
  
  - `fillMemoryBlocks(blockMemory: long[][]) -> void`: Fills memory blocks, single or multi-threaded.
  
  - `fillMemoryBlockSingleThreaded(blockMemory: long[][]) -> void`: Single-threaded memory filling.
  
  - `fillMemoryBlockMultiThreaded(blockMemory: long[][]) -> void`: Multi-threaded memory filling.
  
  - `fillSegment(pass: int, lane: int, slice: int, blockMemory: long[][]) -> void`: Fills a segment of memory.
  
  - `isDataIndependentAddressing(pass: int, slice: int) -> boolean`: Determines if addressing should be data-independent.
  
  - `getPrevOffset(currentOffset: int) -> int`: Calculates the previous offset.
  
  - `rotatePrevOffset(currentOffset: int, prevOffset: int) -> int`: Rotates the previous offset if needed.
  
  - `getPseudoRandom(index: int, addressBlock: long[], inputBlock: long[], zeroBlock: long[], prevOffset: int, dataIndependentAddressing: boolean, blockMemory: long[][]) -> long`: Generates a pseudo-random value for memory access.
  
  - `getRefLane(pass: int, lane: int, slice: int, pseudoRandom: long) -> int`: Calculates reference lane.
  
  - `initAddressBlocks(pass: int, lane: int, slice: int, zeroBlock: long[], inputBlock: long[], addressBlock: long[], blockMemory: long[][]) -> void`: Initializes address blocks.
  
  - `getRefColumn(pass: int, slice: int, index: int, pseudoRandom: long, sameLane: boolean) -> int`: Calculates reference column.
  
  - `isWithXor(pass: int) -> boolean`: Determines if XOR should be used in the current pass.
  
  - `ending(blockMemory: long[][]) -> byte[]`: Finalizes the hash computation.
  
  - `clear(blockMemory: long[][]) -> void`: Clears sensitive data from memory.
  
  - `copyOf(old: long[][]) -> long[][]`: Copies the memory block array.
  
  - `encodeHash(hash: byte[], salt: byte[]) -> String`: Formats the hash and salt into the standard Argon2 string representation.
  
  - `equals(o: Object) -> boolean`: Checks equality based on configuration parameters.
  
  - `hashCode() -> int`: Generates hash code.
  
  - `toString() -> String`: Returns string representation.


`BadParametersException.java`:

- `BadParametersException`: Runtime exception thrown when invalid parameters are provided to a hashing function.

  - `BadParametersException(message: String) -> BadParametersException`: Constructs exception with message.
  
  - `BadParametersException(message: String, exception: Throwable) -> BadParametersException`: Constructs exception with message and cause.


`BalloonHashingFunction.java`:

- `BalloonHashingFunction`: Implementation of the Balloon password hashing function.

  - `BalloonHashingFunction(algorithm: String, spaceCost: int, timeCost: int, parallelism: int, delta: int) -> BalloonHashingFunction`: Constructor.
  
  - `getInstance(algorithm: String, spaceCost: int, timeCost: int, parallelism: int, delta: int) -> BalloonHashingFunction`: Factory method.
  
  - `getInstance(algorithm: String, spaceCost: int, timeCost: int, parallelism: int) -> BalloonHashingFunction`: Factory method with default delta.
  
  - `getUID(algorithm: String, spaceCost: int, timeCost: int, parallelism: int, delta: int) -> String`: Unique ID generation.
  
  - `toString(algorithm: String, spaceCost: int, timeCost: int, parallelism: int, delta: int) -> String`: String representation helper.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Returns null (not implemented?).
  
  - `hash(plainTextPassword: byte[]) -> Hash`: Returns null (not implemented?).
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes password with salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Hashes byte array password with salt.
  
  - `internalHash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Core Balloon hashing logic (supports parallelism).
  
  - `getMessageDigest() -> MessageDigest`: Returns the MessageDigest instance.
  
  - `balloon(messageDigest: MessageDigest, plainTextPassword: byte[], salt: byte[]) -> byte[]`: Performs balloon hashing algorithm steps.
  
  - `expand(messageDigest: MessageDigest, buffer: List<byte[]>, cnt: int) -> int`: Expand step of Balloon.
  
  - `mix(messageDigest: MessageDigest, buffer: List<byte[]>, cnt: int, salt: byte[]) -> void`: Mix step of Balloon.
  
  - `extract(buffer: List<byte[]>) -> byte[]`: Extracts final hash from buffer.
  
  - `get(buffer: List<byte[]>, position: int) -> byte[]`: Helper to access buffer safely.
  
  - `hashFunc(md: MessageDigest, args: Object...) -> byte[]`: Helper to hash concatenated arguments.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password against hash.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Checks password against hash with salt.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks byte array password against hash.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[]) -> boolean`: Checks byte array password against hash with salt.
  
  - `equals(o: Object) -> boolean`: Equality check.


`BcryptFunction.java`:

- `BcryptFunction`: Implementation of the Bcrypt password hashing function.

  - `BcryptFunction() -> BcryptFunction`: Private constructor.
  
  - `BcryptFunction(type: Bcrypt, logRounds: int) -> BcryptFunction`: Protected constructor.
  
  - `getInstance(logRounds: int) -> BcryptFunction`: Factory method.
  
  - `getInstance(type: Bcrypt, logRounds: int) -> BcryptFunction`: Factory method with type.
  
  - `getInstanceFromHash(hashed: String) -> BcryptFunction`: Creates instance from hash string configuration.
  
  - `getUID(type: Bcrypt, logRounds: int) -> String`: UID generation.
  
  - `toString(type: Bcrypt, logRounds: int) -> String`: String representation helper.
  
  - `encodeBase64(toBeEncoded: byte[], length: int, sb: StringBuilder) -> void`: Encodes bytes to custom Bcrypt Base64.
  
  - `char64(c: char) -> byte`: Decodes a Bcrypt Base64 character.
  
  - `decodeBase64(str: String, maxOLength: int) -> byte[]`: Decodes Bcrypt Base64 string.
  
  - `fromStringBuilderToBytes(sb: StringBuilder, oLength: int) -> byte[]`: Helper for StringBuilder conversion.
  
  - `streamToWords(data: byte[], offPointer: int[], signp: int[]) -> int[]`: Helper for key scheduling.
  
  - `streamToWord(data: byte[], offp: int[]) -> int`: Helper to extract word.
  
  - `streamToWordMinorX(data: byte[], offp: int[]) -> int`: Helper for specific bug compatibility.
  
  - `isNotValidMinor(minor: char) -> boolean`: Validates minor version.
  
  - `internalChecks(salt: String) -> void`: Validates salt format.
  
  - `generateSalt(prefix: String, logRounds: int) -> String`: Generates a Bcrypt salt string.
  
  - `equalsNoEarlyReturn(a: byte[], b: byte[]) -> boolean`: Constant-time comparison.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes password with generated salt.
  
  - `hash(plainTextPassword: byte[]) -> Hash`: Hashes byte array password with generated salt.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes password with provided salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Hashes byte array password with provided salt.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password against hash.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks byte array password against hash.
  
  - `internalHash(plainTextPassword: CharSequence, salt: String) -> Hash`: Internal hashing delegation.
  
  - `internalHash(plainTextPasswordAsBytes: byte[], salt: String) -> Hash`: Core Bcrypt hashing logic.
  
  - `getLogarithmicRounds() -> int`: Returns log rounds.
  
  - `getType() -> Bcrypt`: Returns Bcrypt type.
  
  - `toString() -> String`: String representation.
  
  - `hashCode() -> int`: Hash code.
  
  - `encipher(lr: int[], off: int, pArray: int[], sBox: int[]) -> void`: Blowfish enciphering step.
  
  - `feistelSubstitution(p: int, sBox: int[]) -> int`: Feistel network substitution.
  
  - `key(key: byte[], signExtBug: boolean, pArray: int[], sBox: int[]) -> void`: Keys the Blowfish cipher.
  
  - `enhancedKeySchedule(data: byte[], key: byte[], signExtBug: boolean, safety: int, pArray: int[], sBox: int[]) -> void`: Expensive key setup for Bcrypt.
  
  - `cryptRaw(password: byte[], salt: byte[], logRounds: int, sign: boolean, safety: int) -> byte[]`: Raw Bcrypt hash generation.
  
  - `equals(o: Object) -> boolean`: Equality check.
  
  - `generateSalt() -> String`: Generates salt for this instance.
  
  - `internalCheck(plainTextPasswordAsBytes: byte[], hashed: byte[]) -> boolean`: Internal verification.


`BenchmarkResult.java`:

- `BenchmarkResult`: Container for the result of a hashing benchmark, holding the best prototype configuration and execution time.

  - `BenchmarkResult(prototype: P, elapsed: long) -> BenchmarkResult`: Constructor.
  
  - `getPrototype() -> P`: Returns the configured hashing function instance.
  
  - `getElapsed() -> long`: Returns the elapsed time in milliseconds.


`Blake2b.java`:

- `Blake2b`: Implementation of the Blake2b message digest algorithm (package-private).

  - `Blake2b(digestSize: int) -> Blake2b`: Constructor specifying digest size.
  
  - `init() -> void`: Initializes the state vector.
  
  - `initializeInternalState() -> void`: Sets up internal state for processing.
  
  - `update(message: byte[]) -> void`: Updates digest with message.
  
  - `update(message: byte[], offset: int, len: int) -> void`: Updates digest with message chunk.
  
  - `doFinal(out: byte[], outOffset: int) -> void`: Finalizes the hash computation.
  
  - `reset() -> void`: Resets the digest state.
  
  - `compress(message: byte[], messagePos: int) -> void`: Compression function.
  
  - `functionG(m1: long, m2: long, posA: int, posB: int, posC: int, posD: int) -> void`: G mixing function.


`CompressedPBKDF2Function.java`:

- `CompressedPBKDF2Function`: A PBKDF2 variation that packs parameters directly into the hash string.

  - `CompressedPBKDF2Function() -> CompressedPBKDF2Function`: Protected constructor.
  
  - `CompressedPBKDF2Function(fromCode: Hmac, iterations: int, length: int) -> CompressedPBKDF2Function`: Protected constructor.
  
  - `getInstance(algorithm: Hmac, iterations: int, length: int) -> CompressedPBKDF2Function`: Factory method.
  
  - `getInstance(algorithm: String, iterations: int, length: int) -> CompressedPBKDF2Function`: Factory method using string algorithm name.
  
  - `getInstanceFromHash(hashed: String) -> CompressedPBKDF2Function`: Creates instance from hash string.
  
  - `getParts(hashed: byte[]) -> List<byte[]>`: Splits hash bytes.
  
  - `getParts(hashed: String) -> String[]`: Splits hash string.
  
  - `getHash(encodedKey: byte[], salt: byte[]) -> String`: Formats the hash output with parameters.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks byte array password.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Checks password with explicit salt (ignores salt param, extracts from hash).
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[]) -> boolean`: Checks byte array password with explicit salt.
  
  - `getSaltFromHash(hashed: byte[]) -> byte[]`: Extracts salt from the hash string.


`HashBuilder.java`:

- `HashBuilder`: Builder class to configure and execute the hashing process.

  - `HashBuilder() -> HashBuilder`: Private constructor.
  
  - `HashBuilder(plainTextPassword: CharSequence) -> HashBuilder`: Constructor with password.
  
  - `HashBuilder(plainTextPasswordAsBytes: byte[]) -> HashBuilder`: Constructor with byte array password.
  
  - `addSalt(salt: String) -> HashBuilder`: Adds a salt string.
  
  - `addSalt(saltAsBytes: byte[]) -> HashBuilder`: Adds a salt byte array.
  
  - `addRandomSalt() -> HashBuilder`: Adds a generated random salt.
  
  - `addRandomSalt(length: int) -> HashBuilder`: Adds a generated random salt of specific length.
  
  - `addPepper() -> HashBuilder`: Adds a global pepper.
  
  - `addPepper(pepper: CharSequence) -> HashBuilder`: Adds a specific pepper.
  
  - `with(hashingFunction: HashingFunction) -> Hash`: Executes hashing with provided function.
  
  - `withPBKDF2() -> Hash`: Hashes with configured PBKDF2.
  
  - `withCompressedPBKDF2() -> Hash`: Hashes with configured Compressed PBKDF2.
  
  - `withBcrypt() -> Hash`: Hashes with configured Bcrypt.
  
  - `withScrypt() -> Hash`: Hashes with configured Scrypt.
  
  - `withMessageDigest() -> Hash`: Hashes with configured MessageDigest.
  
  - `withArgon2() -> Hash`: Hashes with configured Argon2.
  
  - `withBalloonHashing() -> Hash`: Hashes with configured Balloon Hashing.


`HashChecker.java`:

- `HashChecker`: Builder class to configure and execute the verification process.

  - `HashChecker() -> HashChecker`: Private constructor.
  
  - `HashChecker(plainTextPassword: CharSequence, hashed: String) -> HashChecker`: Constructor.
  
  - `HashChecker(plainTextPassword: byte[], hashed: byte[]) -> HashChecker`: Constructor for byte arrays.
  
  - `addPepper(pepper: CharSequence) -> HashChecker`: Adds pepper for verification.
  
  - `addPepper() -> HashChecker`: Adds global pepper for verification.
  
  - `addSalt(salt: String) -> HashChecker`: Adds salt for verification (if not in hash).
  
  - `addSalt(salt: byte[]) -> HashChecker`: Adds salt bytes for verification.
  
  - `andUpdate() -> HashUpdater`: Transitions to HashUpdater for hash upgrades.
  
  - `with(hashingFunction: HashingFunction) -> boolean`: Verifies using provided function.
  
  - `withPBKDF2() -> boolean`: Verifies with PBKDF2.
  
  - `withCompressedPBKDF2() -> boolean`: Verifies with Compressed PBKDF2.
  
  - `withScrypt() -> boolean`: Verifies with Scrypt.
  
  - `withBcrypt() -> boolean`: Verifies with Bcrypt.
  
  - `withMessageDigest() -> boolean`: Verifies with MessageDigest.
  
  - `withArgon2() -> boolean`: Verifies with Argon2.
  
  - `withBalloonHashing() -> boolean`: Verifies with Balloon Hashing.
  
  - `getHashed() -> String`: Returns the hash being verified.


`HashingFunction.java`:

- `HashingFunction`: Interface defining the contract for all cryptographic hashing functions.

  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes password.
  
  - `hash(plainTextPassword: byte[]) -> Hash`: Hashes byte array password.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes password with salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Hashes byte array password with salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[], pepper: CharSequence) -> Hash`: Hashes byte array password with salt and pepper.
  
  - `hash(plainTextPassword: CharSequence, salt: String, pepper: CharSequence) -> Hash`: Hashes password with salt and pepper.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password against hash.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks byte array password against hash.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Checks password against hash with external salt.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[]) -> boolean`: Checks byte array password against hash with external salt.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String, pepper: CharSequence) -> boolean`: Checks password against hash with salt and pepper.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[], pepper: CharSequence) -> boolean`: Checks byte array password against hash with salt and pepper.


`Hash.java`:

- `Hash`: DTO holding the result of a hashing operation (hash, salt, pepper, function).

  - `Hash() -> Hash`: Private constructor.
  
  - `Hash(hashingFunction: HashingFunction, result: String, bytes: byte[], salt: String) -> Hash`: Deprecated constructor.
  
  - `Hash(hashingFunction: HashingFunction, result: String, bytes: byte[], salt: byte[]) -> Hash`: Constructor.
  
  - `Hash(hashingFunction: HashingFunction, result: byte[], bytes: byte[], salt: byte[]) -> Hash`: Constructor for byte arrays.
  
  - `areEquals(cs1: CharSequence, cs2: CharSequence) -> boolean`: Private equality check.
  
  - `getResult() -> String`: Returns hash string.
  
  - `getResultAsBytes() -> byte[]`: Returns hash bytes including parameters.
  
  - `getBytes() -> byte[]`: Returns raw hash bytes.
  
  - `getHashingFunction() -> HashingFunction`: Returns function used.
  
  - `getSalt() -> String`: Returns salt string.
  
  - `getSaltBytes() -> byte[]`: Returns salt bytes.
  
  - `getPepper() -> CharSequence`: Returns pepper.
  
  - `setPepper(pepper: CharSequence) -> void`: Sets pepper.
  
  - `toString() -> String`: String representation.


`HashUpdate.java`:

- `HashUpdate`: DTO holding the result of a verification-and-update operation.

  - `HashUpdate() -> HashUpdate`: Private constructor for UNVERIFIED.
  
  - `HashUpdate(hash: Hash) -> HashUpdate`: Constructor.
  
  - `HashUpdate(hash: Hash, updated: boolean) -> HashUpdate`: Constructor with update flag.
  
  - `getHash() -> Hash`: Returns new hash.
  
  - `isVerified() -> boolean`: Checks if verification succeeded.
  
  - `isUpdated() -> boolean`: Checks if hash was updated.


`HashUpdater.java`:

- `HashUpdater`: Helper class to handle the logic of verifying an old hash and generating a new one if parameters changed.

  - `HashUpdater(hashChecker: HashChecker, hashBuilder: HashBuilder) -> HashUpdater`: Constructor.
  
  - `with(oldHashingFunction: HashingFunction, newHashingFunction: HashingFunction) -> HashUpdate`: Performs verification with old function and hashing with new function.
  
  - `addNewSalt(salt: String) -> HashUpdater`: Adds new salt for the new hash.
  
  - `addNewSalt(saltAsBytes: byte[]) -> HashUpdater`: Adds new salt bytes for the new hash.
  
  - `addNewRandomSalt() -> HashUpdater`: Adds new random salt.
  
  - `addNewRandomSalt(length: int) -> HashUpdater`: Adds new random salt of length.
  
  - `addNewPepper() -> HashUpdater`: Adds new global pepper.
  
  - `addNewPepper(pepper: CharSequence) -> HashUpdater`: Adds new specific pepper.
  
  - `forceUpdate() -> HashUpdater`: Forces update even if params match.
  
  - `withPBKDF2() -> HashUpdate`: Updates to PBKDF2 default.
  
  - `withPBKDF2(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to PBKDF2 custom.
  
  - `withCompressedPBKDF2() -> HashUpdate`: Updates to Compressed PBKDF2 default.
  
  - `withCompressedPBKDF2(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to Compressed PBKDF2 custom.
  
  - `withBcrypt() -> HashUpdate`: Updates to Bcrypt default.
  
  - `withBcrypt(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to Bcrypt custom.
  
  - `withScrypt() -> HashUpdate`: Updates to Scrypt default.
  
  - `withScrypt(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to Scrypt custom.
  
  - `withMessageDigest() -> HashUpdate`: Updates to MessageDigest default.
  
  - `withMessageDigest(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to MessageDigest custom.
  
  - `withArgon2() -> HashUpdate`: Updates to Argon2 default.
  
  - `withArgon2(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to Argon2 custom.
  
  - `withBalloonHashing() -> HashUpdate`: Updates to Balloon default.
  
  - `withBalloonHashing(newHashingFunction: HashingFunction) -> HashUpdate`: Updates to Balloon custom.


`MessageDigestFunction.java`:

- `MessageDigestFunction`: Adapter for standard Java MessageDigest algorithms.

  - `MessageDigestFunction(algorithm: String, saltOption: SaltOption) -> MessageDigestFunction`: Constructor.
  
  - `getInstance(algorithm: String) -> MessageDigestFunction`: Factory method.
  
  - `getInstance(algorithm: String, saltOption: SaltOption) -> MessageDigestFunction`: Factory method with salt option.
  
  - `getUID(algorithm: String, saltOption: SaltOption) -> String`: UID generation.
  
  - `toString(algorithm: String, saltOption: SaltOption) -> String`: Helper for toString.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes password.
  
  - `hash(plainTextPasswordAsBytes: byte[]) -> Hash`: Hashes byte array.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes with salt.
  
  - `hash(plainTextPasswordAsBytes: byte[], saltAsBytes: byte[]) -> Hash`: Hashes with salt bytes.
  
  - `internalHash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Core hashing logic.
  
  - `getMessageDigest() -> MessageDigest`: Returns Java MessageDigest.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password.
  
  - `check(plainTextPasswordAsBytes: byte[], hashed: byte[]) -> boolean`: Checks byte array.
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Checks with salt.
  
  - `check(plainTextPassword: byte[], hashed: byte[], salt: byte[]) -> boolean`: Checks byte array with salt.
  
  - `getSaltOption() -> SaltOption`: Returns salt concatenation strategy.
  
  - `getAlgorithm() -> String`: Returns algorithm name.
  
  - `concatenateSalt(plainTextPassword: byte[], salt: byte[]) -> byte[]`: Concatenates salt based on option.
  
  - `toString() -> String`: String representation.
  
  - `equals(o: Object) -> boolean`: Equality check.
  
  - `hashCode() -> int`: Hash code.


`Password.java`:

- `Password`: Static facade entry point for hashing and checking passwords.

  - `Password() -> Password`: Private constructor.
  
  - `hash(plainTextPassword: CharSequence) -> HashBuilder`: Initiates hashing builder.
  
  - `hash(plainTextPassword: byte[]) -> HashBuilder`: Initiates hashing builder for bytes.
  
  - `check(plainTextPassword: CharSequence, hash: String) -> HashChecker`: Initiates checking builder.
  
  - `check(plainTextPassword: byte[], hash: byte[]) -> HashChecker`: Initiates checking builder for bytes.
  
  - `check(plainTextPassword: CharSequence, hashObject: Hash) -> boolean`: Verifies password against a Hash object.
  
  - `check(plainTextPassword: byte[], hashObject: Hash) -> boolean`: Verifies byte password against a Hash object.


`PBKDF2Function.java`:

- `PBKDF2Function`: Implementation of PBKDF2 (Password-Based Key Derivation Function 2).

  - `PBKDF2Function() -> PBKDF2Function`: Protected constructor.
  
  - `PBKDF2Function(iterations: int, length: int) -> PBKDF2Function`: Protected constructor.
  
  - `PBKDF2Function(algorithm: Hmac, iterations: int, length: int) -> PBKDF2Function`: Protected constructor.
  
  - `PBKDF2Function(algorithm: String, iterations: int, length: int) -> PBKDF2Function`: Protected constructor.
  
  - `getInstance(algorithm: Hmac, iterations: int, length: int) -> PBKDF2Function`: Factory method.
  
  - `getInstance(algorithm: String, iterations: int, length: int) -> PBKDF2Function`: Factory method with string alg.
  
  - `internalHash(plainTextPassword: byte[], salt: byte[], algorithm: String, iterations: int, length: int) -> SecretKey`: Core PBKDF2 generation.
  
  - `internalHash(plain: char[], salt: byte[], algorithm: String, iterations: int, length: int) -> SecretKey`: Core PBKDF2 generation using char array.
  
  - `getUID(algorithm: String, iterations: int, length: int) -> String`: UID generation.
  
  - `toString(algorithm: String, iterations: int, length: int) -> String`: String helper.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes with random salt.
  
  - `hash(plainTextPasswordAsBytes: byte[]) -> Hash`: Hashes bytes with random salt.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes with provided salt.
  
  - `hash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Hashes bytes with provided salt.
  
  - `getHash(encodedKey: byte[], salt: byte[]) -> String`: Converts hash to string (base64).
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password.
  
  - `check(plainTextPasswordAsBytes: byte[], hashed: byte[]) -> boolean`: Checks bytes (Unsupported without explicit salt).
  
  - `check(plainTextPassword: CharSequence, hashed: String, salt: String) -> boolean`: Checks with salt.
  
  - `check(plainTextPasswordAsBytes: byte[], hashed: byte[], salt: byte[]) -> boolean`: Checks bytes with salt.
  
  - `getAlgorithm() -> String`: Returns algorithm.
  
  - `getIterations() -> int`: Returns iterations.
  
  - `getLength() -> int`: Returns key length.
  
  - `equals(obj: Object) -> boolean`: Equality check.
  
  - `toString() -> String`: String representation.
  
  - `hashCode() -> int`: Hash code.


`PepperGenerator.java`:

- `PepperGenerator`: Utility class to generate or retrieve shared pepper.

  - `PepperGenerator() -> PepperGenerator`: Private constructor.
  
  - `generate(length: int) -> String`: Generates random pepper string of length.
  
  - `generate() -> String`: Generates random pepper (len 24).
  
  - `get() -> String`: Retrieves global pepper from properties.


`PropertyReader.java`:

- `PropertyReader`: Helper class to read configuration from `psw4j.properties`.

  - `PropertyReader() -> PropertyReader`: Private constructor.
  
  - `readInt(key: String, defaultValue: int, message: String) -> int`: Reads int property.
  
  - `readBoolean(key: String, defaultValue: boolean) -> boolean`: Reads boolean property.
  
  - `readString(key: String, defaultValue: String, message: String) -> String`: Reads string property.
  
  - `readChar(key: String, defaultValue: char, message: String) -> char`: Reads char property.
  
  - `readChar(key: String, defaultValue: char) -> char`: Reads char property without log.
  
  - `readString(key: String) -> String`: Internal read string.
  
  - `init() -> void`: Initializes properties loading.
  
  - `getResource(resource: String) -> InputStream`: Loads resource stream.


`SaltGenerator.java`:

- `SaltGenerator`: Utility class to generate cryptographically strong random salts.

  - `SaltGenerator() -> SaltGenerator`: Private constructor.
  
  - `generate(length: int) -> byte[]`: Generates random salt of length.
  
  - `generate() -> byte[]`: Generates random salt (default length 64).
  
  - `get() -> int`: Retrieves default salt length from properies.


`SaltOption.java`:

- `SaltOption`: Enum defining how salt should be combined with the password.
  - `PREPEND`: Prepend salt to password.
  - `APPEND`: Append salt to password.


`ScryptFunction.java`:

- `ScryptFunction`: Implementation of Scrypt password hashing function.

  - `ScryptFunction() -> ScryptFunction`: Private constructor.
  
  - `ScryptFunction(workFactor: int, resources: int, parallelization: int) -> ScryptFunction`: Protected constructor.
  
  - `ScryptFunction(workFactor: int, resources: int, parallelization: int, derivedKeyLength: int) -> ScryptFunction`: Protected constructor.
  
  - `getInstanceFromHash(hashed: String) -> ScryptFunction`: Creates instance from hash string.
  
  - `getInstance(workFactor: int, resources: int, parallelization: int) -> ScryptFunction`: Factory method.
  
  - `getInstance(workFactor: int, resources: int, parallelization: int, derivedKeyLength: int) -> ScryptFunction`: Factory method with length.
  
  - `toString(resources: int, workFactor: int, parallelization: int, derivedKeyLength: int) -> String`: Helper for toString.
  
  - `getUID(resources: int, workFactor: int, parallelization: int, derivedKeyLength: int) -> String`: UID generation.
  
  - `rOperation(a: int, b: int) -> int`: Bitwise rotation helper.
  
  - `salsa208(xArray: byte[]) -> void`: Salsa20/8 core function.
  
  - `blockXOR(sArray: byte[], si: int, dArray: byte[], di: int, length: int) -> void`: XORs two blocks.
  
  - `hash(plainTextPassword: CharSequence) -> Hash`: Hashes with random salt.
  
  - `hash(plainTextPasswordAsBytes: byte[]) -> Hash`: Hashes bytes with random salt.
  
  - `hash(plainTextPassword: CharSequence, salt: String) -> Hash`: Hashes with provided salt.
  
  - `hash(plainTextPasswordAsBytes: byte[], salt: byte[]) -> Hash`: Hashes bytes with provided salt.
  
  - `internalHash(plainTextPassword: byte[], salt: byte[]) -> Hash`: Core Scrypt hashing logic.
  
  - `check(plainTextPassword: CharSequence, hashed: String) -> boolean`: Checks password.
  
  - `check(plainTextPassword: byte[], hashed: byte[]) -> boolean`: Checks bytes.
  
  - `getRequiredBytes() -> long`: Calculates memory requirement.
  
  - `getWorkFactor() -> int`: Returns N.
  
  - `getResources() -> int`: Returns r.
  
  - `getParallelization() -> int`: Returns p.
  
  - `getDerivedKeyLength() -> int`: Returns length.
  
  - `getRequiredMemory() -> String`: Returns human readable memory requirement.
  
  - `equals(obj: Object) -> boolean`: Equality check.
  
  - `toString() -> String`: String representation.
  
  - `hashCode() -> int`: Hash code.
  
  - `scrypt(passwd: byte[], salt: byte[], dkLen: int) -> byte[]`: Raw Scrypt algorithm.
  
  - `sMix(intensiveSalt: byte[], bi: int, vArray: byte[], xyArray: byte[]) -> void`: SMix mixing function.
  
  - `blockmixSalsa8(xyArray: byte[], bi: int, yi: int) -> void`: BlockMix function.
  
  - `integerify(xyArray: byte[], xi: int) -> int`: Integerify function.


`SecureString.java`:

- `SecureString`: A CharSequence implementation that stores characters in a distinct array (not String pool) and allows clearing memory.

  - `SecureString(chars: char[]) -> SecureString`: Constructor copying chars.
  
  - `SecureString(chars: char[], eraseSource: boolean) -> SecureString`: Constructor optionally clearing source.
  
  - `SecureString(chars: char[], start: int, end: int) -> SecureString`: Constructor from subsequence.
  
  - `clear(chars: char[]) -> void`: Static helper to zero-fill array.
  
  - `length() -> int`: Returns length.
  
  - `charAt(index: int) -> char`: Returns char at index.
  
  - `subSequence(start: int, end: int) -> CharSequence`: Returns subsequence.
  
  - `clear() -> void`: Clears internal character array.
  
  - `toString() -> String`: Returns masked string to prevent leakage.
  
  - `equals(other: Object) -> boolean`: Constant-time equality check.
  
  - `hashCode() -> int`: Hash code.


`SystemChecker.java`:

- `SystemChecker`: Utility to benchmark the system and find optimal parameters or check algorithm support.

  - `SystemChecker() -> SystemChecker`: Private constructor.
  
  - `isPBKDF2Supported(algorithm: String) -> boolean`: Checks if PBKDF2 variant is supported.
  
  - `isMessageDigestSupported(algorithm: String) -> boolean`: Checks if MessageDigest algorithm is supported.
  
  - `benchmarkBcrypt(maxMilliseconds: long) -> BenchmarkResult<BcryptFunction>`: Benchmarks Bcrypt to find rounds fitting in time.
  
  - `benchmarkForArgon2(maxMilliseconds: long, memory: int, parallelism: int, outputLength: int, type: Argon2) -> BenchmarkResult<Argon2Function>`: Benchmarks Argon2.
  
  - `benchmarkPBKDF2(maxMilliseconds: long, algorithm: Hmac, length: int) -> BenchmarkResult<PBKDF2Function>`: Benchmarks PBKDF2.
  
  - `findWorkFactorForScrypt(maxMilliseconds: long, resources: int, parallelization: int) -> BenchmarkResult<ScryptFunction>`: Finds optimal N for Scrypt.
  
  - `findResourcesForScrypt(maxMilliseconds: long, workFactor: int, parallelization: int) -> BenchmarkResult<ScryptFunction>`: Finds optimal r for Scrypt.
  
  - `warmUpBcrypt() -> void`: Warms up JVM for Bcrypt.
  
  - `warmUpArgon2() -> void`: Warms up JVM for Argon2.
  
  - `warmUpPBKDF2(algorithm: Hmac, length: int) -> void`: Warms up JVM for PBKDF2.
  
  - `warmUpScrypt(workFactor: int, parallelization: int) -> void`: Warms up JVM for Scrypt.


`Utils.java`:

- `Utils`: Internal utility class for common operations like encoding, conversions, and math.

  - `Utils() -> Utils`: Private constructor.
  
  - `fromCharSequenceToBytes(charSequence: CharSequence) -> byte[]`: Converts CharSequence to bytes.
  
  - `fromStringToUnsignedInts(charSequence: String) -> int[]`: Converts String to unsigned ints.
  
  - `fromCharSequenceToBytes(charSequence: CharSequence, charset: Charset) -> byte[]`: Converts to bytes with charset.
  
  - `fromCharSequenceToChars(charSequence: CharSequence) -> char[]`: Converts to char array.
  
  - `fromBytesToChars(bytes: byte[]) -> char[]`: Converts bytes to char array.
  
  - `append(cs1: CharSequence, cs2: CharSequence) -> CharSequence`: Concatenates CharSequences securely.
  
  - `append(byteArray1: byte[], byteArray2: byte[]) -> byte[]`: Concatenates byte arrays.
  
  - `toHex(bytes: byte[]) -> String`: Converts bytes to Hex string.
  
  - `bytesToInt(bytes: byte[]) -> BigInteger`: Converts bytes to BigInteger.
  
  - `littleEndianToLong(bs: byte[], off: int) -> long`: Reads little-endian long.
  
  - `littleEndianToInt(bs: byte[], off: int) -> int`: Reads little-endian int.
  
  - `longToLittleEndian(n: long) -> byte[]`: Long to little-endian bytes.
  
  - `longToLittleEndian(n: long, bs: byte[], off: int) -> void`: Long to little-endian bytes in buffer.
  
  - `intToLittleEndian(n: int, bs: byte[], off: int) -> void`: Int to little-endian bytes in buffer.
  
  - `intToLittleEndianBytes(a: int) -> byte[]`: Int to 4 bytes.
  
  - `intToLittleEndianBytes(a: int, length: int) -> byte[]`: Int to length bytes.
  
  - `fromBytesToLongs(input: byte[]) -> long[]`: Bytes to long array.
  
  - `fromBytesToString(input: byte[]) -> String`: Bytes to String.
  
  - `littleEndianBytesToLong(b: byte[]) -> long`: Little-endian bytes to long.
  
  - `longToLittleEndianBytes(a: long) -> byte[]`: Long to 8 bytes.
  
  - `intToLong(x: int) -> long`: Int to Long conversion.
  
  - `xor(t: long[], b1: long[], b2: long[]) -> void`: XORs arrays.
  
  - `xor(t: long[], b1: long[], b2: long[], b3: long[]) -> void`: XORs 3 arrays.
  
  - `xor(t: long[], other: long[]) -> void`: XORs in place.
  
  - `log2(number: int) -> int`: Calculates log2.
  
  - `scale(initialLength: int, bytesPerChar: float) -> int`: Scales length.
  
  - `decodeBase64(src: String) -> byte[]`: Decodes Base64 string.
  
  - `encodeBase64(src: byte[]) -> String`: Encodes to Base64.
  
  - `encodeBase64(src: byte[], padding: boolean) -> String`: Encodes to Base64 with optional padding.
  
  - `decodeBase64(src: byte[]) -> byte[]`: Decodes Base64 bytes.
  
  - `encode(src: byte[], padding: boolean) -> byte[]`: Encodes to Base64 bytes.
  
  - `outLength(length: int, doPadding: boolean) -> int`: Calculates output length.
  
  - `outLength(source: byte[], length: int) -> int`: Calculates output length for decode.
  
  - `encode(src: byte[], end: int, dst: byte[], padding: boolean) -> int`: Internal encode.
  
  - `decode(src: byte[], sl: int, dst: byte[]) -> int`: Internal decode.
  
  - `getInstanceStrong() -> SecureRandom`: Gets strong SecureRandom.
  
  - `randomPrintable(count: int) -> String`: Generates random printable string.
  
  - `printBanner(printStream: PrintStream) -> void`: Prints library banner.
  
  - `split(array: byte[], delimiter: byte) -> List<byte[]>`: Splits byte array.
  
  - `createExecutorService() -> ExecutorService`: Creates thread pool.
  
  - `addShutdownHook(executorService: ExecutorService) -> void`: Adds shutdown hook.


`types/Argon2.java`:

- `Argon2`: Enum representing Argon2 variants (D, I, ID).

`types/Bcrypt.java`:

- `Bcrypt`: Enum representing Bcrypt versions (A, B, X, Y).

  - `valueOf(minor: char) -> Bcrypt`: Static lookup by char.
  - `minor() -> char`: Returns minor version char.

`types/Hmac.java`:

- `Hmac`: Enum representing HMAC algorithms (SHA1 to SHA512) and their bit lengths.

  - `Hmac(bits: int, code: int) -> Hmac`: Constructor.
  - `fromCode(code: int) -> Hmac`: Lookup by code.
  - `bits() -> int`: Returns bit length.
  - `code() -> int`: Returns internal code.
  - `toString() -> String`: Returns standard algorithm name.
