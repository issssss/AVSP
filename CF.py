import sys
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def cos_sl(Y, X):
    s = 0
    sx = 0
    sy = 0
    for i in range(len(Y)):
        s += (Y[i]*X[i])
        sx += (X[i]*X[i])
        sy += (Y[i]*Y[i])

    return s/np.sqrt(sx*sy)


def col_fil(mat, i, j, K, ocj):
    x = 0
    slicnosti = []
    for ret in mat:
        slicnosti.append(cos_sl(ret, mat[i-1]))

    najsl = sorted(range(len(slicnosti)), key=lambda el: slicnosti[el], reverse=True)

    dij = 0
    for n in najsl:
        if slicnosti[n] <= 0 or ocj[n][j-1] == -10 or n == i-1:
            continue
        x += ocj[n][j-1]*slicnosti[n]
        dij += slicnosti[n]
        K -= 1
        if K == 0:
            break


    return x/dij

item_user = []
i = 0
upiti = []
for u in sys.stdin:
    s = [-10 if el.strip() == 'X' else int(el.strip()) for el in u.split(' ')]
    if i == 0:
        N = int(s[0])
        M = int(s[1])
    elif i <= N:
        item_user.append(s)
    elif i == N+1:
        Q = int(u)
    else:
        upiti.append(s)

    i += 1

item_item = [] #item_user.copy()
user_user = [] #np.transpose(item_user.copy())

for r in item_user:
    s = 0
    i = 0
    for e in r:
        if e != -10:
            s += e
            i += 1
    avrg = float(s) / i
    no = []
    for e in r:
        if e != -10:
            e = e - avrg
            #print(e)
        else:
            e = 0
        no.append(e)
    item_item.append(no)

for r in np.transpose(item_user):
    i = 0
    s = 0
    for e in r:
        if e != -10:
            s += e
            i += 1
    avrg = float(s) / i
    no = []
    for e in r:
        if e != -10:
            e = e - avrg
            #print(e)
        else:
            e = 0
        no.append(e)

    user_user.append(no)

#f = open("myfile.txt", "w")
for u in upiti:
    if u[2] == 1:
        n = col_fil(user_user, u[1], u[0], u[3], np.transpose(item_user))
    else:
        n = col_fil(item_item, u[0], u[1], u[3], item_user)

    h = Decimal(Decimal(n).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))
    print(h)
    #f.write(str(h)+ "\n")
