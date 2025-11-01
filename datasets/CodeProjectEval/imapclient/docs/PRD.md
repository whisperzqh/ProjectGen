# PRD Document for imapclient

## Introduction

IMAPClient is an easy-to-use, Pythonic and complete IMAP client library for Python.   
The project was created to address significant limitations in Python's standard library imaplib, which is very low-level and expects string values where lists or tuples would be more appropriate, returns server responses almost unparsed, and doesn't make good use of exceptions.   
This forces developers using imaplib to write their own fragile parsing routines and manually check return values of each call to verify success. IMAPClient was built to solve these problems while internally using imaplib as its foundation.  

## Goals

The primary goals of IMAPClient are to provide a developer-friendly IMAP interface through several key features: using natural Python types for arguments and return values, fully parsing IMAP server responses to make them readily usable, and transparently handling IMAP unique message IDs (UIDs) without requiring different methods.   
Additionally, the library aims to transparently handle escaping for internationalized mailbox names with Unicode support, manage time zones automatically even when server and client are in different zones, provide convenience methods for commonly used functionality, and raise exceptions when errors occur.  

## Features and Functionalities

The following features and functionalities are provided by the IMAPClient project:

### Connection and Session Management
- Ability to establish secure SSL/TLS connections to IMAP servers  
- Ability to establish plain text connections when needed  
- Ability to configure separate connection and read/write socket timeouts  
- Ability to use STARTTLS to upgrade plain connections to encrypted ones  
- Ability to use custom SSL contexts for certificate verification and validation  
- Ability to connect via command-based streams (e.g., SSH tunnels)  
- Ability to use context manager for automatic connection cleanup  
- Ability to cleanly logout and shutdown connections  

### Authentication Methods
- Ability to authenticate using username and password  
- Ability to authenticate using OAuth2/XOAUTH2 mechanism  
- Ability to authenticate using OAUTHBEARER mechanism (RFC 7628)  
- Ability to authenticate using PLAIN SASL mechanism  
- Ability to authenticate using custom SASL mechanisms  

### Server Capabilities and Information
- Ability to query server capabilities  
- Ability to check if server supports specific capabilities  
- Ability to enable server-side capability extensions (CONDSTORE, UTF8=ACCEPT)  
- Ability to exchange client/server identification information using ID command  
- Ability to retrieve server namespace information (personal, other, shared)  
- Ability to access server greeting message  

### Folder/Mailbox Operations
- Ability to list all available folders with flags, delimiter, and names  
- Ability to list folders using pattern matching with wildcards (* and %)  
- Ability to list subscribed folders only  
- Ability to use Gmail's XLIST command for localized folder names  
- Ability to automatically detect special folders (Sent, Trash, Drafts, etc.)  
- Ability to select folders for operations (read-write or read-only mode)  
- Ability to unselect folders without expunging deleted messages  
- Ability to create new folders  
- Ability to delete folders  
- Ability to rename folders  
- Ability to get folder status information (message counts, flags, etc.)  

### Message Search and Retrieval
- Ability to search messages using IMAP search criteria  
- Ability to use nested and complex search criteria  
- Ability to search using date/datetime objects in criteria  
- Ability to search with custom character sets  
- Ability to use Gmail-specific X-GM-RAW search syntax  
- Ability to sort messages by various criteria (ARRIVAL, CC, DATE, FROM, SIZE, SUBJECT, TO)  
- Ability to retrieve message threading information (ORDEREDSUBJECT, REFERENCES)  
- Ability to fetch message data (flags, envelope, body parts, headers, etc.)  
- Ability to fetch message data with modifiers (CHANGEDSINCE for conditional fetch)  

### Message Manipulation
- Ability to append new messages to folders with flags and timestamps  
- Ability to append multiple messages atomically using MULTIAPPEND  
- Ability to copy messages between folders  
- Ability to move messages between folders atomically  
- Ability to permanently remove deleted messages using expunge  
- Ability to selectively expunge specific messages by UID  

### Flag Management
- Ability to retrieve current flags for messages  
- Ability to add flags to messages  
- Ability to remove flags from messages  
- Ability to replace all flags on messages  
- Ability to mark messages as deleted  
- Ability to perform silent flag operations (no server response)  
- Ability to use predefined system flags (DELETED, SEEN, ANSWERED, FLAGGED, DRAFT, RECENT)  

### Gmail-Specific Extensions
- Ability to retrieve Gmail labels for messages  
- Ability to add Gmail labels to messages  
- Ability to remove Gmail labels from messages  
- Ability to replace all Gmail labels on messages  
- Ability to retrieve Gmail message IDs and thread IDs  

### Real-time Updates and Monitoring
- Ability to put server into IDLE mode for push notifications  
- Ability to check for IDLE responses without blocking  
- Ability to exit IDLE mode  
- Ability to send NOOP command for status updates and keepalive  

### Access Control and Quota Management
- Ability to retrieve ACLs (Access Control Lists) for folders  
- Ability to set ACLs for folders and users  
- Ability to retrieve quota information for mailboxes  
- Ability to retrieve quota roots for mailboxes  
- Ability to set quotas on resources (STORAGE, MESSAGES)  

