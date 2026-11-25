"""Interactive climate and shipment quality dashboard for AtmoSync."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset" / "curated"

st.set_page_config(
    page_title="AtmoSync | Climate intelligence",
    page_icon="🌤️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #142c3b;
    --muted: #6e818b;
    --teal: #168b83;
    --mint: #e4f4f0;
    --line: #e4eceb;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5f8f7;
    color: var(--ink);
}

.block-container {
    max-width: 1440px;
    padding-top: 2.3rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #112b38;
}

[data-testid="stSidebar"] * {
    color: #edf6f4 !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #168b83;
}

.hero {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 22px;
    padding: 30px 34px;
    margin: 0 0 1.5rem;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 24px;
    background: radial-gradient(circle at 90% 10%, rgba(36,171,155,.32), transparent 28%), linear-gradient(115deg, #102d3b 0%, #164b55 100%);
    box-shadow: 0 18px 42px rgba(17,43,56,.13);
}

.hero-mark {
    display: grid;
    flex: 0 0 64px;
    place-items: center;
    width: 64px;
    height: 64px;
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 20px;
    background: rgba(255,255,255,.12);
    font-size: 30px;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(1.7rem, 3vw, 2.35rem);
    letter-spacing: -.045em;
    margin: 0;
    color: #f5fbfa;
}

.hero p {
    margin: 6px 0 0;
    color: #c2d7d8;
    font-size: .98rem;
}

.hero .eyebrow {
    color: #75d5c5;
    margin-bottom: 7px;
}

.eyebrow {
    color: #168b83;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-weight: 700;
    font-size: .68rem;
    margin-bottom: 5px;
}

.kpi-card {
    position: relative;
    overflow: hidden;
    min-height: 142px;
    padding: 18px 19px 17px;
    border: 1px solid #e5edeb;
    border-radius: 18px;
    background: linear-gradient(145deg, #ffffff, #fbfdfc);
    box-shadow: 0 7px 22px rgba(20,44,59,.045);
    margin-bottom: 12px;
}

.kpi-card:after {
    content: '';
    position: absolute;
    left: 0;
    top: 18px;
    bottom: 18px;
    width: 3px;
    border-radius: 0 4px 4px 0;
    background: #168b83;
}

.kpi-card.risk:after { background: #df9561; }
.kpi-card.cool:after { background: #5794c2; }
.kpi-card.violet:after { background: #8a7ac7; }

.kpi-top {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #71838b;
    font-size: .77rem;
    font-weight: 600;
    letter-spacing: .015em;
}

.kpi-icon {
    display: grid;
    place-items: center;
    width: 29px;
    height: 29px;
    border-radius: 9px;
    background: #e8f5f2;
    font-size: 15px;
}

.kpi-card.risk .kpi-icon { background: #fff2e8; }
.kpi-card.cool .kpi-icon { background: #edf5fb; }
.kpi-card.violet .kpi-icon { background: #f2effa; }

.kpi-value {
    margin-top: 13px;
    color: #142c3b;
    font: 700 1.72rem/1.15 'Manrope', sans-serif;
    letter-spacing: -.04em;
}

.kpi-detail {
    margin-top: 6px;
    color: #8a999f;
    font-size: .72rem;
}

[data-testid="stPlotlyChart"] {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 5px 18px rgba(20, 44, 59, .035);
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    background: #fff;
}

hr {
    border-color: var(--line);
}
</style>

<div class="hero">
    <div class="hero-mark">🌤️</div>
    <div>
        <div class="eyebrow">AtmoSync · climate intelligence</div>
        <h1>Shipment conditions</h1>
        <p>Micro-climate signals and quality risk across your supply chain</p>
    </div>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    daily = pd.read_csv(
        DATA_DIR / "container_daily_summary_curated.csv",
        parse_dates=["event_date_utc"],
    )
    climate = pd.read_csv(
        DATA_DIR / "sensor_shipment_weather_curated.csv",
        parse_dates=["event_timestamp_utc"],
    )
    return daily, climate


daily = None
climate = None
try:
    daily, climate = load_data()
except Exception as exc:
    st.error(f"Could not load curated project data: {exc}")
    st.stop()

# Keep an explicit guard in case execution continues after Streamlit's stop signal.
if daily is None or climate is None:
    st.error("Dashboard data did not load. Check that the curated CSV files exist.")
    st.stop()

commodities = sorted(daily["commodity"].dropna().unique())
markets = sorted(daily["destination_market"].dropna().unique())

with st.sidebar:
    st.markdown("### Explore data")
    st.caption("Choose the shipments included in this view.")

    selected_commodities = st.multiselect(
        "Commodity",
        commodities,
        default=commodities,
    )
    selected_markets = st.multiselect(
        "Destination market",
        markets,
        default=markets,
    )
    min_date = daily["event_date_utc"].min().date()
    max_date = daily["event_date_utc"].max().date()
    selected_dates = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, (tuple, list)):
        start_date = selected_dates[0]
        end_date = selected_dates[-1]
    else:
        start_date = end_date = selected_dates

    st.markdown("---")
    st.caption("Bundled data · UTC timestamps")


filtered = daily[
    daily["commodity"].isin(selected_commodities)
    & daily["destination_market"].isin(selected_markets)
    & daily["event_date_utc"].dt.date.between(start_date, end_date)
].copy()

filtered_climate = climate[
    climate["commodity"].isin(selected_commodities)
    & climate["destination_market"].isin(selected_markets)
    & climate["event_timestamp_utc"].dt.date.between(start_date, end_date)
].copy()

if filtered.empty:
    st.info("No shipments match these filters.")
    st.stop()


active_containers = filtered["container_id"].nunique()
shipment_count = filtered["shipment_id"].nunique()
sensor_readings = int(filtered["sensor_event_count"].sum())
issue_events = int(filtered["quality_issue_event_count"].sum())
issue_pct = issue_events / max(sensor_readings, 1) * 100
shipments_with_issues = filtered.groupby("shipment_id")["quality_issue_event_count"].sum().gt(0).sum()
avg_temp = filtered["temperature_mean_c"].mean()
avg_humidity = filtered["humidity_mean_pct"].mean()
peak_temp = filtered["temperature_max_c"].max()

def render_kpi(label, value, detail, icon, accent=""):
    st.markdown(
        f"""<div class="kpi-card {accent}">
            <div class="kpi-top"><span class="kpi-icon">{icon}</span><span>{label}</span></div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-detail">{detail}</div>
        </div>""",
        unsafe_allow_html=True,
    )


# Operational volume and quality indicators
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi("Active containers", f"{active_containers:,}", "Unique containers in view", "▣")
with k2:
    render_kpi("Shipments tracked", f"{shipment_count:,}", "Across selected destinations", "↗", "cool")
with k3:
    render_kpi("Sensor readings", f"{sensor_readings:,}", "Events in the filtered records", "⌁", "violet")
with k4:
    render_kpi("Shipments with issues", f"{shipments_with_issues:,}", "One or more flagged events", "!", "risk")

# Climate and quality indicators
k5, k6, k7, k8 = st.columns(4)
with k5:
    render_kpi("Quality issue rate", f"{issue_pct:.2f}%", f"{issue_events:,} events flagged", "△", "risk")
with k6:
    render_kpi("Mean temperature", f"{avg_temp:.1f} °C", "Average container reading", "°", "cool")
with k7:
    render_kpi("Mean humidity", f"{avg_humidity:.1f}%", "Average container reading", "◌", "violet")
with k8:
    render_kpi("Peak temperature", f"{peak_temp:.1f} °C", "Highest daily maximum", "↑", "risk")


st.markdown(
    '<div class="eyebrow">Network overview</div>',
    unsafe_allow_html=True,
)
st.subheader("Conditions over time")

trend = filtered.groupby("event_date_utc", as_index=False).agg(
    temperature_mean_c=("temperature_mean_c", "mean"),
    temperature_min_c=("temperature_min_c", "min"),
    temperature_max_c=("temperature_max_c", "max"),
    humidity_mean_pct=("humidity_mean_pct", "mean"),
)

fig = px.line(
    trend,
    x="event_date_utc",
    y="temperature_mean_c",
    markers=True,
    labels={
        "event_date_utc": "Date (UTC)",
        "temperature_mean_c": "Mean sensor temperature (°C)",
    },
    title="Daily shipment temperature",
    template="plotly_white",
)

fig.add_scatter(
    x=trend["event_date_utc"],
    y=trend["temperature_min_c"],
    mode="lines",
    name="Daily minimum",
    line={"dash": "dot", "color": "#84c9bd"},
)

fig.add_scatter(
    x=trend["event_date_utc"],
    y=trend["temperature_max_c"],
    mode="lines",
    name="Daily maximum",
    line={"dash": "dot", "color": "#e7a56d"},
)

fig.update_layout(
    height=370,
    margin={"l": 15, "r": 15, "t": 55, "b": 10},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"family": "DM Sans, sans-serif", "color": "#526873"},
    title={
        "font": {
            "family": "Manrope, sans-serif",
            "size": 16,
            "color": "#183545",
        }
    },
    legend={"orientation": "h", "y": 1.12, "x": 0},
)
fig.update_xaxes(showgrid=False, linecolor="#e4eceb")
fig.update_yaxes(gridcolor="#edf2f1", zeroline=False)

st.plotly_chart(fig, use_container_width=True)


c1, c2 = st.columns(2)

with c1:
    city = filtered.groupby("origin_city", as_index=False).agg(
        issue_events=("quality_issue_event_count", "sum"),
        sensor_events=("sensor_event_count", "sum"),
        shipments=("shipment_id", "nunique"),
    )
    city["issue_rate"] = city["issue_events"] / city["sensor_events"].clip(lower=1) * 100

    chart = px.bar(
        city.sort_values("issue_rate"),
        x="issue_rate",
        y="origin_city",
        orientation="h",
        color="issue_rate",
        hover_data=["shipments", "issue_events", "sensor_events"],
        color_continuous_scale=[[0, "#b9e2d9"], [1, "#dc8065"]],
        labels={
            "origin_city": "Origin city",
            "issue_rate": "Quality issue rate (%)",
            "issue_events": "Issue events",
            "sensor_events": "Sensor events",
            "shipments": "Shipments",
        },
        title="Quality issue rate by origin",
        template="plotly_white",
    )

    chart.update_layout(
        height=350,
        margin={"l": 12, "r": 12, "t": 55, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans, sans-serif", "color": "#526873"},
        title={
            "font": {
                "family": "Manrope, sans-serif",
                "size": 15,
                "color": "#183545",
            }
        },
    )
    chart.update_xaxes(showgrid=True, gridcolor="#edf2f1", zeroline=False)
    chart.update_yaxes(showgrid=False, linecolor="#e4eceb")

    st.plotly_chart(chart, use_container_width=True)


with c2:
    points = filtered_climate.dropna(
        subset=["temperature_2m_c", "temperature_c_clean"]
    )

    if not points.empty:
        points = points.sample(min(len(points), 5000), random_state=7)

        scatter = px.scatter(
            points,
            x="temperature_2m_c",
            y="temperature_c_clean",
            color="commodity",
            opacity=.55,
            labels={
                "temperature_2m_c": "Weather estimate (°C)",
                "temperature_c_clean": "Container sensor (°C)",
            },
            title="Container sensor vs. nearby weather estimate",
            template="plotly_white",
        )

        scatter.update_layout(
            height=350,
            margin={"l": 12, "r": 12, "t": 55, "b": 10},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "DM Sans, sans-serif", "color": "#526873"},
            title={
                "font": {
                    "family": "Manrope, sans-serif",
                    "size": 15,
                    "color": "#183545",
                }
            },
        )
        scatter.update_xaxes(showgrid=False, linecolor="#e4eceb")
        scatter.update_yaxes(gridcolor="#edf2f1", zeroline=False)

        st.plotly_chart(scatter, use_container_width=True)
    else:
        st.info(
            "No paired weather and sensor readings are available for this selection."
        )


st.markdown("---")
st.caption(
    "Data provenance: bundled records are synthetic starter data. "
    "Charts are for dashboard prototyping, not real-world climate or market conclusions."
)

with st.expander("View filtered daily shipment data"):
    st.dataframe(
        filtered.sort_values(["event_date_utc", "container_id"]),
        use_container_width=True,
    )