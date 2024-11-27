from src.connectors import g_connector
from src.dao import account_dao
from src.entities import login, account


def test_Login_login():
    password = 'qwerty'
    hashed_password = account.hash_password(password)

    dao = account_dao.AccountDao.create_from_data_source(
        "account/admin", account_dao.AccountDao, True
    )

    dao.username = "test"
    dao.password = hashed_password

    dao.apply('account')

    credentials = login.Credentials("test", password)

    login_handler = login.Login()
    result = login_handler.try_login(credentials)

    code, entity = result

    assert code == 0
    assert entity.username == "test"
