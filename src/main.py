"""
Entrypoint
"""
from connectors import g_connector
from dao import account_dao
from entities import account, login


def main():
    dao = account_dao.AccountDao.create_from_data_source(
        "account/admin", account_dao.AccountDao, True
    )
    print(dao.username)

    dao["username"] = "admin"
    dao.password = "qwerty"

    print(dao.password)

    acc = account.Account()
    acc.from_dao(dao)

    dao = acc.to_dao()

    dao.apply("account")
    g_connector.finish()


if __name__ == "__main__":
    main()
