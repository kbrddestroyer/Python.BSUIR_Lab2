"""
Entrypoint
"""
from connectors import g_connector
from dao import account_dao


def main():
    dao = account_dao.AccountDao.create_from_data_source(
        "account", account_dao.AccountDao
    )['admin']
    print(dao.username)

    dao["username"] = "admin"
    dao.password = "qwerty"

    print(dao.password)

    dao.apply("account")
    g_connector.finish()


if __name__ == "__main__":
    main()
