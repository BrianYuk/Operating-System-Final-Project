from collections import deque
from types import SimpleNamespace
import copy

def Process(pid, arrival, burst, priority=0):
    return {
        'pid': pid, 'arrival': arrival, 'burst': burst, 'priority': priority,
        'remaining': burst, 'start_time': None, 'completion': None,
    }


def _rows_for(processes):
    rows = []
    for p in sorted(processes, key=lambda p: p['pid']):
        turnaround = p['completion'] - p['arrival']
        waiting = turnaround - p['burst']
        response = p['start_time'] - p['arrival']
        rows.append({
            'pid': p['pid'], 'arrival': p['arrival'], 'burst': p['burst'],
            'priority': p['priority'], 'completion': p['completion'],
            'turnaround': turnaround, 'waiting': waiting, 'response': response,
        })
    return rows


def _execution_order(timeline):
    order = []
    for label, _, _ in timeline:
        if label != 'IDLE' and (not order or order[-1] != label):
            order.append(label)
    return ' -> '.join(order)


def Result(algorithm, timeline, rows):
    n = len(rows)
    return SimpleNamespace(
        algorithm=algorithm,
        timeline=timeline,
        rows=rows,
        avg_waiting=sum(r['waiting'] for r in rows) / n,
        avg_turnaround=sum(r['turnaround'] for r in rows) / n,
        avg_response=sum(r['response'] for r in rows) / n,
        execution_order=_execution_order(timeline),
    )

def fcfs(processes):
    procs = copy.deepcopy(processes) 
    procs = sorted(procs, key = lambda x: (x['arrival'], x['pid']))

    time = 0
    timeline = []
    for p in procs:
        if time < p['arrival']:
            timeline.append(('IDLE', time, p['arrival']))
            time = p['arrival']
        p['start_time'] = time
        timeline.append((p['pid'], time, time + p['burst']))
        time += p['burst']
        p['completion'] = time

    return Result('FCFS', timeline, _rows_for(procs))

def sjf(processes):
    procs = copy.deepcopy(processes)
    time = 0
    timeline = []

    while any(p['completion'] is None for p in procs):
        ready = [p for p in procs if p['completion'] is None and p['arrival'] <= time]
        if not ready:
            next_arrival = min(p['arrival'] for p in procs if p['completion'] is None)
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            continue
        current = min(ready, key = lambda x: (x['burst'], x['arrival'], x['pid']))
        current['start_time'] = time
        timeline.append((current['pid'], time, time + current['burst']))
        time += current['burst']
        current['completion'] = time

    return Result('SJF', timeline, _rows_for(procs))


def priority_scheduling(processes, lower_is_higher=True):
    procs = copy.deepcopy(processes)

    if lower_is_higher:
        rank = lambda p: (p['priority'], p['arrival'], p['pid'])
        name = 'Priority (lower number = higher priority)'
    else:
        rank = lambda p: (-p['priority'], p['arrival'], p['pid'])
        name = 'Priority (higher number = higher priority)'

    time = 0
    timeline = []
    while any(p['completion'] is None for p in procs):
        ready = [p for p in procs if p['completion'] is None and p['arrival'] <= time]
        if not ready:
            next_arrival = min(p['arrival'] for p in procs if p['completion'] is None)
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            continue
        current = min(ready, key=rank)
        current['start_time'] = time
        timeline.append((current['pid'], time, time + current['burst']))
        time += current['burst']
        current['completion'] = time

    return Result(name, timeline, _rows_for(procs))


def srtf(processes):
    procs = copy.deepcopy(processes)

    time = 0
    timeline = []
    while any(p['remaining'] > 0 for p in procs):
        ready = [p for p in procs if p['remaining'] > 0 and p['arrival'] <= time]
        if not ready:
            next_arrival = min(p['arrival'] for p in procs if p['remaining'] > 0)
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            continue
        current = min(ready, key=lambda p: (p['remaining'], p['arrival'], p['pid']))
        if current['start_time'] is None:
            current['start_time'] = time
        if timeline and timeline[-1][0] == current['pid']:
            label, start, end = timeline[-1]
            timeline[-1] = (label, start, end + 1)
        else:
            timeline.append((current['pid'], time, time + 1))
        time += 1
        current['remaining'] -= 1
        if current['remaining'] == 0:
            current['completion'] = time

    return Result('SRTF (preemptive)', timeline, _rows_for(procs))


def round_robin(processes, quantum=2):
    if quantum < 1:
        raise ValueError("Time quantum must be a positive integer.")
    procs = copy.deepcopy(processes)
    order = sorted(procs, key=lambda p: (p['arrival'], p['pid']))

    time = 0
    timeline = []
    queue = deque()
    idx = 0

    def enqueue_arrivals(upto):
        nonlocal idx
        while idx < len(order) and order[idx]['arrival'] <= upto:
            queue.append(order[idx])
            idx += 1

    enqueue_arrivals(time)
    while queue or idx < len(order):
        if not queue:
            next_arrival = order[idx]['arrival']
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            enqueue_arrivals(time)
            continue

        current = queue.popleft()
        if current['start_time'] is None:
            current['start_time'] = time
        run = min(quantum, current['remaining'])
        if timeline and timeline[-1][0] == current['pid']:
            label, start, end = timeline[-1]
            timeline[-1] = (label, start, end + run)
        else:
            timeline.append((current['pid'], time, time + run))
        time += run
        current['remaining'] -= run

        # arrivals DURING this slice queue up before the preempted process rejoins
        enqueue_arrivals(time)
        if current['remaining'] > 0:
            queue.append(current)
        else:
            current['completion'] = time

    return Result(f'Round Robin (q={quantum})', timeline, _rows_for(procs))