package org.nibblesec.tools;

import static java.nio.file.StandardCopyOption.REPLACE_EXISTING;
import static org.hamcrest.CoreMatchers.containsString;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.not;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.fail;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InvalidClassException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.FileTime;

import org.junit.Test;

/**
 * SerialKillerTest
 */
public class SerialKillerCheckTest {
    public static class Dummy implements java.io.Serializable {
        private static final long serialVersionUID = 1L;
    }


    @Test
    public void testStringWhitelisted() throws Exception {
        String s = "hello";
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (ObjectOutputStream stream = new ObjectOutputStream(bytes)) {
            stream.writeObject(s);
        }

        try (ObjectInputStream stream = new SerialKiller(
                new ByteArrayInputStream(bytes.toByteArray()),
                "src/test/resources/serialkiller.conf")) {
            Object obj = stream.readObject();
            assertEquals(s, obj);
        }
    }
}