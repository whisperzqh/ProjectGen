# Architecture Design

Below is a text-based representation of the file tree.

```bash
src
    ├── main
    │   ├── java
    │       └── com
    │           └── github
    │               └── davidmoten
    │                   └── geo
    │                       ├── Base32.java
    │                       ├── Coverage.java
    │                       ├── CoverageLongs.java
    │                       ├── Direction.java
    │                       ├── GeoHash.java
    │                       ├── LatLong.java
    │                       ├── package-info.java
    │                       ├── Parity.java
    │                       └── util
    │                           └── Preconditions.java

```

## `src/main/java/com/github/davidmoten/geo/Base32.java`

- `Base32`: Conversion methods between long values and geohash-style base 32 encoding
    - `encodeBase32(long i, int length)`: Returns the base 32 encoding of the given length from a Long geohash
    - `encodeBase32(long i)`: Returns the base 32 encoding of length `GeoHash.MAX_HASH_LENGTH` from a Long geohash
    - `decodeBase32(String hash)`: Returns the conversion of a base32 geohash to a long
    - `getCharIndex(char ch)`: Returns the index in the digits array of the character ch
    - `padLeftWithZerosToLength(String s, int length)`: Pad left with zeros to desired string length

## `src/main/java/com/github/davidmoten/geo/Coverage.java`

- `Coverage`: A set of hashes and a measure of how well those hashes cover a region
    - `Coverage(Set<String> hashes, double ratio)`: Constructs a coverage with a set of hashes and the ratio of area of hashes to the area of target region
    - `Coverage(CoverageLongs coverage)`: Constructs a coverage from a `CoverageLongs` object by converting the long representations of hashes into their string equivalents
    - `getHashes()`: Returns the hashes which are expected to be all of the same length
    - `getRatio()`: Returns the measure of how well the hashes cover a region
    - `getHashLength()`: Returns the length in characters of the first hash returned by an iterator on the hash set
    - `toString()`: Returns a string representation of the `Coverage` object containing the hashes and the ratio

## `src/main/java/com/github/davidmoten/geo/CoverageLongs.java`

- `CoverageLongs`: A set of hashes represented by longs and a measure of how well those hashes cover a region
    - `CoverageLongs(long[] hashes, int count, double ratio)`: Constructs a coverage with a set of hashes comprising the coverage, the count of hashes, and the ratio of area of hashes to the area of target region
    - `getHashes()`: Returns the hashes which are expected to be all of the same length
    - `getRatio()`: Returns the measure of how well the hashes cover a region
    - `getHashLength()`: Returns the length in characters of the first hash in the set
    - `toString()`: Returns a string representation of the `Coverage` object containing the hashes and the ratio
    - `getCount()`: Returns the count of hashes in the coverage

## `src/main/java/com/github/davidmoten/geo/Direction.java`

- `Direction`: Directions on a WGS84 projection
    - `opposite()`: Returns the opposite direction

## `src/main/java/com/github/davidmoten/geo/GeoHash.java`

- `GeoHash`: Utility functions for geohashing
    - `adjacentHash(String hash, Direction direction)`: Returns the adjacent hash in given Direction
    - `right(String hash)`: Returns the adjacent hash to the right (east)
    - `left(String hash)`: Returns the adjacent hash to the left (west)
    - `top(String hash)`: Returns the adjacent hash to the top (north)
    - `bottom(String hash)`: Returns the adjacent hash to the bottom (south)
    - `adjacentHash(String hash, Direction direction, int steps)`: Returns the adjacent hash N steps in the given Direction
    - `neighbours(String hash)`: Returns a list of the 8 surrounding hashes for a given hash in order left, right, top, bottom, left-top, left-bottom, right-top, right-bottom
    - `encodeHash(double latitude, double longitude)`: Returns a geohash of length 12 for the given WGS84 point
    - `encodeHash(LatLong p, int length)`: Returns a geohash of given length for the given WGS84 point
    - `encodeHash(LatLong p)`: Returns a geohash of length 12 for the given WGS84 point
    - `encodeHash(double latitude, double longitude, int length)`: Returns a geohash of given length for the given WGS84 point (latitude, longitude)
    - `fromLongToString(long hash)`: Takes a hash represented as a long and returns it as a string
    - `encodeHashToLong(double latitude, double longitude, int length)`: Encodes a coordinate and length into a long representation
    - `decodeHash(String geohash)`: Returns a latitude, longitude pair as the centre of the given geohash
    - `hashLengthToCoverBoundingBox(double topLeftLat, double topLeftLon, double bottomRightLat, double bottomRightLon)`: Returns the maximum length of hash that covers the bounding box
    - `hashContains(String hash, double lat, double lon)`: Returns true if and only if the bounding box corresponding to the hash contains the given lat and long
    - `coverBoundingBox(double topLeftLat, double topLeftLon, double bottomRightLat, double bottomRightLon)`: Returns the coverage with a default maximum number of hashes
    - `coverBoundingBoxMaxHashes(double topLeftLat, double topLeftLon, double bottomRightLat, double bottomRightLon, int maxHashes)`: Returns the hashes that are required to cover the given bounding box, constrained by a maximum number of hashes
    - `coverBoundingBox(double topLeftLat, double topLeftLon, double bottomRightLat, double bottomRightLon, int length)`: Returns the hashes of given length that are required to cover the given bounding box
    - `coverBoundingBoxLongs(double topLeftLat, double topLeftLon, double bottomRightLat, double bottomRightLon, int length)`: Returns the coverage in long representation for a bounding box and fixed hash length
    - `heightDegrees(int n)`: Returns height in degrees of all geohashes of length `n`
    - `widthDegrees(int n)`: Returns width in degrees of all geohashes of length `n`
    - `gridAsString(String hash, int size, Set<String> highlightThese)`: Returns a String of lines of hashes to represent the relative positions of hashes on a map centred around the given hash
    - `gridAsString(String hash, int fromRight, int fromBottom, int toRight, int toBottom)`: Returns a String of lines of hashes to represent the relative positions of hashes on a map defined by relative offsets
    - `gridAsString(String hash, int fromRight, int fromBottom, int toRight, int toBottom, Set<String> highlightThese)`: Returns a String of lines of hashes to represent the relative positions of hashes on a map with specific hashes highlighted

## `src/main/java/com/github/davidmoten/geo/LatLong.java`

- `LatLong`: A lat, long pair (WGS84). Immutable
    - `LatLong(double lat, double lon)`: Constructor
    - `getLat()`: Returns the latitude in decimal degrees
    - `getLon()`: Returns the longitude in decimal degrees
    - `add(double deltaLat, double deltaLon)`: Returns a new `LatLong` object with lat, lon increased by deltaLat, deltaLon
    - `toString()`: Returns a string representation of the LatLong object
    - `equals(Object o)`: Checks if this LatLong is equal to another object
    - `hashCode()`: Returns a hash code value for the object

## `src/main/java/com/github/davidmoten/geo/package-info.java`

## `src/main/java/com/github/davidmoten/geo/Parity.java`

- `Parity`: Even or Odd

## `src/main/java/com/github/davidmoten/geo/util/Preconditions.java`

- `Preconditions`: Guava like Preconditions
    - `checkArgument(boolean expression, Object errorMessage)`: Ensures the truth of an expression involving one or more parameters to the calling method
    - `checkNotNull(T reference, Object errorMessage)`: Ensures that an object reference passed as a parameter to the calling method is not null

