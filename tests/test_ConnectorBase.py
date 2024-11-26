from src.connectors import g_connector


def test_ConnectorBase__get_global_connector():
    assert g_connector is not None
