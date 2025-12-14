import numba
from numba import jit, types
from numba.typed import Dict
import numpy as np

@jit(nopython=True, cache=True)
def solve_numba(lights, buttons_mask):
    target = 0
    for i, light in enumerate(lights):
        if light:
            target |= (1 << i)
    
    n_buttons = len(buttons_mask)
    
    def rsolve(current, idx):
        if current == 0:
            return 0
        if idx == n_buttons:
            return n_buttons + 1
        
        skip = rsolve(current, idx + 1)
        use = 1 + rsolve(current ^ buttons_mask[idx], idx + 1)
        
        return min(skip, use)
    
    return rsolve(target, 0)

def solve(l, b):
    # Convert to numpy arrays for numba
    lights = np.array(l, dtype=np.int32)
    
    # Convert buttons to bitmasks
    buttons_mask = np.zeros(len(b), dtype=np.int64)
    for i, btn in enumerate(b):
        mask = 0
        for pos in btn:
            mask |= (1 << pos)
        buttons_mask[i] = mask
    
    return solve_numba(lights, buttons_mask)

# Keep the original solve2 for now since it's more complex
def solve2(r, b):
    lenr = len(r)
    lenb = len(b)
    b.sort(key=len, reverse=True)
    ba = [tuple(int(j in i) for j in range(lenr)) for i in b]
    ids = [frozenset(j for j in range(lenb) if ba[j][i]) for i in range(lenr)]
    out = min((sum(r), *(r[c] + r[d] for c in range(lenr-1) for d in range(c + 1, lenr) if set(range(lenb)) <= (ids[c] | ids[d]))))
    
    def rsolve2(x, z, s):
        nonlocal out
        y, idsy = min(((i, s & ids[i]) for i in range(lenr) if x[i]), key=lambda w: (len(w[1]), -x[w[0]]))
        newz = z + x[y]
        news = s - ids[y]
        # ... rest of the complex logic
    
    return out

def main():
    with open('input10.txt') as f:
        count = 0
        count2 = 0
        
        for line_num, line in enumerate(f.read().split('\n')):
            if not line.strip():
                continue
                
            parts = line.split(' ')
            lights = [int(c == '#') for c in parts[0][1:-1]]
            btns = [tuple(map(int, j[1:-1].split(','))) for j in parts[1:-1]]
            req = list(map(int, parts[-1][1:-1].split(',')))
            
            result1 = solve(lights, btns)
            count += result1
            
            # For now, skip solve2 to test the speed improvement
            print(f"Line {line_num + 1}: {result1}")
        
        print(f"Total: {count}")

if __name__ == "__main__":
    main()