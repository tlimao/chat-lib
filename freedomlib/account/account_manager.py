import uuid
from freedomlib.account.account import Account
from freedomlib.account.account_info import AccountInfo
from freedomlib.account.account_repository import AccountRepository
from freedomlib.account.error.account_not_created_error import AccountNotCreatedError
from freedomlib.account.error.account_not_deleted_error import AccountNotDeletedError
from freedomlib.account.error.account_not_found_error import AccountNotFoundError


class AccountManager:
    
    def __init__(self, account_repository: AccountRepository) -> None:
        self._account_repository: AccountRepository = account_repository

    def get_account(self, account_id: str) -> Account:
        try:
            account: Account = self._account_repository.get(account_id)

            return account
        
        except Exception as e:
            raise AccountNotFoundError(f"Account not found: {e}")

    def get_account_by_email(self, email: str) -> Account:
        try:
            account: Account = self._account_repository.get_by_email(email)

            return account
        
        except Exception as e:
            raise AccountNotFoundError(f"Account not found: {e}")

    def create_account(self, account_info: AccountInfo) -> Account:
        try:
            account: Account = Account(
                id=str(uuid.uuid4()),
                nick=account_info.nick,
                email=account_info.email)
            
            self._account_repository.save(account)
            
            return account
        except Exception as e:
            raise AccountNotCreatedError(f"Account not created: {e}")

    def delete_account(self, account_info: AccountInfo) -> None:
        try:
            self._account_repository.delete(account_info.id)
        
        except Exception as e:
            raise AccountNotDeletedError(f"Account not deleted: {e}")