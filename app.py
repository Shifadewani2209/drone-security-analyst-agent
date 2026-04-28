import streamlit as st
import pandas as pd

from simulator import get_simulated_frames
from agent import analyze_frame, generate_daily_summary
from database import init_db, clear_db, insert_event, get_all_events, search_events


st.set_page_config(
    page_title="DroneSec AI",
    page_icon="🚁",
    layout="wide"
)

init_db()

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #e2e8f0;
    margin-bottom: 0;
}
.subtitle {
    font-size: 18px;
    color: #94a3b8;
    margin-top: 0;
}
.card {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    margin-bottom: 16px;
}
.section-title {
    color: #e2e8f0;
    font-size: 24px;
    font-weight: 700;
}
.small-text {
    color: #94a3b8;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


st.title("🚁 DroneSec AI")
st.caption("Drone Security Analyst Agent for simulated telemetry, frame indexing, event detection, and real-time alerts.")

st.divider()

events = get_all_events()

total_frames = len(events)
alerts = [e for e in events if e["alert_level"] in ["Medium", "High", "Critical"]]
critical_alerts = [e for e in events if e["alert_level"] == "Critical"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Frames Processed", total_frames)

with col2:
    st.metric("Alerts Generated", len(alerts))

with col3:
    st.metric("Critical Alerts", len(critical_alerts))

with col4:
    st.metric("Indexing Engine", "SQLite")

st.divider()

left, right = st.columns([1, 1])

with left:
    st.markdown("### ▶ Simulation Control")
    st.write("Start the drone patrol simulation and process frame-by-frame security events.")

    if st.button("Start Drone Simulation", use_container_width=True):
        clear_db()

        frames = get_simulated_frames()
        previous_frames = []

        for frame in frames:
            event = analyze_frame(frame, previous_frames)
            insert_event(event)
            previous_frames.append(frame)

        st.success("Drone simulation completed. Frames analyzed, alerts generated, and events indexed.")

with right:
    st.markdown("### 🗑 Database Control")
    st.write("Clear all indexed frame records and reset the dashboard.")

    if st.button("Clear Database", use_container_width=True):
        clear_db()
        st.warning("Database cleared successfully.")

st.divider()

events = get_all_events()

st.markdown("### 📍 Security Event Logs")

if events:
    df = pd.DataFrame(events)
    st.dataframe(df, use_container_width=True, height=320)
else:
    st.info("No events found. Click 'Start Drone Simulation' to begin.")

st.divider()

st.markdown("### 🚨 Real-Time Alert Panel")

if events:
    alert_events = [e for e in events if e["alert_level"] in ["Medium", "High", "Critical"]]

    if alert_events:
        for alert in alert_events:
            message = f"{alert['event_type']} detected at {alert['location']} at {alert['timestamp']}. Recommendation: {alert['recommendation']}"

            if alert["alert_level"] == "Critical":
                st.error(f"🚨 CRITICAL — {message}")
            elif alert["alert_level"] == "High":
                st.warning(f"⚠ HIGH — {message}")
            else:
                st.info(f"ℹ MEDIUM — {message}")
    else:
        st.success("No active security alerts.")
else:
    st.info("No alerts yet.")

st.divider()

st.markdown("### 🔎 Query Indexed Frames")

st.caption("Try searches like: truck, person, smoke, main gate, critical, garage, loitering")

keyword = st.text_input(
    "Search by object, location, event type, or alert level",
    placeholder="Example: truck"
)

if keyword:
    results = search_events(keyword)

    if results:
        st.success(f"Found {len(results)} matching indexed frame(s).")
        st.dataframe(pd.DataFrame(results), use_container_width=True)
    else:
        st.warning("No matching events found.")

st.divider()

st.markdown("### 🧠 AI Security Summary")

if events:
    summary = generate_daily_summary(events)
    st.success(summary)
else:
    st.info("Summary will appear after simulation.")

st.divider()

st.markdown("### 🏗 System Architecture")

st.code("""
Simulated Drone Telemetry + Frame Descriptions
                ↓
Frame Processing Engine
                ↓
Object and Event Detection
                ↓
Rule-Based Security Agent
                ↓
SQLite Frame Index
                ↓
Dashboard + Alerts + Search + Summary
""")