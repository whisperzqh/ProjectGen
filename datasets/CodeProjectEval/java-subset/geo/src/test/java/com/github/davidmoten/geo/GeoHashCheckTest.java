package com.github.davidmoten.geo;

import static com.github.davidmoten.geo.GeoHash.adjacentHash;
import static com.github.davidmoten.geo.GeoHash.bottom;
import static com.github.davidmoten.geo.GeoHash.coverBoundingBox;
import static com.github.davidmoten.geo.GeoHash.coverBoundingBoxMaxHashes;
import static com.github.davidmoten.geo.GeoHash.decodeHash;
import static com.github.davidmoten.geo.GeoHash.encodeHash;
import static com.github.davidmoten.geo.GeoHash.gridAsString;
import static com.github.davidmoten.geo.GeoHash.hashLengthToCoverBoundingBox;
import static com.github.davidmoten.geo.GeoHash.heightDegrees;
import static com.github.davidmoten.geo.GeoHash.left;
import static com.github.davidmoten.geo.GeoHash.neighbours;
import static com.github.davidmoten.geo.GeoHash.right;
import static com.github.davidmoten.geo.GeoHash.top;
import static com.github.davidmoten.geo.GeoHash.widthDegrees;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import com.google.common.collect.Sets;
import org.junit.jupiter.api.Test;

/**
 * Unit tests for {@link GeoHash}.
 * 
 * @author dave
 * 
 */
public class GeoHashCheckTest {

    private static final double HARTFORD_LON = -72.727175;
    private static final double HARTFORD_LAT = 41.842967;
    private static final double SCHENECTADY_LON = -73.950691;
    private static final double SCHENECTADY_LAT = 42.819581;
    private static final double PRECISION = 0.000000001;
    private static final int I_LEFT      = 0;
    private static final int I_RIGHT     = 1;
    private static final int I_TOP       = 2;
    private static final int I_BOTTOM    = 3;
    private static final int I_LEFT_TOP  = 4;
    private static final int I_LEFT_BOT  = 5;
    private static final int I_RIGHT_TOP = 6;
    private static final int I_RIGHT_BOT = 7;
    


    @Test
    public void testWhiteHouseHashEncode() {
        assertEquals("dqcjqcp84c6e",
                encodeHash(38.89710201881826, -77.03669792041183));
    }


    @Test
    public void testFromGeoHashDotOrg() {
        assertEquals("6gkzwgjzn820", encodeHash(-25.382708, -49.265506));
    }


    @Test
    public void testEncodeHashWithLatTooBig() {
        assertThrows(IllegalArgumentException.class, () -> encodeHash(1000, 100, 4));
    }

    @Test
    public void testAdjacentTop() {
        assertEquals("u1pc", adjacentHash("u1pb", Direction.TOP));
    }

    @Test
    public void testAdjacentLeft() {
        assertEquals("u1p8", adjacentHash("u1pb", Direction.LEFT));
    }

    @Test
    public void testCoverBoundingBoxWithHashLength3AroundBoston() {
        Set<String> hashes = coverBoundingBox(SCHENECTADY_LAT, SCHENECTADY_LON,
                HARTFORD_LAT, HARTFORD_LON, 3).getHashes();
        assertEquals(Sets.newHashSet("dr7", "dre", "drk", "drs"), hashes);
    }


    
}
