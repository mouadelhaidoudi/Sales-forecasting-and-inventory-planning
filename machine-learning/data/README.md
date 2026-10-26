# Machine-learning data

The CSV files are distributed in `machine-learning/data.zip` because the
uncompressed datasets are too large for normal GitHub storage. Running
`machine-learning/src/main.py` extracts the archive into this directory when
any dataset file is missing.

The extracted CSV files are intentionally ignored by Git.

`sales_train_evaluation.csv`, `calendar.csv`, and `sell_prices.csv` are the M5
competition inputs used by this learning project.

`simulated_inventory.csv` is **synthetic/simulated**, not an M5 source file. It
contains one row for every `item_id` + `store_id` pair in
`sales_train_evaluation.csv`, so it can be joined directly on those two columns.

## Simulated inventory schema

| Column | Meaning |
| --- | --- |
| `item_id`, `store_id` | Join key matching the M5 sales file. |
| `current_stock` | Simulated units currently on hand. |
| `incoming_order_qty` | Simulated units on an open supplier order; zero when no order is open. |
| `supplier_lead_time_days` | Simulated supplier lead time (2-21 days, with category-specific ranges). |
| `safety_stock` | Simulated buffer: `ceil(1.65 * recent daily sales std dev * sqrt(lead time))`. |
| `reorder_point` | Simulated threshold: expected lead-time demand plus safety stock. |
| `recent_avg_daily_sales` | Observed mean sales over the latest 28 M5 days; included to make the assumptions auditable. |
| `is_simulated` | Always `true`; explicitly distinguishes these records from observed M5 values. |

Stock is sampled around each row's reorder point. When it falls below that
point, the open order restores the reorder point plus roughly 14 days of recent
demand. Category-level lead-time ranges are 2-10 days for foods, 5-18 for
household, and 7-21 for hobbies. All randomness uses seed `20261026` by default.

Regenerate from the repository root with:

```powershell
python machine-learning/src/generate_simulated_inventory.py
```

Pass `--seed`, `--sales-file`, or `--output-file` to override the defaults.
