# Architecture Design

Below is a text-based representation of the file tree.
```bash
src
    ├── main
    │   └── java
    │       └── ch
    │           └── hsr
    │               └── geohash
    │                   ├── BoundingBox.java
    │                   ├── GeoHash.java
    │                   ├── queries
    │                   │   ├── GeoHashBoundingBoxQuery.java
    │                   │   ├── GeoHashCircleQuery.java
    │                   │   └── GeoHashQuery.java
    │                   ├── util
    │                   │   ├── BoundingBoxGeoHashIterator.java
    │                   │   ├── BoundingBoxSampler.java
    │                   │   ├── DoubleUtil.java
    │                   │   ├── GeoHashSizeTable.java
    │                   │   ├── LongUtil.java
    │                   │   ├── TwoGeoHashBoundingBox.java
    │                   │   └── VincentyGeodesy.java
    │                   └── WGS84Point.java
```

`BoundingBox.java`:

- `BoundingBox`: Represents a geographic bounding box defined by latitude and longitude boundaries, with support for boxes that cross the 180-degree meridian.

  - `BoundingBox(southWestCorner: WGS84Point, northEastCorner: WGS84Point) -> BoundingBox`: Creates a bounding box from two corner points.

  - `BoundingBox(southLatitude: double, northLatitude: double, westLongitude: double, eastLongitude: double) -> BoundingBox`: Creates a bounding box with explicit latitude and longitude coordinates, validates ranges and throws IllegalArgumentException for invalid values.

  - `BoundingBox(that: BoundingBox) -> BoundingBox`: Clone constructor that copies all values from another BoundingBox.

  - `getNorthWestCorner() -> WGS84Point`: Returns the northwest corner point of the bounding box.

  - `getNorthEastCorner() -> WGS84Point`: Returns the northeast corner point of the bounding box.

  - `getSouthEastCorner() -> WGS84Point`: Returns the southeast corner point of the bounding box.

  - `getSouthWestCorner() -> WGS84Point`: Returns the southwest corner point of the bounding box.

  - `getLatitudeSize() -> double`: Returns the height of the bounding box in degrees of latitude.

  - `getLongitudeSize() -> double`: Returns the width of the bounding box in degrees of longitude, handling 180-meridian crossing cases.

  - `equals(obj: Object) -> boolean`: Compares two BoundingBox instances for equality based on all coordinate values.

  - `hashCode() -> int`: Generates hash code based on all four boundary coordinates.

  - `hashCode(x: double) -> int`: Static helper method that computes hash code for a double value.

  - `contains(point: WGS84Point) -> boolean`: Checks if a given point lies within this bounding box.

  - `intersects(other: BoundingBox) -> boolean`: Checks if this bounding box intersects with another bounding box, handles 180-meridian crossing scenarios.

  - `toString() -> String`: Returns a string representation showing northwest to southeast corners.

  - `getCenter() -> WGS84Point`: Calculates and returns the center point of the bounding box, adjusting for 180-meridian crossing.

  - `expandToInclude(point: WGS84Point) -> void`: Expands the bounding box to include the given point by extending in the direction with minimal distance.

  - `expandToInclude(other: BoundingBox) -> void`: Expands the bounding box to include another bounding box, handling overlapping and global spanning cases.

  - `containsLatitude(latitude: double) -> boolean`: Private method checking if a latitude value falls within the box's latitude range.

  - `containsLongitude(longitude: double) -> boolean`: Private method checking if a longitude value falls within the box's longitude range, considering 180-meridian crossing.

  - `getEastLongitude() -> double`: Returns the eastern boundary longitude.

  - `getWestLongitude() -> double`: Returns the western boundary longitude.

  - `getNorthLatitude() -> double`: Returns the northern boundary latitude.

  - `getSouthLatitude() -> double`: Returns the southern boundary latitude.

  - `intersects180Meridian() -> boolean`: Returns whether this bounding box crosses the 180-degree meridian.

---

`GeoHash.java`:

