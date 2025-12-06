#!/usr/bin/env python3
"""Advent of Code 2025 - Day 06 Part 2"""

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

def load_rows():
    rows = []
    for line in load_input():
        rows.append(line)
    return rows

def solve():
    matrix = load_rows()
    R, C = len(matrix), len(matrix[0])
    op = matrix[R - 1][0]
    total = 0
    stack = []
    for c in range(C):
        num = 0
        for r in range(R - 1):
            digit = matrix[r][c]
            if digit != ' ':
                num = num * 10 + int(digit)
        if num != 0:
            stack.append(num)
        else:
            # We are sure that if the num of the row is zero - we are reaching the next OP
            # In this moment we are performing the operations
            print(f"We are performing op: {op} on nums: {stack}")
            res = 1 if op == '*' else 0
            if op == '*':
                for num in stack:
                    res *= num
            else:
                res = sum(stack)

            print(res)
            print("")
            
            # We are now supposed to clear the stack and fetch new op and add the result
            stack = []
            op = matrix[R - 1][c + 1]
            total += res
    
    # And pick up the last nums
    res == 0
    if op == '*':
        res = 1
        for num in stack:
            res *= num
    else:
        res = sum(stack)
    total += res
    print(total)
                
        
        
        
            
        
if __name__ == "__main__":
    solve()
