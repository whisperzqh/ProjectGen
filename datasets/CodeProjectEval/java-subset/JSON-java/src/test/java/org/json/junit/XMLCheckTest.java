package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringReader;
import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.Map;

import org.json.*;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;


/**
 * Tests for JSON-Java XML.java
 * Note: noSpace() will be tested by JSONMLTest
 */
public class XMLCheckTest {
    /**
     * JUnit supports temporary files and folders that are cleaned up after the test.
     * https://garygregory.wordpress.com/2010/01/20/junit-tip-use-rules-to-manage-temporary-files-and-folders/ 
     */
    @Rule
    public TemporaryFolder testFolder = new TemporaryFolder();


    /**
     * Convenience method, given an input string and expected result,
     * convert to JSONObject and compare actual to expected result.
     * @param xmlStr the string to parse
     * @param expectedStr the expected JSON string
     */
    private void compareStringToJSONObject(String xmlStr, String expectedStr) {
        JSONObject jsonObject = XML.toJSONObject(xmlStr);
        JSONObject expectedJsonObject = new JSONObject(expectedStr);
        Util.compareActualVsExpectedJsonObjects(jsonObject,expectedJsonObject);
    }

    /**
     * Convenience method, given an input string and expected result,
     * convert to JSONObject via reader and compare actual to expected result.
     * @param xmlStr the string to parse
     * @param expectedStr the expected JSON string
     */
    private void compareReaderToJSONObject(String xmlStr, String expectedStr) {
        JSONObject expectedJsonObject = new JSONObject(expectedStr);
        Reader reader = new StringReader(xmlStr);
        JSONObject jsonObject = XML.toJSONObject(reader);
        Util.compareActualVsExpectedJsonObjects(jsonObject,expectedJsonObject);
    }

    /**
     * Convenience method, given an input string and expected result, convert to
     * JSONObject via file and compare actual to expected result.
     * 
     * @param xmlStr
     *            the string to parse
     * @param expectedStr
     *            the expected JSON string
     * @throws IOException
     */
    private void compareFileToJSONObject(String xmlStr, String expectedStr) {
        try {
            JSONObject expectedJsonObject = new JSONObject(expectedStr);
            File tempFile = this.testFolder.newFile("fileToJSONObject.xml");
            FileWriter fileWriter = new FileWriter(tempFile);
            try {
                fileWriter.write(xmlStr);
            } finally {
                fileWriter.close();
            }

            Reader reader = new FileReader(tempFile);
            try {
                JSONObject jsonObject = XML.toJSONObject(reader);
                Util.compareActualVsExpectedJsonObjects(jsonObject,expectedJsonObject);
            } finally {
                reader.close();
            }
        } catch (IOException e) {
            fail("Error: " +e.getMessage());
        }
    }

        /**
     * Valid XML to JSONObject
     */
    @Test
    public void shouldHandleSimpleXML() {
        String xmlStr = 
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"+
            "<addresses xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""+
            "   xsi:noNamespaceSchemaLocation='test.xsd'>\n"+
            "   <address>\n"+
            "       <name>Joe Tester</name>\n"+
            "       <street>[CDATA[Baker street 5]</street>\n"+
            "       <NothingHere/>\n"+
            "       <TrueValue>true</TrueValue>\n"+
            "       <FalseValue>false</FalseValue>\n"+
            "       <NullValue>null</NullValue>\n"+
            "       <PositiveValue>42</PositiveValue>\n"+
            "       <NegativeValue>-23</NegativeValue>\n"+
            "       <DoubleValue>-23.45</DoubleValue>\n"+
            "       <Nan>-23x.45</Nan>\n"+
            "       <ArrayOfNum>1, 2, 3, 4.1, 5.2</ArrayOfNum>\n"+
            "   </address>\n"+
            "</addresses>";

        String expectedStr = 
            "{\"addresses\":{\"address\":{\"street\":\"[CDATA[Baker street 5]\","+
            "\"name\":\"Joe Tester\",\"NothingHere\":\"\",\"TrueValue\":true,\n"+
            "\"FalseValue\":false,\"NullValue\":null,\"PositiveValue\":42,\n"+
            "\"NegativeValue\":-23,\"DoubleValue\":-23.45,\"Nan\":\"-23x.45\",\n"+
            "\"ArrayOfNum\":\"1, 2, 3, 4.1, 5.2\"\n"+
            "},\"xsi:noNamespaceSchemaLocation\":"+
            "\"test.xsd\",\"xmlns:xsi\":\"http://www.w3.org/2001/"+
            "XMLSchema-instance\"}}";

        compareStringToJSONObject(xmlStr, expectedStr);
        compareReaderToJSONObject(xmlStr, expectedStr);
        compareFileToJSONObject(xmlStr, expectedStr);
    }

