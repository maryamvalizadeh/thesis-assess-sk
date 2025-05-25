import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

output_dir = Path("./experiment_order")
output_dir.mkdir(parents=True, exist_ok=True)

all_data = pd.read_excel("./experiment_order/raw/experiment_order.xlsx")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


# palette = {"Route Knowledge Only": "orange", "Survey Knowledge": "#00d1b9"}

# grey_palette = {
#     "Route Knowledge Only": "#333",
#     "Survey Knowledge": "#333",
# }


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
    column1,
    column2,
    title,
    path,
    filename,
    label,
    min,
    max,
    yticks=[],
    ylabel=[],
    show_dots=False,
):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    # Left plot for column1
    sns.boxplot(
        y=column1,
        data=data,
        palette={"column": "blue"},
        medianprops={"linewidth": 2},
        showfliers=not show_dots,
        ax=axes[0],
    )

    # Right plot for column2 (assuming column2 is passed as a parameter)
    sns.boxplot(
        y=column2,
        data=data,
        palette={"column": "red"},
        medianprops={"linewidth": 2},
        showfliers=not show_dots,
        ax=axes[1],
    )

    # Set the same y-axis limits for both plots
    axes[0].set_ylim(min, max)
    axes[1].set_ylim(min, max)

    #

    # ax = axes[0]  # For compatibility with the rest of the function

    # ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    # ax.set_axisbelow(True)

    # if len(yticks) != 0:
    #     ax.set(yticks=yticks)
    # if len(ylabel) != 0:
    #     ax.set(yticklabels=ylabel)

    plt.legend([], [], frameon=False)

    # if show_dots:
    #     ax2 = sns.stripplot(
    #         x="Study Group",
    #         y=column,
    #         data=data,
    #         order=["Route Knowledge Only", "Survey Knowledge"],
    #         palette=grey_palette,
    #         hue="Study Group",
    #         size=7,
    #         jitter=0.2,
    #         edgecolor="black",
    #         linewidth=0.5,
    #         alpha=0.5,
    #         # dodge=True,
    #     )
    #     if len(yticks) != 0:
    #         ax2.set(yticks=yticks)
    #     if len(ylabel) != 0:
    #         ax2.set(yticklabels=ylabel)

    plt.ylim(min, max)
    plt.title(title)
    plt.ylabel(label)
    plt.xlabel("")
    plt.tight_layout()
    save_file(path, filename)


boxplot(
    all_data,
    column1="Task1First",
    column2="Task1Second",
    title="Landmark Recognicion",
    path=output_dir,
    filename="task1",
    label="Score",
    min=0,
    max=1,
    yticks=[0, 0.25, 0.5, 0.75, 1],
    ylabel=["0", "0.25", "0.5", "0.75", "1"],
    show_dots=True,
)
