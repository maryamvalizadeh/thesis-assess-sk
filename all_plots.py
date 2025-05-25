import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

output_dir = Path("./plots")
output_dir.mkdir(parents=True, exist_ok=True)

map1 = pd.read_excel("Data - Map 1.xlsx")
map2 = pd.read_excel("Data - Map 2.xlsx")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

all_maps = pd.concat(
    [map1.assign(Map="Map 1"), map2.assign(Map="Map 2")], ignore_index=True
)

sk_first = all_maps[
    (
        (all_maps["Experiment Order"] == "first")
        & (all_maps["Study Group"] == "Survey Knowledge")
    )
    | (
        (all_maps["Experiment Order"] == "second")
        & (all_maps["Study Group"] == "Route Knowledge Only")
    )
]

rk_first = all_maps[
    (
        (all_maps["Experiment Order"] == "first")
        & (all_maps["Study Group"] == "Route Knowledge Only")
    )
    | (
        (all_maps["Experiment Order"] == "second")
        & (all_maps["Study Group"] == "Survey Knowledge")
    )
]


palette_groups = {"Route Knowledge Only": "orange", "Survey Knowledge": "#00d1b9"}
grey_palette_groups = {
    "Route Knowledge Only": "#333",
    "Survey Knowledge": "#333",
}

palette_order = {"first": "#47c3e6", "second": "#e64747"}
grey_palette_order = {"first": "#333", "second": "#333"}


def save_file(path, filename):
    # create the directories
    path_raw = Path(path) / "raw"
    path_backups = Path(path) / "backups"
    path_raw.mkdir(parents=True, exist_ok=True)
    path_backups.mkdir(parents=True, exist_ok=True)

    plt.savefig(path_raw / f"{filename}.png", dpi=300)
    plt.savefig(path_backups / f"{timestamp}_{filename}.png", dpi=300)
    plt.close()


def boxplot(
    data,
    column,
    title,
    path,
    filename,
    label,
    min,
    max,
    yticks=[],
    ylabel=[],
    show_dots=False,
    separator="Study Group",
    order=["Route Knowledge Only", "Survey Knowledge"],
    box_palette=palette_groups,
    dot_pallete=grey_palette_groups,
    xticklabels=None,
):
    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(
        x=separator,
        y=column,
        data=data,
        order=order,
        palette=box_palette,
        hue=separator,
        medianprops={"linewidth": 2},
        showfliers=not show_dots,  # Hide the outliers
    )

    # ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    # ax.set_axisbelow(True)

    if len(yticks) != 0:
        ax.set(yticks=yticks)
    if len(ylabel) != 0:
        ax.set(yticklabels=ylabel)
    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)

    plt.legend([], [], frameon=False)

    if show_dots:
        ax2 = sns.stripplot(
            x=separator,
            y=column,
            data=data,
            order=order,
            palette=dot_pallete,
            hue=separator,
            size=7,
            jitter=0.2,
            edgecolor="black",
            linewidth=0.5,
            alpha=0.5,
            # dodge=True,
        )
        if len(yticks) != 0:
            ax2.set(yticks=yticks)
        if len(ylabel) != 0:
            ax2.set(yticklabels=ylabel)

    plt.ylim(min, max)
    plt.title(title)
    plt.ylabel(label)
    plt.xlabel("")
    plt.tight_layout()
    save_file(path, filename)


