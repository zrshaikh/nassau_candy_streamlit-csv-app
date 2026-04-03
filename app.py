import streamlit as st
st.set_page_config(layout="wide")
st.markdown("""
<style>

section.main > div {
    padding-top: 1rem;
}

h1, h2, h3 {
    margin-top: 0.5rem;
    margin-bottom: 0.6rem;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)
import html
import os
print("Current Working Directory:", os.getcwd())
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"

# streamlit run app.py

df = pd.read_csv("nassau_candy_processed.csv")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Convert date columns to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Lead_Time_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

## GLOBAL PERFORMANCE COLOR SCALE

PERFORMANCE_SCALE = [
    [0.0, "#ef4444"],   # Red (Worst)
    [0.5, "#facc15"],   # Yellow
    [1.0, "#22c55e"]    # Green (Best)
]

# Title Card

st.markdown("""
<style>

.dashboard-header {
    background: linear-gradient(90deg, #1e3a5f, #2e5c9a);
    padding: 18px 30px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    margin-left: 0px;
}

.dashboard-title {
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin: 0;
}

.dashboard-subtitle {
    color: #dbeafe;
    font-size: 16px;
    margin-top: 2px;
}

.icon {
    font-size: 38px;
    margin-right: 15px;
}

</style>

<div class="dashboard-header">

<div class="icon">🚚</div>

<div>
<div class="dashboard-title">
Factory-to-Customer Shipping Route Efficiency Analysis
</div>

<div class="dashboard-subtitle">
for Nassau Candy Distributor
</div>
</div>

</div>
""", unsafe_allow_html=True)



# SIDEBAR FILTER PANEL

st.sidebar.header("Filters")

# -------------------------
# Date Range Filter
# -------------------------

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

# -------------------------
# Region Selector
# -------------------------

regions = sorted(df["Region"].dropna().unique())

selected_region = st.sidebar.selectbox(
    "Region",
    ["All Regions"] + regions
)

# -------------------------
# State Selector (Dynamic)
# -------------------------

if selected_region != "All Regions":
    states = sorted(df[df["Region"] == selected_region]["State/Province"].dropna().unique())
else:
    states = sorted(df["State/Province"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "State",
    states
)

# -------------------------
# Ship Mode Filter
# -------------------------

ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    ship_modes,
    default=ship_modes
)


# -------------------------
# FILTERING LOGIC
# -------------------------

filtered_df = df.copy()

# Date Filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Order Date"] <= pd.to_datetime(end_date))
    ]

# Region Filter
if selected_region != "All Regions":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

# State Filter
if selected_states:
    filtered_df = filtered_df[
        filtered_df["State/Province"].isin(selected_states)
    ]

# Ship Mode Filter
filtered_df = filtered_df[
    filtered_df["Ship Mode"].isin(selected_ship_modes)
]

lead_time_threshold = st.sidebar.slider(
    "Lead-Time Threshold",
    min_value=900,
    max_value=1650,
    value=1200
)



#KPI Card CSS

st.markdown("""
<style>

.kpi-container{
    background-color:#1f2937;
    padding:16px;
    border-radius:12px;
    border:1px solid #374151;
    transition:0.2s;
    margin-bottom:10px;
}

.kpi-container:hover{
    transform:translateY(-3px);
    border:1px solid #4b5563;
}

.kpi-title{
    color:#9ca3af;
    font-size:12px;
    margin-bottom:4px;
}

.kpi-value{
    font-size:26px;
    font-weight:700;
    color:white;
}

.kpi-change-up{
    color:#22c55e;
    font-size:13px;
}

.kpi-change-down{
    color:#ef4444;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)


#KPI Calculations

# Example comparison (replace later with real month comparison)
lead_time_change = 12


#Create KPI Layout (5 Cards Like Image)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

#KPI 1 — Shipping Lead Time
avg_lead_time = filtered_df["Lead_Time_Days"].mean()

if pd.isna(avg_lead_time):
    avg_lead_time = 0
with kpi1:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Shipping Lead Time</div>
        <div class="kpi-value">{avg_lead_time:.1f} Days</div>
        <div class="kpi-change-up">▲ {lead_time_change}% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

#KPI 2 — Average Lead Time / Route
avg_route_lead = filtered_df.groupby("Ship Mode")["Lead_Time_Days"].mean().mean()

if pd.isna(avg_route_lead):
    avg_route_lead = 0
with kpi2:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Average Lead Time / Route</div>
        <div class="kpi-value">{avg_route_lead:.1f} Days</div>
        <div class="kpi-change-up">▲ 8%</div>
    </div>
    """, unsafe_allow_html=True)

#KPI 3 — Route Volume
route_volume = filtered_df["Order ID"].nunique()

with kpi3:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Route Volume</div>
        <div class="kpi-value">{route_volume:,}</div>
        <div class="kpi-change-up">▲ 15%</div>
    </div>
    """, unsafe_allow_html=True)

#KPI 4 — Delay Frequency
if filtered_df.shape[0] > 0:
    delay_rate = (
        filtered_df[filtered_df["Lead_Time_Days"] > lead_time_threshold].shape[0]
        / filtered_df.shape[0]
    ) * 100
else:
    delay_rate = 0

with kpi4:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Delay Frequency</div>
        <div class="kpi-value">{delay_rate:.1f}%</div>
        <div class="kpi-change-down">▲ 5.2%</div>
    </div>
    """, unsafe_allow_html=True)



#KPI 5 — Route Efficiency Score
if filtered_df.shape[0] > 0:
    efficiency_score = (
        filtered_df[filtered_df["Lead_Time_Days"] <= lead_time_threshold].shape[0]
        / filtered_df.shape[0]
    ) * 100
else:
    efficiency_score = 0

with kpi5:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Route Efficiency Score</div>
        <div class="kpi-value">{efficiency_score:.1f}%</div>
        <div class="kpi-change-up">▲ 6.4% vs last month</div>
    </div>
    """, unsafe_allow_html=True)

# Route Efficiency Overview
st.markdown("## 🚚 Route Efficiency Overview")

route_order = [
    "Same Day",
    "First Class",
    "Second Class",
    "Standard Class"
]

# Average lead time by route
lead_time_route = (
    filtered_df
    .groupby("Ship Mode")["Lead_Time_Days"]
    .mean()
    .reset_index()
    .sort_values("Lead_Time_Days", ascending=True)
)

fig_avg_route = px.bar(
    lead_time_route,
    y="Ship Mode",
    x="Lead_Time_Days",
    orientation="h",
    text=lead_time_route["Lead_Time_Days"].round(2),
    title="Average Lead Time by Route",
    category_orders={"Ship Mode": route_order}
)

# Set bar color to blue
fig_avg_route.update_traces(
    marker_color="#3b82f6",   # blue
    texttemplate="%{text} days",
    textposition="outside"
)

fig_avg_route.update_layout(
    xaxis=dict(range=[900, lead_time_route["Lead_Time_Days"].max() + 100])
)

fig_avg_route.update_yaxes(autorange="reversed")

st.plotly_chart(fig_avg_route, use_container_width=True)

#Route Performance Leaderboard
st.markdown(
    """
    <p style="
        font-size:18px;
        font-weight:600;
        margin-bottom:8px;
    ">
    Route Performance Leaderboard
    </p>
    """,
    unsafe_allow_html=True
)

leaderboard = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Avg_Lead_Time=("Lead_Time_Days", "mean"),
        Delayed_Orders=("Lead_Time_Days", lambda x: (x > lead_time_threshold).sum())
    )
    .reset_index()
)

