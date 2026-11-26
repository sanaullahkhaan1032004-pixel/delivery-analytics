"""Simulate delivery records and save them to data/deliveries.csv.

Columns: order_id, timestamp, zone, driver, volume, delay_minutes
Run:  python generate_data.py [--rows 600] [--seed 42]
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ZONES = {  # zone -> (relative order share, average extra delay in minutes)
    "North": (0.22, 4),
    "South": (0.20, 6),
    "East": (0.18, 8),
    "West": (0.15, 3),
    "Central": (0.25, 10),  # busiest zone, most congestion
}
DRIVERS = ["Ali", "Bilal", "Fatima", "Hamza", "Sana", "Usman", "Zara", "Omar"]


def simulate(n_rows: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    zone_names = list(ZONES)
    zone_probs = [ZONES[z][0] for z in zone_names]
    zones = rng.choice(zone_names, size=n_rows, p=zone_probs)

    # Timestamps: last 30 days, weighted toward working hours (8:00-21:00)
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=30)
    days = rng.integers(0, 30, n_rows)
    hours = rng.choice(np.arange(8, 21), size=n_rows)
    minutes = rng.integers(0, 60, n_rows)
    timestamps = (
        start
        + pd.to_timedelta(days, unit="D")
        + pd.to_timedelta(hours, unit="h")
        + pd.to_timedelta(minutes, unit="m")
    )

    volume = np.clip(rng.gamma(shape=2.5, scale=4.0, size=n_rows), 1, 60).round(1)

    # Delay = zone baseline + rush-hour effect + volume effect + noise (min 0)
    base = np.array([ZONES[z][1] for z in zones])
    rush = np.isin(hours, [12, 13, 18, 19]) * 6
    delay = base + rush + volume * 0.25 + rng.normal(0, 5, n_rows)
    delay = np.clip(delay - 6, 0, None).round().astype(int)

    df = pd.DataFrame(
        {
            "order_id": [f"ORD-{i:05d}" for i in range(1, n_rows + 1)],
            "timestamp": timestamps,
            "zone": zones,
            "driver": rng.choice(DRIVERS, size=n_rows),
            "volume": volume,
            "delay_minutes": delay,
        }
    ).sort_values("timestamp", ignore_index=True)
    df["order_id"] = [f"ORD-{i:05d}" for i in range(1, n_rows + 1)]
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=600)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    out = Path(__file__).parent / "data" / "deliveries.csv"
    out.parent.mkdir(exist_ok=True)
    df = simulate(args.rows, args.seed)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out}")
