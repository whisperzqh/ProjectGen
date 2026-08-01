package org.json.junit;

/*
Public Domain.
*/

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.InputStream;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONPointer;
import org.json.JSONPointerException;
import org.json.JSONTokener;
import org.junit.Test;

public class JSONPointerCheckTest {

    private static final JSONObject document;
    private static final String EXPECTED_COMPLETE_DOCUMENT = "{\"\":0,\" \":7,\"g|h\":4,\"c%d\":2,\"k\\\"l\":6,\"a/b\":1,\"i\\\\j\":5," +
    		"\"obj\":{\"\":{\"\":\"empty key of an object with an empty key\",\"subKey\":\"Some other value\"}," +
            "\"other~key\":{\"another/key\":[\"val\"]},\"key\":\"value\"},\"foo\":[\"bar\",\"baz\"],\"e^f\":3," +
            "\"m~n\":8}";

    
    static {
        @SuppressWarnings("resource")
        InputStream resourceAsStream = JSONPointerTest.class.getClassLoader().getResourceAsStream("jsonpointer-testdoc.json");
        if(resourceAsStream == null) {
            throw new ExceptionInInitializerError("Unable to locate test file. Please check your development environment configuration");
        }
        document = new JSONObject(new JSONTokener(resourceAsStream));
    }

    private Object query(String pointer) {
        return new JSONPointer(pointer).queryFrom(document);
    }


    @Test
    public void objectPropertyQuery() {
        assertEquals("[\"bar\",\"baz\"]", query("/foo").toString());
    }

}
