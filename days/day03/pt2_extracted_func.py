#!/usr/bin/env python3
"""Advent of Code 2025 - Day 03 Part 2"""

import os
from typing import Tuple

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
    total_joltage = 0
    num_bats = 12
    lines = load_input()
    start_time = os.times()
    for line in lines:
        joltage = ""
        start_i = 0
        batt_count = num_bats
        while batt_count:
            lmax, target_i = leftmost_max(line, start_i, len(line) - batt_count)
            joltage += lmax
            start_i = target_i + 1
            batt_count -= 1
        print(joltage)
        total_joltage += int(joltage)
        
    end_time = os.times()
    print("")
    print(total_joltage)
    print(f"Elapsed time: {end_time.elapsed - start_time.elapsed} seconds")
    
def leftmost_max(arr: str, start_i: int, end_i: int) -> Tuple[str, int]:
    lmax = ' ' 
    target_i = start_i
    for i in range(start_i, end_i + 1):
        if arr[i] > lmax:
            target_i = i
            lmax = arr[i]
            if lmax == '9':
                break
    return (lmax, target_i)
            
        
    
        

if __name__ == "__main__":
    solve()
