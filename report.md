# DroneSec AI — Drone Security Analyst Agent Report

## 1. Introduction

DroneSec AI is a prototype AI-powered Drone Security Analyst Agent designed for a docked drone monitoring a fixed property. The system processes simulated drone telemetry and simulated video-frame descriptions to detect objects, analyze security events, generate alerts, index frames, and provide searchable event history.

The prototype demonstrates how an AI agent can support property owners by automatically identifying suspicious activity, safety hazards, and repeated vehicle appearances without requiring constant manual monitoring.

## 2. Problem Understanding

Property owners often rely on CCTV footage or human supervision to detect security incidents. This approach is reactive and time-consuming. A docked drone security analyst can improve monitoring by regularly scanning the property, analyzing observed events, and generating real-time alerts when suspicious or unsafe activity is detected.

The assignment required a prototype that can process simulated drone telemetry and video frames, identify objects or events, log them with context, generate alerts, and index frames for later search.

## 3. Assumptions

- Real drone video footage was not provided, so video frames were simulated using structured text descriptions.
- The prototype focuses on security reasoning, indexing, alert generation, and queryability.
- In a production system, the simulated frame descriptions can be replaced with outputs from a Vision Language Model or object detection model.
- SQLite was selected as a lightweight database for frame-by-frame indexing.
- Rule-based alert logic was used to keep the prototype transparent and explainable.

## 4. Key Features

- Simulated drone telemetry with timestamp, location, and altitude.
- Simulated video frame descriptions.
- Object detection from frame descriptions.
- Security event classification.
- Real-time alert generation.
- SQLite-based frame indexing.
- Searchable event history.
- AI-style daily security summary.
- Test cases for detection and alert logic.

## 5. System Architecture

The system follows a modular pipeline:

```text
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
Dashboard, Alerts, Search, and Summary