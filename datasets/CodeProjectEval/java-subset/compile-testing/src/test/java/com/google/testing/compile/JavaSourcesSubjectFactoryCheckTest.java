/*
 * Copyright (C) 2013 Google, Inc.
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
import static com.google.common.truth.Truth.assertAbout;
import static com.google.common.truth.Truth.assertThat;
import static com.google.testing.compile.JavaSourceSubjectFactory.javaSource;
import static java.nio.charset.StandardCharsets.UTF_8;
import static javax.tools.StandardLocation.CLASS_OUTPUT;
import static org.junit.Assert.fail;

import com.google.common.collect.ImmutableList;
import com.google.common.io.ByteSource;
import com.google.common.truth.ExpectFailure;
import java.util.Arrays;
import javax.tools.Diagnostic;
import javax.tools.JavaFileObject;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

/**
 * Tests {@link JavaSourcesSubjectFactory} (and {@link JavaSourceSubjectFactory}).
 *
 * @author Gregory Kick
 */
@RunWith(JUnit4.class)
public class JavaSourcesSubjectFactoryCheckTest {

  private static final JavaFileObject HELLO_WORLD_RESOURCE =
      JavaFileObjects.forResource("test/HelloWorld.java");

  private static final JavaFileObject HELLO_WORLD =
      JavaFileObjects.forSourceLines(
          "test.HelloWorld",
          "package test;",
          "",
          "import " + DiagnosticMessage.class.getCanonicalName() + ";",
          "",
          "@DiagnosticMessage",
          "public class HelloWorld {",
          "  @DiagnosticMessage Object foo;",
          "}");

  private static final JavaFileObject HELLO_WORLD_BROKEN =
      JavaFileObjects.forSourceLines(
          "test.HelloWorld",
          "package test;",
          "",
          "import " + DiagnosticMessage.class.getCanonicalName() + ";",
          "",
          "@DiagnosticMessage",
          "public class HelloWorld {",
          "  @DiagnosticMessage Object foo;",
          "  Bar noSuchClass;",
          "}");

  @Rule public final ExpectFailure expectFailure = new ExpectFailure();

  @Test
  public void compilesWithoutError() {
    assertAbout(javaSource()).that(HELLO_WORLD_RESOURCE).compilesWithoutError();
    assertAbout(javaSource())
        .that(
            JavaFileObjects.forSourceLines(
                "test.HelloWorld",
                "package test;",
                "",
                "public class HelloWorld {",
                "  public static void main(String[] args) {",
                "    System.out.println(\"Hello World!\");",
                "  }",
                "}"))
        .compilesWithoutError();
  }


  @Test
  public void compilesWithoutError_warnings() {
    assertAbout(javaSource())
        .that(HELLO_WORLD)
        .processedWith(new DiagnosticMessage.Processor(Diagnostic.Kind.WARNING))
        .compilesWithoutError()
        .withWarningContaining("this is a message")
        .in(HELLO_WORLD)
        .onLine(6)
        .atColumn(8)
        .and()
        .withWarningContaining("this is a message")
        .in(HELLO_WORLD)
        .onLine(7)
        .atColumn(29);
  }

//   @Test
//   public void compilesWithoutWarnings_failsWithWarnings() {
//     expectFailure
//         .whenTesting()
//         .about(javaSource())
//         .that(HELLO_WORLD)
//         .processedWith(new DiagnosticMessage.Processor(Diagnostic.Kind.WARNING))
//         .compilesWithoutWarnings();
//     AssertionError expected = expectFailure.getFailure();
//     assertThat(expected.getMessage())
//         .contains("Expected 0 warnings, but found the following 2 warnings:\n");
//   }


  @Test
  public void failsToCompile_throws() {
    expectFailure.whenTesting().about(javaSource()).that(HELLO_WORLD_RESOURCE).failsToCompile();
    AssertionError expected = expectFailure.getFailure();
    assertThat(expected.getMessage())
        .contains("Compilation was expected to fail, but contained no errors");
    assertThat(expected.getMessage()).contains("No files were generated.");
  }


  @Test
  public void failsToCompile_throwsNotOnLine() {
    JavaFileObject fileObject = HELLO_WORLD_RESOURCE;
    expectFailure
        .whenTesting()
        .about(javaSource())
        .that(fileObject)
        .processedWith(new ErrorProcessor())
        .failsToCompile()
        .withErrorContaining("expected error!")
        .in(fileObject)
        .onLine(1);
    AssertionError expected = expectFailure.getFailure();
    int actualErrorLine = 18;
    assertThat(expected.getMessage())
        .contains(
            String.format(
                "Expected an error containing \"expected error!\" in %s on line:\n   1: ",
                fileObject.getName()));
    assertThat(expected.getMessage()).contains("" + actualErrorLine);
  }



  @Test
  public void generatesSources() {
    assertAbout(javaSource())
        .that(HELLO_WORLD_RESOURCE)
        .processedWith(new GeneratingProcessor())
        .compilesWithoutError()
        .and()
        .generatesSources(
            JavaFileObjects.forSourceString(
                GeneratingProcessor.GENERATED_CLASS_NAME, GeneratingProcessor.GENERATED_SOURCE));
  }


  @Test
  public void generatesSources_failOnUnexpected() {
    String failingExpectationSource = "abstract class Blah {}";
    expectFailure
        .whenTesting()
        .about(javaSource())
        .that(HELLO_WORLD_RESOURCE)
        .processedWith(new GeneratingProcessor())
        .compilesWithoutError()
        .and()
        .generatesSources(
            JavaFileObjects.forSourceString(
                GeneratingProcessor.GENERATED_CLASS_NAME, failingExpectationSource));
    AssertionError expected = expectFailure.getFailure();
    assertThat(expected.getMessage()).contains("didn't match exactly");
    assertThat(expected.getMessage()).contains(GeneratingProcessor.GENERATED_CLASS_NAME);
    assertThat(expected.getMessage()).contains(GeneratingProcessor.GENERATED_SOURCE);
  }


  @Test
  public void invokesMultipleProcesors() {
    NoOpProcessor noopProcessor1 = new NoOpProcessor();
    NoOpProcessor noopProcessor2 = new NoOpProcessor();
    assertThat(noopProcessor1.invoked).isFalse();
    assertThat(noopProcessor2.invoked).isFalse();
    assertAbout(javaSource())
        .that(HELLO_WORLD_RESOURCE)
        .processedWith(noopProcessor1, noopProcessor2)
        .compilesWithoutError();
    assertThat(noopProcessor1.invoked).isTrue();
    assertThat(noopProcessor2.invoked).isTrue();
  }


}
