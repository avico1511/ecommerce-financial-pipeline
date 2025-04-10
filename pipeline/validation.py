import json
import pandas as pd
from typing import List
from models.schemas import Transaction, Order, Chargeback

def load_transactions(file_path: str) -> List[Transaction]:
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    return [Transaction(**t) for t in raw_data]

def load_orders(file_path: str) -> List[Order]:
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    return [Order(**o) for o in raw_data]

def load_chargebacks(file_path: str) -> List[Chargeback]:
    df = pd.read_csv(file_path)
    df['dispute_date'] = pd.to_datetime(df['dispute_date'])
    df['resolution_date'] = pd.to_datetime(df['resolution_date'], errors='coerce')
    return [Chargeback(**row._asdict()) for row in df.itertuples(index=False)]
