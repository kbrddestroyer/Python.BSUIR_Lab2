import pytest

from src.dao import account_dao
from src.entities import account
from controllers import login
from connectors import g_connector


@pytest.fixture
def fake_login(monkeypatch, username='test', password='qwerty'):
    hashed_password = account.hash_password(password)
    credentials = login.Credentials(username, password)

    dao = account_dao.AccountDao({'username': username,  'password': hashed_password})
    dao.apply('account')

    return credentials


def test_Login_login(fake_login):
    credentials = fake_login
    result = login.Login.try_login(credentials)

    code, entity = result

    assert code == 0
    assert entity.username == credentials.username


def test_Login_register():
    password = 'qwerty'
    username = 'test1'

    credentials = login.Credentials(username, password)

    result, acc = login.Login.try_register(credentials)

    assert result == 0
    assert acc.username == username
