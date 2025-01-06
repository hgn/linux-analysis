#!/usr/bin/env python3

import os, re, signal, sys, time
from typing import Dict, List, Tuple
from collections import defaultdict

COLOR_RESET = "\033[0m"
COLOR_GRAY = "\033[90m"
COLOR_RED = "\033[31m"

ANSI_ESCAPE_PATTERN = re.compile(r"\033\[[0-9;]*m")

def strip_ansi_codes(text: str) -> str:
    return ANSI_ESCAPE_PATTERN.sub("", text)

def normalize_rows(rows: List[List[str]]) -> List[List[str]]:
    if not rows:
        return []
    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")
    return rows

def left_right_table(rows: List[List[str]], left_cols: int = 1) -> str:
    """
    The first 'left_cols' columns are left-aligned, 
    all other columns are right-aligned.
    We measure widths using stripped text (no ANSI),
    but print the original text (with color).
    """
    rows = normalize_rows(rows)
    if not rows:
        return ""

    # Compute raw (stripped) widths
    col_count = len(rows[0])
    widths = [0]*col_count
    for row in rows:
        for c_i, cell in enumerate(row):
            raw_text = strip_ansi_codes(cell)
            if len(raw_text) > widths[c_i]:
                widths[c_i] = len(raw_text)

    lines = []

    # Print the header row
    header = rows[0]
    header_line = []
    for i, cell in enumerate(header):
        raw_text = strip_ansi_codes(cell)
        if i < left_cols:
            # left align -> cell + spaces
            pad = widths[i] - len(raw_text)
            header_line.append(cell + " "*pad)
        else:
            # right align -> spaces + cell
            pad = widths[i] - len(raw_text)
            header_line.append(" "*pad + cell)
    lines.append("  ".join(header_line))

    # Underline row
    underline_cells = []
    for i in range(col_count):
        underline_cells.append("-"*widths[i])
    lines.append("  ".join(underline_cells))

    # Print data rows
    for row in rows[1:]:
        row_pieces = []
        for i, cell in enumerate(row):
            raw_text = strip_ansi_codes(cell)
            pad = widths[i] - len(raw_text)
            if i < left_cols:
                row_pieces.append(cell + " "*pad)
            else:
                row_pieces.append(" "*pad + cell)
        lines.append("  ".join(row_pieces))

    return "\n".join(lines)

def read_softirqs(path: str = "/proc/softirqs") -> Tuple[List[str], Dict[str, List[int]]]:
    with open(path) as f:
        lines = f.readlines()
    headers = lines[0].split()
    data = {}
    for line in lines[1:]:
        parts = line.split(":")
        if len(parts) != 2:
            continue
        irq_type = parts[0].strip()
        vals = list(map(int, parts[1].split()))
        data[irq_type] = vals
    return headers, data

def calc_diff(prev: Dict[str, List[int]], cur: Dict[str, List[int]]) -> Dict[str, List[int]]:
    diff = {}
    for t in cur:
        if t in prev:
            diff[t] = [c - p for c, p in zip(cur[t], prev[t])]
    return diff

def update_cumulative(cum: Dict[str, List[int]], diff: Dict[str, List[int]]):
    for t, arr in diff.items():
        if t not in cum:
            cum[t] = [0]*len(arr)
        for i, val in enumerate(arr):
            cum[t][i] += val

def color_val(value: int, maxv: int) -> str:
    if value == maxv and value > 0:
        return f"{COLOR_RED}{value}{COLOR_RESET}"
    if value == 0:
        return f"{COLOR_GRAY}{value}{COLOR_RESET}"
    return str(value)

def build_per_cpu_rows(hdrs: List[str], interval_data: Dict[str, List[int]]) -> List[List[str]]:
    rows = []
    # header row: "SoftIRQ Type", then CPU labels
    head = ["SoftIRQ Type"] + hdrs
    rows.append(head)
    # sort by total descending
    sorted_irqs = sorted(interval_data.items(), key=lambda x: sum(x[1]), reverse=True)
    for irq_type, counts in sorted_irqs:
        mx = max(counts) if counts else 0
        row = [irq_type] + [color_val(v, mx) for v in counts]
        rows.append(row)
    return rows

