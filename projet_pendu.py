import random
import os

os.chdir("E:\\NSI\\projet nsi")


ERREURS_POSSIBLES = 7
SYMBOLE_MYSTERE = "?"
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LONGUEUR_MINIMALE = 4

def charge_dictionnaire():
    liste_mots = []
    with open("dictionnaire-francais.txt", "r") as f:
        for mot in f.readlines():
            mot = mot.strip().upper()
            if len(mot) >= LONGUEUR_MINIMALE:
                liste_mots.append(mot)
    return liste_mots

## Exercice 1:


def genere_motif(secret, propositions):
    secret = secret.upper()                         """On met le secret en majuscule... """
    for y in range(len(propositions)):
        propositions[y] = propositions[y].upper()   """... et les lettres proposés aussi."""
    mot = ""
    for i in secret:                               """Pour tout les characters de secret """
        if i not in propositions:
            mot += "?"
            """... si la propositions n'est pas un character de secret,
            on affiche toutes les lettres de secret non proposé par des "?" ."""
        elif i in propositions:
            mot += i
            """Sinon les points d'interrogations qui correspondent aux lettres
            de secret sont remplacé par les bonnes lettres proposés """
    return mot



## Exercice 2:

def partie_simple(limite=10):
    liste_mots = []
    propositions_vraies = []
    propositions_fausses = []
    rep = ""
    with open("dictionnaire-francais.txt", "r") as f:       """On parcourt le dictionnaire de mots"""
        for mot in f.readlines():
            mot = mot.strip().upper()
            if len(mot) >= LONGUEUR_MINIMALE:   """ On verifie que les mots soit supérieur ou égale à la longueur minimale,"""
                liste_mots.append(mot)
        mot = random.choice(liste_mots)         """ on les ajoutes dans la liste de mots crée plus haut et on choisis aleatoirement un mot à deviner"""
    while mot != rep and limite != 0:
        lettre = input("Choisir une lettre: ")
        lettre = lettre.upper()
        """ Tant que le mot n'est pas deviner et que la limite n'est pas atteinte,
        on propose au joueur de deviner une lettre."""
        if lettre in propositions_vraies or lettre in propositions_fausses:
            print (f"Vous avez déja essayé la lettre {lettre}!")                """Si la lettres à déja été proposé on l'indique au joueur"""
        elif lettre in ALPHABET:
            rep = genere_motif(mot, propositions)                               """, sinon on genere un motif du mot a deviner"""
            if lettre in mot:
                propositions_vraies.append(lettre)
            else:
                limite -= 1
                propositions_fausses.append(lettre)
                print(f"Cette lettre n'est pas dans le mot ! Il vous reste {limite} essais.")
                """ si la lettre proposé est correct, on l'ajoute a la liste des propositions vraies
                , sinon on réduit la limite, ajoute la lettre proposé à la liste des propositions fausses
                et on l'indique au joueur"""

            print(rep)
        else:
            print("Vous devez utiliser une lettre !")

## Exercice 3:

def filtrer(motif, mot, deja_donnees):
    if len(mot) > len (motif):
        return False
        """ Si un mot du dictionnaire est plus grand que le motif du mot à trouver
        ,on renvoie que le mot n'est pas une solution"""
    for i in range(len(motif)-1):
        if motif[i] == "?":
            if motif[i] == mot[i]:
                return False
            if mot[i] in deja_donnees:
                return False
                """ Si une des lettres du mot est déja proposé, on renvoie que le mot ne peut pas être une solution"""
    return True




## Exercice 4:

liste_mots_restants = ["MANGER", "CHIEN", "RADIATEUR", "AVION"]