def create_box_plots(
    column,
    title,
    tasknum,
    filename,
    label,
    min,
    max,
    yticks=[],
    ylabel=[],
    show_dots=False,
):

    boxplot(
        data=all_maps,
        column=column,
        title=f"{title} (All Maps)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"boxplot_{filename}_all_maps",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
    )

    boxplot(
        data=map1,
        column=column,
        title=f"{title} (Map 1)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"boxplot_{filename}_map1",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
    )

    boxplot(
        data=map2,
        column=column,
        title=f"{title} (Map 2)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"boxplot_{filename}_map2",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
    )

    boxplot(
        data=all_maps,
        column=column,
        title=f"Order comparision: {title}",
        path=f"{output_dir}/task{tasknum}/order_effect/",
        filename=f"oe_boxplot_{filename}_all",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
        separator="Experiment Order",
        order=["first", "second"],
        box_palette=palette_order,
        dot_pallete=grey_palette_order,
    )

    boxplot(
        data=sk_first,
        column=column,
        title=f"Order comparision: Survey Knowledge First for {title}",
        path=f"{output_dir}/task{tasknum}/order_effect/",
        filename=f"oe_boxplot_{filename}_sk_first",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
        order=["Survey Knowledge", "Route Knowledge Only"],
        xticklabels=["Survey Knowledge (First)", "Route Knowledge Only (Second)"],
    )

    boxplot(
        data=rk_first,
        column=column,
        title=f"Order comparision: Route Knowledge Only First for {title}",
        path=f"{output_dir}/task{tasknum}/order_effect/",
        filename=f"oe_boxplot_{filename}_rk_first",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
        show_dots=show_dots,
        xticklabels=["Route Knowledge Only (First)", "Survey Knowledge (Second)"],
    )


def histogram(data, column, title, path, filename, label, min, max, bins=10):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True)

    # Plot each study group on its own subplot as horizontal histograms
    for ax, group in zip(axes, ["Route Knowledge Only", "Survey Knowledge"]):
        subset = data[data["Study Group"] == group]
        sns.histplot(
            data=subset,
            y=column,
            bins=bins,
            kde=False,
            stat="count",
            color=palette_groups[group],  # use global palette
            edgecolor="black",  # black border for bars
            linewidth=1.2,
            ax=ax,
        )
        ax.set_title(f"{title} — {group}")
        ax.set_ylabel(label)
        ax.set_ylim(min, max)

    # Set common x-axis label
    axes[0].set_xlabel("Count")

    # Adjust layout
    plt.tight_layout()

    save_file(path, filename)

    # # Prepare output directories
    # path_raw = Path(path) / "raw"
    # path_backups = Path(path) / "backups"
    # path_raw.mkdir(parents=True, exist_ok=True)
    # path_backups.mkdir(parents=True, exist_ok=True)

    # # Save the figure
    # plt.savefig(path_raw / f"{filename}.png")
    # plt.savefig(path_backups / f"{timestamp}_{filename}.png")
    # plt.close()


def create_histogram(column, title, tasknum, filename, label, min, max, bins=10):
    histogram(
        data=all_maps,
        column=column,
        title=f"{title} (All Maps)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"histogram_{filename}_all_maps",
        label=label,
        bins=bins,
        min=min,
        max=max,
    )

    histogram(
        data=map1,
        column=column,
        title=f"{title} (Map 1)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"histogram_{filename}_map1",
        label=label,
        bins=bins,
        min=min,
        max=max,
    )

    histogram(
        data=map2,
        column=column,
        title=f"{title} (Map 2)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"histogram_{filename}_map2",
        label=label,
        bins=bins,
        min=min,
        max=max,
    )


def dotplot(data, column, title, path, filename, label, min, max, yticks=[], ylabel=[]):
    plt.figure(figsize=(9, 6))

    # Overlay raw data points
    ax = sns.stripplot(
        x="Study Group",
        y=column,
        data=data,
        order=["Route Knowledge Only", "Survey Knowledge"],
        palette=palette,
        hue="Study Group",
        size=8,
        jitter=0.3,
        edgecolor="black",
        linewidth=0.5,
        alpha=0.7,
        # dodge=True,
    )
    if len(yticks) != 0:
        ax.set(yticks=yticks)
    if len(ylabel) != 0:
        ax.set(yticklabels=ylabel)

    plt.ylim(min, max)
    plt.title(title)
    plt.ylabel(label)
    plt.xlabel("")
    plt.tight_layout()
    save_file(path, filename)

    # create the directories
    # path_raw = Path(path) / "raw"
    # path_backups = Path(path) / "backups"
    # path_raw.mkdir(parents=True, exist_ok=True)
    # path_backups.mkdir(parents=True, exist_ok=True)

    # plt.savefig(path_raw / f"{filename}.png")
    # plt.savefig(path_backups / f"{timestamp}_{filename}.png")
    # plt.close()


