package jetbrick.template.exec.invoker;

import jetbrick.template.Errors;
import jetbrick.template.exec.AbstractJetxTest;
import jetbrick.template.runtime.InterpretException;
import org.junit.Assert;
import org.junit.Test;

public class VoidCheckTest extends AbstractJetxTest {


    @Test
    public void testListGet3() {
        thrown.expect(InterpretException.class);
        thrown.expectMessage(Errors.EXPRESSION_INDEX_IS_VOID);

        eval("${[1,2,3][Thread::yield()]}");
    }
}
