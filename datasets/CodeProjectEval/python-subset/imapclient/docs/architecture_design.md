# Architecture Design

Below is a text-based representation of the file tree.

``` bash
├── imapclient
│   ├── config.py
│   ├── datetime_util.py
│   ├── exceptions.py
│   ├── fixed_offset.py
│   ├── imap4.py
│   ├── imapclient.py
│   ├── imap_utf7.py
│   ├── __init__.py
│   ├── interact.py
│   ├── response_lexer.py
│   ├── response_parser.py
│   ├── response_types.py
│   ├── testable_imapclient.py
│   ├── tls.py
│   ├── typing_imapclient.py
│   ├── util.py
│   └── version.py
```

`config.py` :

- `getenv(name: str, default: Optional[str]) -> Optional[str]`: Retrieves an environment variable prefixed with "imapclient_", returning the given default if not set.

- `get_config_defaults() -> Dict[str, Any]`: Returns a dictionary of default configuration values for IMAP connection parameters, sourcing credentials from environment variables where available.

- `parse_config_file(filename: str) -> argparse.Namespace`: Parses an INI-format configuration file to extract IMAP connection settings, returning a namespace that includes a DEFAULT section and any alternate named sections.

- `get_string_config_defaults() -> Dict[str, str]`: Converts boolean and None-valued defaults from `get_config_defaults()` into string representations suitable for use with `configparser`.

- `refresh_oauth2_token(hostname: str, client_id: str, client_secret: str, refresh_token: str) -> str`: Contacts the OAuth2 provider (e.g., Google or Yahoo) to refresh an access token using the provided credentials and refresh token.

- `get_oauth2_token(hostname: str, client_id: str, client_secret: str, refresh_token: str) -> str`: Returns a cached or newly refreshed OAuth2 access token for the given set of credentials, caching tokens to avoid redundant refresh requests.

- `create_client_from_config(conf: argparse.Namespace, login: bool = True) -> imapclient.IMAPClient`: Instantiates and optionally logs in an `IMAPClient` using connection settings from the provided configuration namespace.

`datetime_util.py` :

- `parse_to_datetime(timestamp: bytes, normalise: bool = True) -> datetime`: Converts an IMAP datetime string (as bytes) into a Python `datetime` object, optionally normalizing it to local system time and stripping timezone info.

- `datetime_to_native(dt: datetime) -> datetime`: Converts a timezone-aware `datetime` to the system’s local time and returns it as a timezone-naive `datetime`.

- `datetime_to_INTERNALDATE(dt: datetime) -> str`: Formats a `datetime` object into an IMAP-compatible INTERNALDATE string (e.g., "08-May-2010 16:03:09 +0200"), using the system timezone if none is set.

- `format_criteria_date(dt: datetime) -> bytes`: Formats a `datetime` object as a date string suitable for IMAP search criteria (e.g., "08-May-2010") and returns it as ASCII-encoded bytes.

`fixed_offset.py` :

- `FixedOffset(minutes: float)`: A timezone class representing a fixed offset from UTC in minutes, implementing the `datetime.tzinfo` interface.

  - `utcoffset(_: Optional[datetime.datetime]) -> datetime.timedelta`: Returns the fixed offset from UTC as a `timedelta`.
  - `tzname(_: Optional[datetime.datetime]) -> str`: Returns the timezone name in the format "+HHMM" or "-HHMM".
  - `dst(_: Optional[datetime.datetime]) -> datetime.timedelta`: Returns a zero `timedelta`, as this timezone has no daylight saving time.
  - `for_system() -> FixedOffset`: A class method that returns a `FixedOffset` instance corresponding to the system’s current local timezone, accounting for daylight saving time if active.

`imap_utf7.py` :

- `encode(s: Union[str, bytes]) -> bytes`: Encodes a Unicode string into IMAP-modified UTF-7 format (using `&` as the shift character), returning ASCII bytes; non-string input is returned unchanged.

- `decode(s: Union[bytes, str]) -> str`: Decodes a byte string encoded in IMAP-modified UTF-7 back to a Unicode string; non-bytes input is returned unchanged.