def find_top_cpu(data: Dict[str, List[int]]) -> Tuple[str, int]:
    if not data:
        return ("CPU?", 0)
    # assume consistent length
    n = len(next(iter(data.values()), []))
    sums = [0]*n
    for arr in data.values():
        for i, v in enumerate(arr):
            sums[i] += v
    idx = max(range(n), key=lambda i: sums[i])
    return (f"CPU{idx}", sums[idx])

def build_merged_cpu_rows(
    interval_data: Dict[str, List[int]],
    cumulative_data: Dict[str, List[int]]
) -> List[List[str]]:
    rows = []
    i_cpu, i_val = find_top_cpu(interval_data)
    c_cpu, c_val = find_top_cpu(cumulative_data)

    # row 1: top CPU info
    rows.append([
        "CPU with highest total (interval)", f"{i_cpu} ({i_val})",
        "CPU with highest total (cumulative)", f"{c_cpu} ({c_val})"
    ])
    # row 2: sub headers
    rows.append([
        "SoftIRQ Type", "Top CPU (Interval)", "Count (Interval)",
        "Top CPU (Cumul.)", "Count (Cumul.)"
    ])
    all_irqs = sorted(set(interval_data.keys()) | set(cumulative_data.keys()))
    for t in all_irqs:
        i_cpu2, i_val2 = "CPU?", 0
        if t in interval_data:
            arr_i = interval_data[t]
            mx_i = max(arr_i)
            idx_i = arr_i.index(mx_i)
            i_cpu2 = f"CPU{idx_i}"
            i_val2 = mx_i
        c_cpu2, c_val2 = "CPU?", 0
        if t in cumulative_data:
            arr_c = cumulative_data[t]
            mx_c = max(arr_c)
            idx_c = arr_c.index(mx_c)
            c_cpu2 = f"CPU{idx_c}"
            c_val2 = mx_c
        rows.append([t, i_cpu2, str(i_val2), c_cpu2, str(c_val2)])
    return rows

def build_summary_rows(
    diff_sums: Dict[str, int],
    softirq_history: defaultdict
) -> List[List[str]]:
    rows = []
    rows.append(["SoftIRQ", "Events (Interval)", "% of Interval", "Min", "Max", "Avg"])
    total = sum(diff_sums.values())
    # sort desc by total in this interval
    for t, val in sorted(diff_sums.items(), key=lambda x: x[1], reverse=True):
        if total > 0:
            perc = val / total * 100
        else:
            perc = 0
        # historical min, max, avg
        hist_vals = softirq_history[t]
        mn = min(hist_vals)
        mx = max(hist_vals)
        avg = sum(hist_vals)/len(hist_vals)
        rows.append([
            t,
            str(val),
            f"{perc:.1f}",
            str(mn),
            str(mx),
            f"{avg:.1f}"
        ])
    return rows

def sig_exit(a, b):
    print("\nExiting cleanly... Goodbye!")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, sig_exit)
    interval = 1
    hdrs, prev = read_softirqs()
    cumulative = {}
    softirq_history = defaultdict(list)

    while True:
        time.sleep(interval)
        hdrs, cur = read_softirqs()
        d = calc_diff(prev, cur)
        update_cumulative(cumulative, d)

        # This-interval sums
        diff_sums = {t: sum(arr) for t, arr in d.items()}
        for t, v in diff_sums.items():
            softirq_history[t].append(v)

        os.system("clear")

        # 1) Per-CPU intervals
        per_cpu_data = build_per_cpu_rows(hdrs, d)
        print(left_right_table(per_cpu_data, left_cols=1))
        print()

        # 2) Merged CPU summary
        merged_cpu_data = build_merged_cpu_rows(d, cumulative)
        print(left_right_table(merged_cpu_data, left_cols=1))
        print()

        # 3) Summary table
        summary_data = build_summary_rows(diff_sums, softirq_history)
        print(left_right_table(summary_data, left_cols=1))

        prev = cur

if __name__ == "__main__":
    main()

