from copy import deepcopy

class Nod:
    def __init__(self, var, valori_clauze):
        self.var = var
        self.valori_clauze = valori_clauze
        self.stanga = None
        self.dreapta = None

    # insereaza un nou nod
    def creare_fiu(self, var, valori_clauza):
        if self.stanga == None:
            self.stanga = Nod(var, valori_clauza)
        else:
            self.dreapta = Nod(var, valori_clauza)

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

# functia "verificare_formula" verifica daca fiecare clauza din
# formula este true
def verificare_formula(valori_clauze):
    if False in valori_clauze:
        return False
    return True

# functia "evaluare_variabila", primeste reprezentarea unei variabile
# in matricea care stocheaza formula si o valoare de adevar
# intoarce valoarea de adevar a literalului
def evaluare_variabila(reprezentare, valoare_adevar):
    if reprezentare == 1:
        if valoare_adevar == True:
            return True
        else:
            return False
    else:
        if valoare_adevar == True:
            return False
        else:
            return True

# functia "prelucrare_clauze" evalueaza valoarea unui literal in toate clauzele
# si decide daca in urma evaluarii acelui literal (acesta obtinand
# valoarea True/False), clauza curenta devine True
def prelucrare_clauze(matrice, valori_clauze, nivel, valoare_adevar):
    for i in range(len(matrice)):
        if (valori_clauze[i]) == True:
            continue
        if matrice[i][nivel] == 0:
            continue
        if evaluare_variabila(matrice[i][nivel], valoare_adevar):
            valori_clauze[i] = True

# functia "inserare_nod" insereaza un nod fiu nodului radacina,
# continand variabila corespunzatoare nivelului si o lista
# reprezentand valorile clauzelor
def inserare_nod(radacina, variabile, valori_clauze, nivel):
    if nivel < len(variabile) - 1:
        radacina.creare_fiu(variabile[nivel + 1], valori_clauze)
    else:
        # ultimul nivel nu mai are o variabila corespondenta
        # ci doar lista cu valorile clauzelor
        radacina.creare_fiu(None, valori_clauze)

# functia "bdd_sat" creeaza un arbore in care un nod contine
# o variabila corespunzatoare nivelului si o lista continand
# valorile clauzelor formulei
# aceasta functie verifica daca exista o interpretare care
# satisface formula
def bdd_sat(matrice, radacina, variabile, nivel):
    # se verifica daca formula este evaluata drept True
    if verificare_formula(radacina.valori_clauze):
        return True

    # cand se ajunge la frunze recursivitatea se opreste
    if nivel == len(variabile):
        return False

    clauze_stanga = deepcopy(radacina.valori_clauze)
    prelucrare_clauze(matrice, clauze_stanga, nivel, False)
    inserare_nod(radacina, variabile, clauze_stanga, nivel)

    if bdd_sat(matrice, radacina.stanga, variabile, nivel + 1):
        return True

    clauze_dreapta = deepcopy(radacina.valori_clauze)
    prelucrare_clauze(matrice, clauze_dreapta, nivel, True)
    inserare_nod(radacina, variabile, clauze_dreapta, nivel)

    if bdd_sat(matrice, radacina.dreapta, variabile, nivel + 1):
        return True

    return False

def main():
    sir_intrare = input()
    lista_clauze = sir_intrare.split('^')
    variabile = variabile_formula(lista_clauze)
    matrice = forma_matriceala(lista_clauze, variabile)
    valori_clauze = [False] * len(matrice)

    radacina = Nod(variabile[0], valori_clauze)

    if bdd_sat(matrice, radacina, variabile, 0):
        rezultat_bdd = 1
    else:
        rezultat_bdd = 0
    print(rezultat_bdd)

if __name__ == '__main__':
    main()