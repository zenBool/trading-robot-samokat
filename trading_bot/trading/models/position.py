from pydantic import BaseModel


class Position(BaseModel):
    symbol: str
    side: str
    price: float
    quantity: float
    stop_loss: float
    take_profit: float
    status: str
    order_id: str
    created_at: int
    updated_at: int

    class Config:
        arbitrary_types_allowed = True
