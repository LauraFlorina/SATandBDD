# functia "variabile_formula" primeste o lista de clauze si returneaza
# o lista a variabilelor intalnite in formula alcatuita din acele clauze
def variabile_formula(lista_clauze):
    variabile = []
    for clauza in lista_clauze:
        # se elimina parantezele
        clauza = clauza[1 : len(clauza) - 1]
        lista_literali = clauza.split('V')
        for literal in lista_literali:
            # daca variabila apare negata in formula, se elimina negatia
            if (literal[0] == '~'):
                literal = literal[1:]
            # daca variabila nu a fost deja adaugata in lista, ea se adauga
            if literal not in variabile:
                variabile.append(literal)
    return variabile

# functia "forma_matriceala" intoarce matricea ce corespunde reprezentarii
# formulei
def forma_matriceala(lista_clauze, variabile):
    matrice = []
    for clauza in lista_clauze:
        # se construiecte matricea linie cu linie
        linie = [0] * len(variabile)
        clauza = clauza[1: len(clauza) - 1]
        lista_literali = clauza.split('V')
        for literal in lista_literali:
            # se presupune initial ca variabila apare fara negatie
            valoare = 1
            # daca variabila apare negata, atunci in matrice se adauga -1
            if (literal[0] == '~'):
                literal = literal[1:]
                valoare = -1
            linie[variabile.index(literal)] = valoare
        matrice.append(linie)
    return matrice

# functia "verifica interpretare" verifica daca interpretarea data face formula
# reprezentata prin matrice, adevarata
def verifica_interpretare(matrice, interpretare, variabile):
    for i in range(0, len(matrice)):
        # in constructia matricei, indicele coloanei corespunde cu indicele
        # variabilei din lista de variabile
        for j in range(0, len(variabile)):
            if matrice[i][j] == 0 and j != len(variabile) - 1:
                continue
            # se verifica cele doua cazuri in cadrul carora clauza
            # corespunzatoare liniei din matrice ar fi adevarata
            if variabile[j] in interpretare:
                if matrice[i][j] == 1:
                    break
            else:
                if matrice[i][j] == -1:
                    break
            # daca se ajunge la sfarsitul liniei si nu este gasita nicio
            # valoare de True, formula nu este satisfiabila
            if (j == len(variabile) - 1):
                return False
    return True

# functia "fcn_sat" creeaza fiecare interpretare, le verifica pe rand,
# in cazul in care se gaseste o prima interpretare buna, se opreste
# avansul in recursivitate
def fcn_sat(matrice, interpretare, variabile, index):
    for i in range(index, len(variabile)):
        interpretare.append(variabile[i])
        if verifica_interpretare(matrice, interpretare, variabile):
            return True
        if fcn_sat(matrice, interpretare, variabile, i + 1):
            return True
        interpretare.pop()
    return False

def main():
    sir_intrare = input()
    lista_clauze = sir_intrare.split('^')
    variabile = variabile_formula(lista_clauze)
    matrice = forma_matriceala(lista_clauze, variabile)
    if fcn_sat(matrice, [], variabile, 0):
        rezultat_fcn = 1
    else:
        rezultat_fcn = 0
    print(rezultat_fcn)

if __name__ == '__main__':
    main()