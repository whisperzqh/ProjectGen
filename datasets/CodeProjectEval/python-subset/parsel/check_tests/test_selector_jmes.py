from parsel import Selector

def test_json_has_html() -> None:
    """Newly constructed test"""

    data = """
    {
        "payload": [
            {
                "title": "X",
                "score": "x"
            },
            {
                "title": {
                    "level": 25
                },
                "score": "y"
            },
            {
                "title": "Z",
                "score": "z"
            },
            {
                "title": "<span>X</span>",
                "score": "<section>z</section>"
            }
        ],
        "markup": "<section><span>p<br>q</span>r</section><section><span>s</span>t<em>u</em></section>"
    }
    """
    sel = Selector(text=data)
    assert (
        sel.jmespath("markup").get()
        == "<section><span>p<br>q</span>r</section><section><span>s</span>t<em>u</em></section>"
    )
    assert sel.jmespath("markup").xpath("//section/span/text()").getall() == ["p", "q", "s"]
    assert sel.jmespath("markup").css("section > em").getall() == ["<em>u</em>"]
    assert sel.jmespath("payload").jmespath("title.level").get() == 25


def test_html_has_json() -> None:
    """Newly constructed test"""

    html_text = """
    <article>
        <header>Data Report</header>
        <metadata>
        {
          "members": [
                        {
                                  "label": "W",
                                  "rank": 21
                        },
                        {
                                  "label": "X",
                                  "rank": 35
                        },
                        {
                                  "label": "Y",
                                  "rank": 28
                        },
                        {
                                  "label": "Z",
                                  "rank": 30
                        }
          ],
          "count": 4,
          "state": "active"
        }
        </metadata>
    </article>
    """
    sel = Selector(text=html_text)
    assert sel.xpath("//article/metadata/text()").jmespath("members[*].label").getall() == [
        "W",
        "X",
        "Y",
        "Z",
    ]
    assert sel.xpath("//article/metadata").jmespath("members[*].label").getall() == [
        "W",
        "X",
        "Y",
        "Z",
    ]
    assert sel.xpath("//article/metadata").jmespath("count").get() == 4