from accounts.models import User
from bank.models import Account


def require_account_owner(account_pk: str, user: User) -> bool:
    return Account.objects.get(pk=account_pk).owner == user
