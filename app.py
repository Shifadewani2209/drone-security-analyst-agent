import pandas as pd
import streamlit as st

from agent import analyze_frame, generate_daily_summary
from database import clear_db, get_all_events, init_db, insert_event, search_events
from simulator import get_patrol_route, get_simulated_frames, simulate_drone_health


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]
SEVERITY_SCORE = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
SEVERITY_COLORS = {
    "Critical": "#dc2626",
    "High": "#ea580c",
    "Medium": "#ca8a04",
    "Low": "#16a34a",
}
CHART_HEIGHT = 220
MAP_HEIGHT = 250
TABLE_HEIGHT = 310
COMPACT_TABLE_HEIGHT = 280
LOCATION_COORDS = {
    "Charging Dock": {"lat": 28.6131, "lon": 77.2098},
    "Main Gate": {"lat": 28.6139, "lon": 77.2090},
    "East Fence": {"lat": 28.6144, "lon": 77.2111},
    "North Yard": {"lat": 28.6152, "lon": 77.2095},
    "Garage": {"lat": 28.6134, "lon": 77.2078},
    "Solar Shed": {"lat": 28.6129, "lon": 77.2104},
    "Warehouse": {"lat": 28.6125, "lon": 77.2087},
    "Backyard": {"lat": 28.6118, "lon": 77.2094},
    "South Door": {"lat": 28.6115, "lon": 77.2082},
    "Perimeter Road": {"lat": 28.6148, "lon": 77.2073},
}