# Calculate delay rate
leaderboard["Delay Rate (%)"] = (
    leaderboard["Delayed_Orders"] / leaderboard["Total_Orders"] * 100
)

# Efficiency score
leaderboard["Efficiency Score (%)"] = 100 - leaderboard["Delay Rate (%)"]

# Round values
leaderboard["Avg_Lead_Time"] = leaderboard["Avg_Lead_Time"].round(2)
leaderboard["Delay Rate (%)"] = leaderboard["Delay Rate (%)"].round(1)
leaderboard["Efficiency Score (%)"] = leaderboard["Efficiency Score (%)"].round(1)

# Sort best routes first
leaderboard = leaderboard.sort_values("Efficiency Score (%)", ascending=False)

# Add ranking
leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))

# Rename columns
leaderboard = leaderboard.rename(columns={
    "Ship Mode": "Route Type",
    "Avg_Lead_Time": "Avg Lead Time (Days)",
    "Total_Orders": "Total Orders"
})

# Display styled leaderboard
styled_table = (
    leaderboard
    .drop(columns=["Delayed_Orders"])
    .style
    .background_gradient(subset=["Efficiency Score (%)"], cmap="Blues")
    .format({
        "Avg Lead Time (Days)": "{:.2f}",
        "Delay Rate (%)": "{:.1f}%",
        "Efficiency Score (%)": "{:.1f}%"
    })
)

