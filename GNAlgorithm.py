import sys
from decimal import Decimal, ROUND_HALF_UP
import copy

zast = 0
naj = 0
veze = set()
svojstva = {}
graf = {}
vrhovi = set()
for s in sys.stdin:
    if s.isspace():
        zast = 1
        continue
    if zast == 0:
        vrhs = s.split()
        veze.add(s.strip())
        vrh1 = int(vrhs[0])
        vrh2 = int(vrhs[1])
        if vrh1 not in graf.keys():
            graf.update({vrh1: set()})

        spojeni = graf.get(vrh1)
        spojeni.add(vrh2)
        if vrh2 not in graf.keys():
            graf.update({vrh2: set()})
        spojeni = graf.get(vrh2)
        spojeni.add(vrh1)
        vrhovi.add(vrh1)
        vrhovi.add(vrh2)
    else:
        spl = s.split(' ')
        vektsv = [int(spl[i]) for i in range(len(spl)) if spl[i] != '\n']
        naj = len(vektsv[1:])
        svojstva.update({vektsv[0]: vektsv[1:]})
        if vektsv[0] not in vrhovi:
            vrhovi.add(vektsv[0])
            graf.update({vektsv[0]: set()})

tezine = {}
for par in veze:
    partneri = par.split(' ')
    svoj1 = svojstva.get(int(partneri[0]))
    svoj2 = svojstva.get(int(partneri[1]))
    slicnost = [svoj1[i] ^ svoj2[i] for i in range(len(svoj1))].count(0)
    tezine.update({par: slicnost})

for brid in tezine:
    tezina = tezine.get(brid)
    tezina = naj - (tezina - 1)
    tezine.update({brid: tezina})


def nadiSvePuteve(bridovi, trenutni, posjeceno, sviPutovi):
    posjeceno.append(trenutni)
    if trenutni in bridovi.keys():
        for vrh in bridovi.get(trenutni):
            if vrh not in posjeceno:
                nadiSvePuteve(bridovi, vrh, posjeceno.copy(), sviPutovi)
    sviPutovi.append(posjeceno)


