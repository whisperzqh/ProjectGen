package com.github.davidmoten.geo;

import com.google.common.collect.Sets;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Unit tests for {@link Coverage}.
 * 
 * @author dave
 * 
 */
public class CoverageCheckTest {


    @Test
    public void testCoverageOfAnAreaThatCantBeCoveredWithHashOfLengthOne() {
        Coverage coverage = GeoHash.coverBoundingBox(-5, 100, -45, 170);
        assertEquals(1, coverage.getHashLength());
        assertEquals(Sets.newHashSet("q", "r"), coverage.getHashes());
    }

}