st.set_page_config(
    page_title="DroneSec AI Command Center",
    page_icon="DS",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()


st.markdown(
    """
    <style>
    :root {
        --bg: #020617;
        --panel: #0f172a;
        --panel-soft: #111c33;
        --border: #24324a;
        --text: #e5e7eb;
        --muted: #94a3b8;
        --accent: #38bdf8;
        --accent-dark: #7dd3fc;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 30rem),
            radial-gradient(circle at top right, rgba(30, 64, 175, 0.16), transparent 28rem),
            linear-gradient(180deg, #020617 0%, #0b1120 44%, #0f172a 100%);
        color: var(--text);
    }

    .block-container {
        padding: 0.75rem 1rem 1.2rem;
        max-width: none;
        width: 100%;
    }

    [data-testid="stAppViewContainer"] > .main {
        width: 100%;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: none;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    section[data-testid="stSidebar"] {
        width: 20.5rem !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 20.5rem !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        max-width: 17rem;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] span {
        max-width: 14.5rem;
        overflow: visible;
        text-overflow: clip;
        white-space: nowrap;
    }

    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.96);
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: 0;
    }

    h3 {
        font-size: 1.05rem;
        margin: 0.35rem 0 0.55rem;
    }

    p {
        margin-bottom: 0.45rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.62rem 0.75rem;
        box-shadow: 0 12px 28px rgba(2, 6, 23, 0.26);
    }

    div[data-testid="stMetric"] label {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.55rem;
    }

    .hero {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem 1.05rem;
        background:
            linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(15, 23, 42, 0.78)),
            rgba(15, 23, 42, 0.9);
        margin-bottom: 0.7rem;
        box-shadow: 0 16px 36px rgba(2, 6, 23, 0.34);
    }

    .hero-title {
        font-size: clamp(1.75rem, 3vw, 2.35rem);
        font-weight: 800;
        line-height: 1.05;
        margin: 0 0 0.35rem;
        color: var(--text);
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        max-width: none;
        margin: 0;
    }

    .eyebrow {
        color: var(--accent-dark);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .panel {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.8rem;
        min-height: 100%;
        box-shadow: 0 12px 28px rgba(2, 6, 23, 0.26);
    }

    .alert-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid var(--border);
        border-left: 5px solid var(--accent);
        border-radius: 8px;
        padding: 0.7rem 0.82rem;
        margin-bottom: 0.55rem;
        box-shadow: 0 12px 28px rgba(2, 6, 23, 0.24);
    }

    .alert-title {
        color: var(--text);
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .alert-body {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.38;
    }

    .chip {
        display: inline-block;
        padding: 0.17rem 0.52rem;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 800;
        color: #ffffff;
        margin-right: 0.35rem;
    }

    .status-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.55rem 0 0.7rem;
    }

    .status-item {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.62rem 0.75rem;
    }

    .status-label {
        color: var(--muted);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .status-value {
        color: var(--text);
        font-size: 1rem;
        font-weight: 800;
        margin-top: 0.16rem;
    }

    .muted {
        color: var(--muted);
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid var(--border);
        font-weight: 700;
        min-height: 2.35rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.42rem 0.68rem;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid var(--border);
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.55rem;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.75rem;
    }

    .stAlert {
        padding: 0.55rem 0.7rem;
    }

    .route-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.6rem;
    }

    .route-step {
        border: 1px solid var(--border);
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.9);
        padding: 0.7rem;
        min-height: 6.6rem;
    }

    .route-number {
        color: var(--accent-dark);
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .route-location {
        color: var(--text);
        font-weight: 800;
        margin-top: 0.2rem;
    }

    .route-action {
        color: var(--muted);
        font-size: 0.84rem;
        margin-top: 0.35rem;
        line-height: 1.35;
    }

    @media (max-width: 900px) {
        .status-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .route-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def event_dataframe(events):
    if not events:
        return pd.DataFrame(
            columns=[
                "frame_id",
                "timestamp",
                "location",
                "alert_level",
                "event_type",
                "objects",
                "altitude",
                "description",
                "recommendation",
            ]
        )

    df = pd.DataFrame(events)
    return df[
        [
            "frame_id",
            "timestamp",
            "location",
            "alert_level",
            "event_type",
            "objects",
            "altitude",
            "description",
            "recommendation",
        ]
    ]


def enrich_dataframe(df):
    if df.empty:
        return df

    enriched = df.copy()
    enriched["severity_score"] = enriched["alert_level"].map(SEVERITY_SCORE)
    enriched["incident_id"] = enriched["frame_id"].apply(lambda value: f"INC-{value:04d}")
    enriched["sla"] = enriched["alert_level"].map(
        {
            "Critical": "Immediate",
            "High": "15 min",
            "Medium": "60 min",
            "Low": "Routine",
        }
    )
    enriched["owner"] = enriched["alert_level"].map(
        {
            "Critical": "Incident Commander",
            "High": "Security Lead",
            "Medium": "Control Room",
            "Low": "Patrol Log",
        }
    )
    enriched["status"] = enriched["alert_level"].map(
        {
            "Critical": "Escalate",
            "High": "Investigate",
            "Medium": "Monitor",
            "Low": "Logged",
        }
    )
    return enriched


def run_simulation():
    clear_db()
    previous_frames = []

    progress = st.progress(0)
    frames = get_simulated_frames()

    for index, frame in enumerate(frames, start=1):
        event = analyze_frame(frame, previous_frames)
        insert_event(event)
        previous_frames.append(frame)
        progress.progress(index / len(frames))


def render_alert(alert):
    severity = alert["alert_level"]
    color = SEVERITY_COLORS.get(severity, "#0f766e")
    st.markdown(
        f"""
        <div class="alert-card" style="border-left-color:{color};">
            <div class="alert-title">
                <span class="chip" style="background:{color};">{severity}</span>
                {alert["event_type"]} - {alert["location"]}
            </div>
            <div class="alert-body">
                <strong>Frame:</strong> {alert["frame_id"]} |
                <strong>Time:</strong> {alert["timestamp"]} |
                <strong>Altitude:</strong> {alert["altitude"]}m<br>
                {alert["description"]}<br>
                <strong>Recommended action:</strong> {alert["recommendation"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_strip(events, df):
    if df.empty:
        average_score = "0.0"
        top_location = "None"
        latest_time = "No data"
        response_mode = "Standby"
    else:
        average_score = f"{df['severity_score'].mean():.1f}/4"
        top_location = df["location"].value_counts().index[0]
        latest_time = events[-1]["timestamp"]
        max_score = df["severity_score"].max()
        response_mode = "Emergency" if max_score >= 4 else "Elevated" if max_score >= 3 else "Routine"

    st.markdown(
        f"""
        <div class="status-strip">
            <div class="status-item">
                <div class="status-label">Risk Index</div>
                <div class="status-value">{average_score}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Watch Zone</div>
                <div class="status-value">{top_location}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Latest Frame</div>
                <div class="status-value">{latest_time}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Response Mode</div>
                <div class="status-value">{response_mode}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_route_steps(route):
    cards = []
    for stop in route:
        cards.append(
            f"""
            <div class="route-step">
                <div class="route-number">Step {stop["step"]}</div>
                <div class="route-location">{stop["location"]}</div>
                <div class="route-action">{stop["action"]}</div>
                <div class="route-action">Battery cost: {stop["battery_cost"]}%</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <div class="route-grid">
            {"".join(cards)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_location_dataframe(df):
    if df.empty:
        return pd.DataFrame(columns=["lat", "lon", "location", "severity_score"])

    map_df = df.copy()
    map_df["lat"] = map_df["location"].map(lambda location: LOCATION_COORDS.get(location, {}).get("lat"))
    map_df["lon"] = map_df["location"].map(lambda location: LOCATION_COORDS.get(location, {}).get("lon"))
    return map_df.dropna(subset=["lat", "lon"])


def make_route_dataframe(route):
    route_df = pd.DataFrame(route)
    route_df["lat"] = route_df["location"].map(lambda location: LOCATION_COORDS.get(location, {}).get("lat"))
    route_df["lon"] = route_df["location"].map(lambda location: LOCATION_COORDS.get(location, {}).get("lon"))
    return route_df.dropna(subset=["lat", "lon"])


with st.sidebar:
    st.markdown("## DroneSec AI")
    st.caption("Security analyst command center")

    if st.button("Run patrol simulation", use_container_width=True, type="primary"):
        run_simulation()
        st.success("Patrol processed and indexed.")

    if st.button("Reset event index", use_container_width=True):
        clear_db()
        st.warning("Event index cleared.")

    st.divider()
    st.markdown("### Analyst Filters")
    keyword = st.text_input(
        "Keyword",
        placeholder="fence, van, smoke, critical",
    )
    severity_filter = st.multiselect(
        "Severity",
        SEVERITY_ORDER,
        default=SEVERITY_ORDER,
    )


events = get_all_events()
df = enrich_dataframe(event_dataframe(events))
locations = sorted(df["location"].dropna().unique()) if not df.empty else []
route = get_patrol_route()
health = simulate_drone_health(len(df))

with st.sidebar:
    location_filter = st.multiselect(
        "Location",
        locations,
        default=locations,
    )
    min_risk = st.slider("Minimum risk score", 1, 4, 1)

if keyword:
    visible_events = search_events(keyword)
else:
    visible_events = events

visible_df = enrich_dataframe(event_dataframe(visible_events))
if not visible_df.empty:
    visible_df = visible_df[
        visible_df["alert_level"].isin(severity_filter)
        & visible_df["location"].isin(location_filter)
        & (visible_df["severity_score"] >= min_risk)
    ]

alert_df = df[df["alert_level"].isin(["Medium", "High", "Critical"])] if not df.empty else df
critical_count = int((df["alert_level"] == "Critical").sum()) if not df.empty else 0
high_count = int((df["alert_level"] == "High").sum()) if not df.empty else 0
latest_alert = alert_df.tail(1).to_dict("records")[0] if not alert_df.empty else None

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Integrated Drone Security Operations</div>
        <div class="hero-title">DroneSec AI Command Center</div>
        <p class="hero-subtitle">
            Monitor drone patrol incidents, triage alerts, search indexed frames, and export response reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_1, metric_2, metric_3, metric_4, metric_5, metric_6 = st.columns(6)
metric_1.metric("Frames", len(df), help="Total indexed patrol frames")
metric_2.metric("Alerts", len(alert_df), help="Medium, high, and critical events")
metric_3.metric("Critical", critical_count)
metric_4.metric("High", high_count)
metric_5.metric("Zones", len(locations), help="Locations covered by the patrol")
metric_6.metric("Battery", f"{health['battery']}%")

render_status_strip(events, df)

overview_tab, drone_tab, incidents_tab, intelligence_tab, search_tab, report_tab = st.tabs(
    ["Operations", "Drone System", "Incidents", "Intelligence", "Search", "Report"]
)

with overview_tab:
    left, right = st.columns([1.3, 0.7])

    with left:
        st.markdown("### Risk Timeline")
        if not df.empty:
            st.line_chart(
                df,
                x="frame_id",
                y="severity_score",
                height=CHART_HEIGHT,
                use_container_width=True,
            )
        else:
            st.info("Run the patrol simulation from the sidebar to populate the dashboard.")

        st.markdown("### Patrol Coverage")
        map_df = make_location_dataframe(df)
        if not map_df.empty:
            st.map(
                map_df,
                latitude="lat",
                longitude="lon",
                size="severity_score",
                height=MAP_HEIGHT,
            )
        else:
            st.info("Coverage map will appear after events are indexed.")

    with right:
        st.markdown("### Current Priority")
        if latest_alert:
            render_alert(latest_alert)
        else:
            st.success("No active alerts.")

        st.markdown("### Severity Mix")
        if not df.empty:
            severity_counts = (
                df["alert_level"]
                .value_counts()
                .reindex(SEVERITY_ORDER, fill_value=0)
                .reset_index()
            )
            severity_counts.columns = ["alert_level", "count"]
            st.bar_chart(
                severity_counts,
                x="alert_level",
                y="count",
                height=CHART_HEIGHT,
                use_container_width=True,
            )
        else:
            st.info("No severity data yet.")

with drone_tab:
    st.markdown("### Autonomous Drone And Dock")
    health_a, health_b, health_c, health_d = st.columns(4)
    health_a.metric("Flight Battery", f"{health['battery']}%")
    health_b.metric("Drone Mode", health["mode"])
    health_c.metric("Dock Temp", f"{health['dock_temperature']} C")
    health_d.metric("Flight Time", f"{health['flight_time_remaining']} min")

    st.info(f"Next action: {health['next_action']}")

    left, right = st.columns([0.85, 1.15])

    with left:
        st.markdown("### Route Map")
        route_df = make_route_dataframe(route)
        if not route_df.empty:
            st.map(route_df, latitude="lat", longitude="lon", size=120, height=MAP_HEIGHT)

    with right:
        st.markdown("### Automation Rules")
        rules = pd.DataFrame(
            [
                {"condition": "Scheduled patrol starts", "system_action": "Launch from charging dock"},
                {"condition": "Battery below 25%", "system_action": "Return to dock immediately"},
                {"condition": "Critical alert detected", "system_action": "Hold position and escalate"},
                {"condition": "Dock temperature high", "system_action": "Pause charging and create equipment warning"},
            ]
        )
        st.dataframe(rules, use_container_width=True, hide_index=True, height=COMPACT_TABLE_HEIGHT)

    st.markdown("### Manual Frame Analysis")
    upload_col, form_col = st.columns([0.55, 1.45])
    with upload_col:
        uploaded_frame = st.file_uploader(
            "Upload drone frame",
            type=["png", "jpg", "jpeg"],
            help="The demo analyzes the description you provide for this frame.",
        )
        if uploaded_frame:
            st.image(uploaded_frame, use_container_width=True)

    with form_col:
        manual_location = st.selectbox(
            "Frame location",
            sorted(LOCATION_COORDS.keys()),
            index=sorted(LOCATION_COORDS.keys()).index("Main Gate"),
        )
        manual_description = st.text_area(
            "What the drone frame shows",
            placeholder="Example: Person climbing east fence near restricted service road",
            height=100,
        )
        if st.button("Analyze manual frame", use_container_width=True):
            if manual_description.strip():
                manual_frame = {
                    "frame_id": len(df) + 1,
                    "timestamp": "Manual",
                    "location": manual_location,
                    "altitude": 35,
                    "description": manual_description.strip(),
                }
                manual_event = analyze_frame(manual_frame, [])
                render_alert(manual_event)
            else:
                st.warning("Add a frame description before analysis.")

with incidents_tab:
    st.markdown("### Incident Queue")
    if not visible_df.empty:
        queue_df = visible_df.sort_values(["severity_score", "frame_id"], ascending=[False, True])
        st.dataframe(
            queue_df[
                [
                    "incident_id",
                    "timestamp",
                    "location",
                    "alert_level",
                    "event_type",
                    "status",
                    "sla",
                    "owner",
                    "recommendation",
                ]
            ],
            use_container_width=True,
            height=TABLE_HEIGHT,
            hide_index=True,
        )

        selected_incident = st.selectbox(
            "Open incident",
            queue_df["incident_id"].tolist(),
        )
        incident = queue_df[queue_df["incident_id"] == selected_incident].iloc[0].to_dict()
        render_alert(incident)
        st.markdown("### Evidence")
        st.write(incident["description"])
        st.caption(f"Objects detected: {incident['objects'] or 'none'}")
    else:
        st.warning("No incidents match the current filters.")

with intelligence_tab:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Event Types")
        if not df.empty:
            event_counts = df["event_type"].value_counts().reset_index()
            event_counts.columns = ["event_type", "count"]
            st.bar_chart(
                event_counts,
                x="event_type",
                y="count",
                height=CHART_HEIGHT,
                use_container_width=True,
            )
        else:
            st.info("Event type analysis will appear after simulation.")

    with col_b:
        st.markdown("### Location Pressure")
        if not df.empty:
            location_counts = df["location"].value_counts().reset_index()
            location_counts.columns = ["location", "count"]
            st.bar_chart(
                location_counts,
                x="location",
                y="count",
                height=CHART_HEIGHT,
                use_container_width=True,
            )
        else:
            st.info("Location pressure will appear after simulation.")

    st.markdown("### Detection Matrix")
    if not df.empty:
        matrix = pd.crosstab(df["location"], df["alert_level"]).reindex(columns=SEVERITY_ORDER, fill_value=0)
        st.dataframe(matrix, use_container_width=True, height=COMPACT_TABLE_HEIGHT)
    else:
        st.info("No detection matrix available yet.")

with search_tab:
    st.markdown("### Indexed Frame Search")
    st.caption("Filters are controlled from the sidebar. Keyword search checks object, location, event, alert level, and description.")

    if not visible_df.empty:
        st.dataframe(
            visible_df[
                [
                    "frame_id",
                    "timestamp",
                    "location",
                    "alert_level",
                    "event_type",
                    "objects",
                    "altitude",
                    "description",
                    "recommendation",
                ]
            ],
            use_container_width=True,
            height=TABLE_HEIGHT,
            hide_index=True,
            column_config={
                "frame_id": "Frame",
                "timestamp": "Time",
                "alert_level": "Severity",
                "event_type": "Event Type",
                "altitude": st.column_config.NumberColumn("Altitude", format="%d m"),
            },
        )

        csv = visible_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download filtered incidents as CSV",
            data=csv,
            file_name="dronesec_filtered_incidents.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.warning("No matching indexed frames.")

with report_tab:
    st.markdown("### Executive Summary")
    if not df.empty:
        st.info(generate_daily_summary(events))

        report_lines = [
            "# DroneSec AI Incident Report",
            "",
            f"Frames processed: {len(df)}",
            f"Alerts generated: {len(alert_df)}",
            f"Critical incidents: {critical_count}",
            f"High-priority incidents: {high_count}",
            f"Drone mode: {health['mode']}",
            f"Battery level: {health['battery']}%",
            f"Dock status: {health['dock_status']}",
            f"Next drone action: {health['next_action']}",
            "",
            "## Recommended Next Actions",
            "- Review critical and high-priority footage first.",
            "- Dispatch patrol to locations with repeated alerts.",
            "- Return drone to dock if battery drops below safe patrol threshold.",
            "- Verify access points and equipment warnings.",
            "- Export filtered incidents for owner or security-team review.",
        ]
        report_text = "\n".join(report_lines)
        st.text_area("Report preview", report_text, height=210)
        st.download_button(
            "Download report",
            data=report_text.encode("utf-8"),
            file_name="dronesec_incident_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info("Run the simulation to generate a report.")