def trouver_mots_restants(motif, deja_donnees, liste_mots_restants):
    motif = motif.upper()
    for y in range(len(deja_donnees)):
        deja_donnees[y] = deja_donnees[y].upper()        """ On verifie que les lettres déja données sont en majuscule"""
    m = ""
    for i in motif:                                     """ On génére un motif pour le mot a deviner"""
        if i not in deja_donnees:
            m += "?"
        elif i in deja_donnees:
            m += i
    mots_possibles = []
    for mot in liste_mots_restants:
        if filtrer(motif, mot, deja_donnees) == False:
            mots_possibles.append(mot)                  """ On met tous les mots restants qui peuvent être une solution dans une liste des mots possibles"""
    return m, deja_donnees, mots_possibles



## Exercice 5:

def partie_avancee(limite=5):
    liste_mots = []
    propositions_vraies = []
    propositions_fausses = []
    prop = []
    rep = ""
    with open("dico_fr.txt", "r") as f:                   """On parcourt le dictionnaire de mots"""
        for mot in f.readlines():
            mot = mot.strip().upper()
            if len(mot) >= LONGUEUR_MINIMALE:             """ On verifie que les mots soit supérieur ou égale à la longueur minimale,"""
                liste_mots.append(mot)
        mot = random.choice(liste_mots)                   """ on les ajoutes dans la liste de mots crée plus haut et on choisis aleatoirement un mot à deviner"""
    while mot != rep:
    """ Tant que le mot n'est pas deviner """
        if limite == 0:
            print(f"Tu as perdu, le mot a trouver était : {mot} !")
            return                                        """ si la limite est atteinte, la partie est terminer et on affiche le mot cherché."""
        lettre = input("Choisir une lettre: ")
        lettre = lettre.upper()
        if lettre in prop:
            print(f"Vous avez déjà essayé la lettre {lettre} !")    """Si la lettres à déja été proposé on l'indique au joueur"""
        elif lettre in ALPHABET:
            prop.append(lettre)                                     """ sinon la lettre peut encore être proposé"""
            if lettre in mot:
                propositions_vraies.append(lettre)
                rep = genere_motif(mot, propositions_vraies)
                """ Si la lettre proposé est dans le mot,
                on génère un motif du mot a chercher et on affiche les lettres bien proposé dans le motif"""
            else:
                limite -= 1
                propositions_fausses.append(lettre)
                rep = genere_motif(mot, propositions_vraies)
                print(f"Cette lettre n'est pas dans le mot ! Il vous reste {limite} essais.")
                """, sinon on réduit la limite, ajoute la lettre proposé à la liste des propositions fausses
                et on indique au joueur le nombre d'essaie possible"""
            print(f"Mot : {rep}; lettre(s) déjà essayée(s) : {propositions_fausses}; essai(s) restant(s) : {limite} \nMot(s) possible(s) : {trouver_mots_restants(rep, prop, liste_mots)}") """ On affiche le motif, les propositions fausses, le nombre d'essaie restant et les mots possibles"""
        if len(lettre) > 1 or type(lettre) != str or lettre not in ALPHABET:
            print("Vous devez utiliser une lettre !")  """ si le joueur ne propose pas une lettre on lui revoie une erreur"""
    print("Tu as gagné ! Bravo !")




## Exercice 6:


def filtrer2(motif, mot, deja_donnees):
    if len(motif) != len(mot):
        return (False, set())            """ Si le motif génèrer est plus grand ou plus petit que le mot
                                         proposé, on renvoie que le mot ne peut pas être une solution"""
    reste_lettre = set()
    rep = True
    longueur_motif = len(motif) - 1
    for i in range(0, longueur_motif):
        if motif[i] == "?":
            if motif[i] in deja_donnees:
                rep = False                 """ Si une des lettres du mot est déja proposé, on renvoie que le mot ne peut pas être une solution"""
        elif motif[i] != mot[i]:
            rep = False                     """ Si une des lettres du mot n'est pas dans le motif, on renvoie que le mot ne peut pas être une solution"""
    if rep == True:
        for i in range(0, longueur_motif):
            if motif[i] == "?":
                reste_lettre.add(mot[i+1]) """ Si le mot peut être une solution, on ajoute toutes les lettres de ce mot comme solution possible"""
        return True
    else:
        return False



## Exercice 7:

