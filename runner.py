# Maps algorithm names to the engine in scheduler.py.
# This is the only place that knows the list of algorithms by name.

import scheduler


ALGORITHMS = ["FCFS", "SJF", "SRTF", "Round Robin", "Priority"]


def run(algorithm, processes, *, quantum=2, lower_is_higher=True):
    runners = {
        "FCFS":        lambda: scheduler.fcfs(processes),
        "SJF":         lambda: scheduler.sjf(processes),
        "SRTF":        lambda: scheduler.srtf(processes),
        "Round Robin": lambda: scheduler.round_robin(processes, quantum),
        "Priority":    lambda: scheduler.priority_scheduling(processes, lower_is_higher),
    }
    if algorithm not in runners:
        raise ValueError(f"Unknown algorithm: {algorithm!r}")
    return runners[algorithm]()


def run_all(processes, *, quantum=2, lower_is_higher=True):
    return [run(name, processes, quantum=quantum, lower_is_higher=lower_is_higher)
            for name in ALGORITHMS]
