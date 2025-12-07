#!/usr/bin/env python3
"""Advent of Code 2025 - Day 07 Part 1"""

import os
from collections import deque
from typing_extensions import List
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
    
def load_grid():
    grid = []
    # Split each line into a list of characters for mutability
    for line in load_input():
        grid.append(list(line))
    return grid

# Utility functions - debug
def update_grid(grid: List[str], row, beam_arr: List[int]):
    for c in beam_arr:
        grid[row][c] = '|'

def render_grid(grid: List[str]):
    for row in grid:
        print(''.join(row))
    print()

def solve():
    grid = load_grid()
    start_time = time.perf_counter()
    R, C = len(grid), len(grid[0])
    beam_cols = []
    splits = 0
    
    for c in range(C):
        if grid[0][c] == 'S':
            beam_cols.append(c)
            break
    
    for r in range(1, R):
        new_beam_cols = []
        nbcset = set()
        for c in beam_cols:
            if grid[r][c] != '^' and c not in nbcset:
                new_beam_cols.append(c)
                nbcset.add(c)
            if grid[r][c] == '^':
                splits += 1
                if 0 <= c - 1 < C and c - 1 not in nbcset:
                    new_beam_cols.append(c - 1)
                    nbcset.add(c - 1)
                if 0 <= c + 1 < C and c + 1 not in nbcset:
                    new_beam_cols.append(c + 1)
                    nbcset.add(c + 1)
        beam_cols = new_beam_cols
        # update_grid(grid, r, beam_cols)
        # render_grid(grid)
            
    end_time = time.perf_counter()
    # Precise time taken in seconds
    print(f"Time taken: {end_time - start_time} seconds")
    print(splits)
                

if __name__ == "__main__":
    solve()
