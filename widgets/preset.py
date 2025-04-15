import os
import json
from datetime import datetime

def get_preset_names():
    os.makedirs('presets', exist_ok=True)
    return [f.replace('.json', '') for f in os.listdir('presets') if f.endswith('.json')]

def save_preset(screen, mode):
    if not os.path.exists("presets"):
        os.makedirs("presets")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{mode}_{timestamp}.json"
    filepath = os.path.join("presets", filename)

    preset_data = {
        "mode": mode,
        "created": timestamp,
        "steps": [{"temp": step.target_temp, "time": step.target_time} for step in screen.steps]
    }

    with open(filepath, "w") as f:
        json.dump(preset_data, f, indent=4)

    print(f"Preset saved as {filename}")

def load_preset(screen, preset_name):
    with open(f'presets/{preset_name}', 'r') as f:
        preset_data = json.load(f)
    screen.clear_steps()
    screen.add_custom_steps(preset_data['steps'])

def get_preset_details(mode=None):
    presets_dir = "presets"
    if not os.path.exists(presets_dir):
        return []

    files = os.listdir(presets_dir)

    if mode:
        files = [f for f in files if f.startswith(f"{mode}_")]

    details = []
    for file in files:
        filepath = os.path.join(presets_dir, file)
        with open(filepath, "r") as f:
            data = json.load(f)
            details.append({
                "name": file.replace(".json", ""),
                "created_at": data.get("created", "Unknown"),
                "file_name": file
            })

    return details

def delete_preset(preset_name):
    filepath = os.path.join("presets", preset_name)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted preset: {preset_name}")
    else:
        print(f"Preset {preset_name} not found.")
