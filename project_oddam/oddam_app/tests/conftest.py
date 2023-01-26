import os
import sys

import pytest

from django.test import Client

from .testutils import *

sys.path.append(os.path.dirname(__file__))



@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def set_up():
    populate_db()







