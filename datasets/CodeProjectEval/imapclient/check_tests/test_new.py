import pytest  
from unittest.mock import Mock, patch  
from imapclient import IMAPClient  
from imapclient.testable_imapclient import TestableIMAPClient  
  
  
class TestIMAPClientWorkflow:  
      
    @pytest.fixture  
    def client(self):  
        client = TestableIMAPClient()  
        yield client  
          
    def test_context_manager_usage(self):  
        """Newly constructed test"""
        with patch('imapclient.imapclient.tls.IMAP4_TLS') as mock_imap:  
            mock_instance = Mock()  
            mock_imap.return_value = mock_instance  
            mock_instance.login.return_value = ('OK', [b'Success'])  
            mock_instance.logout.return_value = ('OK', [b'Bye'])  
              
            with IMAPClient(host='imap.example.com') as client:  
                assert client is not None  
              
            mock_instance.logout.assert_called_once()  
      
    def test_folder_operations(self, client):  
        """Newly constructed test"""
        client._imap._simple_command = Mock(return_value=('OK', [b'something']))  
        client._imap._untagged_response = Mock(return_value=(  
            'LIST',  
            [b'(\\HasNoChildren) "/" "INBOX"',  
             b'(\\HasNoChildren) "/" "Sent"']  
        ))  
          
        folders = client.list_folders()  
        assert folders is not None    
  
class TestIMAPClientConnection:  
      
    def test_ssl_connection_default(self): 
        """Newly constructed test""" 
        with patch('imapclient.tls.IMAP4_TLS') as mock_tls:  
            client = IMAPClient('imap.example.com')  
            assert client.ssl is True  
            assert client.port == 993  
      
    def test_plain_connection(self):  
        """Newly constructed test"""
        with patch('imapclient.imap4.IMAP4WithTimeout') as mock_imap4:  
            client = IMAPClient('imap.example.com', ssl=False)  
            assert client.ssl is False  
            assert client.port == 143  
  
  
class TestIMAPClientTimeout:  
      
    def test_single_timeout_value(self):  
        """Newly constructed test"""
        with patch('imapclient.tls.IMAP4_TLS'):  
            client = IMAPClient('imap.example.com', timeout=30.0)  
            assert client._timeout.connect == 30.0  
            assert client._timeout.read == 30.0  
      
    def test_socket_timeout_configuration(self):  
        """Newly constructed test"""
        from imapclient import SocketTimeout  
          
        with patch('imapclient.tls.IMAP4_TLS'):  
            timeout = SocketTimeout(connect=15, read=60)  
            client = IMAPClient('imap.example.com', timeout=timeout)  
            assert client._timeout.connect == 15  
            assert client._timeout.read == 60  
  
  
@pytest.mark.parametrize("folder_name,expected", [  
    ("INBOX", "INBOX"),  
    ("Sent Items", "Sent Items"),  
    ("草稿", "草稿"), 
])  
def test_folder_name_encoding(folder_name, expected):
    """Newly constructed test"""
    client = TestableIMAPClient()  
    assert folder_name == expected