- `base64_utf7_encode(buffer: List[str]) -> bytes`: Encodes a list of non-ASCII Unicode characters into a modified Base64 representation using UTF-16BE and replacing `/` with `,`, as required by IMAP UTF-7.

- `base64_utf7_decode(s: bytearray) -> str`: Decodes a modified Base64 byte sequence (with `,` instead of `/`) from IMAP UTF-7 back to a Unicode string by converting it to standard UTF-7 format and decoding.

`imap4.py` :

- `IMAP4WithTimeout(address: str, port: int, timeout: Optional[float])`: A subclass of `imaplib.IMAP4` that supports configurable socket timeout during connection.

  - `open(host: str = "", port: int = 143, timeout: Optional[float] = None) -> None`: Establishes a connection to the IMAP server using the specified host and port, ensuring consistent behavior across Python versions by using the instance’s timeout setting.
  - `_create_socket(timeout: Optional[float] = None) -> socket.socket`: Creates and returns a TCP socket connected to the IMAP server, applying the provided or instance-level timeout.

`imapclient.py` :

- `require_capability(capability)`: A decorator factory that returns a decorator which raises `CapabilityError` when the decorated IMAPClient method is called but the server does not advertise the required *capability*.

- `debug_trunc(v, maxlen)`: Return a truncated string representation of *v* when its `repr` exceeds *maxlen*, otherwise return `repr(v)`.

- `utf7_decode_sequence(seq) -> List[str]`: Decode a sequence of modified-UTF7 encoded folder/label names into Unicode strings.

- `_parse_quota(quota_rep) -> List[Quota]`: Parse a raw quota response into a list of `Quota` dataclass instances.

- `_quote(arg) -> str|bytes`: Quote a string or bytes value for safe inclusion in IMAP protocol commands (escapes backslashes and double quotes and wraps in quotes).

- `_normalise_search_criteria(criteria, charset=None) -> List[bytes]`: Convert various forms of search *criteria* (strings, ints, datetimes, nested lists) into a list of IMAP-ready bytes values; raises `InvalidCriteriaError` on empty input.

- `_normalise_sort_criteria(criteria, charset=None) -> bytes`: Produce an IMAP-style sort criteria bytes object from a string or sequence of criteria.

- `normalise_text_list(items) -> List[str]`: Convert a sequence or single value of text/bytes into a list of unicode strings.

- `seq_to_parenstr(items) -> str`: Convert a sequence (or single) text items into a parenthesised space-joined string, returning unicode.

- `seq_to_parenstr_upper(items) -> str`: Like `seq_to_parenstr` but uppercases items before joining.

- `join_message_ids(messages) -> bytes`: Convert a sequence (or single) message ids into a comma-separated bytes representation suitable for IMAP commands.

- `_maybe_int_to_bytes(val) -> bytes`: Convert an integer to ASCII-encoded bytes, otherwise call `to_bytes` on the value.

- `_parse_untagged_response(text)`: Validate and parse an IMAP untagged response line into a tuple or parsed response.

- `as_pairs(items)`: Generator that yields consecutive pairs from *items* (useful for converting flat lists to key/value pairs).

- `as_triplets(items)`: Generator that yields consecutive triplets from *items*.

- `_is8bit(data) -> bool`: Return True if *data* should be treated as an 8-bit literal (either `_literal` or contains bytes > 127).

- `_iter_with_last(items)`: Iterate `(item, is_last_bool)` over *items* (helper to detect last element).

- `debug_trunc(v, maxlen)`: (listed above) Truncate and represent debugging strings.

- `utf7_decode_sequence(seq)`: (listed above) Helper to decode multiple modified-UTF7 values.

- `Namespace(personal, other, shared)`: A lightweight tuple subclass representing IMAP namespace triplet.

  - The instance attribute `personal` is the personal namespace (property).
  - The instance attribute `other` is the other-users namespace (property).
  - The instance attribute `shared` is the shared namespace (property).

