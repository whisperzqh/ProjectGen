```mermaid
classDiagram
direction BT
class AbstractHashingFunction {
  + hash(CharSequence, String, CharSequence) Hash
  + check(byte[], byte[], byte[]) boolean
  # slowEquals(byte[], byte[]) boolean
  + hash(byte[], byte[], CharSequence) Hash
  + check(CharSequence, String, String) boolean
  + check(byte[], byte[], byte[], CharSequence) boolean
  # slowEquals(CharSequence, CharSequence) boolean
  + check(CharSequence, String, String, CharSequence) boolean
  + AbstractHashingFunction() 
}
class AlgorithmFinder {
  - SecureRandom secureRandom
   Argon2Function argon2Instance
   MessageDigestFunction messageDigestInstance
   BcryptFunction bcryptInstance
   List~String~ allPBKDF2Variants
   Set~String~ allMessageDigests
   CompressedPBKDF2Function compressedPBKDF2Instance
   SecureRandom secureRandom
   BalloonHashingFunction balloonHashingInstance
   PBKDF2Function PBKDF2Instance
   ScryptFunction scryptInstance
  - useStrongRandom() boolean
  ~ initialize() void
  - internalGetProperties() Param
  - AlgorithmFinder() 
}
class Argon2 {
<<enumeration>>
  + valueOf(String) Argon2
  + values() Argon2[]
  + Argon2() 
}
class Argon2Function {
  - int iterations
  - int parallelism
  - Argon2 variant
  - int memory
  - int outputLength
  - int version
   int parallelism
   int iterations
   int version
   Argon2 variant
   int memory
   int outputLength
  + check(byte[], byte[], byte[], CharSequence) boolean
  - fBlaMka(long[], int, int) void
  - getInitialHashLong(byte[], byte[]) byte[]
  - remove(String, String) String
  # toString(int, int, int, int, Argon2, int) String
  # getUID(int, int, int, int, Argon2, int) String
  - encodeHash(byte[], byte[]) String
  - updateWithLength(Blake2b, byte[]) void
  - roundFunction(long[], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int) void
  + hash(CharSequence) Hash
  + hash(byte[], byte[], CharSequence) Hash
  - getRefColumn(int, int, int, long, boolean) int
  - internalHash(byte[], byte[], CharSequence) Hash
  - fillMemoryBlockSingleThreaded(long[][]) void
  - getStartingIndex(int, int) int
  - getRefLane(int, int, int, long) int
  - initAddressBlocks(int, int, int, long[], long[], long[], long[][]) void
  - clear(long[][]) void
  + hash(CharSequence, String, CharSequence) Hash
  - blake2bLong(byte[], int) byte[]
  - simpleBlake2b(byte[], byte[], int) byte[]
  - isWithXor(int) boolean
  + getInstanceFromHash(String) Argon2Function
  - rotr64(long[], int, int, long) void
  + getInstance(int, int, int, int, Argon2) Argon2Function
  - isDataIndependentAddressing(int, int) boolean
  + toString() String
  + hashCode() int
  + hash(CharSequence, String) Hash
  + hash(byte[], byte[]) Hash
  + hash(byte[]) Hash
  + check(CharSequence, String) boolean
  + check(byte[], byte[]) boolean
  - fillMemoryBlocks(long[][]) void
  - fillMemoryBlockMultiThreaded(long[][]) void
  - getPrevOffset(int) int
  - getPseudoRandom(int, long[], long[], long[], int, boolean, long[][]) long
  - fillBlock(long[], long[], long[], boolean) void
  + getInstance(int, int, int, int, Argon2, int) Argon2Function
  - f(long[], int, int, int, int) void
  - nextAddresses(long[], long[], long[]) void
  - fillSegment(int, int, int, long[][]) void
  - rotatePrevOffset(int, int) int
  - copyOf(long[][]) long[][]
  + equals(Object) boolean
  - initialize(byte[], byte[], byte[], byte[], long[][]) void
  + check(CharSequence, String, String, CharSequence) boolean
  - ending(long[][]) byte[]
  - decodeHash(String) Object[]
  ~ Argon2Function(int, int, int, int, Argon2, int) 
}
class BadParametersException {
  + BadParametersException(String) 
  + BadParametersException(String, Throwable) 
}
class BalloonHashingFunction {
   MessageDigest messageDigest
  + check(byte[], byte[]) boolean
  - expand(MessageDigest, List~byte[]~, int) int
  + hash(byte[], byte[]) Hash
  + equals(Object) boolean
  - extract(List~byte[]~) byte[]
  - getUID(String, int, int, int, int) String
  - balloon(MessageDigest, byte[], byte[]) byte[]
  + check(CharSequence, String) boolean
  + hash(CharSequence) Hash
  + hash(CharSequence, String) Hash
  # internalHash(byte[], byte[]) Hash
  + check(byte[], byte[], byte[]) boolean
  + toString() String
  + hash(byte[]) Hash
  - get(List~byte[]~, int) byte[]
  + getInstance(String, int, int, int, int) BalloonHashingFunction
  + getInstance(String, int, int, int) BalloonHashingFunction
  # toString(String, int, int, int, int) String
  - mix(MessageDigest, List~byte[]~, int, byte[]) void
  + check(CharSequence, String, String) boolean
  + hashCode() int
  - hashFunc(MessageDigest, Object[]) byte[]
  ~ BalloonHashingFunction(String, int, int, int, int) 
}
class Bcrypt {
<<enumeration>>
  + minor() char
  + values() Bcrypt[]
  + valueOf(char) Bcrypt?
  + valueOf(String) Bcrypt
  + Bcrypt() 
}
class BcryptFunction {
  - Bcrypt type
   int logarithmicRounds
   Bcrypt type
  + hash(CharSequence) Hash
  # decodeBase64(String, int) byte[]
  + hash(byte[], byte[]) Hash
  + getInstance(Bcrypt, int) BcryptFunction
  # streamToWord(byte[], int[]) int
  # toString(Bcrypt, int) String
  - fromStringBuilderToBytes(StringBuilder, int) byte[]
  - isNotValidMinor(char) boolean
  # char64(char) byte
  + getInstanceFromHash(String) BcryptFunction
  # generateSalt() String
  + hashCode() int
  - internalChecks(String) void
  # enhancedKeySchedule(byte[], byte[], boolean, int, int[], int[]) void
  + getInstance(int) BcryptFunction
  # key(byte[], boolean, int[], int[]) void
  # internalHash(byte[], String) Hash
  # internalCheck(byte[], byte[]) boolean
  - feistelSubstitution(int, int[]) int
  # generateSalt(String, int) String
  + hash(CharSequence, String) Hash
  + equals(Object) boolean
  + check(byte[], byte[]) boolean
  # encipher(int[], int, int[], int[]) void
  # streamToWords(byte[], int[], int[]) int[]
  # streamToWordMinorX(byte[], int[]) int
  ~ equalsNoEarlyReturn(byte[], byte[]) boolean
  + check(CharSequence, String) boolean
  # cryptRaw(byte[], byte[], int, boolean, int) byte[]
  + hash(byte[]) Hash
  - internalHash(CharSequence, String) Hash
  # getUID(Bcrypt, int) String
  # encodeBase64(byte[], int, StringBuilder) void
  + toString() String
  - BcryptFunction() 
  # BcryptFunction(Bcrypt, int) 
}
class BenchmarkResult~P~ {
  - long elapsed
  - P prototype
   long elapsed
   P prototype
  ~ BenchmarkResult(P, long) 
}
class Blake2b {
  ~ update(byte[], int, int) void
  - compress(byte[], int) void
  ~ update(byte[]) void
  ~ doFinal(byte[], int) void
  ~ reset() void
  - init() void
  - initializeInternalState() void
  - functionG(long, long, int, int, int, int) void
  ~ Blake2b(int) 
}
class CompressedPBKDF2Function {
  + check(byte[], byte[]) boolean
  + check(byte[], byte[], byte[]) boolean
  + check(CharSequence, String) boolean
  - getSaltFromHash(byte[]) byte[]
  + getInstance(String, int, int) CompressedPBKDF2Function
  + getInstance(Hmac, int, int) CompressedPBKDF2Function
  # getParts(String) String[]
  # getParts(byte[]) List~byte[]~
  # getHash(byte[], byte[]) String
  + getInstanceFromHash(String) CompressedPBKDF2Function
  + check(CharSequence, String, String) boolean
  # CompressedPBKDF2Function(Hmac, int, int) 
  # CompressedPBKDF2Function() 
}
class Hash {
  - byte[] result
  - CharSequence pepper
  - HashingFunction hashingFunction
  - byte[] salt
  - byte[] bytes
   String result
   byte[] saltBytes
   CharSequence pepper
   HashingFunction hashingFunction
   String salt
   byte[] bytes
   byte[] resultAsBytes
  - areEquals(CharSequence, CharSequence) boolean
  + toString() String
  + hashCode() int
  + equals(Object) boolean
  - hasSameValues(Hash) boolean
  + Hash(HashingFunction, String, byte[], String) 
  + Hash(HashingFunction, String, byte[], byte[]) 
  + Hash(HashingFunction, byte[], byte[], byte[]) 
  - Hash() 
}
class HashBuilder {
  + addPepper(CharSequence) HashBuilder
  + with(HashingFunction) Hash
  + addPepper() HashBuilder
  + withBcrypt() Hash
  + addRandomSalt() HashBuilder
  + withScrypt() Hash
  + addSalt(String) HashBuilder
  + addRandomSalt(int) HashBuilder
  + addSalt(byte[]) HashBuilder
  + withCompressedPBKDF2() Hash
  + withArgon2() Hash
  + withBalloonHashing() Hash
  + withMessageDigest() Hash
  + withPBKDF2() Hash
  - HashBuilder() 
  # HashBuilder(byte[]) 
  # HashBuilder(CharSequence) 
}
class HashChecker {
  # byte[] hashed
   String hashed
  + withBcrypt() boolean
  + withBalloonHashing() boolean
  + withMessageDigest() boolean
  + andUpdate() HashUpdater
  + withScrypt() boolean
  + addSalt(byte[]) HashChecker
  + withPBKDF2() boolean
  + addSalt(String) HashChecker
  + addPepper(CharSequence) HashChecker
  + withArgon2() boolean
  + with(HashingFunction) boolean
  + withCompressedPBKDF2() boolean
  + addPepper() HashChecker
  ~ HashChecker(CharSequence, String) 
  - HashChecker() 
  ~ HashChecker(byte[], byte[]) 
}
class HashUpdate {
  - Hash hash
  - boolean updated
   boolean updated
   Hash hash
   boolean verified
  + HashUpdate(Hash) 
  - HashUpdate() 
  + HashUpdate(Hash, boolean) 
}
class HashUpdater {
  + addNewRandomSalt() HashUpdater
  + withPBKDF2(HashingFunction) HashUpdate
  + addNewRandomSalt(int) HashUpdater
  + withBcrypt(HashingFunction) HashUpdate
  + withArgon2() HashUpdate
  + addNewSalt(String) HashUpdater
  + withPBKDF2() HashUpdate
  + addNewSalt(byte[]) HashUpdater
  + addNewPepper(CharSequence) HashUpdater
  + withBalloonHashing() HashUpdate
  + withMessageDigest() HashUpdate
  + withBcrypt() HashUpdate
  + withMessageDigest(HashingFunction) HashUpdate
  + withCompressedPBKDF2() HashUpdate
  + with(HashingFunction, HashingFunction) HashUpdate
  + withArgon2(HashingFunction) HashUpdate
  + withBalloonHashing(HashingFunction) HashUpdate
  + addNewPepper() HashUpdater
  + withCompressedPBKDF2(HashingFunction) HashUpdate
  + withScrypt(HashingFunction) HashUpdate
  + forceUpdate() HashUpdater
  + withScrypt() HashUpdate
  ~ HashUpdater(HashChecker, HashBuilder) 
}
class HashingFunction {
<<Interface>>
  + hash(byte[], byte[]) Hash
  + check(CharSequence, String, String) boolean
  + hash(byte[]) Hash
  + hash(byte[], byte[], CharSequence) Hash
  + hash(CharSequence, String, CharSequence) Hash
  + hash(CharSequence) Hash
  + check(byte[], byte[], byte[], CharSequence) boolean
  + check(CharSequence, String) boolean
  + check(byte[], byte[], byte[]) boolean
  + hash(CharSequence, String) Hash
  + check(byte[], byte[]) boolean
  + check(CharSequence, String, String, CharSequence) boolean
}
class Hmac {
<<enumeration>>
  + code() int
  + valueOf(String) Hmac
  + fromCode(int) Hmac?
  + bits() int
  + values() Hmac[]
  + toString() String
  - Hmac(int, int) 
}
class MessageDigestFunction {
  - SaltOption saltOption
  - String algorithm
   MessageDigest messageDigest
   SaltOption saltOption
   String algorithm
  + check(CharSequence, String) boolean
  + getInstance(String) MessageDigestFunction
  + hash(byte[]) Hash
  # internalHash(byte[], byte[]) Hash
  + check(CharSequence, String, String) boolean
  + hash(CharSequence) Hash
  + hashCode() int
  + check(byte[], byte[], byte[]) boolean
  + equals(Object) boolean
  + hash(byte[], byte[]) Hash
  + hash(CharSequence, String) Hash
  - concatenateSalt(byte[], byte[]) byte[]
  + toString() String
  + check(byte[], byte[]) boolean
  # getUID(String, SaltOption) String
  + getInstance(String, SaltOption) MessageDigestFunction
  # toString(String, SaltOption) String
  ~ MessageDigestFunction(String, SaltOption) 
}
class PBKDF2Function {
  # int length
  # Hmac algorithm
  # int iterations
   int length
   int iterations
   String algorithm
  # toString(String, int, int) String
  + check(CharSequence, String) boolean
  + equals(Object) boolean
  + getInstance(Hmac, int, int) PBKDF2Function
  + getInstance(String, int, int) PBKDF2Function
  + check(CharSequence, String, String) boolean
  + check(byte[], byte[]) boolean
  + hash(byte[]) Hash
  + hash(CharSequence) Hash
  # internalHash(char[], byte[], String, int, int) SecretKey
  + check(byte[], byte[], byte[]) boolean
  + hash(CharSequence, String) Hash
  + hash(byte[], byte[]) Hash
  + toString() String
  # internalHash(byte[], byte[], String, int, int) SecretKey
  # getUID(String, int, int) String
  # getHash(byte[], byte[]) String
  + hashCode() int
  # PBKDF2Function(int, int) 
  # PBKDF2Function() 
  # PBKDF2Function(Hmac, int, int) 
  # PBKDF2Function(String, int, int) 
}
class Param {
  ~ Param(String, int, int) 
}
class Password {
  + check(CharSequence, Hash) boolean
  + hash(byte[]) HashBuilder
  + check(byte[], byte[]) HashChecker
  + check(byte[], Hash) boolean
  + hash(CharSequence) HashBuilder
  + check(CharSequence, String) HashChecker
  - Password() 
}
class PepperGenerator {
  + generate(int) String
  + get() String
  + generate() String
  - PepperGenerator() 
}
class PropertyReader {
  - readString(String) String?
  ~ getResource(String) InputStream
  ~ readBoolean(String, boolean) boolean
  ~ init() void
  ~ readInt(String, int, String) int
  ~ readString(String, String, String) String
  ~ readChar(String, char, String) char
  ~ readChar(String, char) char
  - PropertyReader() 
}
class SaltGenerator {
  + generate() byte[]
  + get() int
  + generate(int) byte[]
  - SaltGenerator() 
}
class SaltOption {
<<enumeration>>
  + values() SaltOption[]
  + valueOf(String) SaltOption
  + SaltOption() 
}
class ScryptFunction {
  - int parallelization
  - int workFactor
  - int resources
  - int derivedKeyLength
   int workFactor
   long requiredBytes
   int derivedKeyLength
   String requiredMemory
   int resources
   int parallelization
  + integerify(byte[], int) int
  + rOperation(int, int) int
  # toString(int, int, int, int) String
  + hash(CharSequence) Hash
  + check(byte[], byte[]) boolean
  + getInstance(int, int, int, int) ScryptFunction
  # getUID(int, int, int, int) String
  + blockmixSalsa8(byte[], int, int) void
  + hash(CharSequence, String) Hash
  + salsa208(byte[]) void
  + hashCode() int
  + getInstance(int, int, int) ScryptFunction
  + scrypt(byte[], byte[], int) byte[]
  + equals(Object) boolean
  + getInstanceFromHash(String) ScryptFunction
  - internalHash(byte[], byte[]) Hash
  + blockXOR(byte[], int, byte[], int, int) void
  + hash(byte[]) Hash
  + sMix(byte[], int, byte[], byte[]) void
  + hash(byte[], byte[]) Hash
  + toString() String
  + check(CharSequence, String) boolean
  - ScryptFunction() 
  # ScryptFunction(int, int, int) 
  # ScryptFunction(int, int, int, int) 
}
class SecureString {
  - clear(char[]) void
  + equals(Object) boolean
  + hashCode() int
  + subSequence(int, int) CharSequence
  + charAt(int) char
  + clear() void
  + toString() String
  + length() int
  + SecureString(char[]) 
  + SecureString(char[], boolean) 
  + SecureString(char[], int, int) 
}
class SystemChecker {
  - warmUpScrypt(int, int) void
  + benchmarkPBKDF2(long, Hmac, int) BenchmarkResult~PBKDF2Function~
  - warmUpArgon2() void
  + findWorkFactorForScrypt(long, int, int) BenchmarkResult~ScryptFunction~
  + benchmarkForArgon2(long, int, int, int, Argon2) BenchmarkResult~Argon2Function~
  + findResourcesForScrypt(long, int, int) BenchmarkResult~ScryptFunction~
  - warmUpBcrypt() void
  - warmUpPBKDF2(Hmac, int) void
  + isPBKDF2Supported(String) boolean
  + isMessageDigestSupported(String) boolean
  + benchmarkBcrypt(long) BenchmarkResult~BcryptFunction~
  - SystemChecker() 
}
class Utils {
   SecureRandom instanceStrong
  ~ toHex(byte[]) String
  ~ bytesToInt(byte[]) BigInteger
  ~ decodeBase64(byte[]) byte[]
  ~ longToLittleEndian(long, byte[], int) void
  - decode(byte[], int, byte[]) int
  ~ intToLittleEndianBytes(int, int) byte[]
  ~ littleEndianBytesToLong(byte[]) long
  ~ encodeBase64(byte[]) String
  ~ longToLittleEndian(long) byte[]
  ~ xor(long[], long[], long[], long[]) void
  - encode(byte[], int, byte[], boolean) int
  ~ append(CharSequence, CharSequence) CharSequence
  ~ fromBytesToLongs(byte[]) long[]
  ~ encodeBase64(byte[], boolean) String
  ~ littleEndianToLong(byte[], int) long
  ~ decodeBase64(String) byte[]
  ~ append(byte[], byte[]) byte[]
  ~ intToLittleEndianBytes(int) byte[]
  ~ intToLittleEndian(int, byte[], int) void
  ~ longToLittleEndianBytes(long) byte[]
  ~ xor(long[], long[]) void
  ~ intToLong(int) long
  ~ log2(int) int
  - outLength(byte[], int) int
  ~ createExecutorService() ExecutorService
  - scale(int, float) int
  ~ fromCharSequenceToBytes(CharSequence) byte[]
  ~ fromBytesToString(byte[]) String
  ~ xor(long[], long[], long[]) void
  ~ fromStringToUnsignedInts(String) int[]
  ~ fromCharSequenceToChars(CharSequence) char[]
  ~ randomPrintable(int) String
  ~ encode(byte[], boolean) byte[]
  ~ fromCharSequenceToBytes(CharSequence, Charset) byte[]
  ~ littleEndianToInt(byte[], int) int
  ~ split(byte[], byte) List~byte[]~
  ~ printBanner(PrintStream) void
  - outLength(int, boolean) int
  ~ fromBytesToChars(byte[]) char[]
  ~ addShutdownHook(ExecutorService) void
  - Utils() 
}

AlgorithmFinder  -->  Param 
```