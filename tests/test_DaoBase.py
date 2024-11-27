import pytest

from src.dao import account_dao


@pytest.mark.parametrize(
    'initial', [
        {},
        {
            'username': 'test',
            'password': 'test'
        }
    ]
)
def test_DaoBase_createDaoBaseFromAccount(initial):
    account = account_dao.AccountDao(initial)

    assert account

    for k, v in initial.items():
        assert getattr(account, k) == v
