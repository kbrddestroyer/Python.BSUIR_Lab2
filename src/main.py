"""
Entrypoint
"""

from connectors import g_connector
from connectors import connector_base
from dao import dao_base
from dao import account_dao


def main():
    dao = account_dao.AccountDao.create_from_data_source('account', account_dao.AccountDao)
    print(dao)

    dao['username'] = 'admin'
    dao.password = 'qwerty'

    print(dao.password)

    dao.apply('account')


if __name__ == "__main__":
    main()
