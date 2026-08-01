package org.nibblesec.tools;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.util.Iterator;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

import org.junit.Test;
import org.nibblesec.tools.SerialKiller.PatternList;

/**
 * PatternListTest
 */
public class PatternListCheckTest {
    @Test(expected = NullPointerException.class)
    public void testCreateNull() {
        new PatternList((String[]) null);
    }

    @Test(expected = PatternSyntaxException.class)
    public void testCreateBadPattern() {
        new PatternList("(");
    }

}