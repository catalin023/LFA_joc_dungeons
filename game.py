#--Rapcea Catalin

import copy

rooms = {       #dictionar cu toate camere care retine descrierea, camerele alaturate, itemurile din ea si ce trebuie ca sa intri in ea
    "EntranceHall": {
        "description": "The grand foyer of the Castle of Illusions.",
        "adjacent_rooms": ["DiningRoom", "Armoury"],
        "items": ["key"],
        "requirments": ["invitation"],
    },
    "DiningRoom": {
        "description": "A room with a large table filled with an everlasting feast.",
        "adjacent_rooms": ["EntranceHall", "Kitchen", "Treasury"],
        "items": ["invitation", "chef's_hat"],
        "requirments": [],
    },
    "Kitchen": {
        "description": "A room packed with peculiar ingredients.",
        "adjacent_rooms": ["DiningRoom", "Pantry"],
        "items": ["spoon"],
        "requirments": ["chef's_hat"],
    },
    "Armoury": {
        "description": "A chamber filled with antiquated weapons and armour.",
        "adjacent_rooms": ["Treasury", "ThroneRoom", "EntranceHall"],
        "items": ["sword", "crown"],
        "requirments": ["key"],
    },
    "Treasury": {
        "description": "A glittering room overflowing with gold and gemstones.",
        "adjacent_rooms": ["Library", "Wizard'sStudy", "Armoury", "DiningRoom"],
        "items": ["ancient_coin"],
        "requirments": ["sword"],
    },
    "Library": {
        "description": "A vast repository of ancient and enchanted texts.",
        "adjacent_rooms": ["SecretExit", "Treasury"],
        "items": ["spell_book"],
        "requirments": ["ancient_coin"],
    },
    "Pantry": {
        "description": "A storage area for the Kitchen.",
        "adjacent_rooms": ["Kitchen"],
        "items": [],
        "requirments": ["spoon"],
    },
    "ThroneRoom": {
        "description": "The command center of the castle.",
        "adjacent_rooms": ["Wizard'sStudy", "Armoury"],
        "items": [],
        "requirments": ["crown"],
    },
    "Wizard'sStudy": {
        "description": "A room teeming with mystical artifacts.",
        "adjacent_rooms": ["SecretExit", "Treasury", "ThroneRoom"],
        "items": ["magic_wand"],
        "requirments": ["spell_book"],
    },
    "SecretExit": {
        "description": "The hidden passage that leads out of the Castle of Illusions.",
        "adjacent_rooms": ["Library", "Wizard'sStudy"],
        "items": [],
        "requirments": ["magic_wand"],
    },
}

#IMPLEMENTAREA PDA
def pda_load_sections(fisier): #incarcarea datelor din fisier
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

def pda_load_sigma(l):
    for i in range(1, len(l[0])):
        if l[0][i] not in pda_sigma:
            pda_sigma.append(l[0][i])
    if len(pda_sigma)==0:
        print("Alfabetul e gol")
    pda_sigma.append('~')

def pda_load_states(l):
    ok1 = 0
    ok2 = 0
    for i in range(1, len(l[1])):
        stare = tuple(l[1][i].split(" "))
        if stare[1]=='1':
            ok1 += 1
        elif stare[1]=='2':
            ok2 = 1
        for tuplu in pda_states:
            if stare[0] == tuplu[0]:
                print(f'deja exista starea {stare[0]}')
        pda_states.append(stare)
    if ok1==0:
        print("stare initiala nu exista")
    elif ok1>=2:
        print("prea multe stari initiale")
    elif ok2 == 0:
        print("stare finala nu exista")

def pda_load_actions(l):
    oki = 0
    okf = 0
    for i in range(1, len(l[2])):
        act = tuple(l[2][i].split(" "))
        ok1 = 0
        ok2 = 0
        for stare in pda_states:
            if act[0] == stare[0]:
                ok1 = 1
                if stare[1] == "1":
                    oki = 1
            if act[4] == stare[0]:
                ok2 = 1
                if stare[1] == "2":
                    okf = 1
        pda_actions.append(act)
    if not oki:
        print("nu exista actiune de la starea initiala")
    if not okf:
        print("nu exista actiune catre starea finala")

