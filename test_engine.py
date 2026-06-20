"""Verify the engine against hand-computed textbook examples."""
from scheduler import Process, fcfs, sjf, srtf, round_robin, priority_scheduling

def approx(a, b): return abs(a - b) < 1e-9

# ---- Example A: FCFS & RR, all arrive at 0 (Silberschatz convoy example) ----
A = [Process("P1",0,24), Process("P2",0,3), Process("P3",0,3)]
r = fcfs(A)
assert approx(r.avg_waiting, 17.0), r.avg_waiting
assert approx(r.avg_turnaround, 27.0), r.avg_turnaround
print("FCFS-A  avg WT =", r.avg_waiting, " order:", r.execution_order)

r = round_robin(A, quantum=4)
assert approx(r.avg_waiting, 17/3), r.avg_waiting   # ~5.667
print("RR-A    avg WT =", round(r.avg_waiting,3), " order:", r.execution_order)
print("        timeline:", r.timeline)

# ---- Example B: with arrivals (classic SRTF example) ----
B = [Process("P1",0,8), Process("P2",1,4), Process("P3",2,9), Process("P4",3,5)]
r = fcfs(B)
assert approx(r.avg_waiting, 8.75), r.avg_waiting
print("FCFS-B  avg WT =", r.avg_waiting)

r = srtf(B)
assert approx(r.avg_waiting, 6.5), r.avg_waiting
print("SRTF-B  avg WT =", r.avg_waiting, " order:", r.execution_order)
print("        timeline:", r.timeline)

r = sjf(B)   # non-preemptive SJF on B
print("SJF-B   avg WT =", r.avg_waiting, " order:", r.execution_order)

# ---- Example C: Priority (lower number = higher priority) ----
C = [Process("P1",0,10,3), Process("P2",0,1,1), Process("P3",0,2,4),
     Process("P4",0,1,5), Process("P5",0,5,2)]
r = priority_scheduling(C, lower_is_higher=True)
assert approx(r.avg_waiting, 8.2), r.avg_waiting
print("PRIO-C  avg WT =", r.avg_waiting, " order:", r.execution_order)

# ---- sanity: idle handling (gap before first arrival) ----
D = [Process("P1",5,3), Process("P2",6,2)]
r = fcfs(D)
assert r.timeline[0][0] == "IDLE" and r.timeline[0] == ("IDLE",0,5), r.timeline
print("IDLE-D  timeline:", r.timeline)

print("\nALL ASSERTIONS PASSED ✔")
