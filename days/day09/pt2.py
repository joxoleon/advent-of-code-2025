#!/usr/bin/env python3
"""Advent of Code 2025 - Day 09 Part 2"""

import os

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
            print(f"Distance between point {x1},{y1} and point {x2},{y2}: {dist}")
    print(f"Maximum distance: {max_dist}")

if __name__ == "__main__":
    solve()
