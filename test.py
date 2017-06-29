import shutil
import os

from manager import MANAGER
import settings
from tests import (
    test_eventstack,
    test_io,
    test_logger,
    test_manager,
    test_reader,
    test_threadsafe
)


def run_tests():
    MANAGER.reset()
    if os.path.exists(settings.LOGDIR):
        shutil.rmtree(settings.LOGDIR)
    print "Testing event stacks... ",
    test_eventstack.run_tests()
    print "OK"
    print "Testing log manager... ",
    test_manager.run_tests()
    print "NICE"
    print "Testing logger... ",
    test_logger.run_tests()
    print "COOL"
    print "Testing reader... ",
    test_reader.run_tests()
    print "AWESOME"
    print "Testing io... ",
    test_io.run_tests()
    print "IT'S WORKING"
    print "Testing (gulp) thread safety... ",
    test_threadsafe.run_tests()
    print "YES!"


if __name__ == "__main__":
    run_tests()