### Data Type Handling and Parsing
- Ability to automatically parse server responses into Python types  
- Ability to handle message UIDs transparently (no separate methods needed)  
- Ability to automatically encode/decode internationalized folder names (modified UTF-7)  
- Ability to handle timezone conversions transparently  
- Ability to parse ENVELOPE responses into structured objects  
- Ability to convert INTERNALDATE to datetime objects  
- Ability to normalize response times to local timezone or preserve timezone info  

### Message Identifiers
- Ability to use UIDs (Unique Identifiers) by default for message operations  
- Ability to switch between UIDs and sequence numbers  
- Ability to specify message IDs as lists, integers, or IMAP range strings  

### Error Handling and Debugging
- Ability to raise exceptions on IMAP command errors  
- Ability to distinguish between different error types (abort, read-only, capability, login, protocol)  
- Ability to log IMAP protocol commands and responses  
- Ability to automatically redact passwords from logs  

### Interactive Development
- Ability to use interactive console for testing and exploration  
- Ability to configure connections via INI-format configuration files  

## Technical Constraints

- **The repository must use Python 3.7 or higher as the primary programming language**, with official support for Python versions 3.7 through 3.11  

- **The repository must be licensed under the New BSD License (3-Clause BSD License)**  

- **The repository must use Python's standard library `imaplib` module internally**  

- **The repository must use `unittest` from the Python standard library for testing**  

- **The repository must enforce code quality using Black for code formatting**  

- **The repository must enforce import ordering using isort**  

- **The repository must pass flake8 linting checks with specific configuration**  

- **The repository must use mypy for static type checking with strict type checking enabled**  

- **The repository must use pylint for Python code static checking**  

- **The repository must use Sphinx for documentation generation**  

## Requirements

### Runtime Dependencies

IMAPClient has **no external runtime dependencies**. The library relies entirely on Python's standard library.  

### Python Version

- **Python >= 3.7.0** - Minimum required Python version
- **Officially supported**: Python 3.7 through 3.11  

### Optional Dependencies

- `sphinx` - Documentation generation (can be installed via `pip install IMAPClient[doc]`) 
 

### Development Dependencies

- `sphinx==8.0.0` - Documentation generation
- `black==25.9.0` - Code formatter
- `flake8==7.3.0` - Code linter
- `isort==5.12.0` - Import sorting tool
- `mypy==1.8.0` - Static type checker
- `pylint==3.2.6` - Python code static checker
- `setuptools==72.1.0` - Package build tool  

### Testing

The project uses Python's built-in `unittest` framework for testing.  

## Usage

### Installation

Install IMAPClient using pip:  

```bash
pip install imapclient
```

### Basic Usage

**Connect and authenticate:**  

```python
from imapclient import IMAPClient

# context manager ensures the session is cleaned up
with IMAPClient(host="imap.host.org") as client:
    client.login('someone', 'secret')
    client.select_folder('INBOX')

    # search criteria are passed in a straightforward way
    # (nesting is supported)
    messages = client.search(['NOT', 'DELETED'])

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['FLAGS', 'RFC822.SIZE'])

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    for message_id, data in response.items():
        print('{id}: {size} bytes, flags={flags}'.format(
            id=message_id,
            size=data[b'RFC822.SIZE'],
            flags=data[b'FLAGS']))
```

**Search and fetch message details:**  

```python
from imapclient import IMAPClient

server = IMAPClient('imap.mailserver.com', use_uid=True)
server.login('someuser', 'somepassword')

select_info = server.select_folder('INBOX')
print('%d messages in INBOX' % select_info[b'EXISTS'])

messages = server.search(['FROM', 'best-friend@domain.com'])
print("%d messages from our best friend" % len(messages))

for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
    envelope = data[b'ENVELOPE']
    print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))

server.logout()
```

### Advanced Usage

**Use as context manager (recommended):**  

```python
import imapclient

with imapclient.IMAPClient(host="imap.foo.org") as c:
    c.login("bar@foo.org", "passwd")
    c.select_folder("INBOX")
    # Connection automatically closes when exiting the context
```

**Watch a mailbox using IDLE:**  

The IDLE extension allows receiving notifications when something changes in a mailbox, as an alternative to polling. The client connects, selects a mailbox, and enters IDLE mode where the server sends notifications.

**Configure TLS/SSL:**

Disable certificate verification (not recommended for production):  

```python
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = IMAPClient('imap.example.com', ssl_context=ssl_context)
```

Use custom CA certificate for self-signed certificates:  

```python
import ssl

ssl_context = ssl.create_default_context(cafile='/path/to/custom/ca-cert.pem')
client = IMAPClient('imap.example.com', ssl_context=ssl_context)
```

Authenticate with client certificate:  

```python
import ssl

ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain("/path/to/client_certificate.crt")
```

**Interactive shell for development:**  

```bash
# Connect with command-line arguments
python -m imapclient.interact -H <host> -u <user>

# Or use a configuration file
python -m imapclient.interact -f <config file>
```  