- `SocketTimeout(connect: float, read: float)`: Dataclass representing distinct socket timeouts.

  - The instance attribute `connect` (float) is the maximum wait time for establishing a connection.
  - The instance attribute `read` (float) is the maximum wait time for read/write operations.

- `MailboxQuotaRoots(mailbox: str, quota_roots: List[str])`: Dataclass representing quota-root information for a mailbox.

  - The instance attribute `mailbox` (str) is the mailbox name.
  - The instance attribute `quota_roots` (List[str]) lists associated quota roots.

- `Quota(quota_root: str, resource: str, usage: bytes, limit: bytes)`: Dataclass representing a single resource quota entry.

  - The instance attribute `quota_root` (str) is the quota root name.
  - The instance attribute `resource` (str) is the resource being limited (e.g., STORAGE).
  - The instance attribute `usage` (bytes) is the current usage value (raw as returned).
  - The instance attribute `limit` (bytes) is the quota limit value (raw as returned).

- `IMAPlibLoggerAdapter`: A `LoggerAdapter` subclass that sanitises IMAP client logging to avoid leaking authentication secrets.

  - `process(msg, kwargs)`: Redacts sensitive text (e.g. arguments to `LOGIN`/`AUTHENTICATE`) in *msg* before passing to the underlying logger.

- `_literal(bytes)`: Marker subclass of `bytes` used to indicate that the contained data must always be sent as an IMAP literal (no quoting).

- `_quoted(bytes)`: A `bytes` subclass representing a value that must be quoted in commands while keeping access to its original unquoted bytes.

  - `maybe(original: bytes) -> bytes | _quoted`: Classmethod that returns a `_quoted` instance when the original needs quoting (or the original bytes unchanged if quoting not necessary). When a `_quoted` is returned it exposes `original` (the unquoted bytes).

- `_dict_bytes_normaliser(d)`: Wraps a dictionary that may have keys in bytes or str and exposes a bytes-normalised view.

  - `iteritems() -> Iterator[(bytes, any)]`: Yield items with keys coerced to bytes.
  - `items = iteritems`: Compatibility alias.
  - `__contains__(ink) -> bool`: Return True if *ink* (bytes or str) exists in the underlying dict (tries both representations).
  - `get(ink, default=_not_present)`: Retrieve value for *ink* trying both bytes and unicode forms; raises `KeyError` if not found and no default provided.
  - `pop(ink, default=_not_present)`: Pop and return value for *ink* trying both bytes and unicode forms; raises `KeyError` if not found and no default provided.
  - `_gen_keys(k)`: Internal generator yielding both forms of key *k* (bytes and unicode).

