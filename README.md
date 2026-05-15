<img width="1905" height="967" alt="image" src="https://github.com/user-attachments/assets/a5594dc6-ca34-4064-bb97-0782ceff78ca" />
<img width="1904" height="1084" alt="image" src="https://github.com/user-attachments/assets/5b2e2236-6943-4fb2-9a13-6c05b3564da4" />

# DroneSec AI - Drone Security Analyst Agent

DroneSec AI is a prototype AI-powered security analyst for an autonomous docked drone monitoring a fixed property.

The system processes simulated drone telemetry and simulated frame descriptions, detects security events, generates alerts, indexes each frame in SQLite, and provides a professional Streamlit command-center dashboard for review and reporting.

---

## Problem Statement

Property owners often rely on fixed CCTV cameras or manual patrols to detect security incidents. CCTV coverage is limited to fixed angles, while manual monitoring can be slow and reactive.

DroneSec AI demonstrates how a docked autonomous drone can act as a mobile monitoring system. The drone follows patrol logic, returns to its charging dock, and sends observations to an analyst agent that classifies risk and recommends action.

---

## Key Features

- Simulated autonomous drone patrol frames
- Battery, dock, and flight-time simulation
- Drone mode tracking, including patrol and return-to-dock states
- Object detection from frame descriptions
- Security event classification
- Alert severity scoring: Low, Medium, High, Critical
- SQLite-based event indexing
- Searchable event history
- Analyst filters by keyword, severity, location, and risk score
- Incident queue with SLA, owner, and status
- Drone system dashboard with route map and automation rules
- Manual frame analysis with optional image upload
- CSV export for filtered incidents
- Markdown incident report export
- Pytest test cases for core detection and alert logic

---

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Pytest

---

## Run Locally

```powershell
cd "C:\Users\dewan\OneDrive\Desktop\drone-security-analyst-agent"
.\venv\Scripts\python.exe -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## System Architecture Diagram

The following diagram shows the end-to-end flow of the DroneSec AI prototype.

![DroneSec AI Architecture](assets/architecture.svg)

---

## Architecture Flow

```text
Autonomous Drone + Charging Dock
                |
Simulated Drone Telemetry + Frame Descriptions
                |
Frame Processing Engine
                |
Object and Event Detection
                |
Rule-Based Security Agent
                |
SQLite Frame Index
                |
Streamlit Command Center
                |
Security Logs + Alerts + Search + Reports
```
