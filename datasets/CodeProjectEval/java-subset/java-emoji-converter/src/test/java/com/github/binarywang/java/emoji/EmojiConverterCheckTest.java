package com.github.binarywang.java.emoji;

import org.apache.log4j.BasicConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.*;

import static org.testng.Assert.*;

public class EmojiConverterCheckTest {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    private final EmojiConverter emojiConverter = EmojiConverter.getInstance();

    @BeforeTest
    public void init(){
        BasicConfigurator.configure();
    }


    @Test
    public void testToUnicode() {
        String str = "   :smiley: :grinning: :wink:";
        String result = this.emojiConverter.toUnicode(str);
        this.logger.info(str);
        this.logger.info("EmojiConverterTest.testToUnicode()=====>");
        this.logger.info(result);
        assertEquals("🙅 🙆 💑 😃 😀 😉", result);
    }

}