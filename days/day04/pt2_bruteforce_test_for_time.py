#!/usr/bin/env python3
"""Advent of Code 2025 - Day 04 Part 2 - Brute Force Version"""
import os

def load_input() -> list[list[str]]:
    """Load and return input lines from input2.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input2.txt")
    
    try:
        with open(input_path, "r") as file:
            # Split each line into a list of characters for mutability
            return [list(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input2.txt with your puzzle input.")
        return

def solve():
    grid: list[list[str]] = load_input()
    ROWS, COLS = len(grid), len(grid[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def count_adj_paper_tiles(sr: int, sc: int) -> int:
        count = 0
        for dr, dc in dirs:
            r, c = sr + dr, sc + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if grid[r][c] == '@':
                    count += 1
        return count

    def print_grid():
        for row in grid:
            print(''.join(row))
        print()
    
    # Compute start time
    start_time = os.times()
    removed = 0
    changed = True
    
    # Keep iterating until no more changes happen
    while changed:
        changed = False
        # Scan entire grid each iteration
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == '@':
                    adj_count = count_adj_paper_tiles(r, c)
                    if adj_count < 4:
                        grid[r][c] = 'x'
                        removed += 1
                        changed = True
                        # print_grid()  # Uncomment to see step-by-step
    
    end_time = os.times()
    print(f"Time taken: {end_time.user - start_time.user} seconds")
    print(removed)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    solve()