- `IMAPClient(host: str, port: int = None, use_uid: bool = True, ssl: bool = True, stream: bool = False, ssl_context: Optional[ssl_lib.SSLContext] = None, timeout: Optional[float] = None)`: Primary class representing a connection to an IMAP server. Establishes the IMAP connection on instantiation and exposes a high-level API for IMAP operations.

  - Important instance attributes:
    - The instance attribute `host` (str) is the server hostname.
    - The instance attribute `port` (int) is the server port.
    - The instance attribute `ssl` (bool) indicates whether SSL/TLS is used.
    - The instance attribute `use_uid` (bool) controls whether UIDs are used by default.
    - The instance attribute `folder_encode` (bool) controls modified-UTF7 encoding/decoding for folder names.
    - The instance attribute `normalise_times` (bool) controls whether FETCH timestamps are normalised to local naive datetimes.
    - The instance attribute `welcome` (property) provides the server greeting message (if available).
    - The instance attribute `socket()` returns the underlying socket (for polling only).

  - Public methods (concise descriptions; preserved type hints where present):
    - `__enter__()`: Enter context manager, returning the client.
    - `__exit__(exc_type, exc_val, exc_tb)`: Exit context manager; attempts to logout/close connection cleanly.
    - `starttls(ssl_context=None)`: Upgrade connection to TLS via the STARTTLS command (requires server capability); returns server data on success.
    - `login(username: str, password: str)`: Authenticate using plain username/password; returns server response or raises `LoginError`.
    - `oauth2_login(user: str, access_token: str, mech: str = "XOAUTH2", vendor: Optional[str] = None)`: Authenticate using XOAUTH2/OAUTH2-style token mechanisms.
    - `oauthbearer_login(identity, access_token)`: Authenticate using the OAUTHBEARER mechanism (Gmail support).
    - `plain_login(identity, password, authorization_identity=None)`: Authenticate using the PLAIN SASL mechanism.
    - `sasl_login(mech_name, mech_callable)`: Authenticate using a provided SASL mechanism callable; supports multi-step stateful/ stateless mechanisms.
    - `logout()`: Logout and return the server response string.
    - `shutdown() -> None`: Close the connection without performing IMAP logout (lower-level close).
    - `enable(*capabilities)`: Activate server-side capability extensions (requires ENABLE capability); returns list of enabled extensions.
    - `id_(parameters=None)`: Send ID command to server and return parsed dictionary of server implementation fields.
    - `capabilities() -> tuple`: Return server capabilities (cached where appropriate).
    - `has_capability(capability) -> bool`: Return True if the server advertises the given capability.
    - `namespace()`: Return `(personal, other, shared)` namespace tuple (requires NAMESPACE capability).
    - `list_folders(directory="", pattern="*")`: Return list of `(flags, delimiter, name)` tuples for matching folders.
    - `xlist_folders(directory="", pattern="*")`: Execute Gmail `XLIST` (deprecated) and return `(flags, delimiter, name)` tuples (requires XLIST).
    - `list_sub_folders(directory="", pattern="*")`: Return subscribed folders (LSUB).
    - `find_special_folder(folder_flag)`: Attempt to locate a special folder (e.g., Sent, Trash) using flags and heuristics; returns folder name or `None`.
    - `select_folder(folder, readonly=False)`: Select a mailbox; returns a dict with select response keys (EXISTS, FLAGS, UIDVALIDITY, etc.).
    - `unselect_folder()`: Unselect the currently selected folder and release resources (requires UNSELECT).
    - `noop()`: Execute NOOP to retrieve server-side updates; returns command response and list of status updates.
    - `idle()`: Enter IDLE mode (server will send unsolicited updates; use `idle_check`/`idle_done` to interact) (requires IDLE).
    - `idle_check(timeout=None)`: Poll for IDLE responses; returns list of parsed untagged responses (requires IDLE).
    - `idle_done()`: Exit IDLE mode and return `(command_text, idle_responses)` parsed results (requires IDLE).
    - `folder_status(folder, what=None)`: Query STATUS for a folder and return requested items as a dict.
    - `close_folder()`: Close selected folder (without expunge) and return server response string.
    - `create_folder(folder)`: Create *folder* on server; return server response string.
    - `rename_folder(old_name, new_name)`: Rename a folder on the server; return server response string.
    - `delete_folder(folder)`: Delete a folder on the server; return server response string.
    - `folder_exists(folder) -> bool`: Return True if *folder* exists on server.
    - `subscribe_folder(folder)`: Subscribe to *folder*; return server response string.
    - `unsubscribe_folder(folder)`: Unsubscribe from *folder*; return server response string.
    - `search(criteria="ALL", charset=None)`: Search selected folder for messages matching criteria; returns list-like message id collection (supports nested criteria and date/int normalization).
    - `gmail_search(query, charset="UTF-8")`: Gmail-specific search via `X-GM-RAW` (requires `X-GM-EXT-1`).
    - `sort(sort_criteria, criteria="ALL", charset="UTF-8")`: Server-side SORT; returns sorted list of message ids (requires SORT capability).
    - `thread(algorithm="REFERENCES", criteria="ALL", charset="UTF-8")`: Return threading results (list of message-id tuples) using specified algorithm (requires THREAD=<alg> capability).
    - `get_flags(messages)`: Return flags for the given messages (wrapper around `fetch`).
    - `add_flags(messages, flags, silent=False)`: Add flags to messages; returns updated flags per message or `None` if *silent*.
    - `remove_flags(messages, flags, silent=False)`: Remove flags from messages; returns updated flags per message or `None` if *silent*.
    - `set_flags(messages, flags, silent=False)`: Set flags for messages (overwrite); returns updated flags per message or `None` if *silent*.
    - `get_gmail_labels(messages)`: Return Gmail `X-GM-LABELS` per message decoded to unicode (requires server support).
    - `add_gmail_labels(messages, labels, silent=False)`: Add Gmail labels (requires `X-GM-LABELS` support); returns updated labels or `None`.
    - `remove_gmail_labels(messages, labels, silent=False)`: Remove Gmail labels; returns updated labels or `None`.
    - `set_gmail_labels(messages, labels, silent=False)`: Set Gmail labels for messages; returns updated labels or `None`.
    - `delete_messages(messages, silent=False)`: Mark messages as deleted (adds `\\Deleted` flag); returns flags per message.
    - `fetch(messages, data, modifiers=None)`: Fetch specified *data* items for messages; returns a dict keyed by message id with parsed typed values (timestamps -> `datetime`, ENVELOPE -> `Envelope`, etc.).
    - `append(folder, msg, flags=(), msg_time=None)`: Append a message string to *folder* with optional flags and internal date; returns server APPEND response.
    - `multiappend(folder, msgs)`: Append multiple messages using MULTIAPPEND extension (message items can be strings or dicts with msg/flags/date); returns server response (requires MULTIAPPEND).
    - `copy(messages, folder)`: Copy messages to another folder; returns server COPY response string (UID-aware).
    - `move(messages, folder)`: Atomically move messages to another folder (requires MOVE capability); returns server response.
    - `expunge(messages=None)`: Expunge messages: with no arg, expunge all `\Deleted` messages; with ids (requires `use_uid`) expunge specified ids.
    - `uid_expunge(messages)`: Expunge specified message UIDs (requires UIDPLUS).
    - `getacl(folder)`: Return list of `(who, acl)` tuples describing access controls (requires ACL).
    - `setacl(folder, who, what)`: Set an ACL entry for *who* on *folder* (requires ACL); return server response string.
    - `get_quota(mailbox="INBOX")`: Return quotas for mailbox (list of `Quota` objects) (requires QUOTA).
    - `_get_quota(quota_root="")`: Low-level quota retrieval (returns list of `Quota`), exposed with underscore to indicate lower-level usage (requires QUOTA).
    - `get_quota_root(mailbox)`: Return `(MailboxQuotaRoots, List[Quota])` for the mailbox (requires QUOTA).
    - `set_quota(quotas)`: Set one or more quotas; accepts list of `Quota` objects and returns parsed server response (requires QUOTA).
    - `socket()`: Return the underlying socket object used by the IMAP connection (intended only for polling/watching, not arbitrary reads/writes).
    - `welcome` (property): Access the server greeting message if available.

