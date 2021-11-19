import hashlib
import sys
import numpy as np

num_bits = 128
jedinkeHash = {}  # rjecnik koji sadrzi par jedinka:njezin md5 hash
hashBit = {}  # rjecnik koji sadrzi par md5 hash: maska binarnog oblika hasha


def simhash(tekst):
    sh = [0 for i in range(0, num_bits)]
    jedinke = generiraj_jedinke(tekst)

    for i in jedinke:

        if i in jedinkeHash.keys():
            hash = jedinkeHash.get(i)  # u slucaju da je jedinka vec bila obradena samo dohvati njezin hash i masku
            maska = hashBit.get(hash)
        else:
            hash = hashlib.md5(i.encode())  # u slucaju da nije provedi md5 kodiranje te napravi novu masku
            bits = bin(int(hash.hexdigest(), base=16))[2:].zfill(num_bits)
            jedinkeHash.update({i: hash})
            maska = [-1 if b == '0' else 1 for b in bits]  # maska koja predstavlja sto se treba dodati u sh (1 ce biti na mjestu bita 1 dok ce -1 biti na mjestu bita 0
            hashBit.update({hash: maska})

        sh = np.add(maska, sh)

    sazetak = ''.join([str(1) if i >= 0 else str(0) for i in sh])  # pretvaranje u zavrsni sazetak

    return sazetak


def generiraj_jedinke(text):
    return text.split(' ')


def HammingsDistance(bit1, bit2):
    return bin(int(bit1, 2) ^ int(bit2, 2)).count(
        '1')  # hammingova distanca dobivena bit1 xor bit2 te su preobrojane prezivjele jedinice


def hash2int(pojas, hash):  # podjela bitova na pojase, ovo je moglo biti ljepse izvedeno, ali sto je tu je
    if pojas == 1:
        a = 0
        b = 16
    elif pojas == 2:
        a = 16
        b = 32
    elif pojas == 3:
        a = 32
        b = 48
    elif pojas == 4:
        a = 48
        b = 64
    elif pojas == 5:
        a = 64
        b = 80
    elif pojas == 6:
        a = 80
        b = 96
    elif pojas == 7:
        a = 96
        b = 112
    else:
        a = 112
        b = 128
    return hash[a:b]


files = []  # lista svih datoteka

quests = []  # lista svih upita

hashs = []  # lista svih sazetaka datoteka, po indeksima se slazu

i = 0
for x in sys.stdin:
    i += 1
    if i - 1 == 0:
        N = x.strip()
    elif i == int(N) + 2:
        Q = x
    elif i > int(N) + 2:
        quests.append(x.strip())
    else:
        files.append(x.strip())

pairs = {}  # parovi datoteka: njezin sazetak
for i in range(len(files)):
    if files[
        i] in pairs.keys():  # provjeri ako slucajno imamo identicnu datoteku s nekom koja je vec prije bila na redu
        hashs.append(pairs[files[i]])
    else:
        has = simhash(files[i])
        hashs.append(has)
        pairs.update({files[i]: has})

# print('gotovo')
b = 8
kandidati = {}
for k in range(int(N)):
    kandidati.update({k: set()})

for i in range(1, b + 1):
    pretinci = {}
    for l in range(int(N)):
        pretinci.update({l: set()})
    for j in range(0, int(N)):
        hashi = hashs[j]
        val = hash2int(i, hashi)
        tekst_pretinac = []
        if pretinci.get(val):
            tekst_pretinac = pretinci.get(val)
            for tekst in tekst_pretinac:
                kandidati.get(j).add(tekst)
                kandidati.get(tekst).add(j)
        else:
            tekst_pretinac = set()
        tekst_pretinac.add(j)
        pretinci.update({val: tekst_pretinac})

for q in quests:
    sim = 0
    d = q.split()
    i = int(d[0])
    k = int(d[1])
    upit = hashs[i]
    lista = kandidati[i]
    for l in lista:
        raz = HammingsDistance(upit, hashs[l])
        if raz <= k:
            sim += 1
    print(sim)
