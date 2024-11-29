import pytest

from src.dao import account_dao
from src.entities import account
from controllers import account_controller
from connectors import g_connector


@pytest.fixture
def fake_login(monkeypatch):
    def call(username='test', password='qwerty'):
        hashed_password = account.hash_password(password)
        credentials = account_controller.Credentials(username, password)

        dao = account_dao.AccountDao({'username': username,  'password': hashed_password})
        dao.apply()
        return credentials

    return call


def test_AccountController_login(fake_login):
    credentials = fake_login()
    result = account_controller.AccountController.try_login(credentials)

    code, entity = result

    assert code == 0
    assert entity.username == credentials.username


def test_AccountController_register():
    password = 'qwerty'
    username = 'test1'

    credentials = account_controller.Credentials(username, password)

    result, acc = account_controller.AccountController.try_register(credentials)

    assert result == 0
    assert acc.username == username


def test_AccountController_remove(fake_login):
    credentials = fake_login(username='test2')

    result = account_controller.AccountController.try_delete(credentials)

    assert result
    result, acc = account_controller.AccountController.try_login(credentials)
    assert result != 0
    assert not acc