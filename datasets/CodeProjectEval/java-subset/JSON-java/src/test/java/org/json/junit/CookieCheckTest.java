package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.*;

import org.json.*;
import org.junit.Test;


/**
 * HTTP cookie specification: RFC6265
 * <p>
 * At its most basic, a cookie is a name=value pair. The value may be subdivided
 * into other cookies, but that is not tested here. The cookie may also include
 * certain named attributes, delimited by semicolons. 
 * <p>
 * The Cookie.toString() method emits certain attributes if present: expires,
 * domain, path, secure. All but secure are name-value pairs. Other attributes
 * are not included in the toString() output.
 * <p>
 * A JSON-Java encoded cookie escapes '+', '%', '=', ';' with %hh values.
 */
public class CookieCheckTest {


    /**
     * A string may be URL-encoded when converting to JSONObject.
     * If found, '+' is converted to ' ', and %hh hex strings are converted
     * to their ascii char equivalents. This test confirms the decoding
     * behavior. 
     */
    @Test
    public void convertEncodedCookieToString() {
        String cookieStr = 
            "PH=deleted;  "+
            " expires=Wed,+19-Mar-2014+17:53:53+GMT;"+
            "path=/%2Bthis/is%26/a/spec%3Bsegment%3D;   "+
            "    domain=.yahoo.com;"+
            "secure";
        String expectedCookieStr = 
            "{\"path\":\"/+this/is&/a/spec;segment=\","+
            "\"expires\":\"Wed, 19-Mar-2014 17:53:53 GMT\","+
            "\"domain\":\".yahoo.com\","+
            "\"name\":\"PH\","+
            "\"secure\":true,"+
            "\"value\":\"deleted\"}";
        JSONObject jsonObject = Cookie.toJSONObject(cookieStr);
        JSONObject expectedJsonObject = new JSONObject(expectedCookieStr);
        String cookieToStr = Cookie.toString(jsonObject);
        JSONObject finalJsonObject = Cookie.toJSONObject(cookieToStr);
        Util.compareActualVsExpectedJsonObjects(jsonObject,expectedJsonObject);
        Util.compareActualVsExpectedJsonObjects(finalJsonObject,expectedJsonObject);
    }
    
    
}
