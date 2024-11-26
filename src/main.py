"""
Entrypoint
"""

from connectors import g_connector
from connectors import connector_base
from dao import dao_base


def main():
    connector: connector_base.ConnectorBase = g_connector
    dao = dao_base.DaoBase({'username': 'admin', 'password': 'qwerty'})
    connector.insert('account', dao)

    init = connector.get_from('account')
    dao2 = dao_base.DaoBase(init)

    assert dao.username == dao2.username


if __name__ == "__main__":
    main()
