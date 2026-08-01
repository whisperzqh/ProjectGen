package com.intuit.fuzzymatcher.component;

import com.intuit.fuzzymatcher.domain.Document;
import com.intuit.fuzzymatcher.domain.Element;
import com.intuit.fuzzymatcher.domain.ElementType;
import com.intuit.fuzzymatcher.domain.Match;
import com.intuit.fuzzymatcher.function.PreProcessFunction;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.CSVWriter;
import org.hamcrest.CoreMatchers;
import org.junit.Assert;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

import static com.intuit.fuzzymatcher.domain.ElementType.*;


/**
 *
 */
public class MatchServiceCheckTest {
    private static final Logger LOGGER = LoggerFactory.getLogger(MatchServiceTest.class);

    private MatchService matchService = new MatchService();


    @Test
    public void itShouldApplyMatch() {
        List<Document> inputData = new ArrayList<>();
        inputData.add(new Document.Builder("1")
                .addElement(new Element.Builder().setType(NAME).setValue("James Parker").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("123 new st. Minneapolis MN").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("(123) 234 2345").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("jparker@gmail.com").setThreshold(0.5).createElement())
                .createDocument());
        inputData.add(new Document.Builder("2")
                .addElement(new Element.Builder().setType(NAME).setValue("James").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("123 new Street, minneapolis mn").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("123-234-2345").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("james_parker@domain.com").setThreshold(0.5).createElement())
                .createDocument());

        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertEquals(2, result.size());
        Assert.assertThat(result.entrySet().stream()
                        .map(entry -> entry.getKey().getKey()).collect(Collectors.toList()),
                CoreMatchers.hasItems("1", "2"));
    }


    @Test
    public void itShouldApplyMatchWithFailure() {
        List<Document> inputData = new ArrayList<>();
        inputData.add(new Document.Builder("1")
                .addElement(new Element.Builder().setType(NAME).setValue("James Parker").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("123 new st. Minneapolis MN").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("(123) 234 2345").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("jparker@gmail.com").setThreshold(0.5).createElement())
                .createDocument());
        inputData.add(new Document.Builder("2")
                .addElement(new Element.Builder().setType(NAME).setValue("Peter Watson").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("321 john Q Hammons Street, Plano, TX - 75054").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("9091238877").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("peter.watson@domain.com").setThreshold(0.5).createElement())
                .createDocument());

        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertTrue(result.isEmpty());
    }


    @Test
    public void itShouldApplyMatchForEmptyInput() {
        List<Document> inputData = new ArrayList<>();
        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertTrue(result.isEmpty());
    }

    @Test
    public void itShouldApplyMatchForWhiteSpaceWithNoFalsePositive() {
        List<Document> inputData = new ArrayList<>();
        inputData.add(new Document.Builder("1")
                .addElement(new Element.Builder().setType(NAME).setValue("sdwet ert rdfgh, LLC").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue(" ").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("sdwet@abc.com").setThreshold(0.5).createElement())
                .createDocument());
        inputData.add(new Document.Builder("2")
                .addElement(new Element.Builder().setType(NAME).setValue("sad sdf LLC").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue(" ").createElement())
                .addElement(new Element.Builder().setType(PHONE).setWeight(2).setValue("").setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("sad@something.com").setThreshold(0.5).createElement())
                .createDocument());

        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertTrue(result.isEmpty());
    }


