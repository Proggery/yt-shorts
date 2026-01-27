import os
import re
import shutil  # az áthelyezéshez

# Fő mappa elérési útja
main_folder = os.path.dirname(os.path.abspath(__file__))
videos_folder = os.path.join(main_folder, "videos")
public_folder = os.path.join(main_folder, "public")  # cél mappa
titles_file = os.path.join(main_folder, "titles.txt")

# Natural sort (számokat helyesen kezeli)
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

# Videók listázása (mp4), természetes sorrendben
video_files = sorted(
    [f for f in os.listdir(videos_folder) if f.lower().endswith(".mp4")],
    key=natural_sort_key
)

# Címek beolvasása
with open(titles_file, "r", encoding="utf-8") as f:
    titles = [line.strip() for line in f if line.strip()]

# Mennyi fájlt nevezünk át (csak annyit, ahány cím van)
rename_count = min(len(titles), len(video_files))

if rename_count == 0:
    print("Nincs mit átnevezni.")
    exit(0)

# Ha nincs public mappa, létrehozzuk
os.makedirs(public_folder, exist_ok=True)

# Videók átnevezése és áthelyezése a public mappába
for i in range(rename_count):
    old_name = video_files[i]
    new_title = titles[i]

    old_path = os.path.join(videos_folder, old_name)
    new_name = f"{new_title}.mp4"
    new_path = os.path.join(public_folder, new_name)  # ide kerül

    if os.path.exists(new_path):
        print(f"Figyelem: {new_name} már létezik a 'public' mappában, kihagyva.")
        continue

    os.rename(old_path, new_path)
    print(f"{old_name} → {new_name} (átmozgatva a public mappába)")

print(f"Kész! {rename_count} videó átnevezve és áthelyezve a 'public' mappába.")