`interact.py` :

- `command_line() -> argparse.Namespace`: Parses command-line arguments for connecting to an IMAP server, supporting both direct options and a configuration file. Prompts for missing compulsory credentials (host, username, password) interactively.

`response_lexer.py` :

- `TokenSource(text: List[bytes])`: A simple iterator wrapper around the `Lexer` class that provides access to the current IMAP literal during tokenization.

  - The instance attribute `current_literal` is an optional `bytes` object representing the literal associated with the current token source, if any.
  - Implements the iterator protocol to yield tokens as `bytes`.

- `Lexer(text: List[bytes])`: A lexical analyzer that tokenizes IMAP response data, handling literals and special syntax such as quoted strings and bracketed sections.

  - `__iter__(self) -> Iterator[bytes]`: Returns an iterator that yields tokens as `bytes` by processing each response record through `read_token_stream`.

- `LiteralHandlingIter(resp_record: Union[Tuple[bytes, bytes], bytes])`: Wraps an IMAP response record (which may contain a literal) and exposes its textual part for tokenization while storing the associated literal separately.

  - The instance attribute `literal` is an optional `bytes` object containing the literal data if the response record includes one; otherwise `None`.
  - The instance attribute `src_text` is the `bytes` string to be tokenized, potentially ending with a literal marker like `b"{...}"`.
  - `__iter__(self) -> "PushableIterator"`: Returns a pushable iterator over the `src_text` bytes for use by the lexer.

