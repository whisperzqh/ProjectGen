from parsel import Selector

def test_simple_selection() -> None:
    """New constructed test"""

    body = "<div><span id='x' data-val='3'/><span id='y' data-val='4'/></div>"
    sel = Selector(text=body)

    xl = sel.xpath("//span")
    assert len(xl) == 2
    for x in xl:
        assert hasattr(x, 'extract')

    assert sel.xpath("//span").extract() == [
        x.extract() for x in sel.xpath("//span")
    ]

    assert [x.extract() for x in sel.xpath("//span[@id='x']/@id")] == ["x"]
    assert [
        x.extract()
        for x in sel.xpath(
            "number(concat(//span[@id='x']/@data-val, //span[@id='y']/@data-val))"
        )
    ] == ["34.0"]

    assert sel.xpath("concat('test', 'data')").extract() == ["testdata"]
    assert [
        x.extract()
        for x in sel.xpath(
            "concat(//span[@id='x']/@data-val, //span[@id='y']/@data-val)"
        )
    ] == ["34"]

def test_nested_selectors() -> None:
    """Newly constructed test"""

    body = """<main>
                <section class='alpha'>
                  <ol>
                    <item>apple</item><item>banana</item>
                  </ol>
                </section>
                <section class='beta'>
                  <ol>
                    <item>cherry</item><item>date</item><item>elderberry</item>
                  </ol>
                </section>
              </main>"""

    x = Selector(text=body)
    sectbeta = x.xpath('//section[@class="beta"]')

    assert sectbeta.xpath("//item").extract() == [
        "<item>apple</item>",
        "<item>banana</item>",
        "<item>cherry</item>",
        "<item>date</item>",
        "<item>elderberry</item>",
    ]

    assert sectbeta.xpath("./ol/item").extract() == [
        "<item>cherry</item>",
        "<item>date</item>",
        "<item>elderberry</item>",
    ]

    assert sectbeta.xpath(".//item").extract() == [
        "<item>cherry</item>",
        "<item>date</item>",
        "<item>elderberry</item>",
    ]

    assert sectbeta.xpath("./item").extract() == []

