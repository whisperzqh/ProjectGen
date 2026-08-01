import pytest

from tinydb import TinyDB, where, Query  
from tinydb.storages import MemoryStorage  
from tinydb.table import Document  
  
  
@pytest.fixture  
def db():  
    """Newly constructed test"""

    _db = TinyDB(storage=MemoryStorage)  
    _db.insert_multiple([  
        {'name': 'Alice', 'age': 25, 'city': 'Beijing'},  
        {'name': 'Bob', 'age': 30, 'city': 'Shanghai'},  
        {'name': 'Charlie', 'age': 35, 'city': 'Beijing'},  
        {'name': 'David', 'age': 28, 'city': 'Guangzhou'},  
        {'name': 'Eve', 'age': 32, 'city': 'Shanghai'}  
    ])  
    return _db 
  
  
def test_insert_and_count(db: TinyDB):  
    """Newly constructed test"""

    db.drop_tables()  
      
    db.insert({'product': 'laptop', 'price': 5000, 'stock': 10})  
    db.insert({'product': 'mouse', 'price': 50, 'stock': 100})  
    db.insert({'product': 'keyboard', 'price': 200, 'stock': 50})  
      
    assert db.count(where('price') > 100) == 2  
    assert db.count(where('stock') >= 50) == 2
    assert len(db) == 3  
  
  
def test_search_with_conditions(db: TinyDB):  
    """Newly constructed test"""

    results = db.search(where('age') > 30)  
    assert len(results) == 2  
      
    results = db.search(where('city') == 'Beijing')  
    assert len(results) == 2  
    assert all(doc['city'] == 'Beijing' for doc in results)  
      
    results = db.search((where('age') > 30) & (where('city') == 'Shanghai'))  
    assert len(results) == 1  
    assert results[0]['name'] == 'Eve'  
  
  
def test_update_documents(db: TinyDB):  
    """Newly constructed test"""

    updated_ids = db.update({'age': 26}, where('name') == 'Alice')  
    assert len(updated_ids) == 1  
      
    alice = db.get(where('name') == 'Alice')  
    assert alice['age'] == 26  

    db.update({'city': 'Shenzhen'}, where('age') > 30)  
    assert db.count(where('city') == 'Shenzhen') == 2  
  
  
def test_remove_documents(db: TinyDB):  
    """Newly constructed test"""

    initial_count = len(db)  
      
    removed_ids = db.remove(where('name') == 'Bob')  
    assert len(removed_ids) == 1  
    assert len(db) == initial_count - 1  
      
    db.remove(where('age') < 30)  
    assert len(db) == 2  
  
  
def test_get_single_document(db: TinyDB):  
    """Newly constructed test"""

    doc = db.get(where('name') == 'Charlie')  
    assert doc is not None  
    assert isinstance(doc, Document)  
    assert doc['age'] == 35  
    assert doc['city'] == 'Beijing'  
     
    doc_by_id = db.get(doc_id=doc.doc_id)  
    assert doc_by_id == doc  
  
  
def test_insert_multiple_with_custom_ids(db: TinyDB):  
    """Newly constructed test"""

    db.drop_tables()  
      
    docs = [  
        Document({'category': 'electronics', 'item': 'phone'}, 100),  
        Document({'category': 'electronics', 'item': 'tablet'}, 200),  
        Document({'category': 'furniture', 'item': 'chair'}, 300)  
    ]  
      
    inserted_ids = db.insert_multiple(docs)  
    assert inserted_ids == [100, 200, 300]  
      
    assert db.get(doc_id=100)['item'] == 'phone'  
    assert db.get(doc_id=200)['item'] == 'tablet'  
    assert db.get(doc_id=300)['item'] == 'chair'  
  
  
def test_upsert_operation(db: TinyDB):  
    """Newly constructed test"""

    result = db.upsert({'name': 'Alice', 'age': 27, 'city': 'Hangzhou'},   
                       where('name') == 'Alice')  
    assert len(result) == 1  
      
    alice = db.get(where('name') == 'Alice')  
    assert alice['age'] == 27  
    assert alice['city'] == 'Hangzhou'  
    
    result = db.upsert({'name': 'Frank', 'age': 40, 'city': 'Chengdu'},   
                       where('name') == 'Frank')  
    assert len(result) == 1  
    assert db.contains(where('name') == 'Frank')  
  
  
def test_contains_check(db: TinyDB):  
    """Newly constructed test"""

    assert db.contains(where('name') == 'Alice')  
    assert db.contains(where('age') == 30)  
    assert not db.contains(where('name') == 'NonExistent')  
    
    first_doc = db.all()[0]  
    assert db.contains(doc_id=first_doc.doc_id)  
    assert not db.contains(doc_id=9999)  
  
  
def test_multiple_tables(db: TinyDB):  
    """Newly constructed test"""

    users_table = db.table('users')  
    orders_table = db.table('orders')  
      
    users_table.insert({'username': 'user1', 'email': 'user1@example.com'})  
    users_table.insert({'username': 'user2', 'email': 'user2@example.com'})  
      
    orders_table.insert({'order_id': 'ORD001', 'user': 'user1', 'amount': 100})  
    orders_table.insert({'order_id': 'ORD002', 'user': 'user2', 'amount': 200})  
      
    assert len(users_table) == 2  
    assert len(orders_table) == 2  
    assert db.tables() == {'_default', 'users', 'orders'}  
    
    db.drop_table('orders')  
    assert 'orders' not in db.tables()  
    assert len(users_table) == 2  
  
  
def test_query_with_nested_fields(db: TinyDB):  
    """Newly constructed test"""

    db.drop_tables()  
      
    db.insert({  
        'user': 'john',  
        'profile': {  
            'address': {  
                'city': 'Beijing',  
                'district': 'Chaoyang'  
            },  
            'preferences': {  
                'language': 'zh-CN',  
                'theme': 'dark'  
            }  
        }  
    })  
      
    db.insert({  
        'user': 'jane',  
        'profile': {  
            'address': {  
                'city': 'Shanghai',  
                'district': 'Pudong'  
            },  
            'preferences': {  
                'language': 'en-US',  
                'theme': 'light'  
            }  
        }  
    })  
      
    User = Query()  
    
    results = db.search(User.profile.address.city == 'Beijing')  
    assert len(results) == 1  
    assert results[0]['user'] == 'john'  
      
    results = db.search(User.profile.preferences.theme == 'light')  
    assert len(results) == 1  
    assert results[0]['user'] == 'jane'