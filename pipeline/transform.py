import pandas as pd
from typing import List
from models.schemas import Transaction, Order, Chargeback

def normalize_transactions(transactions: List[Transaction]) -> pd.DataFrame:
    return pd.json_normalize([t.model_dump() for t in transactions], sep='_')

def normalize_orders(orders: List[Order]) -> pd.DataFrame:
    df = pd.json_normalize([o.model_dump() for o in orders], sep='_')
    df = df.drop(columns=[col for col in df.columns if col.startswith('items')])  # omit nested items for now
    return df

def normalize_chargebacks(chargebacks: List[Chargeback]) -> pd.DataFrame:
    return pd.DataFrame([cb.model_dump() for cb in chargebacks])

def enrich_with_chargebacks(trans_df: pd.DataFrame, cb_df: pd.DataFrame) -> pd.DataFrame:
    trans_df = trans_df.copy()
    cb_df = cb_df.rename(columns={"amount": "chargeback_amount", "status": "chargeback_status"})
    merged = pd.merge(trans_df, cb_df, how='left', on='transaction_id')
    merged['is_chargeback'] = ~merged['chargeback_status'].isna()
    return merged

def match_transactions_to_orders(trans_df: pd.DataFrame, order_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(trans_df, order_df, how='left', left_on='order_id', right_on='order_id', suffixes=('', '_order'))
    df['amount_matches'] = (df['amount'] == df['total_amount'])
    return df