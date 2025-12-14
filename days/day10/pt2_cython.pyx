# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import cython
from libc.stdio cimport printf

@cython.boundscheck(False)
@cython.wraparound(False)
def solve(list l, list b):
    cdef long long l_mask = sum(j << c for c, j in enumerate(l))
    cdef list b_masks = [sum((1 << j) for j in i) for i in b]
    cdef int b_len = len(b_masks)
    
    def rsolve(long long l_val, int idx=0):
        if l_val == 0: 
            return 0
        if idx == b_len: 
            return b_len + 1
        return min(rsolve(l_val, idx + 1), 1 + rsolve(l_val ^ b_masks[idx], idx + 1))
    
    return rsolve(l_mask)

def poss(int s, int n, list B, tuple x, int idx=0):
    if s == 0: 
        yield x
        return
    
    Bidx0, Bidx1 = B[idx]
    g = (min(x[k] for k in B[j][1]) for j in range(idx, len(B)))
    upper = min(next(g), *(x[k] for k in Bidx1))
    
    if n == 1:
        if s <= upper: 
            yield tuple(x[k] - s*Bidx0[k] for k in range(len(x)))
    else:
        lower = max(0, s - sum(g))
        for i in range(min(s, upper), lower-1, -1):
            for j in poss(s - i, n - 1, B, tuple(x[k] - i*Bidx0[k] for k in range(len(x))), idx + 1): 
                yield j

@cython.boundscheck(False)
@cython.wraparound(False)
def solve2(list r, list b):
    cdef int lenr = len(r)
    cdef int lenb = len(b)
    
    b.sort(key=len, reverse=True)
    ba = [tuple(int(j in i) for j in range(lenr)) for i in b]
    ids = [frozenset(j for j in range(lenb) if ba[j][i]) for i in range(lenr)]
    out = min((sum(r), *(r[c] + r[d] for c in range(lenr-1) for d in range(c + 1, lenr) if set(range(lenb)) <= (ids[c] | ids[d]))))
    
    def rsolve2(x, z, s):
        nonlocal out
        y, idsy = min(((i, s & ids[i]) for i in range(lenr) if x[i]), key=lambda w: (len(w[1]), -x[w[0]]))
        newz = z + x[y]
        news = s - ids[y]
        for a in poss(x[y], len(idsy), [(ba[j], b[j]) for j in idsy], x):
            ids2a = {frozenset(): 0}
            if any(ids2a.setdefault(news & ids[i], a[i]) != a[i] for i in range(lenr)): 
                continue
            if (Z:=newz + max(vals := ids2a.values())) >= out: 
                continue
            if len(ids2a) <= 2 or not any(vals): 
                out = Z
                continue
            rsolve2(a, newz, news)
    
    rsolve2(r, 0, frozenset(range(lenb)))
    return out

def main():
    cdef int count = 0
    cdef int count2 = 0
    cdef int c = 0
    
    with open('input10.txt') as f:
        for i in f.read().split('\n')[c:]:
            if not i.strip():
                continue
            l = i.split(' ')
            lights = [int(i == '#') for i in l[0][1:-1]]
            btns = [tuple(map(int, j[1:-1].split(','))) for j in l[1:-1]]
            req = list(map(int, l[-1][1:-1].split(',')))
            
            count += solve(lights, btns)
            count2 += solve2(req, btns)
            c += 1
    
    print(count)
    print(count2)