import pandas as pd
from datetime import datetime
from pathlib import Path

output_dir = Path("./task1score")
output_dir.mkdir(parents=True, exist_ok=True)

map1 = pd.read_excel("Data - Map 1.xlsx")
map2 = pd.read_excel("Data - Map 2.xlsx")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

rk = "Route Knowledge Only"
sk = "Survey Knowledge"


def calculate_accuracy(data, answer, map_number):
    total_real = 7
    total_fake = 3
    users = []
    for index, row in data.iterrows():
        selected_landmarks = row["Landmark Recognition"].rstrip(";").split(";")
        selected_landmarks = [x.strip() for x in selected_landmarks]
        # # count the number of correct answers
        hits = sum(1 for landmark in selected_landmarks if landmark in answer)
        misses = total_real - hits
        false_alarm = sum(
            1 for landmark in selected_landmarks if landmark not in answer
        )
        correct_rejections = total_fake - false_alarm
        accuracy = round(
            0.5
            * (
                (hits / (hits + misses))
                + (correct_rejections / (correct_rejections + false_alarm))
            ),
            3,
        )
        users.append(
            {
                "Participant ID": row["Participant ID"],
                "Study Group": row["Study Group"],
                "Map": f"Map {map_number}",
                "User Answer": row["Landmark Recognition"],
                "Hits": hits,
                "Misses": misses,
                "Correct Rejections": correct_rejections,
                "False Alarm": false_alarm,
                "Accuracy": accuracy,
            }
        )

    # create the directories
    path_raw = Path(output_dir) / f"Map {map_number}" / "raw"
    path_raw.mkdir(parents=True, exist_ok=True)
    path_backups = Path(output_dir) / f"Map {map_number}" / "backups"
    path_backups.mkdir(parents=True, exist_ok=True)
    # convert to excel and save
    excel = pd.DataFrame(users)
    excel.to_excel(path_raw / f"Map{map_number}_accuracy.xlsx", index=False)
    excel.to_excel(
        path_backups / f"{timestamp}_Map{map_number}_accuracy.xlsx", index=False
    )
    return users


answer_map1 = [
    "Bridge",
    "Town Hall",
    "H&M Store",
    "Art Piece",
    "Trees and colorful chairs",
    "Playground",
    "Parking",
]

map1_users = calculate_accuracy(map1, answer_map1, 1)

answer_map2 = [
    "Glass Stairwell Entrance",
    "D&C Store",
    "Shopping Mall",
    "Church",
    "Rossmann Store",
    "Yellow Café",
    "Kiosk",
]

map2_users = calculate_accuracy(map2, answer_map2, 2)

# Combine the results from both maps based on Participant ID and Study Group
combined_results = []

for user in map1_users:
    user_map2 = next(
        (u for u in map2_users if u["Participant ID"] == user["Participant ID"]),
        None,
    )
    if user_map2:
        sk_score = (
            user["Accuracy"] if user["Study Group"] == sk else user_map2["Accuracy"]
        )
        rk_score = (
            user["Accuracy"] if user["Study Group"] == rk else user_map2["Accuracy"]
        )
        ob = {
            "Participant ID": user["Participant ID"],
            "Accuracy - RK": rk_score,
            "Accuracy - SK": sk_score,
        }
        combined_results.append(ob)


path_raw = Path(output_dir) / "paired" / "raw"
path_raw.mkdir(parents=True, exist_ok=True)
path_backups = Path(output_dir) / "paired" / "backups"
path_backups.mkdir(parents=True, exist_ok=True)

# convert to excel and save
excel = pd.DataFrame(combined_results)
excel.to_excel(path_raw / "paired_accuracy.xlsx", index=False)
excel.to_excel(path_backups / f"{timestamp}_paired_accuracy.xlsx", index=False)