def create_dot_plots(
    column, title, tasknum, filename, label, min, max, yticks=[], ylabel=[]
):
    dotplot(
        data=all_maps,
        column=column,
        title=f"{title} (All Maps)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"dotplot_{filename}_all_maps",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
    )

    dotplot(
        data=map1,
        column=column,
        title=f"{title} (Map 1)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"dotplot_{filename}_map1",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
    )

    dotplot(
        data=map2,
        column=column,
        title=f"{title} (Map 2)",
        path=f"{output_dir}/task{tasknum}/",
        filename=f"dotplot_{filename}_map2",
        label=label,
        min=min,
        max=max,
        yticks=yticks,
        ylabel=ylabel,
    )


cal_task = "all"

if cal_task == "1" or cal_task == "all":
    # Task 1: Landmark Recognition
    # create_box_plots(
    #     column="balanced_accuracy",
    #     title="Landmark Recognition",
    #     tasknum=1,
    #     filename="landmark_recognition",
    #     label="Score",
    #     min=0,
    #     max=1.02,
    #     show_dots=False,
    # )

    create_box_plots(
        column="balanced_accuracy",
        title="Landmark Recognition",
        tasknum=1,
        filename="landmark_recognition",
        label="Score",
        min=0,
        max=1.02,
        show_dots=True,
    )

    # create_histogram(
    #     column="balanced_accuracy",
    #     title="Landmark Recognition",
    #     tasknum=1,
    #     filename="landmark_recognition",
    #     label="Score",
    #     bins=10,
    #     min=0,
    #     max=1,
    # )

    # create_dot_plots(
    #     column="balanced_accuracy",
    #     title="Landmark Recognition",
    #     tasknum=1,
    #     filename="landmark_recognition",
    #     label="Score",
    #     min=0,
    #     max=1.05,
    #     yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
    #     ylabel=[
    #         "0",
    #         "0.2",
    #         "0.4",
    #         "0.6",
    #         "0.8",
    #         "1.0 (Max)",
    #     ],
    # )

if cal_task == "2" or cal_task == "all":
    # Task 2: Landmark Ordering
    create_box_plots(
        column="Levenshtein",
        title="Landmark Ordering",
        tasknum=2,
        filename="landmark_ordering",
        label="Score",
        min=0.5714,
        max=1.01,
        show_dots=True,
        yticks=[0.5714, 0.6429, 0.7143, 0.7857, 0.8571, 0.9286, 1.0],
        ylabel=[
            "0.5714 (Min)",
            "0.6429",
            "0.7143",
            "0.7857",
            "0.8571",
            "0.9286",
            "1.0 (Max)",
        ],
    )

if cal_task == "3" or cal_task == "all":
    # Task 3: Landmark Orientation
    create_box_plots(
        column="Orientation - Sum - Scores",
        title="Landmark Orientation",
        tasknum=3,
        filename="landmark_orientation",
        label="Score",
        min=0,
        max=32,
        yticks=[0, 5, 10, 15, 20, 25, 30, 32],
        ylabel=[
            "0",
            "5",
            "10",
            "15",
            "20",
            "25",
            "30",
            "32 (Max)",
        ],
        show_dots=True,
    )

if cal_task == "4" or cal_task == "all":
    # Task 4: Route Choice
    create_box_plots(
        column="Direction - Sum",
        title="Route Choice",
        tasknum=4,
        filename="route_choice",
        label="Number of Correct Choices",
        min=-0.05,
        max=2.05,
        show_dots=True,
        yticks=[0, 1, 2],
        ylabel=[
            "0 (Min)",
            "1",
            "2 (Max)",
        ],
    )

if cal_task == "5" or cal_task == "all":
    # Task 5: Landmark Placement
    create_box_plots(
        column="Task 5 Score",
        title="Landmark Placement",
        tasknum=5,
        filename="landmark_placement",
        label="Score",
        min=3,
        max=12.2,
        yticks=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ylabel=[
            "3 (Min)",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12 (Max)",
        ],
        show_dots=True,
    )


print("Done")
