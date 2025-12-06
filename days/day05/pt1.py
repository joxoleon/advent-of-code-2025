#!/usr/bin/env python3
"""Advent of Code 2025 - Day 05 Part 1"""

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

def load():
    fresh_ranges = []
    ids = []
    load_ranges = True
    
    for line in load_input():
        # After we encounter a newline we start loading ids
        if line == "":
            load_ranges = False
            continue
        if load_ranges:
            parts = line.split("-")
            fresh_ranges.append((int(parts[0]), int(parts[1])))
        else:
            ids.append(int(line))
    return (fresh_ranges, ids)

# ----------------------------------------------------------------------



def solve():
    fresh_ranges, ids = load()
    fresh_ranges.sort()
    ids.sort()

    # Merge intervals - Range start is true, range end is false
    frm = [(fresh_ranges[0][0], True), (fresh_ranges[0][1] + 1, False)]
    for i in range(1, len(fresh_ranges)):
        s, e = fresh_ranges[i]
        ps, pe = frm[-2][0], frm[-1][0]
        if s <= pe:
            # We are merging intervals
            frm[-1] = (max(e + 1, pe), False)
        else:
            frm.append((s, True))
            frm.append((e + 1, False))
    
    ridx = 0
    fresh = False
    fresh_count = 0
    
    for id in ids:
        # First adjust within the current range
        while ridx < len(frm) and id >= frm[ridx][0]:
            fresh = frm[ridx][1]
            ridx += 1
        
        if fresh:
            print(f"{id} is Fresh")
            fresh_count += 1
        else:
            print(f"{id} is not fresh")
    
    print(fresh_count)
             
            
        


if __name__ == "__main__":
    solve()
