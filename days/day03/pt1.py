#!/usr/bin/env python3
"""Advent of Code 2025 - Day 03 Part 1"""

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
    total_joltage = 0
    num_bats = 2
    for line in load_input():
        joltage = ""
        start_i = 0
        batt_count = num_bats
        while batt_count:
            batt_j = '0'
            i = start_i
            while i <= len(line) - batt_count:
                if line[i] > batt_j:
                    batt_j = line[i]
                    start_i = i + 1
                    if batt_j == '9':
                        break
                i += 1
            batt_count -= 1
            joltage += batt_j
        print(joltage)
        total_joltage += int(joltage)
        
    print("")
    print(total_joltage) 
        

if __name__ == "__main__":
    solve()
