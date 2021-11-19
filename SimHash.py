import hashlib
import sys
import numpy as np

num_bits = 128
jedinkeHash = {}
hashBit = {}
def simhash(tekst):
    sh = [0 for i in range(num_bits)]
    jedinke = generiraj_jedinke(tekst)

    for i in jedinke:


        if i in jedinkeHash.keys():
            hash = jedinkeHash.get(i) #u slucaju da je jedinka vec bila obradena samo dohvati njezin hash i masku
            maska = hashBit.get(hash)
        else:
            hash = hashlib.md5(i.encode()) #u slucaju da nije provedi md5 kodiranje te napravi novu masku
            bits = bin(int(hash.hexdigest(), base=16))[2:].zfill(num_bits)
            jedinkeHash.update({i: hash})
            maska = [1 if b == '1' else -1 for b in bits] #maska koja predstavlja sto se treba dodati u sh (1 ce biti na mjestu bita 1 dok ce -1 biti na mjestu bita 0
            hashBit.update({hash: maska})

        sh = np.add(maska, sh)

    rijec = ''.join([str(1) if i >= 0 else str(0) for i in sh])
   # for j in range(len(sh)):
    #    if sh[j] >= 0:
     #       rijec += str(1)
      #  else:
       #     rijec += str(0)
    return rijec


def generiraj_jedinke(text):
    return text.split(' ')

def HammingsDistance(bit1, bit2):
   return bin(int(bit1, 2) ^ int(bit2,2)).count('1')


files = []
quests = []
i = 0
for x in sys.stdin:
    i += 1
    if i - 1 == 0:
        N = x.strip()
    elif i == int(N)+2:
        Q = x
    elif i > int(N)+2:
        quests.append(x.strip())
    else:
        files.append(x.strip())

hashs = {}
for i in range(len(files)):
    hashs.update({i: simhash(files[i])})

for q in quests:
    sim = 0
    d = q.split()
    i = int(d[0])
    k = int(d[1])
    upit = hashs.get(i)
    for j in range(0, int(N)):
        if j == i:
            continue
        raz = HammingsDistance(upit, hashs.get(j))
        if raz <= k:
            sim += 1
    print(sim)

