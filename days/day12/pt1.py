#!/usr/bin/env python3
"""Advent of Code 2025 - Day 12 Part 1"""
from __future__ import annotations

import os
import time
   
def load_input() -> list[str]:
    """Load and return input lines from input1.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "input1.txt")
    
    # Load shapes from input file
    lines = []
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip("\n"))
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print("Please create input1.txt with your puzzle input.")
    return lines

class Shape:
    def __init__(self, grid: list[str]):
        self.grid = grid
        self.area = sum(row.count("#") for row in grid)
        self.orientations = self.generate_orientations()
        
    def generate_orientations(self) -> list[dict]:
        """Return all unique rotations and flips of the shape with precomputed cells."""
        def rotate(g: list[str]) -> list[str]:
            # transpose and reverse rows to rotate 90 degrees clockwise
            return [''.join(row) for row in zip(*g[::-1])]
        
        def flip(g: list[str]) -> list[str]:
            return [row[::-1] for row in g]
        
        seen = set()
        variants: list[dict] = []
        for base in (self.grid, flip(self.grid)):
            current = base
            for _ in range(4):
                key = tuple(current)
                if key not in seen:
                    seen.add(key)
                    cells = [(r, c) for r in range(len(current)) for c, val in enumerate(current[r]) if val == "#"]
                    variants.append(
                        {
                            "grid": current,
                            "cells": cells,
                            "height": len(current),
                            "width": len(current[0]) if current else 0,
                        }
                    )
                current = rotate(current)
        return variants

class Grid:
    def __init__(self, C: int, R: int, shape_counts: dict[int, int]):
        self.C = C
        self.R = R
        self.grid = [['.' for _ in range(C)] for _ in range(R)]
        self.shape_counts = shape_counts
    
    def can_place_cells(self, cells: list[tuple[int, int]], r: int, c: int) -> bool:
        for sr, sc in cells:
            nr, nc = r + sr, c + sc
            if nr < 0 or nc < 0 or nr >= self.R or nc >= self.C or self.grid[nr][nc] == "#":
                return False
        return True
    
    def place_cells(self, cells: list[tuple[int, int]], r: int, c: int):
        for sr, sc in cells:
            self.grid[r + sr][c + sc] = '#'
    
    def remove_cells(self, cells: list[tuple[int, int]], r: int, c: int):
        for sr, sc in cells:
            self.grid[r + sr][c + sc] = '.'
    
    def find_next_empty(self) -> tuple[int, int] | None:
        for r in range(self.R):
            for c in range(self.C):
                if self.grid[r][c] == '.':
                    return r, c
        return None
    
    def can_place_all_shapes(self, shapes_by_id: dict[int, Shape], remaining_counts: dict[int, int] | None = None) -> bool:
        if remaining_counts is None:
            remaining_counts = self.shape_counts.copy()
        if all(count == 0 for count in remaining_counts.values()):
            return True
        candidate_ids = [sid for sid, cnt in remaining_counts.items() if cnt > 0 and sid in shapes_by_id]
        candidate_ids.sort(key=lambda sid: (-shapes_by_id[sid].area, -remaining_counts[sid]))
        
        for shape_id in candidate_ids:
            shape = shapes_by_id[shape_id]
            remaining_counts[shape_id] -= 1
            for orient in shape.orientations:
                cells = orient["cells"]
                h, w = orient["height"], orient["width"]
                for r in range(self.R - h + 1):
                    for c in range(self.C - w + 1):
                        if self.can_place_cells(cells, r, c):
                            self.place_cells(cells, r, c)
                            if self.can_place_all_shapes(shapes_by_id, remaining_counts):
                                return True
                            self.remove_cells(cells, r, c)
            remaining_counts[shape_id] += 1
        return False
    


def solve():
    lines = load_input()
    split_idx = len(lines)
    for i in range(len(lines)-1, -1, -1):
        if lines[i] == "":
            split_idx = i
            break
    shape_lines = lines[:split_idx]
    grid_lines = lines[split_idx+1:]
    
    # Process shapes input
    shapes_by_id: dict[int, Shape] = {}
    i = 0
    while i < len(shape_lines):
        line = shape_lines[i].strip()
        if not line:
            i += 1
            continue
        if line.endswith(":"):
            try:
                shape_id = int(line[:-1])
            except ValueError:
                i += 1
                continue
            i += 1
            grid_rows: list[str] = []
            while i < len(shape_lines):
                row = shape_lines[i].strip()
                if not row or row.endswith(":"):
                    break
                grid_rows.append(row)
                i += 1
            if grid_rows:
                shapes_by_id[shape_id] = Shape(grid_rows)
            continue
        i += 1
    
    # Process grid input
    grids = []
    for line in grid_lines:
        if not line.strip():
            continue
        parts = line.split(":")
        C, R = map(int, parts[0].strip().split('x'))
        counts = list(map(int, parts[1].strip().split()))
        shape_counts = {shape_id: count for shape_id, count in enumerate(counts) if count > 0}
        grids.append(Grid(C, R, shape_counts))
    
    start_time = time.time()
    count = 0
    for grid in grids:
        print(f"Solving grid {grid.C}x{grid.R} with counts {grid.shape_counts}...")
        total_shape_area = sum(shapes_by_id[sid].area * cnt for sid, cnt in grid.shape_counts.items() if sid in shapes_by_id)
        if total_shape_area > grid.C * grid.R:
            print("  Skipping: shapes exceed grid area.")
            continue
        if grid.can_place_all_shapes(shapes_by_id):
            count += 1
    end_time = time.time()
    print(f"Solved in {end_time - start_time:.2f} seconds")
    print(count)
        
    
    

if __name__ == "__main__":
    solve()
