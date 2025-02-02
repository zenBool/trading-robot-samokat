from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


class CommissionRates(BaseModel):
    maker: str
    taker: str
    buyer: str
    seller: str


class Balance(BaseModel):
    asset: str
    free: float
    locked: float

    @validator('free', 'locked', pre=True)
    def convert_str_to_float(cls, value):
        if isinstance(value, str):
            return float(value)
        return value


class Account(BaseModel):
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
