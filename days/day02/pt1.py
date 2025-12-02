#!/usr/bin/env python3
"""Advent of Code 2025 - Day 02 Part 1"""

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
    all_lines = list(load_input())
    all_ranges = all_lines[0].split(",")
    
    invalid_ids = []
    for num_range in all_ranges:
        left, right = num_range.split("-")
        s = int(left)
        e = int(right)
        for num in range(s, e + 1):
            if is_invalid(str(num)):
                print(f"Invalid id: {num}")
                invalid_ids.append(num)
    
    print(sum(invalid_ids))
                

def factors(n: int):
    result = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i and n // i != n:
                result.append(n // i)
    return sorted(result)

def is_invalid(s: str) -> bool:
    if len(s) % 2 != 0:
        return False
    mid = int(len(s) / 2)
    l = s[:mid]
    r = s[mid:]
    return l == r

if __name__ == "__main__":
    solve()
