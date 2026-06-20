"""
Tkinter graphical front-end for the CPU Scheduling Simulator.

It is deliberately "thin": every scheduling decision happens in scheduler.py
(which is unit-tested) and every chart is drawn by charts.py. This file only
collects user input, calls those modules, and shows the results.

Run it with:   python main.py        (or:  python gui.py)
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import scheduler
import charts


class SchedulerApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=10)
        master.title("CPU Scheduling Simulator")
        master.geometry("1050x760")
        self.pack(fill="both", expand=True)

        self._counter = 0                                  # auto PID numbering

        self._build_input_panel()
        self._build_controls()
        self._build_output_tabs()
        self._seed_example()

    # ------------------------------------------------------------------ input
    def _build_input_panel(self):
        frame = ttk.LabelFrame(self, text="1. Processes", padding=8)
        frame.pack(fill="x", pady=(0, 8))

        # --- entry row ---
        entry = ttk.Frame(frame)
        entry.pack(fill="x")
        self.e_pid = self._labelled_entry(entry, "Process ID", 0, "")
        self.e_arr = self._labelled_entry(entry, "Arrival", 1, "0")
        self.e_bur = self._labelled_entry(entry, "Burst", 2, "1")
        self.e_pri = self._labelled_entry(entry, "Priority", 3, "0")
        ttk.Button(entry, text="Add Process",
                   command=self.add_process).grid(row=1, column=4, padx=6)

        # --- table of processes ---
        cols = ("pid", "arrival", "burst", "priority")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=6)
        for c, title in zip(cols, ("Process ID", "Arrival Time",
                                   "Burst Time", "Priority")):
            self.tree.heading(c, text=title)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="x", pady=(8, 4))

        btns = ttk.Frame(frame)
        btns.pack(fill="x")
        ttk.Button(btns, text="Delete Selected",
                   command=self.delete_selected).pack(side="left")
        ttk.Button(btns, text="Clear All",
                   command=self.clear_all).pack(side="left", padx=6)

    def _labelled_entry(self, parent, label, col, default):
        ttk.Label(parent, text=label).grid(row=0, column=col, padx=4, sticky="w")
        var = tk.StringVar(value=default)
        e = ttk.Entry(parent, textvariable=var, width=12)
        e.grid(row=1, column=col, padx=4)
        e.var = var
        return e

    # --------------------------------------------------------------- controls
    def _build_controls(self):
        frame = ttk.LabelFrame(self, text="2. Algorithm & Options", padding=8)
        frame.pack(fill="x", pady=(0, 8))

        ttk.Label(frame, text="Algorithm:").grid(row=0, column=0, padx=4)
        self.algo_var = tk.StringVar(value=scheduler.ALGORITHMS[0])
        ttk.Combobox(frame, textvariable=self.algo_var,
                     values=scheduler.ALGORITHMS, state="readonly",
                     width=16).grid(row=0, column=1, padx=4)

        ttk.Label(frame, text="Time Quantum (RR):").grid(row=0, column=2, padx=4)
        self.quantum_var = tk.StringVar(value="2")
        ttk.Entry(frame, textvariable=self.quantum_var,
                  width=6).grid(row=0, column=3, padx=4)

        self.lower_higher = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Lower number = higher priority",
                        variable=self.lower_higher).grid(row=0, column=4, padx=10)

        ttk.Button(frame, text="Run", command=self.run_single).grid(
            row=0, column=5, padx=6)
        ttk.Button(frame, text="Compare All", command=self.run_compare).grid(
            row=0, column=6, padx=2)

    # ------------------------------------------------------------- output area
    def _build_output_tabs(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        # --- Tab 1: single algorithm ---
        tab1 = ttk.Frame(self.nb, padding=6)
        self.nb.add(tab1, text="Single Algorithm")

        self.order_lbl = ttk.Label(tab1, text="Execution order: —",
                                   font=("TkDefaultFont", 10, "bold"))
        self.order_lbl.pack(anchor="w")

        rcols = ("pid", "arrival", "burst", "completion",
                 "turnaround", "waiting", "response")
        self.result_tree = ttk.Treeview(tab1, columns=rcols,
                                         show="headings", height=6)
        for c, title in zip(rcols, ("PID", "Arrival", "Burst", "Completion",
                                    "Turnaround", "Waiting", "Response")):
            self.result_tree.heading(c, text=title)
            self.result_tree.column(c, width=100, anchor="center")
        self.result_tree.pack(fill="x", pady=4)

        self.avg_lbl = ttk.Label(tab1, text="Averages: —")
        self.avg_lbl.pack(anchor="w", pady=(0, 4))

        self.fig1 = Figure(figsize=(8, 2.4))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=tab1)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True)

        # --- Tab 2: comparison ---
        tab2 = ttk.Frame(self.nb, padding=6)
        self.nb.add(tab2, text="Compare All")

        ccols = ("algorithm", "avg_waiting", "avg_turnaround", "avg_response")
        self.cmp_tree = ttk.Treeview(tab2, columns=ccols,
                                     show="headings", height=6)
        for c, title in zip(ccols, ("Algorithm", "Avg Waiting",
                                    "Avg Turnaround", "Avg Response")):
            self.cmp_tree.heading(c, text=title)
            self.cmp_tree.column(c, width=180, anchor="center")
        self.cmp_tree.pack(fill="x", pady=4)

        self.fig2 = Figure(figsize=(8, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=tab2)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

    # ------------------------------------------------------------ data helpers
    def _collect_processes(self) -> list[scheduler.Process]:
        procs = []
        for iid in self.tree.get_children():
            pid, arr, bur, pri = self.tree.item(iid)["values"]
            procs.append(scheduler.Process(str(pid), int(arr), int(bur), int(pri)))
        return procs

    def add_process(self):
        try:
            pid = self.e_pid.var.get().strip()
            if not pid:
                self._counter += 1
                pid = f"P{self._counter}"
            arr = int(self.e_arr.var.get())
            bur = int(self.e_bur.var.get())
            pri = int(self.e_pri.var.get())
            if arr < 0 or bur <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Arrival must be >= 0 and Burst must be a positive integer.")
            return
        self.tree.insert("", "end", values=(pid, arr, bur, pri))
        self.e_pid.var.set("")

    def delete_selected(self):
        for iid in self.tree.selection():
            self.tree.delete(iid)

    def clear_all(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        self._counter = 0

    def _seed_example(self):
        for pid, a, b, p in [("P1", 0, 8, 3), ("P2", 1, 4, 1),
                             ("P3", 2, 9, 4), ("P4", 3, 5, 2)]:
            self.tree.insert("", "end", values=(pid, a, b, p))
        self._counter = 4

    # ----------------------------------------------------------------- actions
    def run_single(self):
        procs = self._collect_processes()
        if not procs:
            messagebox.showwarning("No processes", "Add at least one process.")
            return
        try:
            quantum = int(self.quantum_var.get())
        except ValueError:
            messagebox.showerror("Invalid quantum", "Quantum must be an integer.")
            return

        result = scheduler.run(self.algo_var.get(), procs,
                               quantum=quantum,
                               lower_is_higher=self.lower_higher.get())

        # fill results table
        for iid in self.result_tree.get_children():
            self.result_tree.delete(iid)
        for r in result.rows:
            self.result_tree.insert("", "end", values=(
                r["pid"], r["arrival"], r["burst"], r["completion"],
                r["turnaround"], r["waiting"], r["response"]))

        self.order_lbl.config(text=f"Execution order: {result.execution_order}")
        self.avg_lbl.config(text=(
            f"Averages →  Waiting: {result.avg_waiting:.2f}   "
            f"Turnaround: {result.avg_turnaround:.2f}   "
            f"Response: {result.avg_response:.2f}"))

        charts.draw_gantt(self.fig1, result)
        self.canvas1.draw()
        self.nb.select(0)

    def run_compare(self):
        procs = self._collect_processes()
        if not procs:
            messagebox.showwarning("No processes", "Add at least one process.")
            return
        try:
            quantum = int(self.quantum_var.get())
        except ValueError:
            messagebox.showerror("Invalid quantum", "Quantum must be an integer.")
            return

        results = scheduler.run_all(procs, quantum=quantum,
                                    lower_is_higher=self.lower_higher.get())

        for iid in self.cmp_tree.get_children():
            self.cmp_tree.delete(iid)
        for r in results:
            self.cmp_tree.insert("", "end", values=(
                r.algorithm, f"{r.avg_waiting:.2f}",
                f"{r.avg_turnaround:.2f}", f"{r.avg_response:.2f}"))

        # highlight the best (lowest avg waiting) by tagging
        best = min(results, key=lambda r: r.avg_waiting)
        self.cmp_tree.tag_configure("best", background="#D6F5D6")
        for iid, r in zip(self.cmp_tree.get_children(), results):
            if r is best:
                self.cmp_tree.item(iid, tags=("best",))

        charts.draw_comparison(self.fig2, results)
        self.canvas2.draw()
        self.nb.select(1)


def main():
    root = tk.Tk()
    SchedulerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
