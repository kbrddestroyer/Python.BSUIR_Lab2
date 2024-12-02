CONNECTOR_CONFIG = "configs/connector.ini"
UI_CONFIG = "configs/ui.ini"
DAO_CONFIGS = "configs/dao/"


class TABLES:
    ACCOUNTS = "accounts"


class ACCOUNTS:
    ACCOUNT_ADMIN = 0
    ACCOUNT_WORKER = 1
    ACCOUNT_CUSTOMER = 2

    TO_STRING = {
        ACCOUNT_ADMIN: "Admin",
        ACCOUNT_WORKER: "Worker",
        ACCOUNT_CUSTOMER: "Customer"
    }


class FLAGS:
    NO_FLAGS = 0
    ACCOUNT_BLOCKED = 1

    TO_STRING = {
        NO_FLAGS: "No Flags",
        ACCOUNT_BLOCKED: "Account Blocked"
    }

    TO_BTN_LABEL = {
        NO_FLAGS: "Ban",
        ACCOUNT_BLOCKED: "Unban"
    }
