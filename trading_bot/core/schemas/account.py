from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CommissionRates(BaseModel):
    maker: str
    taker: str
    buyer: str
    seller: str


class Balance(BaseModel):
    asset: str
    free: str
    locked: str


class AccountSchema(BaseModel):
    maker_commission: int = Field(..., alias="makerCommission")
    taker_commission: int = Field(..., alias="takerCommission")
    buyer_commission: int = Field(..., alias="buyerCommission")
    seller_commission: int = Field(..., alias="sellerCommission")
    commission_rates: CommissionRates = Field(..., alias="commissionRates")
    can_trade: bool = Field(..., alias="canTrade")
    can_withdraw: bool = Field(..., alias="canWithdraw")
    can_deposit: bool = Field(..., alias="canDeposit")
    brokered: bool
    require_self_trade_prevention: bool = Field(..., alias="requireSelfTradePrevention")
    prevent_sor: bool = Field(..., alias="preventSor")
    update_time: datetime = Field(..., alias="updateTime")
    account_type: str = Field(..., alias="accountType")
    balances: List[Balance]
    permissions: List[str]
    uid: int

    class Config:
        allow_population_by_field_name = True