st.dataframe(styled_table, use_container_width=True)

st.divider()

# Geographic Shipping Map
st.markdown("## 🗺 Geographic Shipping Map")

# Shipping Efficiency Map

state_perf = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        On_Time=("Lead_Time_Days", lambda x: (x <= lead_time_threshold).sum())
    )
    .reset_index()
)

# Efficiency Score
state_perf["Efficiency Score"] = (
    state_perf["On_Time"] / state_perf["Total_Orders"] * 100
)

us_state_abbrev = {
"Alabama":"AL","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO",
"Connecticut":"CT","Delaware":"DE","Florida":"FL","Georgia":"GA","Idaho":"ID",
"Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY",
"Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
"Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE",
"Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY",
"North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR",
"Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD",
"Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA",
"Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
}

state_perf["State Code"] = state_perf["State/Province"].map(us_state_abbrev)
state_perf = state_perf.dropna(subset=["State Code"])

state_perf["Delay Rate"] = 100 - state_perf["Efficiency Score"]

fig_map = px.choropleth(
    state_perf,
    locations="State Code",
    locationmode="USA-states",
    color="Efficiency Score",
    scope="usa",
    color_continuous_scale=PERFORMANCE_SCALE,
    range_color=(
        state_perf["Efficiency Score"].min(),
        state_perf["Efficiency Score"].max()
    ),
    hover_name="State/Province",
    hover_data={
        "Efficiency Score":":.1f",
        "Total_Orders":True,
        "State Code":False
    },
    title="US Shipping Efficiency Heatmap"
)

fig_map.update_layout(
    height=500,
    title_x=0,
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_colorbar=dict(
        title="Efficiency %",
        ticksuffix="%"
    )
)

st.plotly_chart(fig_map, use_container_width=True)


st.markdown("## 📊 Regional & Ship Mode Performance")

# -----------------------------
# 1️⃣ Regional Bottleneck (Full Width)
# -----------------------------
region_perf = (
    filtered_df
    .groupby("Region")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Delayed_Orders=("Lead_Time_Days", lambda x: (x > lead_time_threshold).sum())
    )
    .reset_index()
)

region_perf["Delay Rate (%)"] = (
    region_perf["Delayed_Orders"] / region_perf["Total_Orders"] * 100
).round(1)

region_perf = region_perf.sort_values("Delay Rate (%)", ascending=False)

fig_region = px.bar(
    region_perf,
    x="Delay Rate (%)",
    y="Region",
    orientation="h",
    text="Delay Rate (%)",
    color="Delay Rate (%)",
    color_continuous_scale="Blues",
    title="Regional Bottlenecks"
)

fig_region.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

fig_region.update_layout(
    height=420,
    title_x=0,
    xaxis_title="Delay Rate (%)",
    yaxis_title="Region",
    coloraxis_showscale=False
)

fig_region.update_yaxes(autorange="reversed", showgrid=False)
fig_region.update_xaxes(showgrid=False)

st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# -----------------------------
# 2️⃣ Ship Mode Comparison
# -----------------------------
st.markdown("### 🚚 Ship Mode Comparison")

col1, col2 = st.columns(2)

ship_perf = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Avg_Lead_Time=("Lead_Time_Days", "mean"),
        Total_Orders=("Order ID", "nunique"),
        Delayed_Orders=("Lead_Time_Days", lambda x: (x > lead_time_threshold).sum())
    )
    .reset_index()
)

ship_perf["Avg_Lead_Time"] = ship_perf["Avg_Lead_Time"].round(1)

ship_perf["Delay Frequency %"] = (
    ship_perf["Delayed_Orders"] / ship_perf["Total_Orders"] * 100
).round(1)


# Avg Lead Time Chart
with col1:

    fig_lead = px.bar(
        ship_perf.sort_values("Avg_Lead_Time"),
        x="Avg_Lead_Time",
        y="Ship Mode",
        orientation="h",
        text="Avg_Lead_Time",
        color="Avg_Lead_Time",
        color_continuous_scale="Blues"
    )

    fig_lead.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    fig_lead.update_layout(
        title="Avg Lead Time (Days)",
        height=350,
        title_x=0,
        coloraxis_showscale=False
    )

    fig_lead.update_xaxes(showgrid=False)
    fig_lead.update_yaxes(showgrid=False)

    st.plotly_chart(fig_lead, use_container_width=True)


