import os
import pickle
from datetime import datetime, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube feltöltési jogosultság
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEOS_FOLDER = "public"  # videók mappája
TITLES_FILE = "titles.txt"  # címek fájlja

DESCRIPTION_TEMPLATE = """Te is rajongsz a Fortnite: Battle Royale és a Call Of Duty: Warzone 2.0 rejtelmes világáért, illetve szereted nézni a különböző háborús, akciós multiplayer játékok online közvetítését? Akkor itt a helyed a GeryHell csatornán! Ne habozz és iratkozz fel a csatornára, hogy ne maradj le egy közvetítésről sem! Ha van bármilyen gondolatod a videóval kapcsolatban, örülnék ha egy kommentel megosztanád velem, legyen az pozitív vagy akár negatív gondolat is, és mind a kettőt örömmel fogom olvasni! Örülnék, ha te is közénk tartoznál, és mivel még kezdetleges csatornáról van szó, ami bármelyik pillanatban kirobbanhat, így ragadd meg mihamarabb az alkalmat a csatlakozásra, hogy az elsők köztett lehess! Gyere és szórakozzunk együtt :)

- - - - - - - - - - - - -

❗️🔱🔥 GERYHELL 10 PARANCSOLATA 🔥🔱❗️ (csatorna szabályzata)
1. TISZTELD a másik játékost, ha játszottál egy play-ben, akkor ADD ÁT a helyed a másik játékosnak!
2. NE KÉRDEZD, hogy jöhetsz-e játszani, NE SPAM-ELJ, NE POLITIZÁLJ és NE tegyél szexuális megjegyzéseket másoknak!
3. NE küldj invitációt és joint sem, majd én meginvitállak a play-be, ha rajtad a sor!
4. Csak akkor jöhet valaki játszani, ha a CSETEN IS JELEN VAN és aktív!
5. Ha bejelölsz a játékban, akkor írd meg (csak ha lobby-ban vagyok), hogy milyen névvel jelöltél be!
6. Nem küldök baráti felkérést senkinek, küldj te nekem (GeryHell) és el fogom fogadni!
7. FIGYELJ MINDIG ARRA, hogy mit kérdezek és mondok! Így nem fog érni csalódás!
8. NE KUNCSOROGJ gifekért, ajándékokért (ez azonnali bannal jár)!
9. FIGYELJ ÉS FOGADD EL azoknak a nézőknek a tanácsát, akik már a kezdetektől (rendszeresen) itt vannak a cseten, mert tőlük csak tanulhatsz!
10. FOGADD EL a döntésemet, illetve a többség döntését és akkor közénk fogsz tartozni!

- - - - - - - - - - - - -

A GeryHell csatorna közvetítései:
🔥 Brawl Stars
🔥 Fortnite: Battle Royal

✨✨ DONATE: https://streamlabs.com/geryhell01/tip
✨✨ YOUTUBE: @geryhell01
✨✨ DISCORD: Kérd el live-ban!
✨✨ INSTAGRAM: geryhell
✨✨ TIKTOK: @geryhell

#játék #magyar #fortnite #bs #brawlstars #fortnitemagyar #fortnitemagyarul #fortnitemagyarország #live #stream #magyarstream #legjobbstreamer #legjobbmagyarstreamer #fortnite #memes #fortnitememes #meme #gaming #funny #dankmemes #gamer #fortniteclips #fortnitebattleroyale #dank #xbox #lol #fortnitecommunity #twitch #ps4 #youtube #fortnitebr #funnymemes #memesdaily #edgymemes #comedy #pubg #like"""

TAGS_TEMPLATE = [
    "bs","brawlstars","játék","fortnite","Shorts","call of duty","cod","warzone","warzone 2.0",
    "gaming mix 2026","ncs gaming mix","gaming pc","total gaming","gaming room","royalty gaming channel",
    "gaming pc build","royalty gaming","debrecen","nyíregyháza","kidcity gaming","kids gaming",
    "ferran gaming","family gaming","valorant","steam deck","funny game","action games","pc games",
    "pc gaming","játék","magyar","háborús","best streamer","sub","game","2025","minecraft","2026"
]

PRIVACY_STATUS = "public"
DEFAULT_LANGUAGE = "hu"
CATEGORY_ID = 20  # Játékok

VIDEO_LOCATION = {"latitude": 47.9556, "longitude": 21.7167}
LOCATION_DESCRIPTION = "Nyíregyháza, Magyarország"

def get_authenticated_service():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        credentials = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path, title):
    now_iso = datetime.now(timezone.utc).isoformat()
    request = youtube.videos().insert(
        part="snippet,status,recordingDetails",
        body={
            "snippet": {
                "title": f"{title} | Fortnite: Battle Royal",
                "description": DESCRIPTION_TEMPLATE,
                "tags": TAGS_TEMPLATE,
                "categoryId": str(CATEGORY_ID),
                "defaultLanguage": DEFAULT_LANGUAGE,
                "defaultAudioLanguage": "hu",
                "videoGameTitle": "Fortnite"
            },
            "status": {"privacyStatus": PRIVACY_STATUS},
            "recordingDetails": {
                "recordingDate": now_iso,
                "location": VIDEO_LOCATION,
                "locationDescription": LOCATION_DESCRIPTION
            }
        },
        media_body=MediaFileUpload(file_path)
    )
    response = request.execute()
    print(f"Video uploaded: {title}")
    print(f"Video ID: {response['id']}")
    print(f"YouTube link: https://www.youtube.com/watch?v={response['id']}\n")

def clear_public_folder_and_titles():
    # public mappa tartalmának törlése
    if os.path.exists(VIDEOS_FOLDER):
        for f in os.listdir(VIDEOS_FOLDER):
            file_path = os.path.join(VIDEOS_FOLDER, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"A '{VIDEOS_FOLDER}' mappa tartalma törölve lett.")

    # titles.txt tartalmának ürítése (fájl megmarad)
    if os.path.exists(TITLES_FILE):
        with open(TITLES_FILE, "w", encoding="utf-8") as f:
            pass  # üres írás
        print(f"A '{TITLES_FILE}' tartalma törölve lett.")

if __name__ == "__main__":
    youtube = get_authenticated_service()

    if not os.path.exists(VIDEOS_FOLDER):
        print(f"A '{VIDEOS_FOLDER}' mappa nem található!")
        exit(1)

    videos = [f for f in os.listdir(VIDEOS_FOLDER) if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]

    if not videos:
        print(f"Nincs videó a '{VIDEOS_FOLDER}' mappában!")
        exit(1)

    for video_file in videos:
        file_path = os.path.join(VIDEOS_FOLDER, video_file)
        title = os.path.splitext(video_file)[0]
        upload_video(youtube, file_path, title)

    # a végén törlés
    clear_public_folder_and_titles()
