import os
# pylint: disable=W0212,W0613,W9015,W9016,W9011,W9012,W0401,W0614
from contextlib import contextmanager
from pathlib import Path

import pytest

from thankloganforserving.thank_logan import *

TESTS_PATH = Path(os.path.dirname(os.path.realpath(__file__)))


@contextmanager
def does_not_raise():
    """Used in 'raises' arguments for test functions.
    See:
        https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-conditional-raising
    Yields:
        None: Not sure how this works.
    """
    yield


@pytest.mark.parametrize("date,expected,raises", [])
def test_thanked_logan(date, expected, raises):
    pass
