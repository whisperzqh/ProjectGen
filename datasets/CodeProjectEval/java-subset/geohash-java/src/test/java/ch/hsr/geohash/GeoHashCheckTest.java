/*
 * Copyright 2010, Silvio Heuberger @ IFS www.ifs.hsr.ch
 *
 * This code is release under the Apache License 2.0.
 * You should have received a copy of the license
 * in the LICENSE file. If you have not, see
 * http://www.apache.org/licenses/LICENSE-2.0
 */
package ch.hsr.geohash;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.lang.reflect.Method;

import org.junit.Before;
import org.junit.Test;

import ch.hsr.geohash.util.BoundingBoxGeoHashIterator;
import ch.hsr.geohash.util.RandomGeohashes;
import ch.hsr.geohash.util.TwoGeoHashBoundingBox;

public class GeoHashCheckTest {
	private GeoHash hash;

	@Before
	public void setUp() {
		hash = new GeoHash();
	}

	@Test
	public void testAddingOnes() {
		hash.addOnBitToEnd();
		assertEquals(0x1l, hash.bits);
		assertEquals(1, hash.significantBits());
		hash.addOnBitToEnd();
		hash.addOnBitToEnd();
		hash.addOnBitToEnd();
		assertEquals(0xfl, hash.bits);
		assertEquals(4, hash.significantBits());
	}


	@Test
	public void testDecode() {
		// for all lat/lon pairs check decoded point is in the same bbox as the
		// geohash formed by encoder
		for (GeoHash gh : RandomGeohashes.fullRange()) {
			BoundingBox bbox = gh.getBoundingBox();
			GeoHash decodedHash = GeoHash.fromGeohashString(gh.toBase32());
			WGS84Point decodedCenter = decodedHash.getBoundingBoxCenter();

			assertTrue("bbox " + bbox + " should contain the decoded center value " + decodedCenter, bbox
					.contains(decodedCenter));
			BoundingBox decodedBoundingBox = decodedHash.getBoundingBox();
			assertEquals(bbox, decodedBoundingBox);
			assertEquals(gh, decodedHash);
			assertEquals(gh.toBase32(), decodedHash.toBase32());
		}
	}


	private void assertWithin(GeoHash hash, GeoHash bbox) {
		assertTrue(hash + " should be within " + bbox, hash.within(bbox));
	}

	@Test
	public void itShouldCreateAHashWithMinimumPrecisionOf0Bits() {
		GeoHash geoHash = GeoHash.withBitPrecision(10.0, 10.0, 0);
		assertEquals(0, geoHash.significantBits());
		assertEquals(0, geoHash.longValue());
		assertEquals(new WGS84Point(10.0, 10.0), geoHash.getOriginatingPoint());
	}


	private void assertEncodingWithCharacterPrecision(WGS84Point point, int numberOfCharacters, String stringValue) {
		GeoHash hash = GeoHash.withCharacterPrecision(point.getLatitude(), point.getLongitude(), numberOfCharacters);
		assertEquals(stringValue, hash.toBase32());
	}

	@Test
	public void testGetLatitudeBits() {
		hash = GeoHash.withBitPrecision(30, 30, 16);
		long[] latitudeBits = hash.getRightAlignedLatitudeBits();
		assertEquals(0xaal, latitudeBits[0]);
		assertEquals(8, latitudeBits[1]);
	}


	private void checkMovingInCircle(double latitude, double longitude) {
		GeoHash start;
		GeoHash end;
		start = GeoHash.withCharacterPrecision(latitude, longitude, 12);
		end = start.getEasternNeighbour();
		end = end.getSouthernNeighbour();
		end = end.getWesternNeighbour();
		end = end.getNorthernNeighbour();
		assertEquals(start, end);
		assertEquals(start.getBoundingBox(), end.getBoundingBox());
	}


	private void checkMoveAroundStrip(String direction) throws Exception {
		for (int bits = 2; bits < 16; bits++) {

			GeoHash hash = RandomGeohashes.createWithPrecision(bits);
			Method method = hash.getClass().getDeclaredMethod("get" + direction + "Neighbour");
			GeoHash result = hash;

			// moving this direction 2^bits times should yield the same hash
			// again
			for (int i = 0; i < Math.pow(2, bits); i++) {
				result = (GeoHash) method.invoke(result);
			}
			assertEquals(hash, result);
		}
	}


	private void assertAdjacentHashesAre(String centerString, String[] adjacentStrings) {
		GeoHash center = GeoHash.fromGeohashString(centerString);
		GeoHash[] adjacent = center.getAdjacent();
		for (String check : adjacentStrings) {
			assertArrayContainsGeoHash(check, adjacent);
		}
	}

	private void assertArrayContainsGeoHash(String check, GeoHash[] hashes) {
		boolean found = false;
		for (GeoHash hash : hashes) {
			if (hash.toBase32().equals(check)) {
				found = true;
				break;
			}
		}
		assertTrue("Array should contain " + check, found);
	}

	private void printBoundingBox(GeoHash hash) {
		System.out.println("Bounding Box: \ncenter =" + hash.getBoundingBoxCenter());
		System.out.print("corners=");
		System.out.println(hash.getBoundingBox());
	}


}
