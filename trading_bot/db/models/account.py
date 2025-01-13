from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class CommissionRates(Base):
    __tablename__ = "commission_rates"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    maker: Mapped[str] = mapped_column(String)
    taker: Mapped[str] = mapped_column(String)
    buyer: Mapped[str] = mapped_column(String)
    seller: Mapped[str] = mapped_column(String)

    account: Mapped["AccountModel"] = relationship(back_populates="commission_rates")


class Balance(Base):
    __tablename__ = "balances"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    asset: Mapped[str] = mapped_column(String)
    free: Mapped[str] = mapped_column(String)
    locked: Mapped[str] = mapped_column(String)

    account: Mapped["AccountModel"] = relationship(back_populates="balances")


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    maker_commission: Mapped[int] = mapped_column(Integer)
    taker_commission: Mapped[int] = mapped_column(Integer)
    buyer_commission: Mapped[int] = mapped_column(Integer)
    seller_commission: Mapped[int] = mapped_column(Integer)
    can_trade: Mapped[bool] = mapped_column(Boolean)
    can_withdraw: Mapped[bool] = mapped_column(Boolean)
    can_deposit: Mapped[bool] = mapped_column(Boolean)
    brokered: Mapped[bool] = mapped_column(Boolean)
    require_self_trade_prevention: Mapped[bool] = mapped_column(Boolean)
    prevent_sor: Mapped[bool] = mapped_column(Boolean)
    update_time: Mapped[datetime] = mapped_column(DateTime)
    account_type: Mapped[str] = mapped_column(String)
    uid: Mapped[int] = mapped_column(Integer)
    permissions: Mapped[List[str]] = mapped_column(String)

    commission_rates: Mapped[CommissionRates] = relationship(back_populates="account", uselist=False)
    balances: Mapped[List[Balance]] = relationship(back_populates="account")
