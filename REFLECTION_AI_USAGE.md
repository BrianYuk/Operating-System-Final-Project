# Reflection and AI Usage Report

**Course:** Operating Systems (COMP6697001)
**Group members:** _<Name 1 – ID>, <Name 2 – ID>_
**Length limit:** 2 pages — trim to fit.

> **READ THIS FIRST.** Your lecturer explicitly allows AI assistance but
> requires *honest disclosure* and *full understanding* — undisclosed or
> not-understood AI use can be treated as academic misconduct, and duplicated
> submissions can score zero. This file is a **scaffold**: every bracketed line
> is a prompt for *you* to answer truthfully about what *your group* actually
> did. Do not submit it with the brackets still in it, and do not claim work you
> cannot explain. Before submitting, make sure each of you can walk through
> `scheduler.py` and explain any function on the spot.
>
> **Make it genuinely yours (recommended):** rename variables to your style, add
> at least one feature or tweak of your own (e.g. a context-switch counter,
> CPU-utilisation %, a different colour scheme, an extra algorithm like
> preemptive priority, or saving the Gantt chart as an image), and adjust the
> wording below. This makes the disclosure truthful *and* protects you from
> similarity penalties.

---

## A. AI Usage Disclosure

**AI tool(s) used:** _e.g. Claude (Anthropic). List any others you used such as
ChatGPT, GitHub Copilot, Gemini._

**What we asked the AI to do (representative prompts):**
- _"Help me build a Python CPU scheduling simulator with FCFS, SJF, Round Robin
  and Priority, that outputs waiting/turnaround times and a Gantt chart."_
- _"Explain how Round Robin handles processes that arrive during a time
  quantum."_
- _"Add SRTF and an automatic comparison chart that benchmarks all algorithms."_
- _<add any other prompts you actually used, including follow-ups where you
  asked it to fix or explain something>_

**Parts that were AI-assisted:** _Be specific and truthful. For example: the
initial structure of `scheduler.py`, the matplotlib Gantt-chart code in
`charts.py`, and the Tkinter layout in `gui.py` were drafted with AI help._

**Parts we wrote / changed ourselves:** _List what you genuinely did yourself —
e.g. the priority-direction toggle, the report analysis, the test cases you
added, the variable renaming, the colour choices, or a feature you invented. If
you wrote little from scratch, be honest and emphasise the modifications and
verification you did instead._

**How we modified / improved the AI-generated code:** _Describe real changes:
e.g. "we changed the priority convention to lower-number-is-higher to match the
lecture notes", "we added a context-switch counter", "we adjusted the Round
Robin arrival ordering after testing", "we refactored X into its own function".
Even small, real edits count and should be named._

**How we verified correctness:** _e.g. "We ran `test_engine.py`, which checks
the algorithms against hand-computed textbook examples (FCFS average waiting
17.0, SRTF average waiting 6.5, Priority average waiting 8.2). We also
hand-traced the Gantt chart for SRTF on the default workload and confirmed the
timeline P1→P2→P4→P1→P3 matched the program output."_

## B. Reflection

**Where AI was helpful:** _e.g. quickly scaffolding the GUI and the matplotlib
plotting, which would have taken us much longer to look up; explaining the
standard Round Robin queue convention._

**Where AI gave incorrect or poor suggestions:** _Be honest. If everything
worked first time, that is itself worth noting; but most groups hit at least one
issue — e.g. an off-by-one in idle handling, an ambiguous priority direction, a
Gantt chart that didn't show idle gaps, or a suggestion that mutated the input
list so "Compare All" gave wrong numbers until copies were used. Describe what
you noticed and how you fixed/checked it._

**Challenges we faced during implementation:** _e.g. getting Round Robin to
queue mid-quantum arrivals in the right order; embedding matplotlib inside
Tkinter; deciding the priority convention; installing python3-tk._

**What we learned:** _e.g. how preemption changes the metrics; why SJF/SRTF
minimise waiting time but risk starvation; why Round Robin trades waiting time
for responsiveness; the value of separating logic (`scheduler.py`) from UI so it
can be tested._

**Which scheduling algorithm we believe performs best, and why:** _Give a
defensible answer with a reason tied to a metric and a context. There is no
single right answer — for example: "For minimising average waiting and
turnaround time, **SRTF** was best in our tests (6.50 vs 8.75 for FCFS).
However, for an interactive system we would prefer **Round Robin** because its
response time was lowest (2.00). So 'best' depends on the system's goal."_

---

### Honesty checklist before you submit
- [ ] Every bracketed placeholder is replaced with our real answers.
- [ ] We listed every AI tool we used.
- [ ] We can each explain any function in `scheduler.py` if asked.
- [ ] We made at least one real modification of our own and described it.
- [ ] The numbers we quote match what our program actually prints.
