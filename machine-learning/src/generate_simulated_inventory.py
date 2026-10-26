"""Generate deterministic, simulated inventory data for the M5 item/store rows."""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from pathlib import Path


DEFAULT_SEED = 20261026
RECENT_DAYS = 28
SERVICE_FACTOR = 1.65  # roughly a 95% one-sided service level


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sales-file",
        type=Path,
        default=project_root / "machine-learning/data/sales_train_evaluation.csv",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=project_root / "machine-learning/data/simulated_inventory.csv",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def lead_time_range(category: str) -> tuple[int, int]:
    """Use simple category-level supplier profiles, expressed in days."""
    return {
        "FOODS": (2, 10),
        "HOUSEHOLD": (5, 18),
        "HOBBIES": (7, 21),
    }.get(category, (3, 21))


def generate_inventory(sales_file: Path, output_file: Path, seed: int) -> int:
    rng = random.Random(seed)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    rows_written = 0

    with sales_file.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError(f"No header found in {sales_file}")

        day_columns = [name for name in reader.fieldnames if name.startswith("d_")]
        if len(day_columns) < RECENT_DAYS:
            raise ValueError(f"Expected at least {RECENT_DAYS} daily sales columns")
        recent_columns = day_columns[-RECENT_DAYS:]

        fieldnames = [
            "item_id",
            "store_id",
            "current_stock",
            "incoming_order_qty",
            "supplier_lead_time_days",
            "safety_stock",
            "reorder_point",
            "recent_avg_daily_sales",
            "is_simulated",
        ]
        with output_file.open("w", encoding="utf-8", newline="") as destination:
            writer = csv.DictWriter(destination, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                recent_sales = [int(row[column]) for column in recent_columns]
                daily_mean = statistics.fmean(recent_sales)
                daily_std = statistics.pstdev(recent_sales)
                low, high = lead_time_range(row["cat_id"])
                lead_time = rng.randint(low, high)

                safety_stock = math.ceil(SERVICE_FACTOR * daily_std * math.sqrt(lead_time))
                reorder_point = math.ceil(daily_mean * lead_time + safety_stock)

                # Simulate inventory around 0.45-1.65 times its reorder point.
                # A small baseline preserves occasional stock for slow sellers.
                stock_target = reorder_point * rng.uniform(0.45, 1.65)
                current_stock = max(0, round(stock_target + rng.gauss(0, max(1, daily_mean))))

                # Open orders exist when stock is below the reorder point, sized
                # to restore the reorder point plus about two weeks of demand.
                if current_stock < reorder_point:
                    order_up_to = reorder_point + math.ceil(14 * daily_mean)
                    incoming_order_qty = max(0, order_up_to - current_stock)
                else:
                    incoming_order_qty = 0

                writer.writerow(
                    {
                        "item_id": row["item_id"],
                        "store_id": row["store_id"],
                        "current_stock": current_stock,
                        "incoming_order_qty": incoming_order_qty,
                        "supplier_lead_time_days": lead_time,
                        "safety_stock": safety_stock,
                        "reorder_point": reorder_point,
                        "recent_avg_daily_sales": f"{daily_mean:.3f}",
                        "is_simulated": "true",
                    }
                )
                rows_written += 1

    return rows_written


def validate_inventory(sales_file: Path, output_file: Path) -> dict[str, int]:
    """Validate keys, join coverage, labels, and basic quantity constraints."""
    with sales_file.open("r", encoding="utf-8", newline="") as source:
        sales_keys = {
            (row["item_id"], row["store_id"])
            for row in csv.DictReader(source)
        }

    inventory_keys: set[tuple[str, str]] = set()
    maxima = {"current_stock": 0, "incoming_order_qty": 0, "safety_stock": 0}
    with output_file.open("r", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            key = (row["item_id"], row["store_id"])
            if key in inventory_keys:
                raise ValueError(f"Duplicate inventory key: {key}")
            inventory_keys.add(key)

            for column in ("current_stock", "incoming_order_qty", "safety_stock", "reorder_point"):
                if int(row[column]) < 0:
                    raise ValueError(f"Negative {column} for {key}")
            lead_time = int(row["supplier_lead_time_days"])
            if not 2 <= lead_time <= 21:
                raise ValueError(f"Lead time outside 2-21 days for {key}")
            if float(row["recent_avg_daily_sales"]) < 0:
                raise ValueError(f"Negative recent sales average for {key}")
            if row["is_simulated"] != "true":
                raise ValueError(f"Missing simulated label for {key}")
            for column in maxima:
                maxima[column] = max(maxima[column], int(row[column]))

    if inventory_keys != sales_keys:
        missing = len(sales_keys - inventory_keys)
        unexpected = len(inventory_keys - sales_keys)
        raise ValueError(f"Join coverage mismatch: {missing} missing, {unexpected} unexpected")

    return {"rows": len(inventory_keys), **maxima}


def main() -> None:
    args = parse_args()
    rows = generate_inventory(args.sales_file, args.output_file, args.seed)
    checks = validate_inventory(args.sales_file, args.output_file)
    print(f"Wrote {rows:,} simulated inventory rows to {args.output_file}")
    print(f"Seed: {args.seed}; recent sales window: {RECENT_DAYS} days")
    print(
        "Validation passed: unique keys, 100% sales-key coverage, nonnegative "
        "quantities, 2-21 day lead times, and simulated labels"
    )
    print(
        "Observed maxima: "
        f"stock={checks['current_stock']}, incoming={checks['incoming_order_qty']}, "
        f"safety_stock={checks['safety_stock']}"
    )


if __name__ == "__main__":
    main()
