import os
import re

# Fő mappa elérési útja (ahol a 'videos' és a 'titles.txt' található)
main_folder = os.path.dirname(os.path.abspath(__file__))
videos_folder = os.path.join(main_folder, "videos")
titles_file = os.path.join(main_folder, "titles.txt")

# Natural sort függvény (számokat is helyesen kezeli)
def natural_sort_key(s):
    # Felbontja a szöveget számokra és szövegre, pl. "video10.mp4" → ["video", 10, ".mp4"]
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# Videók listázása a 'videos' mappából (csak mp4 fájlok), természetes sorrendben
video_files = sorted(
    [f for f in os.listdir(videos_folder) if f.lower().endswith(".mp4")],
    key=natural_sort_key
)

# Címek beolvasása a titles.txt-ből
with open(titles_file, "r", encoding="utf-8") as f:
    titles = [line.strip() for line in f if line.strip()]

# Ellenőrzés: ugyanannyi cím legyen, mint videó
if len(titles) != len(video_files):
    print(f"Hiba: {len(video_files)} videó van, de {len(titles)} cím a titles.txt-ben.")
    exit(1)

# Videók átnevezése
for old_name, new_title in zip(video_files, titles):
    old_path = os.path.join(videos_folder, old_name)
    new_name = f"{new_title}.mp4"
    new_path = os.path.join(videos_folder, new_name)
    
    # Ha a fájl már létezik, ne írja felül
    if os.path.exists(new_path):
        print(f"Figyelem: {new_name} már létezik, kihagyva.")
        continue
    
    os.rename(old_path, new_path)
    print(f"{old_name} → {new_name}")

print("Átnevezés kész!")
