import pandas as pd

def daily_transaction_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    return df.groupby('date').agg(
        transaction_count=('transaction_id', 'count'),
        transaction_total=('amount', 'sum')
    ).reset_index()

def chargeback_rate_by_payment_method(df: pd.DataFrame) -> pd.DataFrame:
    df['method'] = df['payment_method_type'] + ':' + df['payment_method_provider']
    return df.groupby('method').agg(
        total_transactions=('transaction_id', 'count'),
        chargebacks=('is_chargeback', 'sum')
    ).assign(
        chargeback_rate=lambda d: round(d['chargebacks'] / d['total_transactions'], 3)
    ).reset_index()

def failed_transaction_analysis(df: pd.DataFrame) -> pd.DataFrame:
    failed = df[df['status'] == 'failed']
    return failed.groupby(['payment_method_type', 'error_code']).size().reset_index(name='count')

def payment_method_performance(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['payment_method_type', 'status']).agg(
        total_amount=('amount', 'sum'),
        count=('transaction_id', 'count')
    ).reset_index()