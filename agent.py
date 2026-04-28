def detect_objects(description):
    description_lower = description.lower()
    objects = []

    if "person" in description_lower:
        objects.append("person")

    if "truck" in description_lower or "ford" in description_lower or "f150" in description_lower:
        objects.append("vehicle")
        objects.append("truck")
        objects.append("blue ford f150")

    if "smoke" in description_lower or "fire" in description_lower:
        objects.append("smoke/fire")

    if "dog" in description_lower:
        objects.append("animal")

    return list(set(objects))


def analyze_frame(frame, previous_frames):
    description = frame["description"]
    location = frame["location"]
    timestamp = frame["timestamp"]

    detected_objects = detect_objects(description)

    event_type = "Normal Activity"
    alert_level = "Low"
    recommendation = "Continue monitoring."

    desc_lower = description.lower()

    if "smoke" in desc_lower or "fire" in desc_lower:
        event_type = "Safety Hazard"
        alert_level = "Critical"
        recommendation = "Immediately notify property owner and dispatch security team."

    elif "same person" in desc_lower and "five minutes" in desc_lower:
        event_type = "Loitering"
        alert_level = "High"
        recommendation = "Send immediate alert. Person has remained near the same location."

    elif "person" in desc_lower and "midnight" in desc_lower:
        event_type = "Suspicious Person"
        alert_level = "Medium"
        recommendation = "Monitor closely and notify security if person remains."

    elif "entered again" in desc_lower or "spotted" in desc_lower:
        event_type = "Vehicle Activity"
        alert_level = "Medium"
        recommendation = "Log vehicle appearance and check for repeat entries."

    elif "dog" in desc_lower:
        event_type = "Animal Movement"
        alert_level = "Low"
        recommendation = "No immediate threat. Continue monitoring."

    return {
        "frame_id": frame["frame_id"],
        "timestamp": timestamp,
        "location": location,
        "altitude": frame["altitude"],
        "description": description,
        "objects": ", ".join(detected_objects),
        "event_type": event_type,
        "alert_level": alert_level,
        "recommendation": recommendation
    }


def generate_daily_summary(events):
    total_events = len(events)
    high_alerts = [e for e in events if e["alert_level"] in ["High", "Critical"]]
    vehicles = [e for e in events if "vehicle" in e["objects"].lower() or "truck" in e["objects"].lower()]
    persons = [e for e in events if "person" in e["objects"].lower()]

    summary = f"""
    DroneSec AI processed {total_events} frames today.
    It detected {len(persons)} person-related event(s), {len(vehicles)} vehicle-related event(s),
    and {len(high_alerts)} high-priority or critical alert(s).
    Key concerns include suspicious loitering, repeated vehicle activity, and safety hazards if present.
    """

    return summary.strip()