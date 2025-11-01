import pytest
from query_arxiv import construct_query_url

def test_query_url_header():
    query_url = construct_query_url(category='cs.CL', title=None, author=None, abstract=None)
    assert query_url.startswith('http://export.arxiv.org/api/query?')

# Test Cases with one arg
def test_query_url_with_only_title():
    query_url = construct_query_url(title='Software+Engineering')
    assert 'ti:Software+Engineering' in query_url

# Test Cases Four (All) arguments
def test_construct_query_all_arguments():
    query_url = construct_query_url(category='cs.CL', title='Software+Engineering', author='Smith', abstract='translation')
    assert all(param in query_url for param in ['cat:cs.CL', 'ti:Software+Engineering', 'au:Smith', 'abs:translation'])

# Test Cases for ValueError

# Test Cases for assigning max_results
def test_construct_query_max_results():
    query_url = construct_query_url(category='cs.CL', max_results=200, title='language', author='Smith', abstract='translation')
    assert "max_results=200" in query_url

