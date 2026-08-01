package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.*;

import org.json.*;
import org.junit.Test;


/**
 * Unit tests for JSON-Java HTTP.java. See RFC7230.
 */
public class HTTPCheckTest {

    

    /**
     * Call HTTP.toJSONObject() with a full POST request string including
     * response headers, then convert it back into an HTTP string.
     */
    @Test
    public void convertHTTPRequestToString() {
        String httpStr = 
            "POST /enlighten/calais.asmx HTTP/1.1\n"+
            "Host: api.opencalais.com\n"+
            "Content-Type: text/xml; charset=utf-8\n"+
            "Content-Length: 100";
        String expectedHTTPStr = 
            "{"+
            "\"Request-URI\":\"/enlighten/calais.asmx\","+
            "\"Host\":\"api.opencalais.com\","+
            "\"Method\":\"POST\","+
            "\"HTTP-Version\":\"HTTP/1.1\","+
            "\"Content-Length\":\"100\","+
            "\"Content-Type\":\"text/xml; charset=utf-8\"}";
        JSONObject jsonObject = HTTP.toJSONObject(httpStr);
        JSONObject expectedJsonObject = new JSONObject(expectedHTTPStr);
        String httpToStr = HTTP.toString(jsonObject);
        /**
         * JSONObject objects to crlfs and any trailing chars.
         * For the sake of the test, simplify the resulting string
         */
        httpToStr = httpToStr.replaceAll("("+HTTP.CRLF+HTTP.CRLF+")", "");
        httpToStr = httpToStr.replaceAll(HTTP.CRLF, "\n");
        JSONObject finalJsonObject = HTTP.toJSONObject(httpToStr);
        Util.compareActualVsExpectedJsonObjects(jsonObject,expectedJsonObject);
        Util.compareActualVsExpectedJsonObjects(finalJsonObject,expectedJsonObject);
    }

   
}
