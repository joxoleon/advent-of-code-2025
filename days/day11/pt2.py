#!/usr/bin/env python3
"""Advent of Code 2025 - Day 11 Part 2"""

import os
from typing import List
from collections import defaultdict

def load_input() -> List[str]:
    """Load and return input lines from input1.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input2.txt")
    
    lines = []
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip("\n"))
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input2.txt with your puzzle input.")
    return lines


def solve():
    lines = load_input()
    # Construct adj
    adj = defaultdict(list)
    for line in lines:
        parts = line.split(':')
        node_name = parts[0].strip()
        neighbors = parts[1].strip().split()
        for neighbor in neighbors:
            adj[node_name].append(neighbor)
    
    
    memo = {}
    def dfs(node: str, visited_fft: bool, visited_dac: bool) -> int:
        if (node, visited_fft, visited_dac) in memo:
            return memo[(node, visited_fft, visited_dac)]
        
        if node == "out":
            res = 1 if visited_fft and visited_dac else 0
            memo[(node, visited_fft, visited_dac)] = res
            return res
        if node == "fft":
            visited_fft = True
        if node == "dac":
            visited_dac = True
        out_count = 0
        
        for neigh in adj[node]:
            out_count += dfs(neigh, visited_fft, visited_dac)
        
        memo[(node, visited_fft, visited_dac)] = out_count
        return out_count

    print(dfs("svr", False, False))
    
        

if __name__ == "__main__":
    solve()
