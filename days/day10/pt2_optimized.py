import functools

def solve(l, b):
    l = sum(j << c for c, j in enumerate(l))
    b = [sum((1 << j) for j in i) for i in b]
    
    @functools.lru_cache(maxsize=None)
    def rsolve(l, idx=0):
        if l == 0: return 0
        if idx == len(b): return len(b) + 1
        return min(rsolve(l, idx + 1), 1 + rsolve(l ^ b[idx], idx + 1))
    
    return rsolve(l)

def solve2(r, b):
    lenr = len(r)
    lenb = len(b)
    b.sort(key=len, reverse=True)
    ba = [tuple(int(j in i) for j in range(lenr)) for i in b]
    ids = [frozenset(j for j in range(lenb) if ba[j][i]) for i in range(lenr)]
    out = min((sum(r), *(r[c] + r[d] for c in range(lenr-1) for d in range(c + 1, lenr) if set(range(lenb)) <= (ids[c] | ids[d]))))
    
    def poss(s, n, B, x, idx=0):
        if s == 0: yield x; return
        Bidx0, Bidx1 = B[idx]
        g = (min(x[k] for k in B[j][1]) for j in range(idx, len(B)))
        upper = min(next(g), *(x[k] for k in Bidx1))
        if n == 1:
            if s <= upper: yield tuple(x[k] - s*Bidx0[k] for k in range(len(x)))
        else:
            lower = max(0, s - sum(g))
            for i in range(min(s, upper), lower-1, -1):
                for j in poss(s - i, n - 1, B, tuple(x[k] - i*Bidx0[k] for k in range(len(x))), idx + 1): yield j
    
    def rsolve2(x, z, s):
        nonlocal out
        y, idsy = min(((i, s & ids[i]) for i in range(lenr) if x[i]), key=lambda w: (len(w[1]), -x[w[0]]))
        newz = z + x[y]
        news = s - ids[y]
        for a in poss(x[y], len(idsy), [(ba[j], b[j]) for j in idsy], x):
            ids2a = {frozenset(): 0}
            if any(ids2a.setdefault(news & ids[i], a[i]) != a[i] for i in range(lenr)): continue
            if (Z:=newz + max(vals := ids2a.values())) >= out: continue
            if len(ids2a) <= 2 or not any(vals): out = Z; continue
            rsolve2(a, newz, news)
    rsolve2(r, 0, frozenset(range(lenb)))
    return out

def main():
    with open('input10.txt') as f:
        count = 0   
        count2 = 0
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
        print(f"Processing {len(lines)} lines...")
        
        for line_num, line in enumerate(lines, 1):
            l = line.split(' ')
            lights = [int(c == '#') for c in l[0][1:-1]]
            btns = [tuple(map(int, j[1:-1].split(','))) for j in l[1:-1]]
            req = list(map(int, l[-1][1:-1].split(',')))
            
            result1 = solve(lights, btns)
            result2 = solve2(req, btns)
            
            count += result1
            count2 += result2
            
            if line_num % 10 == 0:  # Progress update every 10 lines
                print(f"Processed {line_num}/{len(lines)} lines. Current totals: {count}, {count2}")

        print(f"Final results:")
        print(f"Part 1: {count}")
        print(f"Part 2: {count2}")

if __name__ == "__main__":
    import time
    start = time.time()
    main()
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")