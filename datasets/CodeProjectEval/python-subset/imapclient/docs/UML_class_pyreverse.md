## UML Class Diagram

```mermaid
classDiagram
  class CapabilityError {
  }
  class IllegalStateError {
  }
  class InvalidCriteriaError {
  }
  class LoginError {
  }
  class ProtocolError {
  }
  class FixedOffset {
    dst(_: Optional[datetime.datetime]) datetime.timedelta
    for_system() 'FixedOffset'
    tzname(_: Optional[datetime.datetime]) str
    utcoffset(_: Optional[datetime.datetime]) datetime.timedelta
  }
  class IMAP4WithTimeout {
    debug : int
    file : BufferedRWPair, BufferedReader, BufferedWriter, SocketIO, TextIOWrapper
    host : str
    port : int
    sock : socket
    open(host: str, port: int, timeout: Optional[float]) None
  }
  class IMAPClient {
    AbortError
    Error
    ReadOnlyError
    folder_encode : bool
    host : str
    normalise_times : bool
    port : Optional[int]
    ssl : bool
    ssl_context : Optional[ssl_lib.SSLContext]
    stream : bool
    use_uid : bool
    welcome
    add_flags(messages, flags, silent)
    add_gmail_labels(messages, labels, silent)
    append(folder, msg, flags, msg_time)
    capabilities()
    close_folder()
    copy(messages, folder)
    create_folder(folder)
    delete_folder(folder)
    delete_messages(messages, silent)
    enable()
    expunge(messages)
    fetch(messages, data, modifiers)
    find_special_folder(folder_flag)
    folder_exists(folder)
    folder_status(folder, what)
    get_flags(messages)
    get_gmail_labels(messages)
    get_quota(mailbox)
    get_quota_root(mailbox)
    getacl(folder)
    gmail_search(query, charset)
    has_capability(capability)
    id_(parameters)
    idle()
    idle_check(timeout)
    idle_done()
    list_folders(directory, pattern)
    list_sub_folders(directory, pattern)
    login(username: str, password: str)
    logout()
    move(messages, folder)
    multiappend(folder, msgs)
    namespace()
    noop()
    oauth2_login(user: str, access_token: str, mech: str, vendor: Optional[str])
    oauthbearer_login(identity, access_token)
    plain_login(identity, password, authorization_identity)
    remove_flags(messages, flags, silent)
    remove_gmail_labels(messages, labels, silent)
    rename_folder(old_name, new_name)
    sasl_login(mech_name, mech_callable)
    search(criteria, charset)
    select_folder(folder, readonly)
    set_flags(messages, flags, silent)
    set_gmail_labels(messages, labels, silent)
    set_quota(quotas)
    setacl(folder, who, what)
    shutdown() None
    socket()
    sort(sort_criteria, criteria, charset)
    starttls(ssl_context)
    subscribe_folder(folder)
    thread(algorithm, criteria, charset)
    uid_expunge(messages)
    unselect_folder()
    unsubscribe_folder(folder)
    xlist_folders(directory, pattern)
  }
  class IMAPlibLoggerAdapter {
    process(msg, kwargs)
  }
  class MailboxQuotaRoots {
    mailbox : str
    quota_roots : List[str]
  }
  class Namespace {
    other : property
    personal : property
    shared : property
  }
  class Quota {
    limit : bytes
    quota_root : str
    resource : str
    usage : bytes
  }
  class SocketTimeout {
    connect : float
    read : float
  }
  class _dict_bytes_normaliser {
    items
    get(ink, default)
    iteritems()
    pop(ink, default)
  }
  class _literal {
  }
  class _quoted {
    original
    maybe(original)
  }
  class Lexer {
    current_source : Optional[LiteralHandlingIter]
    sources
    read_token_stream(stream_i: 'PushableIterator') Iterator[bytearray]
    read_until(stream_i: 'PushableIterator', end_char: int, escape: bool) bytearray
  }
  class LiteralHandlingIter {
    literal : NoneType, Optional[bytes]
    src_text
  }
  class PushableIterator {
    NO_MORE : object
    it
    next
    pushed : List[int]
    push(item: int) None
  }
  class TokenSource {
    current_literal : Optional[bytes]
    lex
    src
  }
  class Address {
    host : bytes
    mailbox : bytes
    name : bytes
    route : bytes
  }
  class BodyData {
    is_multipart : bool
    create(response: Tuple[_Atom, ...]) 'BodyData'
  }
  class Envelope {
    bcc : Optional[Tuple['Address', ...]]
    cc : Optional[Tuple['Address', ...]]
    date : Optional[datetime.datetime]
    from_ : Optional[Tuple['Address', ...]]
    in_reply_to : bytes
    message_id : bytes
    reply_to : Optional[Tuple['Address', ...]]
    sender : Optional[Tuple['Address', ...]]
    subject : bytes
    to : Optional[Tuple['Address', ...]]
  }
  class SearchIds {
    modseq : Optional[int]
  }
  class MockIMAP4 {
    sent : bytes
    tagged_commands : Dict[Any, Any]
    use_uid : bool
    send(data: bytes) None
  }
  class TestableIMAPClient {
  }
  class IMAP4_TLS {
    debug : int
    file : BufferedRWPair, BufferedReader, BufferedWriter, SocketIO
    host : str
    port : int
    sock
    ssl_context : Optional[ssl.SSLContext]
    open(host: str, port: int, timeout: Optional[float]) None
    read(size: int) bytes
    readline() bytes
    send(data: 'Buffer') None
    shutdown() None
  }
  TestableIMAPClient --|> IMAPClient
  Lexer --> LiteralHandlingIter : current_source
  Lexer --* TokenSource : lex

```
## UML Package Diagram

```mermaid
classDiagram
  class imapclient {
  }
  class config {
  }
  class datetime_util {
  }
  class exceptions {
  }
  class fixed_offset {
  }
  class imap4 {
  }
  class imap_utf7 {
  }
  class imapclient {
  }
  class interact {
  }
  class response_lexer {
  }
  class response_parser {
  }
  class response_types {
  }
  class testable_imapclient {
  }
  class tls {
  }
  class typing_imapclient {
  }
  class util {
  }
  class version {
  }
  imapclient --> imapclient
  imapclient --> response_parser
  imapclient --> tls
  imapclient --> version
  config --> imapclient
  datetime_util --> fixed_offset
  imapclient --> datetime_util
  imapclient --> imap_utf7
  imapclient --> response_parser
  imapclient --> util
  interact --> config
  response_lexer --> util
  response_parser --> datetime_util
  response_parser --> exceptions
  response_parser --> response_lexer
  response_parser --> response_types
  response_parser --> typing_imapclient
  response_types --> typing_imapclient
  response_types --> util
  testable_imapclient --> imapclient

```

