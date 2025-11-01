import os
import csv
from query_arxiv import save_to_csv 

def test_file_written(tmpdir):
    file_name = f"{tmpdir}/some_file.csv"
    papers = [{'id': "1", 'name': 'Test Paper'}]
    save_to_csv(papers, file_name)
    
    # Check if file was written
    assert os.path.isfile(file_name)

    # Check the content of the file
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        assert [row for row in reader] == papers

