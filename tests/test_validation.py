import pytest
from models.schemas import Transaction, Order, Chargeback, PaymentMethod, OrderItem
from datetime import datetime


def test_valid_transaction():
    t = Transaction(
        transaction_id="txn_123",
        order_id="ord_123",
        timestamp="2024-01-01T12:00:00Z",
        amount=100.0,
        currency="USD",
        status="completed",
        payment_method={"type": "credit_card", "provider": "Visa"},
        error_code=None
    )
    assert t.currency == "USD"


def test_invalid_currency():
    with pytest.raises(ValueError):
        Transaction(
            transaction_id="txn_124",
            order_id="ord_124",
            timestamp="2024-01-01T12:00:00Z",
            amount=100.0,
            currency="ABC",
            status="completed",
            payment_method={"type": "wallet", "provider": "PayPal"},
            error_code=None
        )


def test_order_total_validation():
    with pytest.raises(ValueError):
        Order(
            order_id="ord_125",
            customer_id="cust_1",
            timestamp="2024-01-01T12:00:00Z",
            total_amount=50.0,
            currency="USD",
            items=[
                OrderItem(product_id="prod_1", quantity=1, unit_price=30.0),
                OrderItem(product_id="prod_2", quantity=1, unit_price=30.0),
            ],
            payment_status="paid"
        )

# tests/test_transform.py
import pandas as pd
from pipeline.transform import match_transactions_to_orders

def test_match_amounts():
    tx = pd.DataFrame({"order_id": ["1"], "amount": [100.0]})
    od = pd.DataFrame({"order_id": ["1"], "total_amount": [100.0]})
    df = match_transactions_to_orders(tx, od)
    assert df['amount_matches'].iloc[0] is True

# tests/test_analysis.py
import pandas as pd
from pipeline.analysis import daily_transaction_metrics

def test_daily_transaction_metrics():
    df = pd.DataFrame({
        "transaction_id": ["t1", "t2"],
        "timestamp": ["2024-01-01T12:00:00Z", "2024-01-01T15:00:00Z"],
        "amount": [100.0, 150.0]
    })
    result = daily_transaction_metrics(df)
    assert result['transaction_count'].iloc[0] == 2
    assert result['transaction_total'].iloc[0] == 250.0
