import pytest


def pytest_addoption(parser):
    parser.addoption("--runsolr", action="store_true", help="run solr tests")


def pytest_runtest_setup(item):
    if 'solr' in item.keywords and not item.config.getoption("--runsolr"):
        pytest.skip("need --runsolr option to run")
