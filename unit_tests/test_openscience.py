import os
import tempfile

import pytest

from open_science import create_app, db


def init_db():
    db.create_all()
    db.session.commit()


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert rv.data is not None


def test_generate_db(client):
    rv = client.get('/t')
    assert rv.data is not None


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_logout(client):
    """Make sure login and logout works."""

    email = 'shayla.jackson@email.com'
    password = 'QWerty12#$%'

    rv = login(client, email, password)
    rv = logout(client)
    rv = login(client, f"{email}x", password)
    rv = login(client, email, f'{password}x')