def najkraciPut(pocetni, krajnji, graf, tezine, centralnosti):
    sviPutovi = []
    nadiSvePuteve(graf, pocetni, [], sviPutovi)
    najkraci = 100000
    N = 0
    najkraciPutovi = []
    for put in sviPutovi:
        tez = 0
        i = 0
        prijasnji = put[0]
        for dio in put:
            if 0 < i < len(put) and prijasnji != dio:
                kljuc = str(prijasnji) + ' ' + str(dio)
                if kljuc not in tezine.keys():
                    kljuc = str(dio) + ' ' + str(prijasnji)

                t = tezine.get(kljuc)
                tez += t
            i += 1
            prijasnji = dio
        if najkraci > tez and pocetni in put and krajnji in put:
            najkraci = tez
            najkraciPutovi.clear()
            N = 1
            najkraciPutovi.append(put)
        elif najkraci == tez and pocetni in put and krajnji in put:
            najkraciPutovi.append(put)
            N += 1
    if N > 0:
        for kratak in najkraciPutovi:
            i = 0
            for dio in kratak:
                if 0 < i < len(kratak) and prijasnji != dio:
                    kljuc = str(prijasnji) + ' ' + str(dio)
                    if kljuc not in tezine.keys():
                        kljuc = str(dio) + ' ' + str(prijasnji)
                    if kljuc in centralnosti.keys():
                        cent = centralnosti.get(kljuc)
                    else:
                        cent = 0
                    cent += Decimal(Decimal(1 / N).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
                    h = Decimal(Decimal(cent).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
                    centralnosti.update({kljuc: h})
                i += 1
                prijasnji = dio
    return centralnosti


def izracunajCentralnosti(vrhovi, graf, tezine):
    centralnosti = {}
    parovi = []
    for vrh1 in vrhovi:
        if len(graf.get(vrh1)) == 0:
            continue
        for vrh2 in vrhovi:
            if vrh1 == vrh2 or str(vrh1) + str(vrh2) in parovi or str(vrh2) + str(vrh1) in parovi or len(
                    graf.get(vrh2)) == 0:
                continue
            najkraciPut(vrh1, vrh2, graf, tezine, centralnosti)
            parovi.append(str(vrh1) + str(vrh2))
            parovi.append(str(vrh2) + str(vrh1))
    return centralnosti


def sortiraj(set):
    dio = set.split(' ')
    el1 = int(dio[0])
    el2 = int(dio[1])
    return el1, el2


def nadiNajveceCentralnosti(centralnosti):
    najveca = 0
    bridovi = set()
    for kljuc in centralnosti.keys():
        cent = centralnosti.get(kljuc)
        dio = kljuc.split(' ')
        if int(dio[0]) > int(dio[1]):
            kljuc = dio[1] + ' ' + dio[0]
        else:
            kljuc = dio[0] + ' ' + dio[1]
        if cent > najveca:
            najveca = cent
            bridovi.clear()
            bridovi.add(kljuc)
        elif cent == najveca:
            bridovi.add(kljuc)

    return bridovi


def modularnost(tezine, vrhovi, graf, ukupne_tezine, m):
    Q = 0
    for vrh1 in vrhovi:
        sviPutovi = []
        nadiSvePuteve(graf, vrh1, [], sviPutovi)
        if vrh1 in ukupne_tezine.keys():
            ku = ukupne_tezine.get(vrh1)
        else:
            ku = 0
            continue
        for vrh2 in vrhovi:
            d = 0
            kljuc = str(vrh1) + ' ' + str(vrh2)
            if kljuc not in tezine.keys():
                kljuc = str(vrh2) + ' ' + str(vrh1)
            if kljuc in tezine.keys():
                Auv = tezine.get(kljuc)
            else:
                Auv = 0
            if vrh2 in ukupne_tezine.keys():
                kv = ukupne_tezine.get(vrh2)
            else:
                kv = 0
                continue
            if vrh1 != vrh2:
                for put in sviPutovi:
                    if vrh1 in put and vrh2 in put:
                        d = 1
                        break
            else:
                d = 1
            v = (Auv - (ku * kv) / (2 * m))
            h = Decimal(Decimal(v).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
            Q = Decimal(Decimal(Q + h * d).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
    Q /= (2*m)
    if Q < 0.00001:
        Q = 0
    return Decimal(Decimal(Q).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))


def GirvanNewman(graf, vrhoviOrg, tezineOrg):
    bridovi = graf.copy()
    vrhovi = vrhoviOrg.copy()
    tezine = copy.deepcopy(tezineOrg)
    mod = 0
    idealnaZajednice = {}
    m = 0
    ukupne_tezine = {}
    for clanovi in tezine:
        t = tezine.get(clanovi)
        m += t
        dva = clanovi.split(' ')
        prvi = int(dva[0])
        drugi = int(dva[1])
        if prvi in ukupne_tezine.keys():
            kt = ukupne_tezine.get(prvi)
        else:
            kt = 0
        kt += t
        ukupne_tezine.update({prvi: kt})
        if drugi in ukupne_tezine.keys():
            kt = ukupne_tezine.get(drugi)
        else:
            kt = 0
        kt += t
        ukupne_tezine.update({drugi: kt})

    while len(tezine) > 0:
        centralnosti = izracunajCentralnosti(vrhovi, bridovi, tezine)
        izbrisani_bridovi = nadiNajveceCentralnosti(centralnosti)
        n = modularnost(tezineOrg, vrhoviOrg, bridovi, ukupne_tezine, m)
        #print('MODULARITY ' + str(n))
        # f.write('MODULARITY '+str(n)+'\n')
        if n > mod:
            mod = n
            idealnaZajednice = copy.deepcopy(graf)
        for brid in sorted(izbrisani_bridovi, key=sortiraj):
            print(brid)
            # f.write(brid + "\n")
            vrhs = brid.split(' ')
            vrh1 = int(vrhs[0])
            vrh2 = int(vrhs[1])
            vrh1set = bridovi.get(vrh1)
            vrh1set.remove(vrh2)
            if len(vrh1set) == 0:
                bridovi.pop(vrh1)
                vrhovi.remove(vrh1)
            else:
                bridovi.update({vrh1: vrh1set})
            vrh2set = graf.get(vrh2)
            vrh2set.remove(vrh1)
            if len(vrh2set) == 0:
                bridovi.pop(vrh2)
                vrhovi.remove(vrh2)
            else:
                bridovi.update({vrh2: vrh2set})
            if brid not in tezine.keys():
                splites = brid.split(' ')
                brid = splites[1] + ' ' + splites[0]
            tezine.pop(brid)

    listaNajduljih = []
    for vrh in vrhoviOrg:
        sviPutevi = []
        nadiSvePuteve(idealnaZajednice, vrh, [], sviPutevi)
        mac = 0
        for put in sviPutevi:
            if len(put) > mac:
                mac = len(put)
                najdulji = sorted(put)
        z = 0
        for list in listaNajduljih:
            if list == najdulji or (all(x in list for x in najdulji)):
                z = 1
                break
            if all(x in najdulji for x in list):
                listaNajduljih.remove(list)
        if z == 0:
            listaNajduljih.append(najdulji)

    for lista in sorted(listaNajduljih, key=lambda x: (len(x), x)):
        i = 0
        for el in lista:
            print(el, end='')
            #f.write(str(el))
            if i < len(lista) - 1:
                print('-', end='')
                #f.write('-')
            else:
                print(' ', end='')
                #f.write(' ')
            i += 1


#f = open("myfile.txt", "w")

GirvanNewman(graf, vrhovi, tezine)
#f.close()
