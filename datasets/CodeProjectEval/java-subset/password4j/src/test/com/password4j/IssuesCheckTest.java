package com.password4j;

import com.password4j.types.Argon2;
import org.junit.Assert;
import org.junit.Assume;
import org.junit.Test;

import java.lang.reflect.Field;
import java.security.Provider;
import java.security.Security;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentMap;
import java.util.stream.Collectors;

import static org.junit.Assert.*;

public class IssuesCheckTest
{



    /**
     * @see <a href="https://github.com/Password4j/password4j/issues/126">issue #126</a>
     */
    @Test
    public void issue126()
    {
        byte[] hashBytes = Password.hash("’(っ＾▿＾)۶\uD83C\uDF78\uD83C\uDF1F\uD83C\uDF7A٩(˘◡˘ ) ❌❌ ❌❌❌")
                .addSalt("\uD83E\uDDC2")
                .withScrypt()
                .getBytes();

        Assert.assertEquals("827b022b411e712e5ae4855d8c71cb047d882b2457120d1019974d17dcf6f1bf59644d9a93e470ab14ee5f7a88ae9b0140d2db121de58f6d830fc9c16c82f212", printBytesToString(hashBytes));


        hashBytes = Password.hash("ŸŁĀPRČ")
                .addSalt("ŸŁĀPRČAA")
                .withArgon2()
                .getBytes();

        Assert.assertEquals("59dedcf45d7a8604926ca66f6abe3990ce8b6ba108f535836fa18e95b7d94e9f56301e422c1d487dd06dc26061261402a5f7fe912bd545b6aeec866fec74df81", printBytesToString(hashBytes));

    }


    private static String printBytesToString(byte[] bytes)
    {
        StringBuilder byteString= new StringBuilder();
        if (bytes!=null)
        {
            for (byte aByte : bytes)
            {
                byteString.append(String.format("%02x", aByte));
            }
        }
        else
        {
            byteString = new StringBuilder("-");
        }
        return byteString.toString();
    }

}
