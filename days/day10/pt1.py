#!/usr/bin/env python3
"""Advent of Code 2025 - Day 10 Part 1"""

import os

def load_input():
    """Load and return input lines from input1.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input1.txt")
    
    with open(input_path, "r") as f:
        for line in f:
            yield line.rstrip("\n")

def solve():
    """Solve Part 1"""
    for line in load_input():
        # TODO: Process each line
        print(line)

if __name__ == "__main__":
    solve()