- `GeoHash`: Represents a geohash encoding of a geographic coordinate with configurable precision, supporting conversion to/from base32 strings and binary representations.

  - `GeoHash() -> GeoHash`: Protected default constructor for internal use.

  - `withCharacterPrecision(latitude: double, longitude: double, numberOfCharacters: int) -> GeoHash`: Static factory method creating a GeoHash with the specified character precision (max 12 characters).

  - `withBitPrecision(latitude: double, longitude: double, numberOfBits: int) -> GeoHash`: Static factory method creating a GeoHash with the specified bit precision (max 64 bits).

  - `fromBinaryString(binaryString: String) -> GeoHash`: Static factory method creating a GeoHash from a binary string representation.

  - `fromGeohashString(geohash: String) -> GeoHash`: Static factory method decoding a base32-encoded geohash string and computing bounding box.

  - `fromLongValue(hashVal: long, significantBits: int) -> GeoHash`: Static factory method creating a GeoHash from a long value with specified precision.

  - `geoHashStringWithCharacterPrecision(latitude: double, longitude: double, numberOfCharacters: int) -> String`: Static method generating a base32 geohash string with specified character precision.

  - `GeoHash(latitude: double, longitude: double, desiredPrecision: int) -> GeoHash`: Private constructor encoding coordinates into geohash with specified bit precision.

  - `setBoundingBox(hash: GeoHash, latitudeRange: double[], longitudeRange: double[]) -> void`: Static helper method setting the bounding box for a GeoHash based on latitude and longitude ranges.

  - `next(step: int) -> GeoHash`: Returns a GeoHash that is the specified number of steps ahead in the geohash space.

  - `next() -> GeoHash`: Returns the next GeoHash in the geohash space.

  - `prev() -> GeoHash`: Returns the previous GeoHash in the geohash space.

  - `ord() -> long`: Returns the ordinal value of this GeoHash, representing its position in the geohash space.

  - `getCharacterPrecision() -> int`: Returns the number of base32 characters representing this hash, throws IllegalStateException if precision is not divisible by 5.

  - `fromOrd(ord: long, significantBits: int) -> GeoHash`: Static factory method creating a GeoHash from an ordinal value.

  - `stepsBetween(one: GeoHash, two: GeoHash) -> long`: Static method calculating the number of steps between two GeoHash instances with same precision.

  - `divideRangeEncode(value: double, range: double[]) -> void`: Private method dividing a range during encoding, adding bits to the hash.

  - `divideRangeDecode(hash: GeoHash, range: double[], b: boolean) -> void`: Static helper method dividing a range during decoding.

  - `getAdjacent() -> GeoHash[]`: Returns an array of 8 adjacent geohashes in order: N, NE, E, SE, S, SW, W, NW.

  - `significantBits() -> int`: Returns the number of significant bits in this GeoHash.

  - `longValue() -> long`: Returns the raw bit representation as a long value.

  - `toBase32() -> String`: Converts the GeoHash to its base32 string representation, throws IllegalStateException if precision is not divisible by 5.

  - `within(boundingBox: GeoHash) -> boolean`: Checks if this GeoHash is within the specified bounding box GeoHash.

  - `contains(point: WGS84Point) -> boolean`: Checks if the given point lies within this GeoHash's bounding box.

  - `getOriginatingPoint() -> WGS84Point`: Returns the original point used to create this GeoHash, or the center if created from a string.

  - `getBoundingBoxCenter() -> WGS84Point`: Returns the center point of this GeoHash's bounding box.

  - `getBoundingBox() -> BoundingBox`: Returns the bounding box associated with this GeoHash.

  - `enclosesCircleAroundPoint(point: WGS84Point, radius: double) -> boolean`: Currently returns false, intended to check if a circle is enclosed by this GeoHash.

  - `recombineLatLonBitsToHash(latBits: long[], lonBits: long[]) -> GeoHash`: Protected method reconstructing a GeoHash from separated latitude and longitude bit arrays.

  - `getNorthernNeighbour() -> GeoHash`: Returns the geographically adjacent GeoHash to the north.

  - `getSouthernNeighbour() -> GeoHash`: Returns the geographically adjacent GeoHash to the south.

  - `getEasternNeighbour() -> GeoHash`: Returns the geographically adjacent GeoHash to the east.

  - `getWesternNeighbour() -> GeoHash`: Returns the geographically adjacent GeoHash to the west.

  - `getRightAlignedLatitudeBits() -> long[]`: Protected method extracting latitude bits as a right-aligned value with bit count.

  - `getRightAlignedLongitudeBits() -> long[]`: Protected method extracting longitude bits as a right-aligned value with bit count.

  - `extractEverySecondBit(copyOfBits: long, numberOfBits: int) -> long`: Private method extracting alternating bits from a long value.

  - `getNumberOfLatLonBits() -> int[]`: Protected method returning the number of latitude and longitude bits in this GeoHash.

  - `addOnBitToEnd() -> void`: Protected method appending a 1 bit to the end of the hash.

  - `addOffBitToEnd() -> void`: Protected method appending a 0 bit to the end of the hash.

  - `toString() -> String`: Returns a string representation including binary, bounding box, and base32 (if applicable).

  - `padLeft(s: String, n: int, pad: String) -> String`: Static helper method padding a string to specified length.

  - `toBinaryString() -> String`: Returns the binary string representation of the significant bits.

  - `equals(obj: Object) -> boolean`: Compares GeoHash instances based on bits and significant bit count.

  - `hashCode() -> int`: Generates hash code from bits and significant bit count.

  - `mask() -> long`: Private method creating a mask for the significant bits.

  - `maskLastNBits(value: long, n: long) -> long`: Private method masking to keep only the last n bits.

  - `compareTo(o: GeoHash) -> int`: Compares GeoHash instances for ordering based on bits and precision.

