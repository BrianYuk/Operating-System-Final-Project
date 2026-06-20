# CPU Scheduling Simulator — Project Report

**Course:** Operating Systems (COMP6697001)
**Group members:** _<Name 1 – ID>, <Name 2 – ID>_
**Date:** June 2026

> **How to use this draft:** Replace every _italic placeholder_ with your own
> words and insert your own screenshots where marked `[SCREENSHOT …]`. Rephrase
> sections in your own voice — markers and similarity checks reward writing that
> sounds like *you*, and you must be able to defend every sentence.

---

## 1. Introduction

CPU scheduling is the part of an operating system that decides which ready
process gets the CPU next. Because a single CPU core can run only one process at
a time, the scheduler directly determines how responsive, fair, and efficient
the whole system feels. Different scheduling policies optimise for different
things: some minimise average waiting time, some guarantee a fast first
response, and some try to be fair to every process.

This project implements a **CPU Scheduling Simulator** in Python that lets a user
enter a set of processes (with arrival time, burst time, and priority) and then
schedules them using five classic algorithms. For each run the simulator reports
the execution order, per-process waiting and turnaround times, the averages, and
a Gantt chart. It can also benchmark all five algorithms on the same workload so
their trade-offs can be compared directly.

The implemented algorithms are **First Come First Serve (FCFS)**, **Shortest Job
First (SJF)**, **Shortest Remaining Time First (SRTF)**, **Round Robin (RR)**,
and **Priority Scheduling**.

Beyond the core requirements, the project includes three Part 2 advanced
features: a **graphical user interface** (Tkinter), the additional preemptive
**SRTF** algorithm, and **automatic algorithm comparison** that benchmarks every
algorithm on the same workload and visualises the results.

## 2. Scheduling Algorithm Explanation

Throughout this section we use the following example workload (also the default
in the program). For Priority, a **lower number means a higher priority**.

| Process | Arrival | Burst | Priority |
|---------|---------|-------|----------|
| P1 | 0 | 8 | 3 |
| P2 | 1 | 4 | 1 |
| P3 | 2 | 9 | 4 |
| P4 | 3 | 5 | 2 |

### 2.1 First Come First Serve (FCFS)
The CPU is given to processes strictly in the order they arrive, and a process
runs to completion before the next one starts (non-preemptive). FCFS is simple
and fair in arrival order, but it suffers from the **convoy effect**: a long
process that arrives first forces every shorter process behind it to wait.

For the example workload the order is **P1 → P2 → P3 → P4**, giving an average
waiting time of **8.75** and average turnaround of **15.25**.

### 2.2 Shortest Job First (SJF)
Among the processes that have already arrived, the scheduler picks the one with
the **smallest burst time** and runs it to completion (non-preemptive). SJF is
provably optimal for minimising *average* waiting time when all jobs are
available, but it requires knowing burst times in advance and can **starve**
long processes if short ones keep arriving.

For the example, the order becomes **P1 → P2 → P4 → P3** with average waiting
**7.75** — lower than FCFS because the shorter P4 is moved ahead of the long P3.

### 2.3 Shortest Remaining Time First (SRTF)
SRTF is the **preemptive** version of SJF. At every moment the scheduler runs
the process with the smallest *remaining* burst time, so a newly arrived short
job can interrupt a longer running one. This produces the lowest average waiting
time of all the algorithms here, at the cost of more context switches.

For the example the timeline is **P1(0–1) → P2(1–5) → P4(5–10) → P1(10–17) →
P3(17–26)**, giving the best average waiting time of **6.50**.

### 2.4 Round Robin (RR)
Each process gets the CPU for at most a fixed **time quantum**; if it is not
finished it goes to the back of the ready queue and the next process runs. RR is
preemptive and time-shared, which makes it excellent for **responsiveness** (no
process waits long for its first turn). With a quantum of 2 it gives the best
average response time (**2.00**) but a higher average waiting time (**12.75**)
because of the frequent switching.

The choice of quantum matters: a very large quantum makes RR behave like FCFS,
while a very small quantum maximises responsiveness but adds context-switch
overhead.

### 2.5 Priority Scheduling
Each process has a priority value; the scheduler always picks the highest-
priority ready process (here, the smallest priority number). Our implementation
is non-preemptive. Priority scheduling lets important work go first, but
low-priority processes can **starve**; a common fix (not required here) is
*ageing*, where a waiting process's priority slowly improves over time.

For the example the order is **P2 → P4 → P1 → P3** _(verify against your own run)_
based on the priority values, independent of burst length.

## 3. Screenshots

> Run the program on your own machine and paste your screenshots here.

[SCREENSHOT 1 — main window with the process input table filled in]

[SCREENSHOT 2 — "Single Algorithm" tab: results table + Gantt chart for one algorithm, e.g. SRTF]

[SCREENSHOT 3 — "Compare All" tab: comparison table + bar chart]

## 4. Performance Comparison

All five algorithms were run on the example workload. The quantum for Round
Robin was 2.

| Algorithm | Avg Waiting | Avg Turnaround | Avg Response |
|-----------|:-----------:|:--------------:|:------------:|
| FCFS | 8.75 | 15.25 | 8.75 |
| SJF (non-preemptive) | 7.75 | 14.25 | 7.75 |
| **SRTF (preemptive)** | **6.50** | **13.00** | 4.25 |
| Round Robin (q = 2) | 12.75 | 19.25 | **2.00** |
| Priority | 7.75 | 14.25 | 7.75 |

_(These are the program's actual outputs for the default workload. If you change
the workload, regenerate this table from your own run.)_

[SCREENSHOT 4 — the comparison bar chart produced by "Compare All"]

## 5. Discussion and Analysis

The comparison highlights that **no single algorithm wins on every metric**:

- **SRTF** achieved the lowest average waiting and turnaround times, confirming
  the theory that preemptive shortest-job scheduling is optimal for minimising
  waiting. The price is the most preemptions, and in a real system the need to
  know remaining burst times, which is usually only estimated.
- **Round Robin** had by far the best average response time because every
  process gets the CPU quickly, but its average waiting and turnaround times were
  the worst here due to repeated context switching. This makes RR a good fit for
  interactive / time-sharing systems where responsiveness matters more than raw
  throughput.
- **SJF and Priority** produced identical averages *for this particular
  workload* — a coincidence caused by the chosen priorities lining up with burst
  order. On other workloads they diverge, which is easy to demonstrate by
  editing the process table.
- **FCFS** was the simplest but not the most efficient; the long P3 and P4
  arriving behind shorter work illustrate the convoy effect.

Other observations worth noting in the demo: changing the Round Robin quantum
visibly trades responsiveness against switching overhead, and SJF/SRTF can
starve a long process if short jobs keep arriving.

## 6. Conclusion

This project implemented and compared five CPU-scheduling algorithms in a single
Python tool with a graphical interface, Gantt-chart visualisation, and automatic
benchmarking. Testing against known textbook examples confirmed the results are
correct. The comparison made the classic trade-offs concrete: **SRTF** minimises
waiting time, **Round Robin** maximises responsiveness, and **FCFS** is simplest
but prone to the convoy effect. The "best" algorithm therefore depends on the
goal of the system — throughput, responsiveness, or fairness — rather than being
absolute. _(State which one your group concluded is best for your chosen
scenario, and why.)_

---

### Appendix: How to reproduce these results
```bash
pip install matplotlib pandas
python main.py --cli      # prints every table shown above
python main.py            # opens the GUI used for the screenshots
python test_engine.py     # confirms correctness vs textbook answers
```
