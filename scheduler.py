"""
Core CPU-scheduling engine for the Operating Systems final project.

This module contains NO user-interface code on purpose. Every scheduling
algorithm is a plain function that takes a list of `Process` objects and
returns a `Result`. Keeping the logic separate from the GUI makes it easy to
test, easy to read, and easy to explain (which you must be able to do!).

Algorithms implemented
----------------------
* FCFS      - First Come First Serve            (non-preemptive)
* SJF       - Shortest Job First                (non-preemptive)
* SRTF      - Shortest Remaining Time First      (preemptive  -> Part 2 extra)
* RR        - Round Robin                        (preemptive, time quantum)
* PRIORITY  - Priority Scheduling                (non-preemptive)

Metrics produced per process
----------------------------
* Completion Time  : the time unit at which the process finishes
* Turnaround Time  : completion - arrival
* Waiting Time     : turnaround - burst
* Response Time    : first time the process gets the CPU - arrival

Author: <YOUR NAME / GROUP>      (rename this so the file is yours)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import copy


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Process:
    """A single process / job to be scheduled.

    The four fields on the left are the *input* the user provides.
    The fields marked "computed" are filled in while an algorithm runs.
    """
    pid: str            # Process ID, e.g. "P1"
    arrival: int        # Arrival Time  (when the process enters the system)
    burst: int          # Burst Time    (CPU time the process needs)
    priority: int = 0   # Priority Value (used only by Priority scheduling)

    # --- computed while scheduling (not provided by the user) ---
    remaining: int = field(default=0, init=False)       # remaining burst time
    start_time: int | None = field(default=None, init=False)  # first time on CPU
    completion: int | None = field(default=None, init=False)  # finish time

    def reset(self) -> None:
        """Restore the working fields so the process can be scheduled again."""
        self.remaining = self.burst
        self.start_time = None
        self.completion = None


@dataclass
class Result:
    """Everything an algorithm produces, bundled together."""
    algorithm: str                       # human-readable name
    timeline: list                       # [(label, start, end), ...] incl. "IDLE"
    rows: list                           # per-process metric dicts
    avg_waiting: float
    avg_turnaround: float
    avg_response: float

    @property
    def execution_order(self) -> str:
        """A compact string like 'P1 -> P3 -> P2' for printing/labelling."""
        order = [label for label, _, _ in self.timeline if label != "IDLE"]
        # collapse immediate repeats (a block that was split is still one visit)
        collapsed = []
        for label in order:
            if not collapsed or collapsed[-1] != label:
                collapsed.append(label)
        return " -> ".join(collapsed)


# ---------------------------------------------------------------------------
# Helpers shared by every algorithm
# ---------------------------------------------------------------------------
def _fresh(processes: list[Process]) -> list[Process]:
    """Return deep copies so running an algorithm never mutates the caller's
    data. This is what lets us run 'Compare All' safely."""
    clones = copy.deepcopy(processes)
    for p in clones:
        p.reset()
    return clones


def _build_timeline(busy: list[tuple]) -> list[tuple]:
    """Turn raw busy segments into a clean display timeline.

    * Sorts segments by start time.
    * Merges back-to-back segments that belong to the same process into one
      block (nicer Gantt chart).
    * Inserts ('IDLE', start, end) blocks wherever the CPU sat idle.
    """
    if not busy:
        return []
    busy = sorted(busy, key=lambda s: s[1])

    merged: list[list] = []
    for label, start, end in busy:
        if merged and merged[-1][0] == label and merged[-1][2] == start:
            merged[-1][2] = end            # extend the previous block
        else:
            merged.append([label, start, end])

    timeline: list[tuple] = []
    for i, (label, start, end) in enumerate(merged):
        if i == 0:
            # show idle time before the first job only if it does not start at 0
            if start > 0:
                timeline.append(("IDLE", 0, start))
        else:
            prev_end = merged[i - 1][2]
            if start > prev_end:
                timeline.append(("IDLE", prev_end, start))
        timeline.append((label, start, end))
    return timeline


def _metrics(processes: list[Process], name: str, timeline: list[tuple]) -> Result:
    """Compute waiting / turnaround / response for every process."""
    rows = []
    total_wt = total_tat = total_rt = 0
    for p in sorted(processes, key=lambda p: p.pid):
        turnaround = p.completion - p.arrival
        waiting = turnaround - p.burst
        response = p.start_time - p.arrival
        total_wt += waiting
        total_tat += turnaround
        total_rt += response
        rows.append({
            "pid": p.pid,
            "arrival": p.arrival,
            "burst": p.burst,
            "priority": p.priority,
            "completion": p.completion,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response,
        })
    n = len(processes)
    return Result(
        algorithm=name,
        timeline=timeline,
        rows=rows,
        avg_waiting=total_wt / n,
        avg_turnaround=total_tat / n,
        avg_response=total_rt / n,
    )


# ---------------------------------------------------------------------------
# Non-preemptive algorithms: FCFS, SJF, Priority
# (they share one engine; they differ only in HOW they pick the next process)
# ---------------------------------------------------------------------------
def _non_preemptive(processes: list[Process], name: str, choose_key):
    """Generic non-preemptive scheduler.

    `choose_key(process)` returns a sort key; among all processes that have
    already arrived, the one with the SMALLEST key is run to completion.
    """
    procs = _fresh(processes)
    n = len(procs)
    time = 0
    finished = 0
    done: set[str] = set()
    busy: list[tuple] = []

    while finished < n:
        ready = [p for p in procs if p.arrival <= time and p.pid not in done]
        if not ready:
            # CPU is idle -> jump forward to the next arrival
            time = min(p.arrival for p in procs if p.pid not in done)
            continue
        current = min(ready, key=choose_key)
        current.start_time = time          # non-preemptive: it starts right now
        busy.append((current.pid, time, time + current.burst))
        time += current.burst
        current.completion = time
        done.add(current.pid)
        finished += 1

    return _metrics(procs, name, _build_timeline(busy))


def fcfs(processes: list[Process]) -> Result:
    # earliest arrival wins; PID breaks ties
    return _non_preemptive(processes, "FCFS",
                           choose_key=lambda p: (p.arrival, p.pid))


def sjf(processes: list[Process]) -> Result:
    # shortest burst wins; arrival then PID break ties
    return _non_preemptive(processes, "SJF (non-preemptive)",
                           choose_key=lambda p: (p.burst, p.arrival, p.pid))


def priority_scheduling(processes: list[Process],
                        lower_is_higher: bool = True) -> Result:
    """Priority scheduling (non-preemptive).

    lower_is_higher=True  -> priority value 1 outranks 2 (textbook default)
    lower_is_higher=False -> a bigger number means more important
    """
    if lower_is_higher:
        key = lambda p: (p.priority, p.arrival, p.pid)
        name = "Priority (lower number = higher priority)"
    else:
        key = lambda p: (-p.priority, p.arrival, p.pid)
        name = "Priority (higher number = higher priority)"
    return _non_preemptive(processes, name, choose_key=key)


# ---------------------------------------------------------------------------
# Round Robin (preemptive, fixed time quantum)
# ---------------------------------------------------------------------------
def round_robin(processes: list[Process], quantum: int = 2) -> Result:
    if quantum < 1:
        raise ValueError("Time quantum must be a positive integer.")

    procs = _fresh(processes)
    # process the queue in arrival order; PID breaks ties
    order = sorted(procs, key=lambda p: (p.arrival, p.pid))
    n = len(order)
    time = 0
    busy: list[tuple] = []
    ready: deque[Process] = deque()
    idx = 0                                  # next not-yet-queued process

    def enqueue_arrivals(upto: int) -> None:
        nonlocal idx
        while idx < n and order[idx].arrival <= upto:
            ready.append(order[idx])
            idx += 1

    enqueue_arrivals(time)

    while ready or idx < n:
        if not ready:
            # nothing ready -> idle until the next arrival
            time = order[idx].arrival
            enqueue_arrivals(time)
            continue

        current = ready.popleft()
        if current.start_time is None:
            current.start_time = time        # record first CPU access
        run = min(quantum, current.remaining)
        busy.append((current.pid, time, time + run))
        time += run
        current.remaining -= run

        # Processes that arrive DURING this slice join the queue *before* the
        # process we just preempted re-joins it (standard RR convention).
        enqueue_arrivals(time)

        if current.remaining > 0:
            ready.append(current)
        else:
            current.completion = time

    return _metrics(procs, f"Round Robin (q={quantum})", _build_timeline(busy))


# ---------------------------------------------------------------------------
# SRTF - Shortest Remaining Time First (preemptive SJF)  [Part 2 extra]
# ---------------------------------------------------------------------------
def srtf(processes: list[Process]) -> Result:
    procs = _fresh(processes)
    n = len(procs)
    time = 0
    finished = 0
    busy: list[tuple] = []                   # raw 1-unit slices, merged later

    while finished < n:
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        if not ready:
            time = min(p.arrival for p in procs if p.remaining > 0)
            continue
        # pick the smallest remaining time; arrival then PID break ties
        current = min(ready, key=lambda p: (p.remaining, p.arrival, p.pid))
        if current.start_time is None:
            current.start_time = time
        # run for ONE time unit, then re-evaluate (this is what makes it
        # preemptive: a shorter job arriving next tick can take over)
        busy.append((current.pid, time, time + 1))
        time += 1
        current.remaining -= 1
        if current.remaining == 0:
            current.completion = time
            finished += 1

    return _metrics(procs, "SRTF (preemptive)", _build_timeline(busy))


# ---------------------------------------------------------------------------
# Public dispatcher  - one entry point the GUI / CLI can call
# ---------------------------------------------------------------------------
ALGORITHMS = ["FCFS", "SJF", "SRTF", "Round Robin", "Priority"]


def run(algorithm: str, processes: list[Process], *,
        quantum: int = 2, lower_is_higher: bool = True) -> Result:
    """Run one algorithm by name and return its Result."""
    a = algorithm.strip().lower()
    if a in ("fcfs", "first come first serve"):
        return fcfs(processes)
    if a in ("sjf", "shortest job first"):
        return sjf(processes)
    if a in ("srtf", "shortest remaining time first"):
        return srtf(processes)
    if a in ("rr", "round robin"):
        return round_robin(processes, quantum)
    if a in ("priority", "priority scheduling"):
        return priority_scheduling(processes, lower_is_higher)
    raise ValueError(f"Unknown algorithm: {algorithm!r}")


def run_all(processes: list[Process], *,
            quantum: int = 2, lower_is_higher: bool = True) -> list[Result]:
    """Run every algorithm on the same input (used by 'Compare All')."""
    return [
        fcfs(processes),
        sjf(processes),
        srtf(processes),
        round_robin(processes, quantum),
        priority_scheduling(processes, lower_is_higher),
    ]
