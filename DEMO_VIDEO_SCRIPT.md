# Demo Video Script (≤ 10 minutes)

Record your screen (OBS Studio, Zoom, Xbox Game Bar, or QuickTime all work) with
both group members speaking. Aim for ~7–8 minutes so you stay under the limit.

---

## 0:00 – 0:45  Introduction
- Both members say name + student ID.
- One line on the project: *"A Python CPU scheduling simulator that implements
  FCFS, SJF, SRTF, Round Robin and Priority scheduling, with a GUI, Gantt
  charts, and automatic comparison."*
- Show the project folder and the files (`scheduler.py`, `charts.py`, `gui.py`,
  `main.py`).

## 0:45 – 2:00  Program execution
- Run `python main.py` and show the window.
- Add a few processes using the input fields and the **Add Process** button.
  Explain the four inputs (Process ID, Arrival, Burst, Priority).

## 2:00 – 4:30  Feature explanation (run each algorithm)
- Select **FCFS**, click **Run**. Point at the results table (waiting,
  turnaround, completion, response) and the **Gantt chart**. Read the execution
  order aloud.
- Switch to **SJF**, run, note how shorter jobs move ahead.
- Switch to **SRTF**, run, point out the *preemption* in the Gantt chart (a
  process appears in two blocks).
- Switch to **Round Robin**, set quantum to 2, run, show how the Gantt chart is
  sliced into quanta. Change the quantum to 4 and re-run to show the effect.
- Switch to **Priority**, run, explain the lower-number-is-higher convention and
  the toggle.

## 4:30 – 6:30  Algorithm comparison (advanced feature)
- Click **Compare All**. Show the comparison table and bar chart.
- Talk through the trade-off: *SRTF has the lowest average waiting time; Round
  Robin has the lowest response time but the highest waiting time.* The
  best-performing row is highlighted.

## 6:30 – 7:30  Brief explanation of AI usage
- State which AI tool(s) you used (e.g. Claude).
- Say which parts were AI-assisted and which you wrote/modified yourselves.
- Mention how you verified correctness — e.g. running `python test_engine.py`
  and showing the "ALL ASSERTIONS PASSED" output, or hand-tracing a Gantt chart.

## 7:30 – 8:00  Wrap up
- One sentence on which algorithm you think is best and why.
- Thank the viewer.

---

### Tips
- Do a quick dry run first so the clicks are smooth.
- If the GUI won't open on the recording machine, `python main.py --cli` gives a
  clean text output you can narrate as a backup.
- Keep the window large enough that the Gantt chart text is readable on video.
