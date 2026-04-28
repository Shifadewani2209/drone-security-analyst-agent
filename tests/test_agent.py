import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import analyze_frame, detect_objects


def test_detect_truck():
    description = "Blue Ford F150 spotted near garage"
    objects = detect_objects(description)

    assert "vehicle" in objects
    assert "truck" in objects
    assert "blue ford f150" in objects


def test_detect_person():
    description = "Person standing near main gate at midnight"
    objects = detect_objects(description)

    assert "person" in objects


def test_detect_smoke():
    description = "Smoke detected near warehouse"
    objects = detect_objects(description)

    assert "smoke/fire" in objects


def test_loitering_alert():
    frame = {
        "frame_id": 2,
        "timestamp": "00:06",
        "location": "Main Gate",
        "altitude": 35,
        "description": "Same person still standing near main gate after five minutes"
    }

    result = analyze_frame(frame, [])

    assert result["event_type"] == "Loitering"
    assert result["alert_level"] == "High"


def test_smoke_alert():
    frame = {
        "frame_id": 5,
        "timestamp": "23:45",
        "location": "Warehouse",
        "altitude": 38,
        "description": "Smoke detected near warehouse"
    }

    result = analyze_frame(frame, [])

    assert result["event_type"] == "Safety Hazard"
    assert result["alert_level"] == "Critical"