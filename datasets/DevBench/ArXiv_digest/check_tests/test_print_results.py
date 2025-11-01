from query_arxiv import print_results

def test_print_papers(capfd):
    papers = [
        {
            "title": "Paper 1",
            "authors": "Author 1",
            "abstract": "Abstract 1 " * 50,  # repeating to ensure it's long enough
            "published": "Date 1",
            "link": "Link 1"
        }
    ]
    print_results(papers)
    captured = capfd.readouterr()  # Capture the print output
    
    assert "Paper 1" in captured.out
    assert "Author 1" in captured.out
    assert "Abstract 1" in captured.out
    assert "Date 1" in captured.out
    assert "Link 1" in captured.out

