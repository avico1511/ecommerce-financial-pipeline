# README.md

## 📦 E-commerce Financial Data Pipeline

A Python-based data pipeline for processing e-commerce transaction, chargeback, and order data. Enables financial reporting and fraud analysis with validation, transformation, and key metric generation.

---

## 🛠 Setup Instructions

### Prerequisites:
- Python 3.9+

### Installation:
```bash
pip install -r requirements.txt
```

### Run Pipeline:
```bash
python pipeline/main.py
```

---

## 📑 Data Validation Rules (via Pydantic)
- **Transaction:**
  - Must contain valid `status`, `currency`, and ISO 8601 timestamps.
  - `amount` should be a float; `payment_method` must be valid.
- **Order:**
  - `total_amount` must match the sum of items.
  - `currency` and `payment_status` must be valid.
- **Chargebacks:**
  - Includes `resolution_date`, `dispute_date` parsing and optional validation.

---

## 🔄 Data Transformation Logic
- Normalize nested JSON structures (e.g., `payment_method`, `order_items`).
- Match `chargebacks` to `transactions` by `transaction_id`.
- Join `transactions` with `orders` by `order_id`.
- Flag mismatches in `amount`.

### ⚠ Currency Assumption:
All monetary values are assumed to be **in the same currency**. No currency conversion is performed. If mixed currencies are introduced, additional logic (e.g., exchange rate APIs) is needed for normalization.

---

## 📊 Financial Metrics Implemented

### 1. Daily Transaction Metrics
- Volume and value per day

### 2. Chargeback Rate by Payment Method
- Ratio of chargebacks to total transactions by payment method

### 3. Failed Transaction Analysis
- Breakdown by `error_code` and payment method

### 4. Payment Method Performance
- Total and count of transactions per method + status

---

## ☁ AWS Architecture Overview

### Components:
- **S3**: Raw data landing and transformed output
- **EventBridge**: Triggers on new file uploads
- **Lambda**: Validation, transformation logic (Python)
- **Step Functions / Glue**: Orchestration or batch processing
- **Athena / Redshift**: Analysis and reporting
- **CloudWatch**: Logs and metric monitoring
- **SNS**: Alerts on failures or job completions

### Design Highlights:
- Fully serverless, event-driven architecture
- Cost-effective scaling with pay-as-you-go services
- Clear separation of concerns: ingest → process → analyze → monitor

---

## ✅ Testing

### Run Unit Tests:
```bash
pytest tests/
```

### Coverage:
- Data validation edge cases (Pydantic models)
- Transformation logic (e.g., order amount match, chargeback enrichment)
- Metric computations (e.g., totals and ratios)

---

## 🧠 Technical Decisions

| Aspect                   | Decision                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| Data Models              | Pydantic used for strict schema validation                              |
| Language                 | Python 3.9+ for compatibility and pandas support                        |
| Transformations          | Pandas-based normalization and enrichment                               |
| Tests                   | `pytest` for clarity and extensibility                                  |
| Currency Handling        | Assumes single currency; FX not implemented                            |

---

## 📈 Scaling Considerations
- Use **Athena** for querying large datasets in-place.
- Switch to **Glue or Spark on EMR** for high-volume ETL.
- Store partitioned Parquet in S3 for performance & cost savings.
- Add **AWS Lake Formation** for security and governance if needed.
- Add **Quicksight / Tableau** for BI reporting layer.
