import os
import shutil
import pickle
import random
from datetime import datetime, timezone

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


# ===== BEÁLLÍTÁSOK =====
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEOS_FOLDER = "public"
SUCCESS_FOLDER = "tiktok"

DESCRIPTIONS_FOLDER = os.path.join("data", "descriptions")
TAGS_FOLDER = os.path.join("data", "tags")

FORTNITE = "#shorts #fortnite"
BRAWLSTARS = "#shorts #brawlstars"

# PRIVACY_STATUS = "public"
PRIVACY_STATUS = "private"

DEFAULT_LANGUAGE = "hu"
CATEGORY_ID = 20

VIDEO_LOCATION = {"latitude": 47.9556, "longitude": 21.7167}
LOCATION_DESCRIPTION = "Nyíregyháza, Magyarország"


# ===== AUTH =====
def get_authenticated_service():
    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        credentials = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


# ===== RANDOM DESCRIPTION =====
def get_random_description():
    if not os.path.exists(DESCRIPTIONS_FOLDER):
        raise FileNotFoundError("❌ A data/descriptions mappa nem létezik")

    files = [f for f in os.listdir(DESCRIPTIONS_FOLDER) if f.endswith(".txt")]

    if not files:
        raise FileNotFoundError("❌ Nincs .txt fájl a data/descriptions mappában")

    chosen = random.choice(files)
    path = os.path.join(DESCRIPTIONS_FOLDER, chosen)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content, chosen


# ===== RANDOM TAGS =====
def get_random_tags():
    if not os.path.exists(TAGS_FOLDER):
        raise FileNotFoundError("❌ A data/tags mappa nem létezik")

    files = [f for f in os.listdir(TAGS_FOLDER) if f.endswith(".txt")]

    if not files:
        raise FileNotFoundError("❌ Nincs .txt fájl a data/tags mappában")

    chosen = random.choice(files)
    path = os.path.join(TAGS_FOLDER, chosen)

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # vessző vagy sortörés alapú tagek kezelése
    tags = []
    for line in raw.replace(",", "\n").splitlines():
        tag = line.strip()
        if tag:
            tags.append(tag)

    return tags, chosen


# ===== UPLOAD =====
def upload_video(youtube, file_path, title):
    now_iso = datetime.now(timezone.utc).isoformat()

    description_text, desc_file = get_random_description()
    tags_list, tags_file = get_random_tags()

    request = youtube.videos().insert(
        part="snippet,status,recordingDetails",
        body={
            "snippet": {
                "title": f"{title} | {BRAWLSTARS}",
                "description": f"{title} | {description_text}",
                "tags": tags_list,
                "categoryId": str(CATEGORY_ID),
                "defaultLanguage": DEFAULT_LANGUAGE,
                "defaultAudioLanguage": "hu"
            },
            "status": {
                "privacyStatus": PRIVACY_STATUS
            },
            "recordingDetails": {
                "recordingDate": now_iso,
                "location": VIDEO_LOCATION,
                "locationDescription": LOCATION_DESCRIPTION
            }
        },
        media_body=MediaFileUpload(file_path, resumable=True)
    )

    try:
        response = request.execute()
        print(f"✅ Feltöltve: {title}")
        print(f"📝 Leírás fájl: {desc_file}")
        print(f"🏷️ Tag fájl: {tags_file}")
        print(f"🔗 https://www.youtube.com/watch?v={response['id']}\n")
        return True

    except HttpError as e:
        error = e.content.decode("utf-8")

        if "uploadLimitExceeded" in error:
            print(f"⛔ NAPI LIMIT – kihagyva: {title}\n")
            return False

        print(f"❌ Hiba ennél a videónál: {title}")
        print(error, "\n")
        return False


# ===== MAIN =====
if __name__ == "__main__":
    youtube = get_authenticated_service()

    if not os.path.exists(VIDEOS_FOLDER):
        print("❌ public mappa nem létezik")
        exit(1)

    os.makedirs(SUCCESS_FOLDER, exist_ok=True)

    videos = sorted([
        f for f in os.listdir(VIDEOS_FOLDER)
        if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
    ])

    if not videos:
        print("❌ Nincs videó a public mappában")
        exit(1)

    print(f"🎬 Feldolgozás alatt: {len(videos)} videó\n")

    for video in videos:
        src_path = os.path.join(VIDEOS_FOLDER, video)
        dst_path = os.path.join(SUCCESS_FOLDER, video)
        title = os.path.splitext(video)[0]

        success = upload_video(youtube, src_path, title)

        if success:
            shutil.move(src_path, dst_path)
            print(f"📁 Átmozgatva ide: {SUCCESS_FOLDER}/{video}\n")

    print("🏁 Kész. Csak a sikeres videók lettek áthelyezve.")

