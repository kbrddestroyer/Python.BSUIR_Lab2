from connectors.connector_base import get_global_connector, g_connector


def test_ConnectorBase__get_global_connector():
    get_global_connector()

    assert g_connector
