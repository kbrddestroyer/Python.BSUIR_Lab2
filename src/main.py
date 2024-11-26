"""
Entrypoint
"""

from connectors import g_connector
from connectors import connector_base
from dao import dao_base
from dao import account_dao


def main():
    dao = account_dao.AccountDao.create_from_data_source('account', dao_base.DaoBase)
    print(dao)

    dao['username'] = 'admin'
    dao['password'] = 'qwerty123'

    dao.apply('account')


if __name__ == "__main__":
    main()
