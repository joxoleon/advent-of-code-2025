#!/usr/bin/env python3
"""Advent of Code 2025 - Day 07 Part 1"""

import os

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

def solve():
    """Solve Part 1"""
    for line in load_input():
        # TODO: Process each line
        print(line)

if __name__ == "__main__":
    solve()