---

`WGS84Point.java`:

- `WGS84Point`: Immutable representation of a geographic coordinate point using WGS84 coordinate system.

  - `WGS84Point(latitude: double, longitude: double) -> WGS84Point`: Creates a point with the given latitude and longitude, validates ranges and throws IllegalArgumentException for out-of-range coordinates.

  - `WGS84Point(other: WGS84Point) -> WGS84Point`: Copy constructor creating a new point from an existing point.

  - `getLatitude() -> double`: Returns the latitude value of this point.

  - `getLongitude() -> double`: Returns the longitude value of this point.

  - `toString() -> String`: Returns a formatted string representation of the point as "(latitude,longitude)".

  - `equals(obj: Object) -> boolean`: Compares two WGS84Point instances for equality based on coordinate values.

  - `hashCode() -> int`: Generates hash code based on latitude and longitude values.

---

`queries/GeoHashBoundingBoxQuery.java`:

- `GeoHashBoundingBoxQuery`: Query implementation that finds all geohashes covering a bounding box, handling 180-meridian crossing and returning 1, 2, or 4 covering hashes.

  - `GeoHashBoundingBoxQuery(bbox: BoundingBox) -> GeoHashBoundingBoxQuery`: Creates a query for the given bounding box, splitting into multiple queries if it crosses the 180-meridian.

  - `generateSearchHashes(bbox: BoundingBox) -> void`: Private method generating geohashes that cover the specified bounding box.

  - `expandSearch(centerHash: GeoHash, bbox: BoundingBox) -> void`: Private method expanding search to include adjacent hashes that intersect the bounding box.

  - `hashContainsBoundingBox(hash: GeoHash, bbox: BoundingBox) -> boolean`: Private method checking if a geohash completely contains a bounding box.

  - `contains(hash: GeoHash) -> boolean`: Checks if the given geohash falls within any of the search hashes.

  - `contains(point: WGS84Point) -> boolean`: Checks if the given point is contained within the query area.

  - `getSearchHashes() -> List<GeoHash>`: Returns the list of geohashes required to cover the query area.

  - `toString() -> String`: Returns a string representation of all search hashes.

  - `getWktBox() -> String`: Returns a Well-Known Text (WKT) BOX representation of the combined bounding box.

---

`queries/GeoHashCircleQuery.java`:

- `GeoHashCircleQuery`: Query implementation for radius-based searches around a center point, approximating the circle with a square bounding box.

  - `GeoHashCircleQuery(center: WGS84Point, radius: double) -> GeoHashCircleQuery`: Creates a circle query with specified center point and radius in meters, internally delegates to a bounding box query.

  - `contains(hash: GeoHash) -> boolean`: Checks if the given geohash is contained within the approximated circle area.

  - `getWktBox() -> String`: Returns the WKT BOX representation of the underlying bounding box query.

  - `getSearchHashes() -> List<GeoHash>`: Returns the list of geohashes covering the circle area.

  - `toString() -> String`: Returns a string representation showing center point and radius.

  - `getRadiusString() -> String`: Private method formatting radius as kilometers if over 1000m, otherwise meters.

  - `contains(point: WGS84Point) -> boolean`: Checks if the given point falls within the circle query area.

---

`queries/GeoHashQuery.java`:

- `GeoHashQuery`: Interface defining the contract for geohash-based spatial queries.

  - `contains(hash: GeoHash) -> boolean`: Checks whether a geohash is within the hashes that make up this query.

  - `contains(point: WGS84Point) -> boolean`: Checks whether a point lies within the query area.

  - `getSearchHashes() -> List<GeoHash>`: Returns the hashes required to perform this search.

  - `getWktBox() -> String`: Returns a Well-Known Text representation of the query area.

---

`util/BoundingBoxGeoHashIterator.java`:

