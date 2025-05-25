import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np


output_dir = Path("./task2score")
output_dir.mkdir(parents=True, exist_ok=True)

map1 = pd.read_excel("Data - Map 1.xlsx")
map2 = pd.read_excel("Data - Map 2.xlsx")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

rk = "Route Knowledge Only"
sk = "Survey Knowledge"


def levenshtein(a, b, ratio=False, print_matrix=False, lowercase=False):
    if type(a) != type(""):
        raise TypeError("First argument is not a string!")
    if type(b) != type(""):
        raise TypeError("Second argument is not a string!")
    if a == "":
        return len(b)
    if b == "":
        return len(a)
    if lowercase:
        a = a.lower()
        b = b.lower()

    n = len(a)
    m = len(b)
    lev = np.zeros((n + 1, m + 1))

    for i in range(0, n + 1):
        lev[i, 0] = i
    for i in range(0, m + 1):
        lev[0, i] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insertion = lev[i - 1, j] + 1
            deletion = lev[i, j - 1] + 1
            substitution = lev[i - 1, j - 1] + (1 if a[i - 1] != b[j - 1] else 0)
            lev[i, j] = min(insertion, deletion, substitution)

    if print_matrix:
        print(lev)

    if ratio:
        return (n + m - lev[n, m]) / (n + m)
    else:
        return lev[n, m]


def rescaled_similarity(r):
    r_min = 8 / 14  # = 0.5714
    return (r - r_min) / (1 - r_min)


def calculate_scores(data, answer, map_number):
    answer_str = "".join(answer.keys())
    value_to_key = {v: k for k, v in answer.items()}

    users = []
    for index, row in data.iterrows():
        user_order = row["Ordering the Landmarks"].rstrip(";").split(";")
        user_order_str = "".join(
            value_to_key[item.replace("\xa0", " ")] for item in user_order
        )
        score = levenshtein(
            answer_str,
            user_order_str,
            ratio=True,
        )
        rescaled_score = rescaled_similarity(score)
        users.append(
            {
                "Participant ID": row["Participant ID"],
                "Study Group": row["Study Group"],
                "Map": f"Map {map_number}",
                "User Answer": row["Ordering the Landmarks"],
                "Score": score,
                "Rescaled Score": rescaled_score,
                "answer_str": answer_str,
                "user_order_str": user_order_str,
            }
        )
        # print(
        #     f"Participant ID: {row['Participant ID']}",
        #     user_order_str,
        #     f"Score: {score}",
        # )
    return users


# test the function

map1_answer = {
    "0": "Bridge",
    "1": "Town Hall",
    "2": "Playground",
    "3": "Trees and colorful chairs",
    "4": "H&M Store",
    "5": "Art Piece",
    "6": "Parking",
}

map2_answer = {
    "0": "Glass Stairwell Entrance",
    "1": "Church",
    "2": "Yellow Café",
    "3": "Hot Dog Cart",
    "4": "Shopping Mall",
    "5": "Rossmann Store",
    "6": "Kiosk",
}

map1_users = calculate_scores(map1, map1_answer, 1)
map2_users = calculate_scores(map2, map2_answer, 2)


combined_results = []

for user in map1_users:
    user_map2 = next(
        (u for u in map2_users if u["Participant ID"] == user["Participant ID"]),
        None,
    )
    if user_map2:
        rk_score = user["Score"] if user["Study Group"] == rk else user_map2["Score"]
        sk_score = user["Score"] if user["Study Group"] == sk else user_map2["Score"]

        rk_rescaled_score = (
            user["Rescaled Score"]
            if user["Study Group"] == rk
            else user_map2["Rescaled Score"]
        )
        sk_rescaled_score = (
            user["Rescaled Score"]
            if user["Study Group"] == sk
            else user_map2["Rescaled Score"]
        )

        rk_user_order_str = (
            user["user_order_str"]
            if user["Study Group"] == rk
            else user_map2["user_order_str"]
        )
        sk_user_order_str = (
            user["user_order_str"]
            if user["Study Group"] == sk
            else user_map2["user_order_str"]
        )

        rk_answer_str = (
            user["answer_str"] if user["Study Group"] == rk else user_map2["answer_str"]
        )
        sk_answer_str = (
            user["answer_str"] if user["Study Group"] == sk else user_map2["answer_str"]
        )

        ob = {
            "Participant ID": user["Participant ID"],
            "Score - RK": rk_score,
            "Score - SK": sk_score,
            "Rescaled Score - RK": rk_rescaled_score,
            "Rescaled Score - SK": sk_rescaled_score,
            "answer_str - RK": rk_answer_str,
            "user_order_str - RK": rk_user_order_str,
            "answer_str - SK": sk_answer_str,
            "user_order_str - SK": sk_user_order_str,
        }
        combined_results.append(ob)


path_raw = Path(output_dir) / "paired" / "raw"
path_raw.mkdir(parents=True, exist_ok=True)
path_backups = Path(output_dir) / "paired" / "backups"
path_backups.mkdir(parents=True, exist_ok=True)

# convert to excel and save
excel = pd.DataFrame(combined_results)
excel.to_excel(path_raw / "task2_levenshtein.xlsx", index=False)
excel.to_excel(path_backups / f"{timestamp}_task2_levenshtein.xlsx", index=False)


path_raw = Path(output_dir) / "maps" / "raw"
path_raw.mkdir(parents=True, exist_ok=True)
path_backups = Path(output_dir) / "maps" / "backups"
path_backups.mkdir(parents=True, exist_ok=True)

# convert to excel and save
excel_map1 = pd.DataFrame(map1_users)
excel_map1.to_excel(path_raw / "task2_map1_levenshtein.xlsx", index=False)
excel_map1.to_excel(
    path_backups / f"{timestamp}_task2_map1_levenshtein.xlsx", index=False
)

excel_map2 = pd.DataFrame(map2_users)
excel_map2.to_excel(path_raw / "task2_map2_levenshtein.xlsx", index=False)
excel_map2.to_excel(
    path_backups / f"{timestamp}_task2_map2_levenshtein.xlsx", index=False
)
