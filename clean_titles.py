# titles.txt üres sorainak törlése

# titles = "titles.txt"
titles = "all-titles.txt"

with open(titles, "r", encoding="utf-8") as f:
    lines = f.readlines()

# csak a nem üres sorok megtartása
clean_lines = [line for line in lines if line.strip()]

with open(titles, "w", encoding="utf-8") as f:
    f.writelines(clean_lines)
