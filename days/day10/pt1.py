#!/usr/bin/env python3
"""Advent of Code 2025 - Day 10 Part 1"""

import os
from typing import List, Tuple
from collections import deque
import heapq
import math

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

def process_machine_input(line: str) -> Tuple[int, int, List[int], List[int]]:
    """Process a single line of input for the machine"""
    # This is definitely the worst input format I've ever seen and the ugliest code I've ever written.
    # Example line:
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    # [.##.] Indicator lights - extract the string between the brackets
    bracket_start = line.find('[')
    bracket_end = line.find(']')
    
    ind_light_target_str = line[bracket_start + 1:bracket_end]
    ind_light_target_binary = 0
    for c in line[bracket_start + 1:bracket_end]:
        ind_light_target_binary <<= 1
        if c == '#':
            ind_light_target_binary += 1
    
    # Button presses - extract the numbers in parentheses
    buttons = []
    button_strs = line.split()[1:-1]  # Skip the first and last parts
    for bstr in button_strs:
        bnums = bstr.strip('()').split(',')
        buttons.append(list(int(num) for num in bnums))
    
    button_transitions_binary = []
    num_lights = len(ind_light_target_str)
    for b in buttons:
        # (3) -> turns into 0001, (1,3) -> turns into 0101
        # Pressing a button turns the numbered lights on from left to right in the binary representation
        transition = 0
        for num in b:
            transition |= 1 << (num_lights - 1 - num)
        button_transitions_binary.append(transition)
    
    # Joltage ratings - extract the numbers in curly braces
    curly_start = line.find('{')
    curly_end = line.find('}')
    joltage_ratings = list(int(num) for num in line[curly_start + 1:curly_end].split(','))

    return num_lights, ind_light_target_binary, button_transitions_binary, joltage_ratings

def min_button_presses_for_machine(num_lights: int, ind_light_target_binary: int, button_transitions_binary: List[int], joltage_ratings: List[int]) -> int:
    dst = [-1 for _ in range(2 ** num_lights)]
    dst[0] = 0
    heap = [(0, 0)] # cnt, node
    
    while heap:
        count, node = heapq.heappop(heap)
        if node == ind_light_target_binary:
            return count
        for b in button_transitions_binary:
            next_node = node ^ b
            if dst[next_node] == -1 or dst[next_node] > count + 1:
                dst[next_node] = count + 1
                heapq.heappush(heap, (count + 1, next_node))
    return -1
    

def solve():
    """Solve Part 1"""
    total_presses = 0
    for line in load_input():
        total_presses += min_button_presses_for_machine(*process_machine_input(line))
    print(total_presses)

if __name__ == "__main__":
    solve()
