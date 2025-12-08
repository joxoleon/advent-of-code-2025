#!/usr/bin/env python3
"""Advent of Code 2025 - Day 08 Part 2"""

import os
import heapq

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

def load_lines():
    lines = []
    for line in load_input():
        str_line = line.split(",")
        lines.append([int(x) for x in str_line])
    return lines

# Union find with path compression
class UnionFind:
    def __init__(self, size):
        self.parent = [i for i in range(size)]
        self.rank = [1] * size
        self.size = [1] * size
        self.num_components = size
    
    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]
    
    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP != rootQ:
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
                self.size[rootP] += self.size[rootQ]
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
                self.size[rootQ] += self.size[rootP]
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
                self.size[rootP] += self.size[rootQ]
            self.num_components -= 1
    
    def get_component_sizes(self):
        sizes = [self.size[i] for i in range(len(self.size)) if self.parent[i] == i]
        return sizes
    

def solve():
    lines = load_lines()
    total = 0
    heap = []
    # Precompte distances and place them in a heap
    for i in range(len(lines)):
        x1, y1, z1 = lines[i]
        for j in range(i + 1, len(lines)):
            x2, y2, z2 = lines[j]
            dist = abs(x1 - x2) * abs(x1 - x2) + abs(y1 - y2) * abs(y1 - y2) + abs(z1 - z2) * abs(z1 - z2)
            heapq.heappush(heap, (dist, i, j))
    
    heapq.heapify(heap)
    uf = UnionFind(len(lines))
    
    i, j = 0,0
    while uf.num_components > 1:
        dist, i, j = heapq.heappop(heap)
        uf.union(i, j)
    res = lines[i][0] * lines[j][0]
    print(res)
    
        

if __name__ == "__main__":
    solve()