def trouver_mots_restants2(motif, deja_donnees, liste_mots_restants):
    l = 0
    motif = motif.upper()
    dico_lettres = {l : 0 for l in ALPHABET if l not in deja_donnees}   """ on crée un dictionnaire qui affiche pour toutes lettres non proposé
                                                                        le nombre de mot la contenant"""
    for y in range(len(deja_donnees)):
        deja_donnees[y] = deja_donnees[y].upper()
    m = ""
    for i in motif:                                 """ On génére un motif pour le mot a deviner"""
        if i not in deja_donnees:
            m += "?"
        elif i in deja_donnees:
            m += i
    mots_possibles = []
    for mot in liste_mots_restants:
        if filtrer2(motif, mot, deja_donnees) == True:
            mots_possibles.append(mot)                   """ On met tous les mots restants qui peuvent être une solution dans une liste des mots possibles"""
    for l in dico_lettres:
        if l not in deja_donnees:
            if l in str(mots_possibles):
                dico_lettres[l] += 1                    """ On rajoute le nombre de fois qu'une lettre non proposé et contenu dans un mot possible"""
    return m , mots_possibles, trier_dictionnaire(dico_lettres)


def trier_dictionnaire(dico):
    liste_couples = [(dico[k], k) for k in dico if dico[k] > 0]
    liste_couples.sort(reverse=True)
    return liste_couples                         """ On renvoie un dictionnaire avec uniquement des valeurs au dessus de 0"""




## Exercice 8:

def partie_avancee2(limite=10):
    liste_mots = []
    propositions_vraies = []
    propositions_fausses = []
    prop = []
    rep = ""
    with open("dico_fr.txt", "r") as f:         """On parcourt le dictionnaire de mots"""
        for mot in f.readlines():
            mot = mot.strip().upper()
            if len(mot) >= LONGUEUR_MINIMALE:    """ On verifie que les mots soit supérieur ou égale à la longueur minimale,"""
                liste_mots.append(mot)
        mot = random.choice(liste_mots)          """ on les ajoutes dans la liste de mots crée plus haut et on choisis aleatoirement un mot à deviner"""
    while mot != rep:
     """ Tant que le mot n'est pas deviner """
        if limite == 0:
            print(f"Tu as perdu, le mot a trouver était : {mot} !")
            return                                                   """ si la limite est atteinte, la partie est terminer et on affiche le mot cherché."""
        lettre = input("Choisir une lettre: ")
        lettre = lettre.upper()
        if lettre in prop:
            print(f"Vous avez déjà essayé la lettre {lettre} !")    """Si la lettres à déja été proposé on l'indique au joueur"""
        elif lettre in ALPHABET:                                   """, sinon la lettre peut encore être proposé"""
            prop.append(lettre)
            if lettre in mot:
                propositions_vraies.append(lettre)
                rep = genere_motif(mot, propositions_vraies)
                """ Si la lettre proposé est dans le mot,
                on génère un motif du mot a chercher et on affiche les lettres bien proposé dans le motif"""
            else:
                limite -= 1
                propositions_fausses.append(lettre)
                rep = genere_motif(mot, propositions_vraies)
                print(f"Cette lettre n'est pas dans le mot ! Il vous reste {limite} essais.")
                """, sinon on réduit la limite, ajoute la lettre proposé à la liste des propositions fausses
                et on indique au joueur le nombre d'essaie possible"""
            print(f"Mot : {rep}; lettre(s) déjà essayée(s) : {propositions_fausses}; essai(s) restant(s) : {limite} \nMot(s) possible(s) : {trouver_mots_restants2(rep, prop, liste_mots)}")   """ On affiche le motif, les propositions fausses, le nombre d'essaie restant et les mots possibles"""
        if len(lettre) > 1 or type(lettre) != str or lettre not in ALPHABET:
            print("Vous devez utiliser une lettre !")     """ si le joueur ne propose pas une lettre on lui revoie une erreur"""
    print("Tu as gagné ! Bravo !")