    @Test
    public void itShouldApplyMatchWithScoreNotMoreThanOne() {
        List<Document> inputData = new ArrayList<>();
        Document doc1 = new Document.Builder("1")
                .addElement(new Element.Builder().setType(NAME).setValue("Kapa Limited").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("123 some street, plano, texas - 75070").createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("123-456-7890").setThreshold(0.5).setWeight(2).createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("1234567890").setThreshold(0.5).setWeight(2).createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("").setWeight(2).setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("kirit@kapalimited.com").setThreshold(0.5).createElement())
                .createDocument();
        Document doc2 = new Document.Builder("2")
                .addElement(new Element.Builder().setType(NAME).setValue("ABC CORP").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("123 some street, plano, texas - 75070").createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("123-456-7890").setWeight(2).setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("1234567890").setWeight(2).setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("").setWeight(2).setThreshold(0.5).createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("kirit@nekoproductions.com").setThreshold(0.5).createElement())
                .createDocument();
        inputData.addAll(Arrays.asList(doc1, doc2));
        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertEquals(2, result.size());
        Assert.assertThat(result.entrySet().stream()
                        .map(entry -> entry.getKey().getKey()).collect(Collectors.toList()),
                CoreMatchers.hasItems("1", "2"));
        Assert.assertTrue(result.get(doc1).get(0).getResult() <= 1);
    }


    @Test
    public void itShouldApplyMatchForBalancedEmptyElements() throws FileNotFoundException {
        List<Document> inputData = new ArrayList<>();
        inputData.add(new Document.Builder("1")
                .addElement(new Element.Builder().setType(NAME).setValue("James Parker").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("").createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("").createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("jamesparker@email.com").createElement())
                .createDocument());
        inputData.add(new Document.Builder("2")
                .addElement(new Element.Builder().setType(NAME).setValue("James").createElement())
                .addElement(new Element.Builder().setType(ADDRESS).setValue("").createElement())
                .addElement(new Element.Builder().setType(PHONE).setValue("").createElement())
                .addElement(new Element.Builder().setType(EMAIL).setValue("jamesparker@email.com").createElement())
                .createDocument());

        Map<Document, List<Match<Document>>> result = matchService.applyMatch(inputData);
        Assert.assertThat(result.entrySet().stream()
                        .map(entry -> entry.getKey().getKey()).collect(Collectors.toList()),
                CoreMatchers.hasItems("1", "2"));
        Assert.assertEquals(0.75, result.entrySet().stream()
                .map(entry -> entry.getValue()).collect(Collectors.toList()).get(0).get(0).getResult(), 0.01);
    }


    @Test
    public void itShouldApplyMatchWithInteger() {
        List<Object> numbers = Arrays.asList(91, 100, 200, 152, 11, 15, 10, 200);
        List<Document> documentList1 = getTestDocuments(numbers, NUMBER, null);
        Map<Document, List<Match<Document>>> result1 = matchService.applyMatch(documentList1);
        Assert.assertEquals(6, result1.size());

        for (Map.Entry<Document, List<Match<Document>>> entry : result1.entrySet()) {
            int doc = (int) entry.getKey().getElements().iterator().next().getValue();
            List<Object> matches = entry.getValue().stream().map(m -> m.getMatchedWith().getElements().iterator().next().getValue()).collect(Collectors.toList());
            for (Object matchWith : matches) {
                int match = (int) matchWith;
                int small = Math.min(doc, match);
                int big = Math.max(doc, match);
                Assert.assertTrue(small >= (int) 0.9 * big && small <= (int) 1.1 * big);
            }
        }

        List<Document> documentList2 = getTestDocuments(numbers, NUMBER, 0.99);
        Map<Document, List<Match<Document>>> result2 = matchService.applyMatch(documentList2);
        Assert.assertEquals(2, result2.size());
    }


    @Test
    public void itShouldApplyMatchWithDate() {
        List<Object> dates = Arrays.asList(getDate("01/01/2020"), getDate("12/01/2020"), getDate("02/01/2020"));
        List<Document> documentList = getTestDocuments(dates, DATE, null);
        Map<Document, List<Match<Document>>> result = matchService.applyMatch(documentList);
        Assert.assertEquals(2, result.size());
    }

    public static Stream<Element> getOrderedElements(Set<Element> elements) {
        List<Element> l = elements.stream()
                .sorted(Comparator.comparing(ele -> ele.getElementClassification().getElementType()))
                .collect(Collectors.toList());
        return l.stream();
    }

