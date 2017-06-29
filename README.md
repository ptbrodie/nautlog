# nautlog
A threadsafe transactional logger

## Logging
nautlog exposes a very simple interface for logging at priority and transactionally.
```python
from logger import Logger

# log a message at the default priority of 1
logger = Logger()
logger.log("my message")

# log a message at an elevated priority
logger = Logger(10)
logger.log("high priority message here!")

# log messages transactionally
logger = Logger()
logger.log_t("message 1")     # add messages to transaction with log_t
logger.log_t("message 2")
logger.log_t("last message")
logger.commit()

# log messages on multiple lines
logger = Logger()
logger.log_t("nice ")
logger.log_t("message ")
logger.log_t("friend")
logger.commit_whole()    # commits 'nice message friend' as one event
```

## Reading Logs
You can either specify a priority at which to read, or read all messages by priority and timestamp
```python
from reader import Reader

# read the most recent message at priority 10
reader = Reader(10)
reader.get()

# read the messages in priority order and chronologically
reader = Reader()
reader.get()
reader.get()

# read messages 1000 messages at once
reader = Reader()
for event in reader.get_all(1000):
    print event.message
```

## Notes
### 1) Specifying Priority:
You can specify the priority of the logger by passing a priority to the constructor. This way you can use multiple loggers with different priorities in the same block of code.
```python
lo = Logger(1)
hi = Logger(10)
lo.log("hello")    # log at low priority
hi.log("goodbye")  # log at higher priority.
```
### 2) Multiple messages over multiple lines:
Two things here:
- "Transactional logging" allows a user to log in bulk. Buffer messages in memory then acquire a lock and commit them all at once.
- Multiple line logging: buffer messages in memory then concatenate them and commit them as one event.
```python
logger = Logger()
logger.log_t("a ")
logger.log_t("message")
logger.commit_whole()   # logs 'a message'
```
### 3) Resource constraints:
The logger uses a setting `INMEM_EVENT_STACK_CAPACITY` to decide when it should clear memory and persist to disk. When a stack reaches capacity it flushes its contents in batches to files on disk. These can be read later by the reader. 
### 4) Message Decoration:
The logger implements an `Event` class that is used to store messages along with metadata.

