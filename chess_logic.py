
def is_white(p): return p.isupper()
def clone(b): return [r[:] for r in b]

def king_pos(b, w):
    k = "K" if w else "k"
    for r in range(8):
        for c in range(8):
            if b[r][c] == k:
                return r, c

def in_bounds(r,c): return 0<=r<8 and 0<=c<8

def moves(b,r,c):
    p=b[r][c]; res=[]
    d=-1 if is_white(p) else 1

    def add(rr,cc):
        if in_bounds(rr,cc):
            if b[rr][cc]=="" or is_white(b[rr][cc])!=is_white(p):
                res.append((rr,cc))

    if p.lower()=="p":
        if in_bounds(r+d,c) and b[r+d][c]=="":
            add(r+d,c)
        for dc in (-1,1):
            if in_bounds(r+d,c+dc) and b[r+d][c+dc]!="":
                add(r+d,c+dc)

    if p.lower() in "rq":
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            rr,cc=r+dr,c+dc
            while in_bounds(rr,cc):
                if b[rr][cc]=="":
                    res.append((rr,cc))
                else:
                    if is_white(b[rr][cc])!=is_white(p):
                        res.append((rr,cc))
                    break
                rr+=dr; cc+=dc

    if p.lower() in "bq":
        for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
            rr,cc=r+dr,c+dc
            while in_bounds(rr,cc):
                if b[rr][cc]=="":
                    res.append((rr,cc))
                else:
                    if is_white(b[rr][cc])!=is_white(p):
                        res.append((rr,cc))
                    break
                rr+=dr; cc+=dc

    if p.lower()=="n":
        for dr,dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
            add(r+dr,c+dc)

    if p.lower()=="k":
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr or dc:
                    add(r+dr,c+dc)

    return res

def check(b,w):
    kr,kc=king_pos(b,w)
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p and is_white(p)!=w:
                if (kr,kc) in moves(b,r,c):
                    return True
    return False

def mate(b,w):
    if not check(b,w): return False
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p and is_white(p)==w:
                for mr,mc in moves(b,r,c):
                    nb=clone(b)
                    nb[mr][mc]=nb[r][c]
                    nb[r][c]=""
                    if not check(nb,w):
                        return False
    return True
