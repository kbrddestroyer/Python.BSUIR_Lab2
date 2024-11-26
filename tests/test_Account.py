from entities.account import Account


def test_Account_password():
    account = Account()

    password = 'qwerty'
    account.password = password

    assert password != account.password
