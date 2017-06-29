"""
Settings for the logger.
These can be changed or overridden
"""

# Number of events allowed in an EventQueue
# before flushing to disk
INMEM_EVENT_QUEUE_CAPACITY = 100000

# Max number of queues allowed in the Manager
MAX_QUEUES = 3

# Directory where logfiles are stored
LOGDIR = "log"
