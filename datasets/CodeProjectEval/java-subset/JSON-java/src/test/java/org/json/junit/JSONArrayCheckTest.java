package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONParserConfiguration;
import org.json.JSONPointerException;
import org.json.JSONString;
import org.json.JSONTokener;
import org.json.ParserConfiguration;
import org.json.junit.data.MyJsonString;
import org.junit.Ignore;
import org.junit.Test;

import com.jayway.jsonpath.Configuration;
import com.jayway.jsonpath.JsonPath;


/**
 * Tests for JSON-Java JSONArray.java
 */
public class JSONArrayCheckTest {
    private final String arrayStr = 
            "["+
                "true,"+
                "false,"+
                "\"true\","+
                "\"false\","+
                "\"hello\","+
                "23.45e-4,"+
                "\"23.45\","+
                "42,"+
                "\"43\","+
                "["+
                    "\"world\""+
                "],"+
                "{"+
                    "\"key1\":\"value1\","+
                    "\"key2\":\"value2\","+
                    "\"key3\":\"value3\","+
                    "\"key4\":\"value4\""+
                "},"+
                "0,"+
                "\"-1\""+
            "]";



    /**
     * Exercise the JSONArray.put(index, value) method with various parameters
     * and confirm the resulting JSONArray.
     */
    @SuppressWarnings("boxing")
    @Test
    public void putIndex() {
        JSONArray jsonArray = new JSONArray();

        // 1
        jsonArray.put(1, false);
        // index 0
        jsonArray.put(0, true);

        String jsonArrayStr =
            "["+
                "\"hello\","+
                "\"world\""+
            "]";
        // 2
        jsonArray.put(2, new JSONArray(jsonArrayStr));

        // 5
        jsonArray.put(5, 45L);
        // 4
        jsonArray.put(4, 1);
        // 3
        jsonArray.put(3, 2.5);

        // 6
        jsonArray.put(6, "objectPut");

        // 7 will be null

        String jsonObjectStr = 
            "{"+
                "\"key10\":\"val10\","+
                "\"key20\":\"val20\","+
                "\"key30\":\"val30\""+
            "}";
        JSONObject jsonObject = new JSONObject(jsonObjectStr);
        jsonArray.put(8, jsonObject);
        Collection<Object> collection = new ArrayList<Object>();
        collection.add(1);
        collection.add(2);
        jsonArray.put(9,collection);

        Map<String, Object> map = new HashMap<String, Object>();
        map.put("k1", "v1");
        jsonArray.put(10, map);
        try {
            jsonArray.put(-1, "abc");
            assertTrue("put index < 0 should have thrown exception", false);
        } catch(Exception ignored) {}

        // validate JSON
        Object doc = Configuration.defaultConfiguration().jsonProvider().parse(jsonArray.toString());
        assertTrue("expected 11 top level items", ((List<?>)(JsonPath.read(doc, "$"))).size() == 11);
        assertTrue("expected true", Boolean.TRUE.equals(jsonArray.query("/0")));
        assertTrue("expected false", Boolean.FALSE.equals(jsonArray.query("/1")));
        assertTrue("expected 2 items in [2]", ((List<?>)(JsonPath.read(doc, "$[2]"))).size() == 2);
        assertTrue("expected hello", "hello".equals(jsonArray.query("/2/0")));
        assertTrue("expected world", "world".equals(jsonArray.query("/2/1")));
        assertTrue("expected 2.5", Double.valueOf(2.5).equals(jsonArray.query("/3")));
        assertTrue("expected 1", Integer.valueOf(1).equals(jsonArray.query("/4")));
        assertTrue("expected 45", Long.valueOf(45).equals(jsonArray.query("/5")));
        assertTrue("expected objectPut", "objectPut".equals(jsonArray.query("/6")));
        assertTrue("expected null", JSONObject.NULL.equals(jsonArray.query("/7")));
        assertTrue("expected 3 items in [8]", ((Map<?,?>)(JsonPath.read(doc, "$[8]"))).size() == 3);
        assertTrue("expected val10", "val10".equals(jsonArray.query("/8/key10")));
        assertTrue("expected val20", "val20".equals(jsonArray.query("/8/key20")));
        assertTrue("expected val30", "val30".equals(jsonArray.query("/8/key30")));
        assertTrue("expected 2 items in [9]", ((List<?>)(JsonPath.read(doc, "$[9]"))).size() == 2);
        assertTrue("expected 1", Integer.valueOf(1).equals(jsonArray.query("/9/0")));
        assertTrue("expected 2", Integer.valueOf(2).equals(jsonArray.query("/9/1")));
        assertTrue("expected 1 item in [10]", ((Map<?,?>)(JsonPath.read(doc, "$[10]"))).size() == 1);
        assertTrue("expected v1", "v1".equals(jsonArray.query("/10/k1")));
        Util.checkJSONObjectMaps(jsonObject);
        Util.checkJSONArrayMaps(jsonArray);
    }


    public static ArrayList<Object> buildNestedArray(int maxDepth) {
        if (maxDepth <= 0) {
            return new ArrayList<>();
        }
        ArrayList<Object> nestedArray = new ArrayList<>();
        nestedArray.add(buildNestedArray(maxDepth - 1));
        return nestedArray;
    }
}
