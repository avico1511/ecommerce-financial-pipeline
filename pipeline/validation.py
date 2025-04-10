import json
import pandas as pd
from typing import List
from models.schemas import Transaction, Order, Chargeback

def load_transactions(file_path: str) -> List[Transaction]:
    """
    Loads transaction data from a JSON file and converts it into a list of Transaction objects.

    Args:
        file_path (str): The path to the JSON file containing transaction data.

    Returns:
        List[Transaction]: A list of Transaction objects.
    """
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    return [Transaction(**t) for t in raw_data]

def load_orders(file_path: str) -> List[Order]:
    """
    Loads order data from a JSON file and converts it into a list of Order objects.

    Args:
        file_path (str): The path to the JSON file containing order data.

    Returns:
        List[Order]: A list of Order objects.
    """
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    return [Order(**o) for o in raw_data]

def load_chargebacks(file_path: str) -> List[Chargeback]:
    """
    Loads chargeback data from a CSV file and converts it into a list of Chargeback objects.

    Args:
        file_path (str): The path to the CSV file containing chargeback data.

    Returns:
        List[Chargeback]: A list of Chargeback objects.
    """
    df = pd.read_csv(file_path)
    df['dispute_date'] = pd.to_datetime(df['dispute_date'])
    df['resolution_date'] = pd.to_datetime(df['resolution_date'], errors='coerce')
    return [Chargeback(**row._asdict()) for row in df.itertuples(index=False)]