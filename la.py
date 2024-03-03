#--Rapcea Catalin

import copy
def load_sections(fisier): #incarcarea datelor din fisier
    f = open(fisier)
    l = [[]]
    i = 0
    for linie in f:
        if linie[0] == "[":
            l[i].append(linie[1:len(linie)-2])
        elif linie[0] != "#" and len(linie)!=1:
            linie = linie.replace('\n', '')
            l[i].append(linie)
        elif len(linie)==1:
            l.append([])
            i+=1
    f.close()
    return l

def load_sigma(l): #alfabetul de intrare
    for i in range(1, len(l[0])):
        if l[0][i] not in sigma:
            sigma.append(l[0][i])
    if len(sigma)==0:
        print("Alfabetul e gol")

def load_states(l): #multimea de stari
    ok1 = 0
    ok2 = 0
    for i in range(1, len(l[1])):
        stare = tuple(l[1][i].split(" "))
        if stare[1]=='1':
            ok1 += 1 #numara cate stari de start sunt
        elif stare[1]=='2':
            ok2 = 1 #verifica daca exista macar o stare finala
        for tuplu in states:
            if stare[0] == tuplu[0]:
                print(f'deja exista starea {stare[0]}')
        states.append(stare)
    if ok1==0:
        print("stare initiala nu exista")
    elif ok1>=2:
        print("prea multe stari initiale")
    elif ok2 == 0:
        print("stare finala nu exista")

def load_gama(l): #alfabetul listei
    for i in range(1, len(l[2])):
        if l[2][i] not in gama:
            gama.append(l[2][i])
    if len(gama)==0:
        print("Alfabetul e gol")
    gama.append('~')

def load_actions(l): #functia de tranzitie
    oki = 0
    okf = 0
    for i in range(1, len(l[3])):
        act = tuple(l[3][i].split(" "))
        ok1 = 0
        ok2 = 0
        for stare in states:
            if act[0] == stare[0]:
                ok1 = 1
                if stare[1] == "1": #verifica ca sa existe macar o tranzitie de la starea de start
                    oki = 1
            if act[5] == stare[0]:
                ok2 = 1
                if stare[1] == "2": #verifica ca sa exista macar o tranzitie catre o starea finala
                    okf = 1
        if not ok1:
            print(f'starea {act[0]} inexistenta')
        if not ok2:
            print(f'starea {act[2]} inexistenta')
        if act[1] not in sigma:
            print(f"elementul {act[1]} inexistent")
        if act[2] not in gama and act[2][1:] not in gama:
            print(f"elementul {act[2]} inexistent")
        if act[3] not in gama:
            print(f"elementul {act[3]} inexistent")
        if act[4] not in gama:
            print(f"elementul {act[4]} inexistent")
        actions.append(act)
    if not oki:
        print("nu exista actiune de la starea initiala")
    if not okf:
        print("nu exista actiune catre starea finala")

#INCARCAREA DATELOR DIN FISIER
l = load_sections("la.in")
sigma = []
load_sigma(l)
states = []
load_states(l)
gama = []
load_gama(l)
actions = []
load_actions(l)

#MULTIMEA DE STARI FINALE
F = []
for l in states:
    if l[1] == '1':
        si = l[0] #starea de start
        if len(l) == 3:
            F.append(l[0])
    if l[1] == '2':
        F.append(l[0])

def laemulate(start, i, multime):
    for l in actions:
        if l[0] == start: #cauta tranzitia care incepe din starea "start"
            if i<len(str) and l[1] == str[i]:
                if l[2][0] == "!": #tranzitia pt verificare ca elementu sa nu se afle in lista
                    if l[2][1:] not in multime:
                        multime.discard(l[3]) #elimina elemntul
                        multime.add(l[4]) #adauga elementul
                        if laemulate(l[5], i+1, copy.deepcopy(multime)): #apeleaza recursiv functia
                            return True
                elif l[2] in multime or l[2]=='~': #tranzitia pt verificare ca elementu sa se afle in lista
                    multime.discard(l[3]) #elimina elemntul
                    multime.add(l[4]) #adauga elementul
                    if laemulate(l[5], i+1, copy.deepcopy(multime)): #apeleaza recursiv functia
                        return True
    if i == len(str): #daca sa terminat sinrul din input
        if start in F: #verifica daca ultima stare se afla in multimea starilor finale
            return True
        else:
            return False
    return False

str = '0011' #stringul din input
print(laemulate(si, 0, set()))


