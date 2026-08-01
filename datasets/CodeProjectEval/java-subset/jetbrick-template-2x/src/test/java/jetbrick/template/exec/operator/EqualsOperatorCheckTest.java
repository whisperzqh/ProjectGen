package jetbrick.template.exec.operator;

import jetbrick.template.exec.AbstractJetxTest;
import org.junit.Assert;
import org.junit.Test;

public class EqualsOperatorCheckTest extends AbstractJetxTest {


    @Test
    public void testCompare() {
        Assert.assertEquals("1", eval("${(0==0)?1:0}"));
        Assert.assertEquals("1", eval("${(0D==0.0F)?1:0}"));
        Assert.assertEquals("1", eval("${(0D==0L)?1:0}"));
        Assert.assertEquals("1", eval("${(1!=0)?1:0}"));
        Assert.assertEquals("1", eval("${(1>0d)?1:0}"));
        Assert.assertEquals("1", eval("${(1>=1)?1:0}"));
        Assert.assertEquals("1", eval("${(1f>=0)?1:0}"));
        Assert.assertEquals("1", eval("${(0<1)?1:0}"));
        Assert.assertEquals("1", eval("${(0<=1)?1:0}"));
        Assert.assertEquals("1", eval("${(0<=0)?1:0}"));
    }

    
}