    @Test
    public void testIndentComplicatedJsonObject(){
        String str = "{\n" +
                "  \"success\": true,\n" +
                "  \"error\": null,\n" +
                "  \"response\": [\n" +
                "    {\n" +
                "      \"timestamp\": 1664917200,\n" +
                "      \"dateTimeISO\": \"2022-10-05T00:00:00+03:00\",\n" +
                "      \"loc\": {\n" +
                "        \"lat\": 39.91987,\n" +
                "        \"long\": 32.85427\n" +
                "      },\n" +
                "      \"place\": {\n" +
                "        \"name\": \"ankara\",\n" +
                "        \"state\": \"an\",\n" +
                "        \"country\": \"tr\"\n" +
                "      },\n" +
                "      \"profile\": {\n" +
                "        \"tz\": \"Europe/Istanbul\"\n" +
                "      },\n" +
                "      \"sun\": {\n" +
                "        \"rise\": 1664941721,\n" +
                "        \"riseISO\": \"2022-10-05T06:48:41+03:00\",\n" +
                "        \"set\": 1664983521,\n" +
                "        \"setISO\": \"2022-10-05T18:25:21+03:00\",\n" +
                "        \"transit\": 1664962621,\n" +
                "        \"transitISO\": \"2022-10-05T12:37:01+03:00\",\n" +
                "        \"midnightSun\": false,\n" +
                "        \"polarNight\": false,\n" +
                "        \"twilight\": {\n" +
                "          \"civilBegin\": 1664940106,\n" +
                "          \"civilBeginISO\": \"2022-10-05T06:21:46+03:00\",\n" +
                "          \"civilEnd\": 1664985136,\n" +
                "          \"civilEndISO\": \"2022-10-05T18:52:16+03:00\",\n" +
                "          \"nauticalBegin\": 1664938227,\n" +
                "          \"nauticalBeginISO\": \"2022-10-05T05:50:27+03:00\",\n" +
                "          \"nauticalEnd\": 1664987015,\n" +
                "          \"nauticalEndISO\": \"2022-10-05T19:23:35+03:00\",\n" +
                "          \"astronomicalBegin\": 1664936337,\n" +
                "          \"astronomicalBeginISO\": \"2022-10-05T05:18:57+03:00\",\n" +
                "          \"astronomicalEnd\": 1664988905,\n" +
                "          \"astronomicalEndISO\": \"2022-10-05T19:55:05+03:00\"\n" +
                "        }\n" +
                "      },\n" +
                "      \"moon\": {\n" +
                "        \"rise\": 1664976480,\n" +
                "        \"riseISO\": \"2022-10-05T16:28:00+03:00\",\n" +
                "        \"set\": 1664921520,\n" +
                "        \"setISO\": \"2022-10-05T01:12:00+03:00\",\n" +
                "        \"transit\": 1664994240,\n" +
                "        \"transitISO\": \"2022-10-05T21:24:00+03:00\",\n" +
                "        \"underfoot\": 1664949360,\n" +
                "        \"underfootISO\": \"2022-10-05T08:56:00+03:00\",\n" +
                "        \"phase\": {\n" +
                "          \"phase\": 0.3186,\n" +
                "          \"name\": \"waxing gibbous\",\n" +
                "          \"illum\": 71,\n" +
                "          \"age\": 9.41,\n" +
                "          \"angle\": 0.55\n" +
                "        }\n" +
                "      }\n" +
                "    }\n" +
                "  ]\n" +
                "}" ;
        JSONObject jsonObject = new JSONObject(str);
        String actualIndentedXmlString = XML.toString(jsonObject, 1);
        JSONObject actualJsonObject = XML.toJSONObject(actualIndentedXmlString);
        String expected = "<success>true</success>\n" +
                "<response>\n" +
                " <dateTimeISO>2022-10-05T00:00:00+03:00</dateTimeISO>\n" +
                " <loc>\n" +
                "  <lat>39.91987</lat>\n" +
                "  <long>32.85427</long>\n" +
                " </loc>\n" +
                " <moon>\n" +
                "  <phase>\n" +
                "   <phase>0.3186</phase>\n" +
                "   <name>waxing gibbous</name>\n" +
                "   <angle>0.55</angle>\n" +
                "   <illum>71</illum>\n" +
                "   <age>9.41</age>\n" +
                "  </phase>\n" +
                "  <setISO>2022-10-05T01:12:00+03:00</setISO>\n" +
                "  <underfoot>1664949360</underfoot>\n" +
                "  <set>1664921520</set>\n" +
                "  <transit>1664994240</transit>\n" +
                "  <transitISO>2022-10-05T21:24:00+03:00</transitISO>\n" +
                "  <riseISO>2022-10-05T16:28:00+03:00</riseISO>\n" +
                "  <rise>1664976480</rise>\n" +
                "  <underfootISO>2022-10-05T08:56:00+03:00</underfootISO>\n" +
                " </moon>\n" +
                " <profile>\n" +
                "  <tz>Europe/Istanbul</tz>\n" +
                " </profile>\n" +
                " <place>\n" +
                "  <country>tr</country>\n" +
                "  <name>ankara</name>\n" +
                "  <state>an</state>\n" +
                " </place>\n" +
                " <sun>\n" +
                "  <setISO>2022-10-05T18:25:21+03:00</setISO>\n" +
                "  <midnightSun>false</midnightSun>\n" +
                "  <set>1664983521</set>\n" +
                "  <transit>1664962621</transit>\n" +
                "  <polarNight>false</polarNight>\n" +
                "  <transitISO>2022-10-05T12:37:01+03:00</transitISO>\n" +
                "  <riseISO>2022-10-05T06:48:41+03:00</riseISO>\n" +
                "  <rise>1664941721</rise>\n" +
                "  <twilight>\n" +
                "   <civilEnd>1664985136</civilEnd>\n" +
                "   <astronomicalBegin>1664936337</astronomicalBegin>\n" +
                "   <astronomicalEnd>1664988905</astronomicalEnd>\n" +
                "   <astronomicalBeginISO>2022-10-05T05:18:57+03:00</astronomicalBeginISO>\n" +
                "   <civilBegin>1664940106</civilBegin>\n" +
                "   <nauticalEndISO>2022-10-05T19:23:35+03:00</nauticalEndISO>\n" +
                "   <astronomicalEndISO>2022-10-05T19:55:05+03:00</astronomicalEndISO>\n" +
                "   <nauticalBegin>1664938227</nauticalBegin>\n" +
                "   <nauticalEnd>1664987015</nauticalEnd>\n" +
                "   <nauticalBeginISO>2022-10-05T05:50:27+03:00</nauticalBeginISO>\n" +
                "   <civilBeginISO>2022-10-05T06:21:46+03:00</civilBeginISO>\n" +
                "   <civilEndISO>2022-10-05T18:52:16+03:00</civilEndISO>\n" +
                "  </twilight>\n" +
                " </sun>\n" +
                " <timestamp>1664917200</timestamp>\n" +
                "</response>\n" +
                "<error>null</error>\n";
        JSONObject expectedJsonObject = XML.toJSONObject(expected);
        assertTrue(expectedJsonObject.similar(actualJsonObject));


    }

    
}



