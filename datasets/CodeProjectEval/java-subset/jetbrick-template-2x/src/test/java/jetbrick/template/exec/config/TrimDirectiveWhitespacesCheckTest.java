package jetbrick.template.exec.config;

import java.io.IOException;
import jetbrick.template.exec.AbstractJetxTest;
import jetbrick.template.runtime.JetTagContext;
import org.junit.Assert;
import org.junit.Test;

public class TrimDirectiveWhitespacesCheckTest extends AbstractJetxTest {

    @Test
    public void testBasic1() {
        StringBuilder sb = new StringBuilder();
        sb.append("#for(int i:range(1,10))\n");
        sb.append("    #if(for.odd)  \n");
        sb.append("${i}\n");
        sb.append("    #end\n");
        sb.append("#end");
        Assert.assertEquals("1\n3\n5\n7\n9\n", eval(sb.toString()));
    }

    

    static class Tags {
        public static void body(JetTagContext ctx) throws IOException {
            ctx.invoke();
        }
    }
}
