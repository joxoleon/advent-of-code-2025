#!/usr/bin/env python3
"""Advent of Code 2025 - Day 10 Part 2"""

import os
from typing import List, Tuple
from collections import defaultdict, deque
import heapq
import math


def load_input():
    """Load and return input lines from input2.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input2.txt")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input2.txt with your puzzle input.")
        return

def process_machine_input(line: str) -> Tuple[int, List[int], List[List[int]]]:
    """Process a single line of input for the machine"""
    # Joltage ratings - extract the numbers in curly braces
    curly_start = line.find('{')
    curly_end = line.find('}')
    target_joltage_ratings = tuple(int(num) for num in line[curly_start + 1:curly_end].split(','))
    
    # Button presses - extract the numbers in parentheses
    buttons = []
    button_strs = line.split()[1:-1]  # Skip the first and last parts
    for bstr in button_strs:
        bnums = bstr.strip('()').split(',')
        buttons.append(list(int(num) for num in bnums))
    
    return target_joltage_ratings, buttons
    
def build_button_vectors(buttons: List[List[int]], n: int) -> List[List[int]]:
    button_vecs = []
    for b in buttons:
        vec = [0] * n
        for num in b:
            vec[num] = 1
        button_vecs.append(vec)
    return button_vecs

def sort_buttons(button_vecs: List[List[int]]) -> List[List[int]]:
    # sort by number of lights turned on (descending)
    return sorted(button_vecs, key=lambda x: -sum(x))

def lower_bound(remaining, button_vecs, start_idx):
    n = len(remaining)
    lb = 0

    for i in range(n):
        max_inc = 0
        for b in button_vecs[start_idx:]:
            if b[i]:
                max_inc = 1
                break

        if max_inc == 0:
            if remaining[i] > 0:
                return math.inf
        else:
            lb = max(lb, remaining[i])

    return lb

def eliminate_dominated(buttons):
    res = []
    for i, a in enumerate(buttons):
        dominated = False
        for j, b in enumerate(buttons):
            if i == j:
                continue
            if all(b[k] >= a[k] for k in range(len(a))) and sum(b) >= sum(a):
                dominated = True
                break
        if not dominated:
            res.append(a)
    return res


def min_button_presses_for_machine(target, buttons):
    n = len(target)

    # preprocess
    button_vecs = build_button_vectors(buttons, n)
    button_vecs = eliminate_dominated(button_vecs)
    button_vecs = sort_buttons(button_vecs)

    best = sum(target)  # absolute worst case: press single counters
    memo = {}

    def dfs(idx, remaining, used):
        nonlocal best

        if used >= best:
            return

        if all(x == 0 for x in remaining):
            best = used
            return

        if idx == len(button_vecs):
            return

        key = (idx, remaining)
        prev = memo.get(key)
        if prev is not None and prev <= used:
            return
        memo[key] = used


        # lower bound prune
        lb = lower_bound(remaining, button_vecs, idx)
        if used + lb >= best:
            return

        b = button_vecs[idx]

        # max presses for this button
        max_k = math.inf
        for i in range(n):
            if b[i]:
                max_k = min(max_k, remaining[i])
        if max_k is math.inf:
            max_k = 0

        # try large k first (find good solutions early)
        for k in range(max_k, -1, -1):
            new_remaining = list(remaining)
            for i in range(n):
                if b[i]:
                    new_remaining[i] -= k
            dfs(idx + 1, tuple(new_remaining), used + k)

    dfs(0, tuple(target), 0)
    return best

    
def solve():
    total_presses = 0
    for line in load_input():
        total_presses += min_button_presses_for_machine(*process_machine_input(line))
        print(total_presses)
    print(total_presses)

if __name__ == "__main__":
    solve()
