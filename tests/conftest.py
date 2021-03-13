import tempfile
import pytest
from config import Config
from app.models import JobPosting, Resume, CoverLetter
from app import create_app
from app import db as _db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('tests.settings')

    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # close DB connection
    _db.session.close()
    _db.drop_all()

