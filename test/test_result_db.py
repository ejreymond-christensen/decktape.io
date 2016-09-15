from decktape_io.result_db import ResultDB
import pymongo
import pytest
import uuid


@pytest.fixture()
def single_use_db():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['decktape_io_unittests']
    yield ResultDB(db)
    client.drop_database(db)


@pytest.fixture(scope='module')
def db():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['decktape_io_unittests']
    yield ResultDB(db)
    client.drop_database(db)


def test_empty_on_construction(single_use_db):
    assert len(list(single_use_db)) == 0


def test_create_adds_entry(db):
    original_size = len(list(db))
    db.create(uuid.uuid1(), 'http://example.com')
    assert len(list(db)) == original_size + 1