l = pda_load_sections("pdagame.in")
pda_sigma = []
pda_load_sigma(l)
pda_states = []
pda_load_states(l)
pda_actions = []
pda_load_actions(l)

pda_F = []
for l in pda_states:
    if l[1] == '1':
        si = l[0]
        if len(l) == 3:
            pda_F.append(l[0])
    if l[1] == '2':
        pda_F.append(l[0])


def pdaemulate(str, start, i, stiva):
    for l in pda_actions:
        if l[0] == start:
            if l[1] == '~':
                if len(stiva):
                    if stiva[-1] == l[2]:
                        stiva.pop(-1)
                        if l[3] != '~':
                            stiva.append(l[3])
                        if pdaemulate(str, l[4], i, copy.deepcopy(stiva)):
                            return True
                    elif l[2] == '~':
                        if l[3] != '~':
                            stiva.append(l[3])
                        if pdaemulate(str, l[4], i, copy.deepcopy(stiva)):
                            return True
                elif l[2] == '~':
                    if l[3] != '~':
                        stiva.append(l[3])
                    if pdaemulate(str, l[4], i, copy.deepcopy(stiva)):
                        return True
            elif i<len(str) and l[1] == str[i]:
                if len(stiva):
                    if stiva[-1] == l[2]:
                        stiva.pop(-1)
                        if l[3] != '~':
                            stiva.append(l[3])
                        if pdaemulate(str, l[4], i + 1, copy.deepcopy(stiva)):
                            return True
                    elif l[2] == '~':
                        if l[3] != '~':
                            stiva.append(l[3])
                        if pdaemulate(str, l[4], i + 1, copy.deepcopy(stiva)):
                            return True
                elif l[2] == '~':
                    if l[3] != '~':
                        stiva.append(l[3])
                    if pdaemulate(str, l[4], i+1, copy.deepcopy(stiva)):
                        return True
    if i == len(str):
        if start in pda_F and len(stiva) == 0:
            return True
        else:
            return False
    return False



#IMPLEMENTAREA LA PT JOACA
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
        act = tuple(l[3][i].split(","))
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
l = load_sections("lagame.in")
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
    if start in F: #verifica daca am ajuns in camerea finala
        return "Ati terminat joaca"
    str = input("Comanda:")
    if not pdaemulate(str.split(), pda_states[0][0], 0, list()): #verifica cu ajtorul PDA daca comanda a fost introdusa corect
        print("Comanda gresita")
        return laemulate(start, i + 1, copy.deepcopy(multime))
    if(str == "look"): #afisarea informatiei desroe camera cu ajutorul look
        print(rooms[start])
        return laemulate(start, i + 1, copy.deepcopy(multime))
    if(str == "inventory"): #afisarea inventarului
        print(multime)
        return laemulate(start, i + 1, copy.deepcopy(multime))
    if(str.split()[0] == "drop"): #drop item
        actions.append((start, f'take {str.split()[1]}', '~', '~', str.split()[1], start)) #adauga o noua actiune de take item
        rooms[start]["items"].append(str.split()[1]) #se adauga itemul la camera unde sa facut drop la item
        return laemulate(start, i + 1, copy.deepcopy(multime))
    for l in actions:
        if l[0] == start: #cauta tranzitia care incepe din starea "start"
            if l[1] == str:
                if l[2] in multime or l[2]=='~': #tranzitia pt verificare ca elementu sa se afle in lista
                    multime.discard(l[3]) #elimina elemntul
                    multime.add(l[4]) #adauga elementul
                    if(str.split()[0]=="take"):
                        rooms[l[0]]["items"].remove(l[4])
                        actions.remove(l)
                    return laemulate(l[5], i+1, copy.deepcopy(multime)) #apeleaza recursiv functia
    print("Comanda gresita")
    return laemulate(start, i + 1, copy.deepcopy(multime))

print(laemulate(si, 0, set()))


