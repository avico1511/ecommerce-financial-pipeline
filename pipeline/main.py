from pipeline.validation import load_transactions, load_orders, load_chargebacks
from pipeline.transform import normalize_transactions, normalize_orders, normalize_chargebacks, enrich_with_chargebacks, match_transactions_to_orders
from pipeline.analysis import daily_transaction_metrics, chargeback_rate_by_payment_method, failed_transaction_analysis, payment_method_performance

TRANSACTIONS_FILE = 'data/transactions.json'
ORDERS_FILE = 'data/orders.json'
CHARGEBACKS_FILE = 'data/chargebacks.csv'

def main():
    # Load & validate
    transactions = load_transactions(TRANSACTIONS_FILE)
    orders = load_orders(ORDERS_FILE)
    chargebacks = load_chargebacks(CHARGEBACKS_FILE)

    # Normalize
    trans_df = normalize_transactions(transactions)
    order_df = normalize_orders(orders)
    cb_df = normalize_chargebacks(chargebacks)

    # Enrich & join
    enriched_df = enrich_with_chargebacks(trans_df, cb_df)
    full_df = match_transactions_to_orders(enriched_df, order_df)

    # Analysis
    print("\nDaily Transaction Metrics:\n", daily_transaction_metrics(full_df))
    print("\nChargeback Rates by Payment Method:\n", chargeback_rate_by_payment_method(full_df))
    print("\nFailed Transaction Analysis:\n", failed_transaction_analysis(full_df))
    print("\nPayment Method Performance:\n", payment_method_performance(full_df))

if __name__ == "__main__":
    main()