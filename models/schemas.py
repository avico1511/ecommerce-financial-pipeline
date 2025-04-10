from pydantic import BaseModel, field_validator, ValidationInfo
from typing import List, Optional, Literal
from datetime import datetime

VALID_CURRENCIES = {"USD", "EUR", "GBP", "JPY"}
VALID_STATUSES = {"completed", "failed", "pending"}
VALID_PAYMENT_TYPES = {"credit_card", "debit_card", "wallet"}

class PaymentMethod(BaseModel):
    type: Literal["credit_card", "debit_card", "wallet"]
    provider: str

class Transaction(BaseModel):
    transaction_id: str
    order_id: str
    timestamp: datetime
    amount: float
    currency: str
    status: Literal["completed", "failed", "pending"]
    payment_method: PaymentMethod
    error_code: Optional[str]

    @field_validator("currency")
    def validate_currency(cls, v: str):
        if v not in VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}")
        return v

class Chargeback(BaseModel):
    transaction_id: str
    dispute_date: datetime
    amount: float
    reason_code: str
    status: str
    resolution_date: Optional[datetime]

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    order_id: str
    customer_id: str
    timestamp: datetime
    total_amount: float
    currency: str
    items: List[OrderItem]
    payment_status: Literal["paid", "failed", "refunded"]

    @field_validator("currency")
    def validate_currency(cls, v: str):
        if v not in VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}")
        return v

    @field_validator("total_amount")
    def validate_total_amount(cls, v: float, info: ValidationInfo):
        items = info.data.get("items")
        if items:
            calculated = round(sum(item["quantity"] * item["unit_price"] for item in items), 2)
            if round(v, 2) != calculated:
                raise ValueError(f"Total amount {v} does not match items total {calculated}")
        return v