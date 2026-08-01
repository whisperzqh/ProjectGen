package ch.hsr.geohash.util;

import ch.hsr.geohash.BoundingBox;
import ch.hsr.geohash.GeoHash;
import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.hamcrest.core.Is.is;
import static org.hamcrest.core.IsCollectionContaining.hasItem;
import static org.hamcrest.core.IsNot.not;
import static org.junit.Assert.assertThat;

/**
 * Created by IntelliJ IDEA. User: kevin Date: Jan 6, 2011 Time: 3:05:43 PM
 */
public class BoundingBoxGeoHashIteratorCheckTest {

	@Test
	public void testIter2() {
		BoundingBox box = new BoundingBox(37.7, 37.84, -122.52, -122.35);
		BoundingBoxGeoHashIterator iter = new BoundingBoxGeoHashIterator(
				TwoGeoHashBoundingBox.withBitPrecision(box, 35));
		checkIterator(iter);
	}


	private List<GeoHash> checkIterator(BoundingBoxGeoHashIterator iter) {
		BoundingBox newBox = iter.getBoundingBox().getBoundingBox();
		List<GeoHash> hashes = new ArrayList<>();
		while (iter.hasNext()) {
			hashes.add(iter.next());
		}

		GeoHash prev = null;
		for (GeoHash gh : hashes) {
			if (prev != null) {
				Assert.assertTrue(prev.compareTo(gh) < 0);
			}
			Assert.assertTrue(newBox.contains(gh.getOriginatingPoint()));
			prev = gh;
		}

		return hashes;
	}
}
