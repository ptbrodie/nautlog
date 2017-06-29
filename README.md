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

