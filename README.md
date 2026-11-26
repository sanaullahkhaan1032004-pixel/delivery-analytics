# Delivery Analytics

A small data project built on simulated last-mile delivery records. It provides a reproducible dataset for exploring delays by zone, driver, time of day, and order volume.

## Dataset

`data/deliveries.csv` (600 rows by default)

| Column | Description |
|---|---|
| `order_id` | Unique order identifier (`ORD-00001`, ...) |
| `timestamp` | Delivery date and time (last 30 days, 08:00-21:00) |
| `zone` | Delivery zone: North, South, East, West, Central |
| `driver` | Driver name |
| `volume` | Order volume (units) |
| `delay_minutes` | Minutes late (0 = on time) |

Delays are simulated with zone baselines, rush-hour peaks (12-14h, 18-20h), a volume effect, and random noise, so there are real patterns to find.

## Quick start

```bash
pip install -r requirements.txt
python generate_data.py --rows 600 --seed 42
jupyter notebook notebooks/01_load_data.ipynb
```

## Structure

```
generate_data.py          # simulates the data and writes the CSV
data/deliveries.csv       # generated dataset
notebooks/01_load_data.ipynb  # loads the CSV and previews it
```

## Next steps

- Average delay by zone and by hour
- Driver performance comparison
- Predict delay from zone, hour, and volume
