/*
 * Copyright (C) 2014 Google, Inc.
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

import static com.google.common.collect.ImmutableList.toImmutableList;
import static com.google.common.collect.Iterables.getOnlyElement;
import static com.google.common.truth.Truth.assertThat;

import com.google.common.collect.ImmutableList;
import com.google.testing.compile.Parser.ParseResult;
import com.sun.source.tree.CompilationUnitTree;
import com.sun.source.tree.Tree;
import com.sun.source.util.TreePath;
import java.util.Objects;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

/**
 * A test for {@link TreeDiffer}.
 */
@RunWith(JUnit4.class)
public class TreeDifferCheckTest {
  private static final CompilationUnitTree EXPECTED_TREE =
      MoreTrees.parseLinesToTree("package test;",
          "import java.util.Set;",
          "",
          "final class TestClass {",
          "    public String toString() {",
          "        Object variable = new Object();",
          "        return \"literal\" + variable;",
          "    }",
          "",
          "    public void nonsense() {",
          "        int[] numbers = {0, 1, 2, 3, 4};",
          "        loop: for (int x : numbers) {",
          "            if (x % 2 == 0) {",
          "                throw new IllegalStateException();",
          "            }",
          "            break loop;",
          "        }",
          "    }",
          "}");
  private static final CompilationUnitTree ACTUAL_TREE =
      MoreTrees.parseLinesToTree("package test;",
          "import java.util.List;",
          "",
          "final class TestClass {",
          "    public String toString() {",
          "        Object variable = new Object();",
          "        return \"literal\" + variable;",
          "    }",
          "",
          "    public void nonsense() {",
          "        int[] numberz = {0, 1, 2, 3, 4, 5};",
          "        loop: for (int x : numberz) {",
          "            if (x % 2 == 0) {",
          "                throw new RuntimeException();",
          "            }",
          "            break;",
          "        }",
          "    }",
          "    public int extraNonsense() {",
          "      return 0;",
          "    }",
          "}");
  private static final CompilationUnitTree ASSERT_TREE_WITH_MESSAGE =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "   private void fail() {",
          "      assert false : \"details\";",
          "   }",
          "}");
  private static final CompilationUnitTree ASSERT_TREE_WITHOUT_MESSAGE =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "   private void fail() {",
          "      assert false;",
          "   }",
          "}");

  // These are used to test null tree iterators.
  // getInitializers() on NewArrayTrees will return null if the array is dimension-defined.
  private static final CompilationUnitTree NEW_ARRAY_SIZE_THREE =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final int[] myArray = new int[3];",
          "}");

  private static final CompilationUnitTree NEW_ARRAY_SIZE_FOUR =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final int[] myArray = new int[4];",
          "}");

  private static final CompilationUnitTree NEW_ARRAY_STATIC_INITIALIZER =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final int[] myArray = {1, 2, 3};",
          "}");

  private static final CompilationUnitTree LAMBDA_1 =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Consumer<Integer> NEWLINE = (int i) -> System.out.println(i);",
          "}");

  private static final CompilationUnitTree LAMBDA_2 =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Consumer<Integer> NEWLINE =",
          "      (int i) -> System.out.println(i);",
          "}");

  private static final CompilationUnitTree LAMBDA_IMPLICIT_ARG_TYPE =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Consumer<Integer> NEWLINE =",
          "      (i) -> System.out.println(i);",
          "}");

  private static final CompilationUnitTree LAMBDA_IMPLICIT_ARG_TYPE_NO_PARENS =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Consumer<Integer> NEWLINE =",
          "      i -> System.out.println(i);",
          "}");

  private static final CompilationUnitTree METHOD_REFERENCE =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Runnable NEWLINE = System.out::println;",
          "}");

  private static final CompilationUnitTree ANONYMOUS_CLASS =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  private static final Runnable NEWLINE = new Runnable() {",
          "    public void run() { System.out.println(); }",
          "  };",
          "}");

  private static final CompilationUnitTree TRY_WITH_RESOURCES_1 =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  void f() {",
          "    try (Resource1 r = new Resource1()) {}",
          "  }",
          "}");

  private static final CompilationUnitTree TRY_WITH_RESOURCES_2 =
      MoreTrees.parseLinesToTree("package test;",
          "final class TestClass {",
          "  void f() {",
          "    try (Resource2 r = new Resource2()) {}",
          "  }",
          "}");

  private static final ImmutableList<String> ANNOTATED_TYPE_SOURCE =
      ImmutableList.of(
          "package test;",
          "",
          "import java.lang.annotation.*;",
          "import java.util.List;",
          "",
          "@Target(ElementType.TYPE_USE)",
          "@interface Nullable {}",
          "",
          "interface NullableStringList extends List<@Nullable String> {}");

  private static final CompilationUnitTree ANNOTATED_TYPE_1 =
      MoreTrees.parseLinesToTree(ANNOTATED_TYPE_SOURCE);

  private static final CompilationUnitTree ANNOTATED_TYPE_2 =
      MoreTrees.parseLinesToTree(
          ANNOTATED_TYPE_SOURCE.stream()
              .map(s -> s.replace("@Nullable ", ""))
              .collect(toImmutableList()));

  private static final ImmutableList<String> MULTICATCH_SOURCE =
      ImmutableList.of(
          "package test;",
          "",
          "class TestClass {",
          "  void f() {",
          "    try {",
          "      System.gc();",
          "    } catch (IllegalArgumentException | NullPointerException e) {",
          "    }",
          "  }",
          "}");

  private static final CompilationUnitTree MULTICATCH_1 =
      MoreTrees.parseLinesToTree(MULTICATCH_SOURCE);

  private static final CompilationUnitTree MULTICATCH_2 =
      MoreTrees.parseLinesToTree(
          MULTICATCH_SOURCE.stream()
              .map(s -> s.replace("IllegalArgumentException", "IllegalStateException"))
              .collect(toImmutableList()));


  @Test
  public void scan_testAnnotatedTypeDifferent() {
    TreeDifference diff =
        TreeDiffer.diffCompilationUnits(ANNOTATED_TYPE_1, ANNOTATED_TYPE_2);
    assertThat(diff.isEmpty()).isFalse();
  }



  private TreePath asPath(CompilationUnitTree compilationUnit) {
    return MoreTrees.findSubtreePath(compilationUnit, Tree.Kind.COMPILATION_UNIT);
  }

  private TreePath baseToStringTree() {
    return MoreTrees.findSubtreePath(EXPECTED_TREE, Tree.Kind.METHOD, "toString");
  }

  private TreePath diffToStringTree() {
    return MoreTrees.findSubtreePath(ACTUAL_TREE, Tree.Kind.METHOD, "toString");
  }

  private static class SimplifiedDiff {
    private final Tree.Kind kind;
    private final String details;

    SimplifiedDiff(Tree.Kind kind, String details) {
      this.kind = kind;
      this.details = details;
    }

    static SimplifiedDiff create(TreeDifference.OneWayDiff other) {
      return new SimplifiedDiff(other.getNodePath().getLeaf().getKind(), other.getDetails());
    }

    static SimplifiedDiff create(TreeDifference.TwoWayDiff other) {
      return new SimplifiedDiff(
          other.getExpectedNodePath().getLeaf().getKind(), other.getDetails());
    }

    @Override
    public String toString() {
      return String.format("%s: %s", this.kind.toString(), this.details.toString());
    }

    @Override
    public boolean equals(Object o) {
      if (o == this) {
        return true;
      } else if (o instanceof SimplifiedDiff) {
        SimplifiedDiff that = (SimplifiedDiff) o;
        return this.kind.equals(that.kind)
            && this.details.equals(that.details);
      } else {
        return false;
      }
    }

    @Override
    public int hashCode() {
      return Objects.hash(kind, details);
    }
  }
}
