package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.*;

import org.json.*;
import org.junit.Test;

/**
 * Tests for org.json.JSONML.java
 *
 * Certain inputs are expected to result in exceptions. These tests are
 * executed first. JSONML provides an API to:
 *     Convert an XML string into a JSONArray or a JSONObject.
 *     Convert a JSONArray or JSONObject into an XML string.
 * Both fromstring and tostring operations operations should be symmetrical
 * within the limits of JSONML.
 * It should be possible to perform the following operations, which should
 * result in the original string being recovered, within the limits of the
 * underlying classes:
 *  Convert a string -> JSONArray -> string -> JSONObject -> string
 *  Convert a string -> JSONObject -> string -> JSONArray -> string
 *
 */
public class JSONMLCheckTest {

    /**
     * JSON string cannot be reverted to original xml. See test result in
     * comment below.
     */
    @Test
    public void testToJSONObject_reversibility() {
        final String originalXml = "<readResult><errors someAttr=\"arrtValue\"><code>400</code></errors><errors><code>402</code></errors></readResult>";
        final JSONObject originalObject=JSONML.toJSONObject(originalXml,false);
        final String originalJson = originalObject.toString();
        final String xml = JSONML.toString(originalObject);
        final JSONObject revertedObject = JSONML.toJSONObject(xml, false);
        final String newJson = revertedObject.toString();
        assertTrue("JSON Objects are not similar", originalObject.similar(revertedObject));
        assertTrue("JSON Strings are not similar", new JSONObject(originalJson).similar(new JSONObject(newJson)));
    }

        /**
     * Convert an XML document into a JSONArray, then use JSONML.toString()
     * to convert it into a string. This string is then converted back into
     * a JSONArray. Both JSONArrays are compared against a control to
     * confirm the contents.
     */
    @Test
    public void toJSONArray() {
        /**
         * xmlStr contains XML text which is transformed into a JSONArray.
         * Each element becomes a JSONArray:
         * 1st entry = elementname
         * 2nd entry = attributes object (if present)
         * 3rd entry = content (if present)
         * 4th entry = child element JSONArrays (if present)
         * The result is compared against an expected JSONArray.
         * The transformed JSONArray is then transformed back into a string
         * which is used to create a final JSONArray, which is also compared
         * against the expected JSONArray.
         */
        String xmlStr =
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"+
            "<addresses xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""+
                 "xsi:noNamespaceSchemaLocation='test.xsd'>\n"+
                 "<address attr1=\"attrValue1\" attr2=\"attrValue2\" attr3=\"attrValue3\">\n"+
                     "<name nameType=\"mine\">myName</name>\n"+
                     "<nocontent/>>\n"+
                 "</address>\n"+
            "</addresses>";
        String expectedStr =
            "[\"addresses\","+
                "{\"xsi:noNamespaceSchemaLocation\":\"test.xsd\","+
                    "\"xmlns:xsi\":\"http://www.w3.org/2001/XMLSchema-instance\"},"+
                "[\"address\","+
                    "{\"attr1\":\"attrValue1\",\"attr2\":\"attrValue2\",\"attr3\":\"attrValue3\"},"+
                    "[\"name\", {\"nameType\":\"mine\"},\"myName\"],"+
                    "[\"nocontent\"],"+
                    "\">\""+
                "]"+
            "]";
        JSONArray jsonArray = JSONML.toJSONArray(xmlStr);
        JSONArray expectedJsonArray = new JSONArray(expectedStr);
        String xmlToStr = JSONML.toString(jsonArray);
        JSONArray finalJsonArray = JSONML.toJSONArray(xmlToStr);
        Util.compareActualVsExpectedJsonArrays(jsonArray, expectedJsonArray);
        Util.compareActualVsExpectedJsonArrays(finalJsonArray, expectedJsonArray);
    }


}
