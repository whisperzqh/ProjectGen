package jetbrick.template.exec.value;

import jetbrick.template.exec.AbstractJetxTest;
import org.junit.Assert;
import org.junit.Test;

public class ConstantCheckTest extends AbstractJetxTest {
   

    @Test
    public void testMap() {
        Assert.assertEquals("{}", eval("${{}}"));
        Assert.assertEquals("{name=jetbrick}", eval("${{name:'jetbrick'}}"));
        Assert.assertEquals("{name=jetbrick}", eval("${{'name':'jetbrick'}}"));
        Assert.assertEquals("{name=jetbrick, lang=java}", eval("${{name:'jetbrick', lang: 'java'}}"));
    }
}
