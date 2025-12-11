#!/usr/bin/env python3
import bisect
from collections import defaultdict
import os

# ------------------------------------------------------------
# READ INPUT
# ------------------------------------------------------------

def read_points():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "input2.txt")
    
    pts = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            x, y = map(int, line.split(","))
            pts.append((x, y))
    return pts


# ------------------------------------------------------------
# BUILD ORTHOGONAL POLYGON EDGES
# pts are TILE coordinates, but polygon edges run on the grid lines.
# ------------------------------------------------------------

def build_edges(pts):
    n = len(pts)
    edges = []
    for i in range(n):
        x1,y1 = pts[i]
        x2,y2 = pts[(i+1)%n]
        if x1 == x2:
            # vertical edge at x = x1, from y1 to y2
            if y1 < y2:
                edges.append(("V", x1, y1, y2))
            else:
                edges.append(("V", x1, y2, y1))
        else:
            # horizontal edge at y = y1, from x1 to x2
            if x1 < x2:
                edges.append(("H", y1, x1, x2))
            else:
                edges.append(("H", y1, x2, x1))
    return edges


# ------------------------------------------------------------
# SCANLINE FILL (VERTEX-SPACE → TILE-SPACE)
#
# For vertical edge x, y1→y2:
#   scanlines intersect at rows y = y1..y2-1
#   The interior tiles run from x = L..R-1
#
# IMPORTANT:
#   The bottommost tile row (max_y) must be copied from (max_y-1)
#   because tile-space is one unit bigger than vertex-space scanlines.
# ------------------------------------------------------------

def build_row_spans(edges):
    raw = defaultdict(list)

    # Collect raw intersections (vertex-space)
    for typ, x, y1, y2 in edges:
        if typ == "V":
            for y in range(y1, y2):
                raw[y].append(x)

    rowSpans = {}

    # Pair intersections → interior spans
    for y, xs in raw.items():
        xs.sort()
        intervals = []
        for i in range(0, len(xs), 2):
            L = xs[i]
            R = xs[i+1]
            # tile x ∈ [L .. R-1]
            intervals.append((L, R-1))
        rowSpans[y] = intervals

    # FIX: Add missing final tile row
    if rowSpans:
        ys = sorted(rowSpans.keys())
        last = ys[-1]
        if last+1 not in rowSpans:
            # copy last row's spans
            rowSpans[last+1] = rowSpans[last]

    return rowSpans


def build_col_spans(edges):
    raw = defaultdict(list)

    # Collect raw intersections
    for typ, y, x1, x2 in edges:
        if typ == "H":
            for x in range(x1, x2):
                raw[x].append(y)

    colSpans = {}

    for x, ys in raw.items():
        ys.sort()
        intervals = []
        for i in range(0, len(ys), 2):
            T = ys[i]
            B = ys[i+1]
            # tile y ∈ [T .. B-1]
            intervals.append((T, B-1))
        colSpans[x] = intervals

    # FIX: Add missing final tile column
    if colSpans:
        xs = sorted(colSpans.keys())
        last = xs[-1]
        if last+1 not in colSpans:
            colSpans[last+1] = colSpans[last]

    return colSpans


# ------------------------------------------------------------
# CONTAINMENT CHECK
# ------------------------------------------------------------

def interval_inside(intervals, L, R):
    """Check if [L,R] is completely inside one of the intervals."""
    i = bisect.bisect_right(intervals, (L, float('inf'))) - 1
    if i < 0:
        return False
    L1, R1 = intervals[i]
    return (L >= L1 and R <= R1)


def rect_inside(rowSpans, colSpans, x1, y1, x2, y2):
    """Check if rectangle with opposite corners in tile-space is inside polygon."""
    xL, xR = sorted((x1, x2))
    yT, yB = sorted((y1, y2))

    # top row
    top = rowSpans.get(yT)
    if not top or not interval_inside(top, xL, xR):
        return False

    # bottom row
    bot = rowSpans.get(yB)
    if not bot or not interval_inside(bot, xL, xR):
        return False

    # left column
    left = colSpans.get(xL)
    if not left or not interval_inside(left, yT, yB):
        return False

    # right column
    right = colSpans.get(xR)
    if not right or not interval_inside(right, yT, yB):
        return False

    return True


# ------------------------------------------------------------
# RED POINT MAPS
# ------------------------------------------------------------

def build_red_maps(pts):
    reds_by_row = defaultdict(list)
    reds_by_col = defaultdict(list)
    for x, y in pts:
        reds_by_row[y].append(x)
        reds_by_col[x].append(y)
    for y in reds_by_row:
        reds_by_row[y].sort()
    for x in reds_by_col:
        reds_by_col[x].sort()
    return reds_by_row, reds_by_col


# ------------------------------------------------------------
# MAIN SOLVER
# ------------------------------------------------------------

def solve(pts):
    edges = build_edges(pts)
    rowSpans = build_row_spans(edges)
    colSpans = build_col_spans(edges)

    reds_by_row, reds_by_col = build_red_maps(pts)
    all_rows = sorted(reds_by_row.keys())

    best = 0
    R = len(all_rows)

    # Compare every pair of rows containing red tiles
    for i in range(R):
        y1 = all_rows[i]
        xs1 = reds_by_row[y1]

        for j in range(i+1, R):
            y2 = all_rows[j]
            height = y2 - y1

            # prune (even square wouldn't beat best)
            if height * height <= best:
                continue

            xs2 = reds_by_row[y2]

            # 2-pointer merge for x's across rows
            p = q = 0
            while p < len(xs1) and q < len(xs2):
                x1 = xs1[p]
                x2 = xs2[q]

                if x1 == x2:
                    # thin rectangle (width = 0 or 1)
                    area = height * 1
                    if area > best and rect_inside(rowSpans, colSpans, x1, y1, x2, y2):
                        best = area
                    p += 1
                    q += 1
                elif x1 < x2:
                    p += 1
                else:
                    q += 1

            # try wide rectangles
            p = q = 0
            while p < len(xs1) and q < len(xs2):
                x1 = xs1[p]

                while q < len(xs2) and xs2[q] < x1:
                    q += 1
                if q < len(xs2):
                    x2 = xs2[q]
                    width = x2 - x1
                    area = width * height

                    if area > best and rect_inside(rowSpans, colSpans, x1, y1, x2, y2):
                        best = area

                p += 1

    return best


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    pts = read_points()
    print(solve(pts))
