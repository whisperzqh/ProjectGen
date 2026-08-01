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

import static com.google.common.truth.Truth.assertThat;
import static com.google.testing.compile.CompilationSubject.assertThat;
import static com.google.testing.compile.Compiler.javac;
import static javax.tools.StandardLocation.SOURCE_OUTPUT;
import static org.junit.Assert.fail;

import com.google.common.collect.ImmutableList;
import javax.tools.JavaFileObject;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public class CompilationCheckTest {
  
  private static final JavaFileObject source1 =
      JavaFileObjects.forSourceLines(
          "test.Source1", // format one per line
          "package test;",
          "",
          "class Source1 {}");

  private static final JavaFileObject source2 =
      JavaFileObjects.forSourceLines(
          "test.Source2", // format one per line
          "package test;",
          "",
          "interface Source2 {}");

  private static final JavaFileObject brokenSource =
      JavaFileObjects.forSourceLines(
          "test.BrokenSource", // format one per line
          "package test;",
          "",
          "interface BrokenSource { what is this }");

  @Test
  public void generatedSourceFile() {
    Compiler compiler = compilerWithGenerator();
    Compilation compilation = compiler.compile(source1, source2);
    assertThat(compilation.generatedSourceFile("test.generated.Blah")).isPresent();
  }

  private static Compiler compilerWithGenerator() {
    return javac().withProcessors(new GeneratingProcessor("test.generated"));
  }

}
