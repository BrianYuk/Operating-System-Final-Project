
import sys
from scheduler import Process
from runner import run_all

DEMO = [
    Process("P1", 0, 8, 3),
    Process("P2", 1, 4, 1),
    Process("P3", 2, 9, 4),
    Process("P4", 3, 5, 2),
]

def _print_result(result):
    print(f"\n=== {result.algorithm} ===")
    print(f"Execution order : {result.execution_order}")
    print(f"{'PID':<5}{'Arr':<5}{'Burst':<6}{'Comp':<6}"
          f"{'TAT':<6}{'Wait':<6}{'Resp':<6}")
    for row in result.rows:
        print(f"{row['pid']:<5}{row['arrival']:<5}{row['burst']:<6}"
              f"{row['completion']:<6}{row['turnaround']:<6}"
              f"{row['waiting']:<6}{row['response']:<6}")
    print(f"Average waiting    : {result.avg_waiting:.2f}")
    print(f"Average turnaround : {result.avg_turnaround:.2f}")
    print(f"Average response   : {result.avg_response:.2f}")

def _print_summary(results):
    print("\n=== Summary (lower is better) ===")
    print(f"{'Algorithm':<40}{'Wait':<8}{'TAT':<8}{'Resp':<8}")
    for result in results:
        print(f"{result.algorithm:<40}{result.avg_waiting:<8.2f}"
              f"{result.avg_turnaround:<8.2f}{result.avg_response:<8.2f}")
    best = min(results, key=lambda r: r.avg_waiting)
    print(f"\nLowest average waiting time: {best.algorithm}")

def cli_demo():
    print("CPU Scheduling Simulator — text demo")
    print("Workload: P1(0,8,p3)  P2(1,4,p1)  P3(2,9,p4)  P4(3,5,p2)")
    results = run_all(DEMO, quantum=2, lower_is_higher=True)
    for result in results:
        _print_result(result)
    _print_summary(results)

def main():
    if "--cli" in sys.argv:
        cli_demo()
        return
    try:
        from gui import main as gui_main
        gui_main()
    except Exception as exc:
        print(f"Could not start the GUI ({exc}).")
        print("Falling back to the text demo. Run 'python main.py --cli' "
              "to skip this message.\n")
        cli_demo()

if __name__ == "__main__":
    main()
