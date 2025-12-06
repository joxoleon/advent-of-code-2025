#!/usr/bin/env python3
"""Advent of Code 2025 - Day 06 Part 1"""

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

def load_matrix():
    matrix = []
    for line in load_input():
        row = line.split()
        matrix.append(row)
    return matrix


def solve():
    matrix = load_matrix()
    start_time = os.times()
    R, C = len(matrix), len(matrix[0])
    total = 0
    for c in range(C):
        op = matrix[R - 1][c]
        res = 1 if op == '*' else 0 
        for r in range(R - 1):
            if op == '*':
                res *= int(matrix[r][c])
            else:
                res += int(matrix[r][c])
        total += res
    end_time = os.times()
    print(f"Time taken: {end_time.user - start_time.user} seconds")
    print(total)
            
            

if __name__ == "__main__":
    solve()
