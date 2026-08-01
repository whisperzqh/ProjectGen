package jetbrick.template.exec.directive;

import jetbrick.template.exec.AbstractJetxTest;
import org.junit.Assert;
import org.junit.Test;

public class DirectiveForCheckTest extends AbstractJetxTest {

    @Test
    public void testForList() {
        Assert.assertEquals("", eval("#for(i:[])${i}#end"));
        Assert.assertEquals("123", eval("#for(i:[1,2,3])${i}#end"));
    }

}
