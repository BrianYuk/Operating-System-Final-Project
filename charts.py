"""
Drawing helpers built on matplotlib. Each function draws onto a Figure that is
passed in, so the SAME code works whether we are:

  * embedding the figure inside the Tkinter GUI (FigureCanvasTkAgg), or
  * saving the figure to a PNG file from the command line.

Nothing here knows about Tkinter -> the plotting stays reusable and testable.
"""

from __future__ import annotations
import matplotlib

# A stable, readable colour for each process (cycles if there are many).
_PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]


def _colour_for(pid: str, mapping: dict) -> str:
    if pid not in mapping:
        mapping[pid] = _PALETTE[len(mapping) % len(_PALETTE)]
    return mapping[pid]


def draw_gantt(fig, result) -> None:
    """Draw a single horizontal Gantt chart for one Result onto `fig`."""
    fig.clear()
    ax = fig.add_subplot(111)
    colours: dict = {}

    for label, start, end in result.timeline:
        width = end - start
        if label == "IDLE":
            ax.barh(0, width, left=start, height=0.5,
                    color="#E6E6E6", edgecolor="#BFBFBF", hatch="//")
            ax.text(start + width / 2, 0, "idle", ha="center", va="center",
                    fontsize=8, color="#888888")
        else:
            ax.barh(0, width, left=start, height=0.5,
                    color=_colour_for(label, colours), edgecolor="black")
            ax.text(start + width / 2, 0, label, ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
        # time tick under the start of every block
        ax.text(start, -0.45, str(start), ha="center", va="top", fontsize=8)

    # final time tick at the very end
    if result.timeline:
        end = result.timeline[-1][2]
        ax.text(end, -0.45, str(end), ha="center", va="top", fontsize=8)

    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(f"Gantt Chart — {result.algorithm}\nOrder: {result.execution_order}",
                 fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.tight_layout()


def draw_comparison(fig, results) -> None:
    """Grouped bar chart comparing avg waiting / turnaround / response across
    every algorithm in `results` (a list of Result objects)."""
    fig.clear()
    ax = fig.add_subplot(111)

    names = [r.algorithm.split(" (")[0] for r in results]   # short names
    waiting = [r.avg_waiting for r in results]
    turnaround = [r.avg_turnaround for r in results]
    response = [r.avg_response for r in results]

    x = range(len(names))
    w = 0.26
    b1 = ax.bar([i - w for i in x], waiting, w, label="Avg Waiting", color="#4C72B0")
    b2 = ax.bar([i for i in x], turnaround, w, label="Avg Turnaround", color="#DD8452")
    b3 = ax.bar([i + w for i in x], response, w, label="Avg Response", color="#55A868")

    for bars in (b1, b2, b3):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h, f"{h:.1f}",
                    ha="center", va="bottom", fontsize=7)

    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=15, ha="right", fontsize=8)
    ax.set_ylabel("Time units (lower is better)")
    ax.set_title("Algorithm Performance Comparison", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
