package org.mdkt.compiler;

import java.util.List;
import java.util.Map;

import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InMemoryJavaCompilerCheckTest {
	private static final Logger logger = LoggerFactory.getLogger(InMemoryJavaCompilerTest.class);

	@Rule
	public ExpectedException thrown = ExpectedException.none();

	@Test
	public void compile_WhenTypical() throws Exception {
		StringBuffer sourceCode = new StringBuffer();

		sourceCode.append("package org.mdkt;\n");
		sourceCode.append("public class HelloClass {\n");
		sourceCode.append("   public String hello() { return \"hello\"; }");
		sourceCode.append("}");

		Class<?> helloClass = InMemoryJavaCompiler.newInstance().compile("org.mdkt.HelloClass", sourceCode.toString());
		Assert.assertNotNull(helloClass);
		Assert.assertEquals(1, helloClass.getDeclaredMethods().length);
	}

}