# Delay Frequency Donut
with col2:

    fig_delay = px.pie(
        ship_perf,
        names="Ship Mode",
        values="Delay Frequency %",
        hole=0.65
    )

    fig_delay.update_traces(textinfo="label+percent")

    fig_delay.update_layout(
        title="Delay Frequency %",
        height=350,
        title_x=0,
        showlegend=False
    )

    st.plotly_chart(fig_delay, use_container_width=True)

st.divider()

# Lead Time Comparison by Shipping Method

st.markdown("### ⏱ Lead Time Comparison by Shipping Method")

# -------------------------------------------------
# SECTION TITLE
# -------------------------------------------------

title1, title2 = st.columns([1,1.3])

with title1:
    st.markdown(
        "<p style='font-size:18px; font-weight:600;'>🛣 Route Drill-Down</p>",
        unsafe_allow_html=True
    )

with title2:
    st.markdown(
        "<p style='font-size:18px; font-weight:600;'>📦 Order-Level Shipment Timeline</p>",
        unsafe_allow_html=True
    )


# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------

col1, col2 = st.columns([1,1.3])

# -------------------------------------------------
# COLUMN 1 — ROUTE DRILL DOWN
# -------------------------------------------------

with col1:

    selected_state = st.selectbox(
        "Select State",
        sorted(filtered_df["State/Province"].dropna().unique())
    )

    route_df = filtered_df[filtered_df["State/Province"] == selected_state]

    avg_time = route_df["Lead_Time_Days"].mean()
    volume = route_df["Order ID"].nunique()
    delay_pct = (route_df["Lead_Time_Days"] > lead_time_threshold).mean()*100
    on_time_pct = 100 - delay_pct

   # st.markdown(f"### {selected_state}")

    # KPI GRID
    k1,k2 = st.columns(2)

    with k1:
        st.metric("Avg Lead Time", f"{avg_time:.1f} Days")

    with k2:
        st.metric("Volume", f"{volume:,} Orders")

    k3,k4 = st.columns(2)

    with k3:
        st.metric("Delay %", f"{delay_pct:.1f}%")

    with k4:

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=on_time_pct,
            number={"suffix":"%"},
            title={"text":"On-Time"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"#1f77b4"},
                "steps":[
                    {"range":[0,60],"color":"#d9534f"},
                    {"range":[60,80],"color":"#f0ad4e"},
                    {"range":[80,100],"color":"#5cb85c"}
                ]
            }
        ))

        fig_gauge.update_layout(height=200,margin=dict(l=0,r=0,t=40,b=0))

        st.plotly_chart(fig_gauge,use_container_width=True)


# -------------------------------------------------
# COLUMN 2 — ORDER TIMELINE TABLE
# -------------------------------------------------

with col2:

    export_col, spacer = st.columns([0.3,0.7])

    timeline_df = route_df[[
        "Order ID",
        "Order Date",
        "Ship Date",
        "Lead_Time_Days"
    ]].copy()

    timeline_df["Status"] = timeline_df["Lead_Time_Days"].apply(
        lambda x: "Delayed" if x > lead_time_threshold else "On-Time"
    )

    timeline_df = timeline_df.rename(columns={
        "Lead_Time_Days":"Lead Time"
    })

    timeline_df = timeline_df.head(15)

    with export_col:
        csv = timeline_df.to_csv(index=False)

        st.download_button(
            "⬇ Export CSV",
            csv,
            "shipment_timeline.csv",
            "text/csv"
        )

    st.dataframe(
        timeline_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("""
<hr style="margin-top:40px; margin-bottom:15px;">

<div style="text-align:center; font-size:12.5px; color:#9ca3af; line-height:1.8;">
    
<b>🚚 Factory-to-Customer Shipping Route Efficiency Dashboard</b><br>

Created by <b>Zaid Shaikh</b> | Guided by <b>Saiprasad Kagne</b><br>

📧 zrshaikh@outlook.com.com | saikagne2601@gmail.com<br>

© 2026 Nassau Candy Distributor • Built with Streamlit & Plotly

</div>
""", unsafe_allow_html=True)