import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "medium"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        for key, value in DEFAULT_SETTINGS.items():
            if key not in data:
                data[key] = value
        return data
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        save_leaderboard([])
        return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_score(name, score, distance, coins):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance,
        "coins": coins
    })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_leaderboard(leaderboard)