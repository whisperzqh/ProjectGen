/*
 * Copyright (C) 2016 Google, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.testing.compile;

import static com.google.common.truth.ExpectFailure.assertThat;
import static com.google.common.truth.Truth.assertThat;
import static com.google.testing.compile.JavaFileObjectSubject.assertThat;
import static com.google.testing.compile.JavaFileObjectSubject.javaFileObjects;
import static java.nio.charset.StandardCharsets.UTF_8;
import static org.junit.Assert.assertThrows;

import com.google.common.truth.ExpectFailure;
import java.io.IOException;
import javax.tools.JavaFileObject;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public final class JavaFileObjectSubjectCheckTest {
  @Rule public final ExpectFailure expectFailure = new ExpectFailure();

  private static final JavaFileObject CLASS =
      JavaFileObjects.forSourceLines(
          "test.TestClass", //
          "package test;",
          "",
          "public class TestClass {}");

  private static final JavaFileObject DIFFERENT_NAME =
      JavaFileObjects.forSourceLines(
          "test.TestClass2", //
          "package test;",
          "",
          "public class TestClass2 {}");

  private static final JavaFileObject CLASS_WITH_FIELD =
      JavaFileObjects.forSourceLines(
          "test.TestClass", //
          "package test;",
          "",
          "public class TestClass {",
          "  Object field;",
          "}");

  private static final JavaFileObject UNKNOWN_TYPES =
      JavaFileObjects.forSourceLines(
          "test.TestClass",
          "package test;",
          "",
          "public class TestClass {",
          "  Bar badMethod(Baz baz) { return baz.what(); }",
          "}");


  @Test
  public void hasSourceEquivalentTo_failOnExtraInExpected() throws IOException {
    expectFailure
        .whenTesting()
        .about(javaFileObjects())
        .that(CLASS)
        .hasSourceEquivalentTo(CLASS_WITH_FIELD);
    AssertionError expected = expectFailure.getFailure();
    assertThat(expected).factKeys().contains("expected to be equivalent to");
    assertThat(expected.getMessage()).contains("unmatched nodes in the expected tree");
    assertThat(expected.getMessage()).contains(CLASS.getName());
    assertThat(expected).factValue("but was").isEqualTo(CLASS.getCharContent(false));
  }

}
