#!/usr/bin/env python3
"""Advent of Code 2025 - Day 04 Part 2"""
import os
from collections import deque

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
    count = 0
    
    def get_adj_paper_tiles(sr: int, sc: int) -> list[(int, int)]:
        adj: list[(int, int)] = []
        for dr, dc in dirs:
            r, c = sr + dr, sc + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if grid[r][c] == '@':
                    adj.append((r, c))
        return adj

    def print_grid():
        for row in grid:
            print(''.join(row))
        print()
                    
    queue = deque()
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == '@':
                adj = get_adj_paper_tiles(r, c)
                if len(adj) < 4:
                    queue.append((r, c))
    
    removed = 0
    while queue:
        r, c = queue.popleft()
        adj = get_adj_paper_tiles(r, c)
        if grid[r][c] == '@' and len(adj) < 4:
            grid[r][c] = 'x'
            removed += 1
            queue.extend(adj)
            # print_grid()
    
    print(removed)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    solve()

