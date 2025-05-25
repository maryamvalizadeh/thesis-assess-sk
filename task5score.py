import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np
import Levenshtein

output_dir = Path("./task5score")
output_dir.mkdir(parents=True, exist_ok=True)

map1 = pd.read_excel("Data - Map 1.xlsx")
map2 = pd.read_excel("Data - Map 2.xlsx")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

rk = "Route Knowledge Only"
sk = "Survey Knowledge"

column_name = "Placement"


# ratio returns the levenshtein ratio instead of levenshtein distance
# print_matrix prints the matrix
# lowercase compares the strings as lowercase


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


def compare_strings(answer, test):
    score = 0
    for i in range(len(answer)):
        if test[i] == answer[i]:
            score += 2
        elif test[i] in answer:
            score += 1
    return score


def calculate_scores(data, options, map_number):
    value_to_key = {v: k for k, v in options.items()}

    users = []
    for index, row in data.iterrows():
        user_order = row[column_name].rstrip(";").split(";")
        user_order_str = "".join(
            value_to_key[item.replace("\xa0", " ")] for item in user_order
        )

        score = compare_strings("012345", user_order_str[:6])
        # jaro = round(
        #     Levenshtein.jaro("012345", user_order_str[:6]),
        #     3,
        # )
        number_of_matches = sum(
            1 for i, j in zip("012345", user_order_str[:6]) if i == j
        )
        users.append(
            {
                "Participant ID": row["Participant ID"],
                "Study Group": row["Study Group"],
                "Map": f"Map {map_number}",
                "User Answer": row[column_name],
                "Score": score,
                # "Jaro": jaro,
                "number_of_matches": number_of_matches,
                "answer_str": "012345",
                "user_order_str": user_order_str[:6],
            }
        )
        # print(
        #     f"Participant ID: {row['Participant ID']}",
        #     user_order_str,
        #     f"Score: {score}",
        # )
    return users


# test the function
map1_options = {
    "0": "Bus Stop",
    "1": "Town Hall",
    "2": "Icecream Shop",
    "3": "Tedi",
    "4": "Large Tree",
    "5": "Commerzbank",
    "6": "Parking",
    "7": "C&A",
    "8": "Hairsalon",
    "9": "Kanne Coffee Place",
}

map2_options = {
    "0": "Glass stairwell entrance",
    "1": "Church",
    "2": "Yellow Cafe",
    "3": "Shopping Mall",
    "4": "H&M Store",
    "5": "dm store",
    "6": "Hot Dog cart",
    "7": "Douglas",
    "8": "Kiosk",
    "9": "Douglas",
}

map1_users = calculate_scores(map1, map1_options, 1)
map2_users = calculate_scores(map2, map2_options, 2)


combined_results = []

for user in map1_users:
    user_map2 = next(
        (u for u in map2_users if u["Participant ID"] == user["Participant ID"]),
        None,
    )
    if user_map2:
        rk_score = user["Score"] if user["Study Group"] == rk else user_map2["Score"]
        sk_score = user["Score"] if user["Study Group"] == sk else user_map2["Score"]

        rk_number_of_matches = (
            user["number_of_matches"]
            if user["Study Group"] == rk
            else user_map2["number_of_matches"]
        )
        sk_number_of_matches = (
            user["number_of_matches"]
            if user["Study Group"] == sk
            else user_map2["number_of_matches"]
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

        # rk_jaro = user["Jaro"] if user["Study Group"] == rk else user_map2["Jaro"]
        # sk_jaro = user["Jaro"] if user["Study Group"] == sk else user_map2["Jaro"]

        ob = {
            "Participant ID": user["Participant ID"],
            "Score - RK": rk_score,
            "Score - SK": sk_score,
            # "Jaro - RK": rk_jaro,
            # "Jaro - SK": sk_jaro,
            "number_of_matches - RK": rk_number_of_matches,
            "number_of_matches - SK": sk_number_of_matches,
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
excel.to_excel(path_raw / "task5_levenshtein.xlsx", index=False)
excel.to_excel(path_backups / f"{timestamp}_task5_levenshtein.xlsx", index=False)


path_raw = Path(output_dir) / "maps" / "raw"
path_raw.mkdir(parents=True, exist_ok=True)
path_backups = Path(output_dir) / "maps" / "backups"
path_backups.mkdir(parents=True, exist_ok=True)

# convert to excel and save
excel_map1 = pd.DataFrame(map1_users)
excel_map1.to_excel(path_raw / "task5_map1_levenshtein.xlsx", index=False)
excel_map1.to_excel(
    path_backups / f"{timestamp}_task5_map1_levenshtein.xlsx", index=False
)

excel_map2 = pd.DataFrame(map2_users)
excel_map2.to_excel(path_raw / "task5_map2_levenshtein.xlsx", index=False)
excel_map2.to_excel(
    path_backups / f"{timestamp}_task5_map2_levenshtein.xlsx", index=False
)
