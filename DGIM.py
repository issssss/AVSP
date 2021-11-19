import math
import sys
import time


def checkPretinci(pretinci, timeList, lenPretinaca):
    zaKoristenje = lenPretinaca.copy()
    for l in lenPretinaca:
        isteDuzine = zaKoristenje.get(l)
        if len(isteDuzine) > 2:
            isteDuzine.sort()
            prviPret = pretinci.get(isteDuzine[0])
            novi = set.union(prviPret, pretinci.get(isteDuzine[1]))
            pretinci.update({isteDuzine[1]: novi})
            pretinci.pop(isteDuzine[0])
            noviKljuc = 2 * l
            noviBr = []
            if noviKljuc in lenPretinaca.keys():
                noviBr = lenPretinaca.get(noviKljuc)
            noviBr.append(isteDuzine[1])
            timeList.pop(timeList.index(isteDuzine[0]))
            isteDuzine.pop(0)
            isteDuzine.pop(0)
            zaKoristenje.update({noviKljuc: noviBr})
            zaKoristenje.update({l: isteDuzine})
    return zaKoristenje


def deletePretinci(pretinci, timeList, lenPretinaca):
    zaKoristenje = lenPretinaca.copy()
    pretinci.pop(timeList[0])
    for l in lenPretinaca.keys():
        b = zaKoristenje.get(l)
        if timeList[0] in b:
            b.pop(0)
    timeList.pop(0)
    return pretinci, zaKoristenje


# dgim funkcija
def dgim(N, tok, pretinci, t, timeList, lenPretinaca):
    for bit in tok:
        if bit == 1:
            vrijed = set()
            vrijed.add(t)
            pretinci.update({t: vrijed})
            timeList.append(t)
            br = []
            if 1 in lenPretinaca.keys():
                br = lenPretinaca.get(1)
            br.append(t)
            lenPretinaca.update({1: br})
            lenPretinaca = checkPretinci(pretinci, timeList, lenPretinaca)
        keysList = list(pretinci.keys())
        if len(keysList) > 1:
            #print(keysList)
            if keysList[0] < (t - N + 2):
                #print(keysList[0])
                #print(keysList[-1])
                pretinci, lenPretinaca = deletePretinci(pretinci, keysList, lenPretinaca)
        t += 1
    return pretinci, t, lenPretinaca


# citanje datoteke
pocetno = time.time()
# tok = []
br = 0
N = 0
t = 0
q = 0
pretinci = {}
timeList = []
lenPretinaca = {}
#f = open("myfile.txt", "w")
for line in sys.stdin:
    if br == 0:
        N = int(line.strip())
        brojac = N
        br += 1
    elif "q" in line:
        z = -1
        q += 1
        upit = line.split(' ')
        k = int(upit[1].strip())
        # #print('k = ' +str(k))
        skoroz = t - k
        # #print(skoroz)
        keysList = list(pretinci.keys())
        keysList.sort()
        c = 0
        pretinciZaZbrojit = []
        for key in keysList:
            if key >= skoroz:
                if c == 0:
                    z = key
                    c += 1
                else:
                    pretinciZaZbrojit.append(key)
        brJed = 0
        if z != -1:
            for p in pretinciZaZbrojit:
                bits = pretinci.get(p)
                brJed += len(bits)
            bits = []
            bits = pretinci.get(z)
            brJed += math.floor(len(bits) / 2.0)
            print(brJed)
            #f.write(str(brJed) + '\n')
        else:
            print(0)
            #f.write(str(0) + '\n')

    else:
        novo = [int(i) for i in line.strip()]
        pretinci, t, lenPretinaca = dgim(N, novo, pretinci, t, timeList, lenPretinaca)

# #print(len(tok))

#print(time.time() - pocetno)
#f.close()
