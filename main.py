"""
Entry point for the CPU Scheduling Simulator.

Usage
-----
    python main.py            -> launches the graphical interface (recommended)
    python main.py --cli      -> prints a text demo (works without a display)

The --cli mode is handy for quickly checking the engine, for machines without
Tkinter installed, and for taking the numbers shown in the project report.
"""

import sys
from scheduler import Process, run_all


# A small fixed workload used by the text demo and the report.
DEMO = [
    Process("P1", arrival=0, burst=8, priority=3),
    Process("P2", arrival=1, burst=4, priority=1),
    Process("P3", arrival=2, burst=9, priority=4),
    Process("P4", arrival=3, burst=5, priority=2),
]


def _print_result(r):
    print(f"\n=== {r.algorithm} ===")
    print(f"Execution order : {r.execution_order}")
    print(f"{'PID':<5}{'Arr':<5}{'Burst':<6}{'Comp':<6}"
          f"{'TAT':<6}{'Wait':<6}{'Resp':<6}")
    for row in r.rows:
        print(f"{row['pid']:<5}{row['arrival']:<5}{row['burst']:<6}"
              f"{row['completion']:<6}{row['turnaround']:<6}"
              f"{row['waiting']:<6}{row['response']:<6}")
    print(f"Average waiting    : {r.avg_waiting:.2f}")
    print(f"Average turnaround : {r.avg_turnaround:.2f}")
    print(f"Average response   : {r.avg_response:.2f}")


def cli_demo():
    print("CPU Scheduling Simulator — text demo")
    print("Workload: P1(0,8,p3)  P2(1,4,p1)  P3(2,9,p4)  P4(3,5,p2)")
    results = run_all(DEMO, quantum=2, lower_is_higher=True)
    for r in results:
        _print_result(r)

    print("\n=== Summary (lower is better) ===")
    print(f"{'Algorithm':<40}{'Wait':<8}{'TAT':<8}{'Resp':<8}")
    for r in results:
        print(f"{r.algorithm:<40}{r.avg_waiting:<8.2f}"
              f"{r.avg_turnaround:<8.2f}{r.avg_response:<8.2f}")
    best = min(results, key=lambda r: r.avg_waiting)
    print(f"\nLowest average waiting time: {best.algorithm}")


def main():
    if "--cli" in sys.argv:
        cli_demo()
        return
    try:
        from gui import main as gui_main
        gui_main()
    except Exception as exc:        # e.g. Tkinter not installed / no display
        print(f"Could not start the GUI ({exc}).")
        print("Falling back to the text demo. Run 'python main.py --cli' "
              "to skip this message.\n")
        cli_demo()


if __name__ == "__main__":
    main()