The connected IMAPClient instance is available as variable "c" for interactive exploration.

**Enable debug logging:**  

```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.DEBUG
)
```

## Command Line Configuration Arguments

The IMAPClient project provides an interactive IMAP shell with the following command-line options:  

```
Options:
  -H, --host TEXT          IMAP host connect to
  -u, --username TEXT      Username to login with
  -p, --password TEXT      Password to login with
  -P, --port INTEGER       IMAP port to use (default is 993 for TLS, or 143 otherwise)
  -s, --ssl                Use SSL/TLS connection (default)
  --insecure               Use insecure connection (i.e. without SSL/TLS)
  -f, --file TEXT          Config file (same as livetest)
```

## Terms/Concepts Explanation

**IMAP (Internet Message Access Protocol)**: A protocol for accessing and managing email messages on a remote mail server. IMAPClient provides a Pythonic interface to interact with IMAP servers, parsing responses and handling complexities transparently.  

**UID (Unique Identifier)**: Persistent integer identifiers assigned to each message by the IMAP server that remain stable across sessions and don't change when folders are expunged. IMAPClient uses UIDs by default instead of sequence numbers for reliable message identification.  

**Message Sequence Number**: Temporary message identifiers where messages in a folder are numbered from 1 to N. These numbers don't persist between sessions and may be reassigned after operations like expunge, making them less reliable than UIDs.  

**Message Flags**: Zero or more flags that indicate properties of a message or track client-side data. Standard flags include `\Deleted`, `\Seen`, `\Answered`, `\Flagged`, `\Draft`, and `\Recent` (read-only).  

**IMAP UTF-7**: A modified UTF-7 encoding scheme specified by RFC 3501 for folder names, allowing arbitrary Unicode characters in mailbox names. IMAPClient automatically encodes and decodes folder names using this format, with special handling for the ampersand character.  

**Envelope**: A parsed structure containing email header information including date, subject, from, sender, reply-to, to, cc, bcc, in-reply-to, and message-id fields. Returned as a dataclass with properly typed fields when fetching ENVELOPE data.  

**Address**: A dataclass representing an email address with fields for name (personal name), route (SMTP source route), mailbox (local part before @), and host (domain name). Used within Envelope structures to represent email addresses.  

**IDLE**: An IMAP extension (RFC 2177) that allows the server to send unsolicited notifications about mailbox changes to the client, enabling real-time updates without polling. The client enters IDLE mode and waits for server notifications until issuing a DONE command.  

**Capabilities**: A list of features and extensions supported by the IMAP server, such as IDLE, SORT, THREAD, CONDSTORE, etc. IMAPClient can query and check for specific capabilities before using extension features.  

**FETCH**: An IMAP command for retrieving message data and metadata such as flags, envelope, body structure, internal date, and message content. IMAPClient's fetch method returns a dictionary indexed by message ID with parsed and typed values.  

**Folder/Mailbox**: A container for organizing email messages on the IMAP server. Messages exist within folders, and operations like search and fetch act on the currently selected folder.  

**MODSEQ (Modification Sequence)**: A per-message attribute that increases each time a message is modified, enabling efficient synchronization by allowing clients to fetch only messages changed since a specific sequence number. Part of the CONDSTORE extension (RFC 4551).  

**CONDSTORE**: An IMAP extension (RFC 4551) that must be explicitly enabled and provides modification sequence tracking for efficient delta synchronization. When enabled, select_folder returns HIGHESTMODSEQ and search/fetch can use MODSEQ-based criteria.  

**Namespace**: The organizational structure of folders on an IMAP server, divided into personal, other users', and shared namespaces. Each namespace has a prefix and hierarchy delimiter for folder naming conventions.  

**System Flags**: Predefined IMAP flags with special meaning: `\Deleted` (marked for deletion), `\Seen` (has been read), `\Answered` (has been replied to), `\Flagged` (marked as important), `\Draft` (incomplete message), and `\Recent` (arrived since last session, read-only).  

**Special Folders**: Standardized folder names defined in RFC 6154 for common purposes like `\Sent`, `\Drafts`, `\Trash`, `\Junk`, `\Archive`, and `\All`. Different IMAP providers may use different actual names for these standard functions.  

**SSL/TLS**: Encryption protocols used to secure the connection between client and IMAP server. IMAPClient uses SSL by default with certificate verification and hostname checking enabled, supporting both direct SSL connections and STARTTLS upgrade.  

**SocketTimeout**: A configuration object with separate timeout values for connection establishment and read/write operations, allowing fine-grained control over network timeout behavior.  

**Quota**: Resource limits on IMAP mailboxes, typically for storage (bytes) or message count. IMAPClient can query quota information including current usage and maximum allowed limits through GETQUOTA commands.  

**SASL (Simple Authentication and Security Layer)**: An authentication framework supporting various mechanisms like PLAIN, OAUTH2, OAUTHBEARER, and others. IMAPClient provides methods for different SASL mechanisms with extensible custom mechanism support.  
