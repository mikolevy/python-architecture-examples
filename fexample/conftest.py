import pytest
from sqlalchemy.orm import clear_mappers

from fexample.flask_app import create_app

IN_MEMORY_DB_URI = 'sqlite:///:memory:'


def override_db_config():
    from fexample import config
    config.DB_URI = IN_MEMORY_DB_URI


@pytest.fixture
def app():
    override_db_config()
    from fexample import db
    app = create_app()
    app.config['TESTING'] = True
    yield app
    clear_mappers()
    db.drop_tables()


@pytest.fixture
def session(app):
    from fexample import db
    return db.db_session


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