- `PushableIterator(it: bytes)`: An iterator over bytes that supports pushing values back onto the stream, enabling lookahead and backtracking during lexical analysis.

  - `__next__(self) -> int`: Returns the next byte (as an integer) from the underlying iterator, or from the pushed-back buffer if available.
  - `push(item: int) -> None`: Pushes a byte (as an integer) back onto the iterator so it will be returned on the next call to `__next__`.

`response_parser.py` :

- `parse_response(data: List[bytes]) -> Tuple[_Atom, ...]`: Parses raw IMAP command responses into nested tuples of appropriately typed objects (e.g., integers, strings, literals, or nested structures).

- `parse_message_list(data: List[Union[bytes, str]]) -> SearchIds`: Efficiently parses a list of message IDs from an IMAP SEARCH response, including optional MODSEQ data, and returns them as a `SearchIds` object with a `modseq` attribute if present.

- `parse_fetch_response(text: List[bytes], normalise_times: bool = True, uid_is_key: bool = True) -> defaultdict[int, _ParseFetchResponseInnerDict]`: Parses IMAP FETCH responses into a dictionary keyed by message ID (or UID if `uid_is_key=True`), where each value is a dictionary mapping FETCH attributes (e.g., `b"UID"`, `b"ENVELOPE"`) to their parsed values.

- `atom(src: TokenSource, token: bytes) -> _Atom`: Recursively parses a single IMAP token into a Python-native value (e.g., `int`, `bytes`, `None`, or nested `tuple`), handling literals, quoted strings, NIL, and parentheses.

- `parse_tuple(src: TokenSource) -> _Atom`: Parses a sequence of tokens enclosed in parentheses into a Python `tuple`, using `atom()` to interpret each element recursively.

`response_types.py` :

- `Envelope(date: Optional[datetime.datetime], subject: bytes, from_: Optional[Tuple["Address", ...]], sender: Optional[Tuple["Address", ...]], reply_to: Optional[Tuple["Address", ...]], to: Optional[Tuple["Address", ...]], cc: Optional[Tuple["Address", ...]], bcc: Optional[Tuple["Address", ...]], in_reply_to: bytes, message_id: bytes)`: A dataclass that represents the envelope structure of an email message as returned by IMAP ENVELOPE responses.

  - The instance attribute `date` is an optional `datetime.datetime` object parsed from the "Date" header.
  - The instance attribute `subject` is the raw bytes of the "Subject" header.
  - The instance attribute `from_` is an optional tuple of `Address` objects representing the "From" header.
  - The instance attribute `sender` is an optional tuple of `Address` objects for the "Sender" header.
  - The instance attribute `reply_to` is an optional tuple of `Address` objects for the "Reply-To" header.
  - The instance attribute `to` is an optional tuple of `Address` objects for the "To" header.
  - The instance attribute `cc` is an optional tuple of `Address` objects for the "Cc" header.
  - The instance attribute `bcc` is an optional tuple of `Address` objects for the "Bcc" header.
  - The instance attribute `in_reply_to` is the raw bytes of the "In-Reply-To" header.
  - The instance attribute `message_id` is the raw bytes of the "Message-Id" header.

- `Address(name: bytes, route: bytes, mailbox: bytes, host: bytes)`: A dataclass representing an individual email address, typically used within `Envelope` fields.

  - The instance attribute `name` contains the personal name (e.g., "Mary Smith").
  - The instance attribute `route` holds the SMTP source route (rarely used).
  - The instance attribute `mailbox` is the local part of the email address (before the "@").
  - The instance attribute `host` is the domain part of the email address.
  - `__str__(self) -> str`: Returns a human-readable string representation of the email address using standard email formatting.

- `SearchIds(*args: Any)`: A list subclass that holds message IDs returned by IMAP SEARCH commands and optionally stores a MODSEQ value.

  - The instance attribute `modseq` is an optional integer that holds the MODSEQ value returned by the server when the SEARCH criteria include MODSEQ (per RFC 4551).

