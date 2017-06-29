"""
Settings for the logger.
These can be changed or overridden
"""

# Number of events allowed in an EventStack
# before flushing to disk
INMEM_EVENT_STACK_CAPACITY = 100000

# Max number of stacks allowed in the Manager
MAX_STACKS = 3

# Directory where logfiles are stored
LOGDIR = "log"
