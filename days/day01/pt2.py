#!/usr/bin/env python3
"""Advent of Code 2025 - Day 01 Part 2"""

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

def solve():
    lines = load_input()
    dial = 50
    password = 0
    for line in lines:
        inc = int(line[1:])
        if line[0] == 'L':
            inc = -inc
        
        new_dial = dial + inc
        password += abs(new_dial // 100)
        dial = new_dial % 100
        
    print(password)

if __name__ == "__main__":
    solve()
