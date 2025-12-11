#!/usr/bin/env python3
"""Advent of Code 2025 - Day 09 Part 1"""

import os
import time

def load_input():
    """Load and return input lines from input1.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input1.txt")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input1.txt with your puzzle input.")
        return

def load_lines():
    lines = []
    for line in load_input():
        strs = line.split(",")
        ints = [int(s) for s in strs]
        lines.append(ints)
    return lines

def solve():
    coords = load_lines()
    max_dist = 0
    for i, (x1, y1) in enumerate(coords):
        for j in range(i + 1, len(coords)):
            x2, y2 = coords[j]
            dist = abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
            max_dist = max(max_dist, dist)
    print(f"Maximum distance: {max_dist}")
    
    max_x = max(x for x, y in coords)
    max_y = max(y for x, y in coords)
    
    # Compute duration
    start_time = time.time()
    for i in range (1000):
        for j in range(100000):
            a = 100 + 200
    end_time = time.time()
    print(f"Duration: {end_time - start_time} seconds")
if __name__ == "__main__":
    solve()