    public static CSVReader getCSVReader(String FileName) throws FileNotFoundException {
        return new CSVReaderBuilder(
                new FileReader(MatchServiceTest.class.getClassLoader().getResource(FileName).getFile()))
                .withSkipLines(1)
                .build();
    }


    private List<Document> getTestDocuments(List<Object> values, ElementType elementType, Double neighborhoodRange) {
        AtomicInteger ai = new AtomicInteger(0);
        return values.stream().map(num -> {
            Element.Builder elementBuilder = new Element.Builder().setType(elementType).setValue(num);
            if (neighborhoodRange != null) {
                elementBuilder.setNeighborhoodRange(neighborhoodRange);
            }
            return new Document.Builder(Integer.toString(ai.incrementAndGet()))
                    .addElement(elementBuilder.createElement())
                    .createDocument();
        }).collect(Collectors.toList());
    }

    private Date getDate(String val) {
        DateFormat df = new SimpleDateFormat("MM/dd/yyyy");
        try {
            return df.parse(val);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void writeOutput(Map<String, List<Match<Document>>> result) throws IOException {
        CSVWriter writer = new CSVWriter(new FileWriter("src/test/resources/output.csv"));
        writer.writeNext(new String[]{"Key", "Matched Key", "Score", "Name", "Address", "Email", "Phone"});

        result.entrySet().stream().sorted(Map.Entry.<String, List<Match<Document>>>comparingByKey())
                .forEach(entry -> {
                    String[] keyArrs = Stream.concat(Stream.of(entry.getKey(), entry.getKey(), ""),
                            getOrderedElements(entry.getValue().stream()
                                    .map(match -> match.getData())
                                    .findFirst().get()
                                    .getElements()).map(e -> e.getValue())).toArray(String[]::new);
                    writer.writeNext(keyArrs);

                    entry.getValue().stream().forEach(match -> {
                        Document md = match.getMatchedWith();
                        String[] matchArrs = Stream.concat(Stream.of("", md.getKey(), Double.toString(match.getResult())),
                                getOrderedElements(md.getElements()).map(e -> e.getValue())).toArray(String[]::new);
                        writer.writeNext(matchArrs);
                        LOGGER.info("        " + match);
                    });
                });
        writer.close();
    }

    public static void writeOutput(Set<Set<Match<Document>>> result) throws IOException {
        CSVWriter writer = new CSVWriter(new FileWriter("src/test/resources/output.csv"));
        writer.writeNext(new String[]{"Key", "Matched Key", "Score", "Name", "Address", "Email", "Phone"});

        result.forEach(matches -> {
            String[] arr = {"Group"};
            writer.writeNext(arr);

            matches.stream().forEach(match -> {
                Document md = match.getMatchedWith();
                String[] matchArrs = Stream.concat(Stream.of("", md.getKey(), Double.toString(match.getResult())),
                        getOrderedElements(md.getElements()).map(e -> e.getValue())).toArray(String[]::new);
                writer.writeNext(matchArrs);
            });
        });
        writer.close();
    }

    private List<Document> getTestData(Function namePreProcessing,
                                       Function addressPreProcessing, double docThreshold) throws FileNotFoundException {
        return StreamSupport.stream(getCSVReader("test-data.csv").spliterator(), false).map(csv -> {
            return new Document.Builder(csv[0])
                    .addElement(new Element.Builder().setType(NAME).setValue(csv[1])
                            .setPreProcessingFunction(namePreProcessing)
                            .createElement())
                    .addElement(new Element.Builder().setType(ADDRESS).setValue(csv[2])
                            .setPreProcessingFunction(addressPreProcessing)
                            .createElement())
                    .addElement(new Element.Builder().setType(PHONE).setValue(csv[3]).createElement())
                    .addElement(new Element.Builder().setType(EMAIL).setValue(csv[4]).createElement())
                    .setThreshold(docThreshold)
                    .createDocument();
        }).collect(Collectors.toList());
    }


}
