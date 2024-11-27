"""
Entrypoint
"""
from controllers import login


def main():
    username = input('> ')
    password = input('> ')

    credentials = login.Credentials(username, password)

    result, entity = login.Login.try_login(credentials)

    if not entity:
        print(f"Login invalid, error code: {result}")
        return

    print(f"Logged in as {entity.username}")


if __name__ == "__main__":
    main()
