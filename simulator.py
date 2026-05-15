def get_patrol_route():
    return [
        {"step": 1, "location": "Charging Dock", "action": "Launch from dock", "battery_cost": 0},
        {"step": 2, "location": "Main Gate", "action": "Check entry point", "battery_cost": 8},
        {"step": 3, "location": "East Fence", "action": "Scan perimeter breach risk", "battery_cost": 10},
        {"step": 4, "location": "North Yard", "action": "Inspect loading zone", "battery_cost": 9},
        {"step": 5, "location": "Garage", "action": "Verify vehicle activity", "battery_cost": 8},
        {"step": 6, "location": "Warehouse", "action": "Check fire and smoke risk", "battery_cost": 11},
        {"step": 7, "location": "Backyard", "action": "Scan fence line", "battery_cost": 7},
        {"step": 8, "location": "Charging Dock", "action": "Return and recharge", "battery_cost": 0},
    ]


def simulate_drone_health(frames_processed):
    start_battery = 96
    battery_used = min(frames_processed * 6, 82)
    battery = max(start_battery - battery_used, 14)

    if frames_processed == 0:
        mode = "Docked"
        next_action = "Await scheduled patrol"
    elif battery <= 25:
        mode = "Return to Dock"
        next_action = "Land and recharge before next patrol"
    elif battery <= 45:
        mode = "Patrol - Battery Watch"
        next_action = "Complete nearest route segment, then return"
    else:
        mode = "Autonomous Patrol"
        next_action = "Continue route and monitor priority zones"

    dock_temperature = 31 + min(frames_processed, 12)
    dock_status = "Thermal Warning" if dock_temperature >= 40 else "Ready"
    charging_status = "Charging" if mode in ["Docked", "Return to Dock"] else "Discharging"
    flight_time_remaining = max(int((battery - 20) * 0.55), 0)

    return {
        "battery": battery,
        "mode": mode,
        "next_action": next_action,
        "dock_temperature": dock_temperature,
        "dock_status": dock_status,
        "charging_status": charging_status,
        "flight_time_remaining": flight_time_remaining,
    }


def get_simulated_frames():
    return [
        {
            "frame_id": 1,
            "timestamp": "00:01",
            "location": "Main Gate",
            "altitude": 35,
            "description": "Person standing near main gate at midnight"
        },
        {
            "frame_id": 2,
            "timestamp": "00:06",
            "location": "Main Gate",
            "altitude": 35,
            "description": "Same person still standing near main gate after five minutes"
        },
        {
            "frame_id": 3,
            "timestamp": "00:14",
            "location": "East Fence",
            "altitude": 34,
            "description": "Person climbing east fence near restricted service road"
        },
        {
            "frame_id": 4,
            "timestamp": "03:18",
            "location": "North Yard",
            "altitude": 36,
            "description": "Unauthorized van parked near north yard loading zone"
        },
        {
            "frame_id": 5,
            "timestamp": "12:00",
            "location": "Garage",
            "altitude": 40,
            "description": "Blue Ford F150 spotted near garage"
        },
        {
            "frame_id": 6,
            "timestamp": "14:20",
            "location": "Garage",
            "altitude": 40,
            "description": "Blue Ford F150 entered again near garage"
        },
        {
            "frame_id": 7,
            "timestamp": "16:10",
            "location": "Solar Shed",
            "altitude": 33,
            "description": "Drone battery dock temperature warning at solar shed"
        },
        {
            "frame_id": 8,
            "timestamp": "23:45",
            "location": "Warehouse",
            "altitude": 38,
            "description": "Smoke detected near warehouse"
        },
        {
            "frame_id": 9,
            "timestamp": "18:30",
            "location": "Backyard",
            "altitude": 32,
            "description": "Dog detected moving near backyard fence"
        },
        {
            "frame_id": 10,
            "timestamp": "19:05",
            "location": "Backyard",
            "altitude": 31,
            "description": "Wind-blown tarp moving near backyard fence"
        },
        {
            "frame_id": 11,
            "timestamp": "21:30",
            "location": "South Door",
            "altitude": 35,
            "description": "Open door detected at south door after business hours"
        },
        {
            "frame_id": 12,
            "timestamp": "22:12",
            "location": "Perimeter Road",
            "altitude": 42,
            "description": "Two persons walking along perimeter road with flashlight"
        }
    ]
