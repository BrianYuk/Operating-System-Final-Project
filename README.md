# CPU Scheduling Simulator

A Python simulator for the Operating Systems final project. It implements five
CPU-scheduling algorithms, computes the standard performance metrics, draws a
Gantt chart, and compares all algorithms on the same workload.

## Algorithms
| Algorithm | Type | Notes |
|-----------|------|-------|
| FCFS – First Come First Serve | Non-preemptive | runs in arrival order |
| SJF – Shortest Job First | Non-preemptive | shortest burst first |
| SRTF – Shortest Remaining Time First | **Preemptive** | Part 2 extra feature |
| RR – Round Robin | Preemptive | configurable time quantum |
| Priority Scheduling | Non-preemptive | configurable priority direction |

## Part 2 advanced features (3)
1. **Graphical user interface** (Tkinter) — `gui.py`.
2. **SRTF** — an additional preemptive algorithm beyond the four required.
3. **Automatic algorithm comparison** — the *Compare All* button runs every
   algorithm on the same workload and shows a comparison table + bar chart,
   highlighting the best result.

(The per-run Gantt chart is part of the core Part 1 requirement.)

## Project files
| File | What it does |
|------|--------------|
| `scheduler.py` | The scheduling engine – the algorithms + metrics only (no UI, no dispatch) |
| `runner.py` | Maps algorithm names to the engine (`run`, `run_all`, `ALGORITHMS`) |
| `charts.py` | Draws the Gantt chart and the comparison bar chart (matplotlib) |
| `gui.py` | Tkinter graphical interface |
| `main.py` | Entry point: launches the GUI, or `--cli` for a text demo |

## How to run

### 1. Install the libraries
```bash
pip install matplotlib
```
Tkinter ships with most Python installs. On Debian/Ubuntu Linux you may need:
```bash
sudo apt-get install python3-tk
```

### 2. Launch
```bash
python main.py          # graphical interface
python main.py --cli    # text-only demo (no display needed)
```

## Using the GUI
1. Add processes with the **Add Process** button.
2. Pick an algorithm and (for Round Robin) a time quantum.
3. Click **Run** to see the metrics table and Gantt chart, or **Compare All**
   to benchmark every algorithm at once (the best result is highlighted).

## Priority convention
By default a **lower** priority number means a **higher** priority (this is the
common textbook convention, e.g. priority 1 outranks priority 2). Untick the
"Lower number = higher priority" box to reverse it.
