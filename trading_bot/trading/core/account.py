from core.schemas.account import Account as AccountSchema


class Account(AccountSchema):

    def asset(self, asset: str):
        for balance in self.balances:
            if balance.asset.lower() == asset.lower():
                return balance.asset, balance.free, balance.locked

        return -1

    def total(self):
        for asset in self.balances:
            pass
