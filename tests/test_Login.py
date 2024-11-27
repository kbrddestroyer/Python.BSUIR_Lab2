from src.dao import account_dao
from src.entities import account
from controllers import login


def test_Login_login():
    username = 'test'
    password = 'qwerty'
    hashed_password = account.hash_password(password)

    dao = account_dao.AccountDao.create_from_data_source(
        "account/admin", account_dao.AccountDao, True
    )

    dao.username = username
    dao.password = hashed_password

    dao.apply('account')

    credentials = login.Credentials("test", password)

    result = login.Login.try_login(credentials)

    code, entity = result

    assert code == 0
    assert entity.username == username


def test_Login_register():
    password = 'qwerty'
    username = 'test1'

    credentials = login.Credentials(username, password)

    result, acc = login.Login.try_register(credentials)

    assert result == 0
    assert acc.username == username
