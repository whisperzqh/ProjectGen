from parsel import Selector

def test_has_class_simple() -> None:
    """Newly constructed test"""

    body = """
    <div class="primary active-item">Alpha</div>
    <div class="primary">Beta</div>
    <div class="secondary">Gamma</div>
    <div>Delta</div>
    """
    sel = Selector(text=body)

    assert [x.extract() for x in sel.xpath('//div[has-class("primary")]/text()')] == [
        "Alpha",
        "Beta",
    ]
    assert [x.extract() for x in sel.xpath('//div[has-class("secondary")]/text()')] == ["Gamma"]
    assert [x.extract() for x in sel.xpath('//div[has-class("primary","secondary")]/text()')] == []
    assert [
        x.extract() for x in sel.xpath('//div[has-class("primary","active-item")]/text()')
    ] == ["Alpha"]