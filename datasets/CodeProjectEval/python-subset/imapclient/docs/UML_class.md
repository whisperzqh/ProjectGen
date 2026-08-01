## UML Class Diagram

```mermaid

classDiagram
    class IMAPClient {
        +str host
        +int port
        +bool use_uid
        +bool ssl
        +bool folder_encode
        +bool normalise_times
        -_imap: IMAP4
        -_timeout: SocketTimeout
        -_cached_capabilities: tuple
        -_idle_tag: str
        +__init__(host, port, use_uid, ssl, stream, ssl_context, timeout)
        +login(username, password)
        +logout()
        +select_folder(folder, readonly)
        +search(criteria, charset)
        +fetch(messages, data, modifiers)
        +capabilities()
        +list_folders(directory, pattern)
        +idle()
        +idle_check(timeout)
        +idle_done()
        +starttls(ssl_context)
        +namespace()
        +get_quota(mailbox)
        +copy(messages, folder)
        +move(messages, folder)
        +expunge(messages)
    }

    class SocketTimeout {
        +float connect
        +float read
    }

    class Namespace {
        +tuple personal
        +tuple other
        +tuple shared
    }

    class Quota {
        +str quota_root
        +str resource
        +bytes usage
        +bytes limit
    }

    class MailboxQuotaRoots {
        +str mailbox
        +List~str~ quota_roots
    }

    class IMAP4WithTimeout {
        -float _timeout
        +__init__(address, port, timeout)
        +open(host, port, timeout)
        -_create_socket(timeout)
    }

    class IMAP4_TLS {
        +SSLContext ssl_context
        -float _timeout
        +__init__(host, port, ssl_context, timeout)
        +open(host, port, timeout)
        +read(size)
        +readline()
        +send(data)
    }

    class Envelope {
        +datetime date
        +bytes subject
        +tuple from_
        +tuple sender
        +tuple reply_to
        +tuple to
        +tuple cc
        +tuple bcc
        +bytes in_reply_to
        +bytes message_id
    }

    class Address {
        +bytes name
        +bytes route
        +bytes mailbox
        +bytes host
        +__str__()
    }

    class BodyData {
        +create(response)
        +is_multipart()
    }

    class SearchIds {
        +int modseq
    }

    class TokenSource {
        +Lexer lex
        +Iterator src
        +current_literal()
        +__iter__()
    }

    class Lexer {
        +Iterator sources
        +LiteralHandlingIter current_source
        +read_until(stream_i, end_char, escape)
        +read_token_stream(stream_i)
        +__iter__()
    }

    class IMAPClientError {
    }

    class CapabilityError {
    }

    class LoginError {
    }

    class IllegalStateError {
    }

    class InvalidCriteriaError {
    }

    class ProtocolError {
    }

    IMAPClient --> SocketTimeout: uses
    IMAPClient --> IMAP4WithTimeout: creates
    IMAPClient --> IMAP4_TLS: creates
    IMAPClient --> Namespace: returns
    IMAPClient --> Quota: returns
    IMAPClient --> MailboxQuotaRoots: returns
    IMAPClient --> Envelope: returns
    IMAPClient --> BodyData: returns
    IMAPClient --> SearchIds: returns
    
    IMAP4WithTimeout --|> IMAP4: extends
    IMAP4_TLS --|> IMAP4: extends
    
    Envelope --> Address: contains
    SearchIds --|> List: extends
    BodyData --|> tuple: extends
    
    TokenSource --> Lexer: uses
    
    CapabilityError --|> IMAPClientError: extends
    LoginError --|> IMAPClientError: extends
    IllegalStateError --|> IMAPClientError: extends
    InvalidCriteriaError --|> IMAPClientError: extends
    ProtocolError --|> IMAPClientError: extends
```  

## UML Package Diagram

```mermaid

graph TD
    A["imapclient/__init__.py<br/>(Main Package)"] --> B["imapclient.py<br/>(Core Client)"]
    A --> C["response_parser.py<br/>(Response Processing)"]
    A --> D["tls.py<br/>(TLS Support)"]
    
    B --> E["imap4.py<br/>(Plain IMAP4)"]
    B --> D
    B --> F["exceptions.py<br/>(Error Handling)"]
    B --> G["response_lexer.py<br/>(Tokenization)"]
    B --> H["datetime_util.py<br/>(Date/Time Utils)"]
    B --> I["imap_utf7.py<br/>(UTF-7 Encoding)"]
    B --> C
    
    C --> J["response_types.py<br/>(Data Structures)"]
    C --> G
    C --> H
    C --> F
    
    B --> K["util.py<br/>(Utilities)"]
    K --> F
    
    L["imaplib<br/>(Python stdlib)"] -.-> E
    L -.-> D
    
    M["ssl<br/>(Python stdlib)"] -.-> D
    
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style C fill:#e1ffe1
    style D fill:#ffe1e1
    style E fill:#ffe1e1
    style F fill:#fff3e1
    style G fill:#e1ffe1
    style H fill:#f0e1ff
    style I fill:#f0e1ff
    style J fill:#e1ffe1
    style K fill:#f0e1ff
    style L fill:#f5f5f5
    style M fill:#f5f5f5
```  