- `BodyData(response: Tuple[_Atom, ...])`: A tuple subclass that represents parsed IMAP BODY or BODYSTRUCTURE response data, supporting both single-part and multipart messages.

  - `create(response: Tuple[_Atom, ...]) -> "BodyData"`: A class method that recursively constructs a `BodyData` instance from a raw IMAP BODY/BODYSTRUCTURE response tuple, nesting multipart sections appropriately.
  - The instance property `is_multipart` returns `True` if the body represents a multipart message (i.e., the first element is a list of parts).

`testable_imapclient.py` :

- `TestableIMAPClient()`: A subclass of `IMAPClient` that replaces the real IMAP connection with a mock for safe use in testing environments.

  - `_create_IMAP4(self) -> "MockIMAP4"`: Overrides the parent method to return a `MockIMAP4` instance instead of a real IMAP4 connection.

- `MockIMAP4(*args: Any, **kwargs: Any)`: A mock implementation of an IMAP4 connection for testing, based on `unittest.mock.Mock`, which records sent commands and simulates server interaction.

  - The instance attribute `use_uid` is a boolean flag (default `True`) indicating whether UID-based commands are used.
  - The instance attribute `sent` is a `bytes` object that accumulates all data passed to the `send()` method.
  - The instance attribute `tagged_commands` is a dictionary that tracks IMAP command tags and their associated responses (though not actively used in this minimal mock).
  - The instance attribute `_starttls_done` is a boolean flag indicating whether STARTTLS has been simulated.
  - `send(data: bytes) -> None`: Appends the given bytes to the `sent` buffer, simulating network transmission.
  - `_new_tag(self) -> str`: Returns a fixed tag string (`"tag"`) for consistent command tagging during tests.

`tls.py` :

- `wrap_socket(sock: socket.socket, ssl_context: Optional[ssl.SSLContext], host: str) -> socket.socket`: Wraps a raw socket with TLS using the provided SSL context (or a default secure context if none is given), setting the server hostname for SNI and certificate validation.

- `IMAP4_TLS(host: str, port: int, ssl_context: Optional[ssl.SSLContext], timeout: Optional[float] = None)`: An IMAP4 client class that establishes a TLS/SSL-encrypted connection to an IMAP server, adapted from `imaplib.IMAP4_SSL` but with explicit SSL context and timeout support.

  - The instance attribute `ssl_context` holds the `ssl.SSLContext` used for the TLS connection.
  - The instance attribute `_timeout` stores the connection timeout value.
  - The instance attribute `file` is a buffered binary reader (`io.BufferedReader`) used for reading server responses.
  - `open(host: str = "", port: int = 993, timeout: Optional[float] = None) -> None`: Opens a TLS-encrypted connection to the specified IMAP server and port, using the stored SSL context and timeout.
  - `read(size: int) -> bytes`: Reads up to `size` bytes from the server response stream.
  - `readline() -> bytes`: Reads a single line (terminated by newline) from the server response stream.
  - `send(data: "Buffer") -> None`: Sends raw data to the server over the TLS-encrypted socket.
  - `shutdown() -> None`: Closes the connection cleanly by invoking the parent class’s shutdown method.

`util.py` :

- `to_unicode(s: Union[bytes, str]) -> str`: Converts a bytes object to a Unicode string using ASCII decoding; if decoding fails, falls back to ignoring invalid characters and logs a warning.

- `to_bytes(s: Union[bytes, str], charset: str = "ascii") -> bytes`: Encodes a string into bytes using the specified charset (default: ASCII); returns bytes unchanged if input is already bytes.

- `assert_imap_protocol(condition: bool, message: Optional[bytes] = None) -> None`: Raises a `ProtocolError` if the given condition is false, indicating that the IMAP server returned a protocol-violating response; optionally includes a decoded server message in the error.

- `chunk(lst: _TupleAtom, size: int) -> Iterator[_TupleAtom]`: Splits a tuple into consecutive chunks of the specified size and returns an iterator over those chunks.
