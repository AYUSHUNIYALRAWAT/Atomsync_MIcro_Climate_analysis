"""Interactive climate and shipment quality dashboard for AtmoSync."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset" / "curated"

st.set_page_config(page_title="AtmoSync Climate Dashboard", page_icon="🌦️", layout="wide")
st.title("AtmoSync | Micro-climate & shipment quality")
st.caption("Explore shipment sensor conditions alongside the supplied weather estimates.")

@st.cache_data
def load_data():
    daily = pd.read_csv(DATA_DIR / "container_daily_summary_curated.csv", parse_dates=["event_date_utc"])
    climate = pd.read_csv(DATA_DIR / "sensor_shipment_weather_curated.csv", parse_dates=["event_timestamp_utc"])
    return daily, climate

try:
    daily, climate = load_data()
except Exception as exc:
    st.error(f"Could not load curated project data: {exc}")
    st.stop()

commodities = sorted(daily["commodity"].dropna().unique())
markets = sorted(daily["destination_market"].dropna().unique())
left, right = st.columns(2)
selected_commodities = left.multiselect("Commodity", commodities, default=commodities)
selected_markets = right.multiselect("Destination market", markets, default=markets)
filtered = daily[daily["commodity"].isin(selected_commodities) & daily["destination_market"].isin(selected_markets)].copy()
filtered_climate = climate[climate["commodity"].isin(selected_commodities) & climate["destination_market"].isin(selected_markets)].copy()

if filtered.empty:
    st.info("No shipments match these filters.")
    st.stop()

shipments = filtered["container_id"].nunique()
issue_pct = (filtered["quality_issue_event_count"].sum() / max(filtered["sensor_event_count"].sum(), 1)) * 100
avg_temp = filtered["temperature_mean_c"].mean()
avg_humidity = filtered["humidity_mean_pct"].mean()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Shipments", f"{shipments:,}")
k2.metric("Avg sensor temperature", f"{avg_temp:.1f} °C")
k3.metric("Avg sensor humidity", f"{avg_humidity:.1f}%")
k4.metric("Events with quality issues", f"{issue_pct:.2f}%")

st.subheader("Conditions over time")
trend = filtered.groupby("event_date_utc", as_index=False).agg(
    temperature_mean_c=("temperature_mean_c", "mean"),
    temperature_min_c=("temperature_min_c", "min"),
    temperature_max_c=("temperature_max_c", "max"),
    humidity_mean_pct=("humidity_mean_pct", "mean"),
)
fig = px.line(trend, x="event_date_utc", y="temperature_mean_c", markers=True,
              labels={"event_date_utc": "Date (UTC)", "temperature_mean_c": "Mean sensor temperature (°C)"},
              title="Daily shipment temperature")
fig.add_scatter(x=trend["event_date_utc"], y=trend["temperature_min_c"], mode="lines", name="Daily minimum", line={"dash": "dot"})
fig.add_scatter(x=trend["event_date_utc"], y=trend["temperature_max_c"], mode="lines", name="Daily maximum", line={"dash": "dot"})
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    city = filtered.groupby("origin_city", as_index=False).agg(
        avg_temperature=("temperature_mean_c", "mean"), issue_rate=("quality_issue_event_pct", "mean"),
        shipments=("container_id", "nunique"))
    chart = px.bar(city.sort_values("avg_temperature"), x="origin_city", y="avg_temperature", color="issue_rate",
                   hover_data=["shipments", "issue_rate"], color_continuous_scale="OrRd",
                   labels={"origin_city": "Origin city", "avg_temperature": "Mean temperature (°C)", "issue_rate": "Quality issue events (%)"},
                   title="Temperature and quality issue rate by origin")
    st.plotly_chart(chart, use_container_width=True)
with c2:
    points = filtered_climate.dropna(subset=["temperature_2m_c", "temperature_c_clean"])
    if not points.empty:
        points = points.sample(min(len(points), 5000), random_state=7)
        scatter = px.scatter(points, x="temperature_2m_c", y="temperature_c_clean", color="commodity", opacity=.55,
                             labels={"temperature_2m_c": "Weather estimate (°C)", "temperature_c_clean": "Container sensor (°C)"},
                             title="Container sensor vs. nearby weather estimate")
        st.plotly_chart(scatter, use_container_width=True)
    else:
        st.info("No paired weather and sensor readings are available for this selection.")

st.caption("Data provenance: bundled records are synthetic starter data. Charts are for dashboard prototyping, not real-world climate or market conclusions.")
with st.expander("View filtered daily shipment data"):
    st.dataframe(filtered.sort_values(["event_date_utc", "container_id"]), use_container_width=True)
