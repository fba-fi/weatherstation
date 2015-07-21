import sys
import os

from pytest import fixture

from mock import Mock

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def pytest_addoption(parser):
    parser.addoption("--display-integration", action="store_true",
        help="run slow tests")
    parser.addoption("--receiver-integration", action="store_true",
        help="run slow tests")

def pytest_runtest_setup(item):
    if 'display_integration' in item.keywords and not item.config.getoption("--display-integration"):
        pytest.skip("need --display-integration option to run")


@fixture
def receiver(request):
    """Return receiver instance or mockup version"""

    if request.config.getoption("--receiver-integration"):
        return MicrochipReceiver()
    else:
        return Mock()
