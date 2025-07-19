import requests
import os

# URL to your update index (you will host this yourself - GitHub/Firebase)
BASE_UPDATE_URL = "https://your-update-server.com/ChrisAI/"
UPDATE_INDEX_FILE = "update_index.json"
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "features")
VERSION_FILE = os.path.join(os.path.dirname(__file__), "version.txt")

def read_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            return f.read().strip()
    return "0.0"

def write_version(new_version):
    with open(VERSION_FILE, 'w') as f:
        f.write(new_version)

def fetch_update_index():
    try:
        url = BASE_UPDATE_URL + UPDATE_INDEX_FILE
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch update index. HTTP:", response.status_code)
    except Exception as e:
        print("Error fetching update index:", e)
    return {}

def apply_updates(update_index):
    for feature, metadata in update_index.items():
        if feature == "version":
            continue  # Skip version field
        url = metadata.get("url")
        if not url:
            print(f"Missing URL for {feature}, skipping.")
            continue

        try:
            response = requests.get(url)
            if response.status_code == 200:
                feature_path = os.path.join(FEATURES_PATH, feature + ".py")
                os.makedirs(FEATURES_PATH, exist_ok=True)
                with open(feature_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Updated feature: {feature}")
            else:
                print(f"❌ Failed to download {feature}. HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Error updating {feature}:", e)

def upgrade():
    print("🔄 Checking for updates...")
    update_index = fetch_update_index()
    if update_index:
        apply_updates(update_index)
        latest_version = update_index.get("version", read_version())
        write_version(latest_version)
        print(f"✅ Upgrade completed. Current version: {latest_version}")
    else:
        print("❌ No updates found or failed to fetch.")
