from pydantic import BaseModel, field_validator, ValidationInfo
from typing import List, Optional, Literal
from datetime import datetime

VALID_CURRENCIES = {"USD", "EUR", "GBP", "JPY"}
VALID_STATUSES = {"completed", "failed", "pending"}
VALID_PAYMENT_TYPES = {"credit_card", "debit_card", "wallet"}

class PaymentMethod(BaseModel):
    """
    Represents a payment method used in a transaction.

    Attributes:
        type (Literal): The type of payment method (e.g., credit_card, debit_card, wallet).
        provider (str): The provider of the payment method (e.g., Visa, PayPal).
    """
    type: Literal["credit_card", "debit_card", "wallet"]
    provider: str

class Transaction(BaseModel):
    """
    Represents a financial transaction.

    Attributes:
        transaction_id (str): Unique identifier for the transaction.
        order_id (str): Identifier for the associated order.
        timestamp (datetime): The date and time of the transaction.
        amount (float): The monetary amount of the transaction.
        currency (str): The currency used in the transaction.
        status (Literal): The status of the transaction (e.g., completed, failed, pending).
        payment_method (PaymentMethod): The payment method used for the transaction.
        error_code (Optional[str]): An optional error code if the transaction failed.
    """
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
        """
        Validates that the currency is within the set of valid currencies.

        Args:
            v (str): The currency to validate.

        Returns:
            str: The validated currency.

        Raises:
            ValueError: If the currency is not valid.
        """
        if v not in VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}")
        return v

class Chargeback(BaseModel):
    """
    Represents a chargeback for a transaction.

    Attributes:
        transaction_id (str): The ID of the transaction being disputed.
        dispute_date (datetime): The date the chargeback was initiated.
        amount (float): The amount being disputed.
        reason_code (str): The reason code for the chargeback.
        status (str): The current status of the chargeback.
        resolution_date (Optional[datetime]): The date the chargeback was resolved, if applicable.
    """
    transaction_id: str
    dispute_date: datetime
    amount: float
    reason_code: str
    status: str
    resolution_date: Optional[datetime]

class OrderItem(BaseModel):
    """
    Represents an item in an order.

    Attributes:
        product_id (str): The ID of the product.
        quantity (int): The quantity of the product ordered.
        unit_price (float): The price per unit of the product.
    """
    product_id: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    """
    Represents a customer order.

    Attributes:
        order_id (str): Unique identifier for the order.
        customer_id (str): Identifier for the customer who placed the order.
        timestamp (datetime): The date and time the order was placed.
        total_amount (float): The total monetary amount of the order.
        currency (str): The currency used in the order.
        items (List[OrderItem]): A list of items included in the order.
        payment_status (Literal): The payment status of the order (e.g., paid, failed, refunded).
    """
    order_id: str
    customer_id: str
    timestamp: datetime
    total_amount: float
    currency: str
    items: List[OrderItem]
    payment_status: Literal["paid", "failed", "refunded"]

    @field_validator("currency")
    def validate_currency(cls, v: str):
        """
        Validates that the currency is within the set of valid currencies.

        Args:
            v (str): The currency to validate.

        Returns:
            str: The validated currency.

        Raises:
            ValueError: If the currency is not valid.
        """
        if v not in VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}")
        return v

    @field_validator("total_amount")
    def validate_total_amount(cls, v: float, info: ValidationInfo):
        """
        Validates that the total amount matches the sum of the items' total prices.

        Args:
            v (float): The total amount to validate.
            info (ValidationInfo): Validation context containing the order data.

        Returns:
            float: The validated total amount.

        Raises:
            ValueError: If the total amount does not match the calculated sum of items.
        """
        items = info.data.get("items")
        if items:
            calculated = round(sum(item["quantity"] * item["unit_price"] for item in items), 2)
            if round(v, 2) != calculated:
                raise ValueError(f"Total amount {v} does not match items total {calculated}")
        return v