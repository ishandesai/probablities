from fractions import Fraction as Fr

def SM(i, j):
    g = gcd(i, j)
    return Fr(int(i/g), int(j/g))

def CP(TM,I):
    tm = []
    for i in range(len(TM)):
        tm.append([])
        em = []
        for j in range(len(TM)):
            if j not in I:
                tm[i].append(TM[i][j])
            else:
                em.append(TM[i][j])
        tm[i].extend(em)
    return tm

def change_prob(m):
    S = list(map(sum, m))
    B = list(map(lambda x: x == 0, S))
    I = set([i for i, x in enumerate(B) if x])
    NM = []
    for i in range(len(m)):
        NM.append(list(map(lambda x: Fr(0, 1) if(S[i] == 0) else SM(x, S[i]), m[i])))
    TM = []
    ZM = []
    for i in range(len(NM)):
        if i not in I:
            TM.append(NM[i])
        else:
            ZM.append(NM[i])
    TM.extend(ZM)
    tm = CP(TM,I)
    return [tm, len(ZM)]

def CM(m):
    cm = []
    for i in range(len(m)):
        cm.append([])
        for j in range(len(m[i])):
            cm[i].append(Fr(m[i][j].numerator, m[i][j].denominator))
    return cm

def QR_decompose(m, LR):
    LQ, Q, R = len(m)-LR, [], []
    for i in range(LQ):
        Q.append([int(i==j)-m[i][j] for j in range(LQ)])
        R.append(m[i][LQ:])
    return [Q, R]

def gcd(i, j):
    def use(i, j):
        if j == 0:
            return i
        return use(j, i%j)
    return use(abs(i), abs(j))

def lcm(i, j):
    return int(i*j/gcd(i,j))

def OUT(m,val):
    out = [0 for i in range(len(m))]
    for i in range(len(m)):
        idx = len(m) -1 -i
        end = len(m) - 1
        while end > idx:
            val[idx] -= m[idx][end] * out[end]
            end -= 1
        out[idx] = val[idx]/m[idx][idx]
    return out

def GM(m, val):
    mat = CM(m)
    for i in range(len(mat)):
        idx = -1
        for j in range(i, len(mat)):
            if mat[j][i].numerator != 0:
                idx = j
                break
        if idx == -1:
            raise ValueError('GM failed!')
        mat[i], mat[idx] = mat[idx], mat[j]
        val[i], val[idx] = val[idx], val[i]
        for j in range(i+1, len(mat)):
            if mat[j][i].numerator == 0:
                continue
            ratio = -mat[j][i]/mat[i][i]
            for k in range(i, len(mat)):
                mat[j][k] += ratio * mat[i][k]
            val[j] += ratio * val[i]
    return OUT(mat,val)

def REV(m):
    tm = []
    for i in range(len(m)):
        for j in range(len(m)):
            if i == 0:
                tm.append([])
            tm[j].append(m[i][j])
    mrev = []
    for i in range(len(tm)):
        val = [Fr(int(i==j), 1) for j in range(len(m))]
        mrev.append(GM(tm, val))
    return mrev

def MM(m1, m2):
    r = []
    for i in range(len(m1)):
        r.append([])
        for j in range(len(m2[0])):
            r[i].append(Fr(0, 1))
            for k in range(len(m1[0])):
                r[i][j] += m1[i][k] * m2[k][j]
    return r

def solution(m):
    ans = change_prob(m)
    if ans[1] == len(m):
        return [1, 1]
    Q, R = QR_decompose(*ans)
    rev = REV(Q)
    ans = MM(rev, R)
    r = ans[0]
    l = 1
    for i in r:
        l = lcm(l, i.denominator)
    ans = list(map(lambda x: int(x.numerator*l/x.denominator), r))
    ans.append(l)
    return ans


m1 = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

m2 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

print(solution(m1))
print(solution(m2))
