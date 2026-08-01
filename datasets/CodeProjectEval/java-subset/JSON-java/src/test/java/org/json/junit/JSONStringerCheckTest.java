package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.*;

import java.math.BigDecimal;
import java.util.*;

import org.json.*;
import org.junit.Test;

import com.jayway.jsonpath.*;


/**
 * Tests for JSON-Java JSONStringer and JSONWriter.
 */
public class JSONStringerCheckTest {


    /**
     * Build a nested JSON doc using JSONString API calls, then convert to
     * JSONObject. Will create a long cascade of output by reusing the
     * returned values..
     */
    @Test
    public void complexObjectString() {
        JSONStringer jsonStringer = new JSONStringer();
        jsonStringer.object().
            key("trueValue").value(true).
            key("falseValue").value(false).
            key("nullValue").value(null).
            key("stringValue").value("hello world!").
            key("object2").object().
            key("k1").value("v1").
            key("k2").value("v2").
            key("k3").value("v3").
            key("array1").array().
            value(1).
            value(2).
            object().
            key("k4").value("v4").
            key("k5").value("v5").
            key("k6").value("v6").
            key("array2").array().
            value(5).
            value(6).
            value(7).
            value(8).
            endArray().
            endObject().
            value(3).
            value(4).
            endArray().
            endObject().
            key("complexStringValue").value("h\be\tllo w\u1234orld!").
            key("intValue").value(42).
            key("doubleValue").value(-23.45e67).
            endObject();
        String str = jsonStringer.toString();
        JSONObject jsonObject = new JSONObject(str);

        // validate JSON content
        Object doc = Configuration.defaultConfiguration().jsonProvider().parse(jsonObject.toString());
        assertTrue("expected 8 top level items", ((Map<?,?>)(JsonPath.read(doc, "$"))).size() == 8);
        assertTrue("expected 4 object2 items", ((Map<?,?>)(JsonPath.read(doc, "$.object2"))).size() == 4);
        assertTrue("expected 5 array1 items", ((List<?>)(JsonPath.read(doc, "$.object2.array1"))).size() == 5);
        assertTrue("expected 4 array[2] items", ((Map<?,?>)(JsonPath.read(doc, "$.object2.array1[2]"))).size() == 4);
        assertTrue("expected 4 array1[2].array2 items", ((List<?>)(JsonPath.read(doc, "$.object2.array1[2].array2"))).size() == 4);
        assertTrue("expected true", Boolean.TRUE.equals(jsonObject.query("/trueValue")));
        assertTrue("expected false", Boolean.FALSE.equals(jsonObject.query("/falseValue")));
        assertTrue("expected null", JSONObject.NULL.equals(jsonObject.query("/nullValue")));
        assertTrue("expected hello world!", "hello world!".equals(jsonObject.query("/stringValue")));
        assertTrue("expected 42", Integer.valueOf(42).equals(jsonObject.query("/intValue")));
        assertTrue("expected -23.45e67", BigDecimal.valueOf(-23.45e67).equals(jsonObject.query("/doubleValue")));
        assertTrue("expected h\be\tllo w\u1234orld!", "h\be\tllo w\u1234orld!".equals(jsonObject.query("/complexStringValue")));
        assertTrue("expected v1", "v1".equals(jsonObject.query("/object2/k1")));
        assertTrue("expected v2", "v2".equals(jsonObject.query("/object2/k2")));
        assertTrue("expected v3", "v3".equals(jsonObject.query("/object2/k3")));
        assertTrue("expected 1", Integer.valueOf(1).equals(jsonObject.query("/object2/array1/0")));
        assertTrue("expected 2", Integer.valueOf(2).equals(jsonObject.query("/object2/array1/1")));
        assertTrue("expected v4", "v4".equals(jsonObject.query("/object2/array1/2/k4")));
        assertTrue("expected v5", "v5".equals(jsonObject.query("/object2/array1/2/k5")));
        assertTrue("expected v6", "v6".equals(jsonObject.query("/object2/array1/2/k6")));
        assertTrue("expected 5", Integer.valueOf(5).equals(jsonObject.query("/object2/array1/2/array2/0")));
        assertTrue("expected 6", Integer.valueOf(6).equals(jsonObject.query("/object2/array1/2/array2/1")));
        assertTrue("expected 7", Integer.valueOf(7).equals(jsonObject.query("/object2/array1/2/array2/2")));
        assertTrue("expected 8", Integer.valueOf(8).equals(jsonObject.query("/object2/array1/2/array2/3")));
        assertTrue("expected 3", Integer.valueOf(3).equals(jsonObject.query("/object2/array1/3")));
        assertTrue("expected 4", Integer.valueOf(4).equals(jsonObject.query("/object2/array1/4")));
    }

}