- `BoundingBoxGeoHashIterator`: Iterator implementation that traverses all geohashes within a bounding box at a specific resolution.

  - `BoundingBoxGeoHashIterator(bbox: TwoGeoHashBoundingBox) -> BoundingBoxGeoHashIterator`: Creates an iterator starting from the southwest corner of the bounding box.

  - `getBoundingBox() -> TwoGeoHashBoundingBox`: Returns the bounding box being iterated over.

  - `hasNext() -> boolean`: Checks if there are more geohashes to iterate.

  - `next() -> GeoHash`: Returns the next geohash in the iteration, skipping hashes outside the bounding box, throws NoSuchElementException if no more elements.

  - `remove() -> void`: Throws UnsupportedOperationException as removal is not supported.

---

`util/BoundingBoxSampler.java`:

- `BoundingBoxSampler`: Provides random sampling of geohashes within a bounding box without replacement.

  - `BoundingBoxSampler(bbox: TwoGeoHashBoundingBox) -> BoundingBoxSampler`: Creates a sampler for the given bounding box, throws IllegalArgumentException if the bounding box contains more than Integer.MAX_VALUE geohashes.

  - `BoundingBoxSampler(bbox: TwoGeoHashBoundingBox, seed: long) -> BoundingBoxSampler`: Creates a sampler with a specific random seed for reproducible sampling.

  - `getBoundingBox() -> TwoGeoHashBoundingBox`: Returns the bounding box being sampled.

  - `next() -> GeoHash`: Returns the next random sample, or null if all samples have been returned, recursively retries if sampled hash is outside bounding box.

---

`util/DoubleUtil.java`:

- `DoubleUtil`: Utility class for double arithmetic operations with cross-version Java compatibility.

  - `remainderWithFix(value: double, remainder: int) -> double`: Static method computing the remainder operation consistently across all Java versions, handling negative results by adding the divisor.

---

`util/GeoHashSizeTable.java`:

- `GeoHashSizeTable`: Lookup table for geohash size calculations, providing methods to determine appropriate precision levels.

  - `dLat(bits: int) -> double`: Protected static method calculating the latitude size in degrees for a given number of bits.

  - `dLon(bits: int) -> double`: Protected static method calculating the longitude size in degrees for a given number of bits.

  - `numberOfBitsForOverlappingGeoHash(boundingBox: BoundingBox) -> int`: Static method determining the maximum number of bits such that a single geohash can overlap the given bounding box.

---

`util/LongUtil.java`:

- `LongUtil`: Utility class for bit manipulation operations on long values.

  - `commonPrefixLength(a: long, b: long) -> int`: Static method calculating the number of leading common bits between two long values.

---

`util/TwoGeoHashBoundingBox.java`:

- `TwoGeoHashBoundingBox`: Represents a bounding box defined by two geohash corner points with the same precision, used for iteration and sampling operations.

  - `withCharacterPrecision(bbox: BoundingBox, numberOfCharacters: int) -> TwoGeoHashBoundingBox`: Static factory method creating a TwoGeoHashBoundingBox with specified character precision.

  - `withBitPrecision(bbox: BoundingBox, numberOfBits: int) -> TwoGeoHashBoundingBox`: Static factory method creating a TwoGeoHashBoundingBox with specified bit precision.

  - `TwoGeoHashBoundingBox(southWestCorner: GeoHash, northEastCorner: GeoHash) -> TwoGeoHashBoundingBox`: Creates a bounding box from two corner geohashes, throws IllegalArgumentException if precisions differ.

  - `getBoundingBox() -> BoundingBox`: Returns the geographic bounding box represented by the two corner geohashes.

  - `getSouthWestCorner() -> GeoHash`: Returns the southwest corner geohash.

  - `getNorthEastCorner() -> GeoHash`: Returns the northeast corner geohash.

  - `toBase32() -> String`: Returns the base32 representation concatenating both corner geohashes.

---

`util/VincentyGeodesy.java`:

- `VincentyGeodesy`: Implements Vincenty's geodesy algorithms for accurate distance and bearing calculations on the WGS84 ellipsoid.

  - `moveInDirection(point: WGS84Point, bearingInDegrees: double, distanceInMeters: double) -> WGS84Point`: Static method calculating the destination point from a starting point, bearing (0-360 degrees), and distance in meters, throws IllegalArgumentException for invalid bearing values.

  - `distanceInMeters(foo: WGS84Point, bar: WGS84Point) -> double`: Static method calculating the distance in meters between two points using Vincenty's inverse formula, returns NaN if calculation does not converge.
