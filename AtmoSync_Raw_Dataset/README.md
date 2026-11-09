# AtmoSync — Raw Dataset Starter Pack

## Provenance warning
This is a **synthetic starter dataset**. It is not real sensor telemetry, weather observations, commodity-market records, or verified route data. Use it for pipeline development, schema design, joins, data-quality profiling, EDA, and dashboard prototyping.

The project roadmap identifies Open-Meteo Historical Weather data and a supplied W60 benchmark workbook. The W60 workbook was not attached in this chat, so it has not been fabricated or included. Weather and market files here are placeholders and should be replaced with source-backed records before making real-world claims.

## Files
- `containers_raw.csv`: 100 container/shipment metadata rows.
- `sensor_events_raw.csv`: 15-minute events for 100 containers across 7 days, including deliberate data-quality issues and 12 duplicate rows.
- `weather_raw.csv`: hourly weather-like records for Delhi, Mumbai, Chennai, Kolkata, and Bengaluru across 7 days.
- `commodity_market_prices_raw.csv`: daily snapshots for Tomato, Potato, Onion, and Apple across five markets.
- `market_routes_raw.csv`: illustrative inter-city route distance, time, and cost estimates.
- `source_log.csv`: provenance and limitation register.
- `data_dictionary.csv`: column inventory and sample values.

## Record counts
- Containers: 100
- Sensor events: 67,212 (67,200 scheduled + 12 deliberate duplicates)
- Weather: 840
- Commodity prices: 140
- Routes: 10

## Next steps
1. Keep these files in `data/raw/` and never overwrite them.
2. Import the original W60 workbook unchanged when available.
3. Replace `weather_raw.csv` with Open-Meteo Historical Weather API output; retain request parameters and retrieval timestamp.
4. Replace `commodity_market_prices_raw.csv` with AGMARKNET/data.gov.in records and retain source identifiers.
5. Put cleaned outputs in `data/processed/`; document every cleaning decision.
6. Align timestamps, units, coordinates, and market/date keys before comparisons.

## Units
- Sensor/weather timestamps: UTC ISO-8601.
- Temperature: °C; humidity: %; vibration: g.
- Market prices: INR per quintal.
- Route distance: km; travel time: hours.
