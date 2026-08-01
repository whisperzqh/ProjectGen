/*
 *  (C) Copyright 2020 Password4j (http://password4j.com/).
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 */
package com.password4j;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.security.CodeSource;
import java.security.PermissionCollection;
import java.security.Permissions;
import java.security.Policy;
import java.security.Provider;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Random;

import org.junit.Assert;
import org.junit.Test;

import com.password4j.types.Argon2;
import com.password4j.types.Bcrypt;
import com.password4j.types.Hmac;

import static org.junit.Assert.*;


public class PasswordCheckTest
{

    private static final String PASSWORD = "password";

    private static final byte[] PASSWORD_BYTES = PASSWORD.getBytes(StandardCharsets.UTF_8);
    private static final String SALT = "salt";

    private static final byte[] SALT_BYTES = SALT.getBytes(StandardCharsets.UTF_8);
    private static final String PEPPER = "pepper";

    private static final SecureString SECURE_PASSWORD = new SecureString(PASSWORD.toCharArray());

    private static final Random RANDOM = new Random();


    @Test
    public void testHashingFunction()
    {
        // GIVEN


        // WHEN
        Hash hash1 = Password.hash(PASSWORD).withPBKDF2();
        Hash hash2 = Password.hash(PASSWORD).withBcrypt();
        Hash hash3 = Password.hash(PASSWORD).withScrypt();
        Hash hash4 = Password.hash(PASSWORD).withCompressedPBKDF2();
        Hash hash5 = Password.hash(PASSWORD).withMessageDigest();
        Hash hash6 = Password.hash(PASSWORD).withArgon2();



        // THEN
        assertTrue(hash1.getHashingFunction() instanceof PBKDF2Function);
        assertTrue(hash2.getHashingFunction() instanceof BcryptFunction);
        assertTrue(hash3.getHashingFunction() instanceof ScryptFunction);
        assertTrue(hash4.getHashingFunction() instanceof CompressedPBKDF2Function);
        assertTrue(hash5.getHashingFunction() instanceof MessageDigestFunction);
        assertTrue(hash6.getHashingFunction() instanceof Argon2Function);
    }

    @Test
    public void testMigrationBytes4()
    {
        // GIVEN
        Hash oldHash = Password.hash(PASSWORD_BYTES).addPepper(PEPPER).addSalt(SALT_BYTES).withMessageDigest();

        // WHEN
        HashUpdate update = Password.check(PASSWORD_BYTES, oldHash.getResultAsBytes()).addPepper(PEPPER).addSalt(SALT_BYTES)
                .andUpdate()
                .with(AlgorithmFinder.getMessageDigestInstance(), AlgorithmFinder.getArgon2Instance());

        boolean newCheck = Password.check(PASSWORD_BYTES, update.getHash().getResultAsBytes()).addPepper(PEPPER).withArgon2();


        // THEN
        assertTrue(update.isVerified());
        assertTrue(newCheck);
    }

    @Test
    public void testCoherence()
    {
        // GIVEN

        // WHEN
        Hash hash1 = Password.hash(PASSWORD).addPepper(PEPPER).addSalt(SALT).withPBKDF2();
        Hash hash2 = Password.hash(PASSWORD).addPepper(PEPPER).withBcrypt();
        Hash hash3 = Password.hash(PASSWORD).addPepper(PEPPER).addSalt(SALT).withScrypt();

        // THEN
        assertTrue(Password.check(PASSWORD, hash1));
        assertTrue(Password.check(PASSWORD, hash2));
        assertTrue(Password.check(PASSWORD, hash3));
    }

    @Test
    public void testMigrationBytes2()
    {
        // GIVEN
        Hash oldHash = Password.hash(PASSWORD_BYTES).addPepper(PEPPER).addSalt(SALT_BYTES).withCompressedPBKDF2();

        // WHEN
        HashUpdate update = Password.check(PASSWORD_BYTES, oldHash.getResultAsBytes()).addPepper(PEPPER)
                .andUpdate()
                .with(AlgorithmFinder.getCompressedPBKDF2Instance(), AlgorithmFinder.getScryptInstance());

        boolean newCheck = Password.check(PASSWORD_BYTES, update.getHash().getResultAsBytes()).addPepper(PEPPER).withScrypt();


        // THEN
        assertTrue(update.isVerified());
        assertTrue(newCheck);
    }

    @Test
    public void testRawUpdate3()
    {
        // GIVEN
        Hash hash = Password.hash(PASSWORD).addPepper(PEPPER).addSalt(SALT).withScrypt();

        // WHEN
        HashUpdate update = Password.check(PASSWORD, hash.getResult()).addPepper(PEPPER).addSalt(SALT)
                .andUpdate().addNewSalt("newsalt").addNewPepper("newpepper").withScrypt();

        // THEN
        assertTrue(update.isVerified());
        Assert.assertEquals(Password.hash(PASSWORD).addPepper("newpepper").addSalt("newsalt").withScrypt().getResult(), update.getHash().getResult());
    }


}
