#--Rapcea Catalin

import random
import time
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

def load_variables(l):
    for i in range(1, len(l[0])):
        if l[0][i] not in variables:
            if l[0][i] == l[0][i].upper() or not l[1][i].isnumeric():
                variables.append(l[0][i])
            else:
                print("variabila mica", l[0][i])
    if len(variables)==0:
        print("Nu sunt variabile")

def load_symbols(l):
    for i in range(1, len(l[1])):
        if l[1][i] not in symbols:
            # if l[1][i] != l[1][i].lower() and l[1][i].isalpha():
            #     print("simbol mare", l[1][i])
            # else:
            symbols.append(l[1][i])
    if len(symbols) == 0:
        print("Nu sunt simboluri")

def load_rules(l):
    for i in range(1, len(l[2])):
        rules.append(tuple(l[2][i].split(" -> ")))
        if rules[i-1][0] not in variables:
            print("nu exista variabila", rules[i-1][0])


l = load_sections("cfggame.in")
variables = []
load_variables(l)
symbols = []
load_symbols(l)
rules = []
load_rules(l)

print(variables)
print(symbols)
print(rules)

def generate(str):
    for indice in range(len(str)):
        if str[indice] in variables:
            if len(str) > 500:
                if rules[len(rules)-1][0] == str[indice]:
                    str = str[:indice] + rules[len(rules)-1][1] + str[indice + 1:]
                    return generate(str)
            for i in range(10*len(rules)):
                number = random.randrange(len(rules))
                if rules[number][0] == str[indice]:
                    str = str[:indice] + rules[number][1] + str[indice+1:]
                    return generate(str)
    return str

def generateaux(str):
    if rules[0][0] == str:
        str = rules[0][1]
        return generate2(str)
    return False

def generate2(str):
    for indice in range(len(rules)):
        for i in range(10 * len(rules)):
            number = random.randrange(len(rules))
            if rules[number][0] in str:
                str = str.replace(rules[number][0], rules[number][1])
                return generate2(str)
    return str

start=time.time()

set = set()
for i in range(1000):
    set.add(generateaux(rules[0][0]))
for el in set:
    print(el)

print("--- %s secunde",(time.time()-start))