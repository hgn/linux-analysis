#!/usr/bin/env python3

import os
import re
import signal
import sys
import time
from typing import Dict, List, Tuple

COLOR_RESET: str = "\033[0m"
COLOR_GRAY: str = "\033[90m"
COLOR_RED: str = "\033[31m"

ANSI_ESCAPE_PATTERN: re.Pattern = re.compile(r"\033\[[0-9;]*m")

def read_softirqs(file_path: str = "/proc/softirqs") -> Tuple[List[str], Dict[str, List[int]]]:
    softirq_data: Dict[str, List[int]] = {}
    with open(file_path, "r") as f:
        lines: List[str] = f.readlines()
    cpu_headers: List[str] = lines[0].split()
    for line in lines[1:]:
        parts: List[str] = line.split(":")
        if len(parts) != 2:
            continue
        irq_type: str = parts[0].strip()
        counts: List[int] = list(map(int, parts[1].split()))
        softirq_data[irq_type] = counts
    return cpu_headers, softirq_data

def calculate_differences(
    prev_data: Dict[str, List[int]], 
    current_data: Dict[str, List[int]]
) -> Dict[str, List[int]]:
    return {
        irq_type: [
            curr - prev for curr, prev in zip(current_data[irq_type], prev_data[irq_type])
        ]
        for irq_type in current_data if irq_type in prev_data
    }

def summarize_differences(differences: Dict[str, List[int]]) -> Dict[str, int]:
    return {irq_type: sum(counts) for irq_type, counts in differences.items()}

def calculate_percentages(summary: Dict[str, int]) -> Dict[str, float]:
    total: int = sum(summary.values())
    return {irq_type: (count / total * 100 if total > 0 else 0) for irq_type, count in summary.items()}

def format_value(value: int, max_value: int) -> str:
    if value == max_value and value > 0:
        return f"{COLOR_RED}{value}{COLOR_RESET}"
    elif value == 0:
        return f"{COLOR_GRAY}{value}{COLOR_RESET}"
    return str(value)

def align_columns(values: List[str], col_width: int) -> List[str]:
    return [
        " " * (col_width - len(strip_ansi_codes(value))) + value 
        for value in values
    ]

def strip_ansi_codes(text: str) -> str:
    return ANSI_ESCAPE_PATTERN.sub("", text)

def print_softirq_top(
    cpu_headers: List[str], 
    differences: Dict[str, List[int]], 
    interval: int
) -> None:
    col_width: int = max(6, max(len(cpu) for cpu in cpu_headers))
    sorted_irqs: List[Tuple[str, List[int]]] = sorted(
        differences.items(), 
        key=lambda x: sum(x[1]), 
        reverse=True
    )
    os.system("clear")
    print(f"SoftIRQ Top (refresh every {interval}s):")
    print(f"{'SoftIRQ Type':<12} " + " ".join(f"{cpu:>{col_width}}" for cpu in cpu_headers))
    print("-" * (12 + len(cpu_headers) * (col_width + 1)))
    for irq_type, counts in sorted_irqs:
        max_value: int = max(counts)
        formatted_counts: List[str] = [format_value(value, max_value) for value in counts]
        aligned_counts: List[str] = align_columns(formatted_counts, col_width)
        print(f"{irq_type:<12} " + " ".join(aligned_counts))

def print_summary(summary: Dict[str, int], percentages: Dict[str, float]) -> None:
    print("\nSummary by SoftIRQ Type (All CPUs):")
    print(f"{'SoftIRQ Type':<12} {'Total':>12} {'% of Total':>12}")
    print("-" * 40)
    sorted_summary: List[Tuple[str, int]] = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    for irq_type, total in sorted_summary:
        percentage: float = percentages[irq_type]
        print(f"{irq_type:<12} {total:>12} {percentage:>11.2f}%")

def handle_exit(signal: int, frame) -> None:
    print("\nExiting cleanly... Goodbye!")
    sys.exit(0)

def main() -> None:
    signal.signal(signal.SIGINT, handle_exit)
    interval: int = 1
    cpu_headers, prev_softirqs = read_softirqs()
    while True:
        time.sleep(interval)
        cpu_headers, current_softirqs = read_softirqs()
        differences: Dict[str, List[int]] = calculate_differences(prev_softirqs, current_softirqs)
        summary: Dict[str, int] = summarize_differences(differences)
        percentages: Dict[str, float] = calculate_percentages(summary)
        print_softirq_top(cpu_headers, differences, interval)
        print_summary(summary, percentages)
        prev_softirqs = current_softirqs

if __name__ == "__main__":
    main()

