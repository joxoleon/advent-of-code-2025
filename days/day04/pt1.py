#!/usr/bin/env python3
"""Advent of Code 2025 - Day 04 Part 1"""

import os

def load_input() -> list[str]:
    """Load and return input lines from input1.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input1.txt")
    
    try:
        with open(input_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input1.txt with your puzzle input.")
        return

def solve():
    grid: list[str] = load_input()
    ROWS, COLS = len(grid), len(grid[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    
    def check_surrounding(sr: int, sc: int) -> int:
        count = 0
        for dr, dc in dirs:
            r, c = sr + dr, sc + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if grid[r][c] == '@':
                    count += 1
        return count
                    
    total = 0    
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == '@' and check_surrounding(r, c) < 4:
                total += 1
    
    print(total)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    solve()
