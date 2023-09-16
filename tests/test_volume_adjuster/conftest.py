import tempfile

import pytest


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture(scope="function")
def fixture_function():
    print("fixture_function: function")


@pytest.fixture(scope="class")
def fixture_class():
    print("fixture_function: class")


@pytest.fixture(scope="module")
def fixture_module():
    print("fixture_function: module")


@pytest.fixture(scope="session")
def fixture_session():
    print("fixture_function: session")
