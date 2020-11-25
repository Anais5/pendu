import random

ERREURS_POSSIBLES = 7 #ne pas changer ca créerai des erreurs
SYMOBOLE_MYSTERE = "?"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LONGUEUR_MINIMALE = 4

def ascii(erreurs : int):
    """Cette fonction retourne un bonhomme pendu suivant le
    nombre d'erreurs."""
    bonhomme = ("|", "O", "|", "/", "\ ", "/", "\ ")
    dessin = " _______ \n |/    0  \n |     1  \n |    324 \n |    5 6 \n |        \n/|\        "
    for chiffre in range(erreurs):
        for i in range(len(dessin)):
            if dessin[i] == str(chiffre):
                dessin = dessin.replace(dessin[i], bonhomme[chiffre])
    for j in range(len(dessin)):
        if dessin[j] in ("0", "1", "2", "3", "4", "5", "6"):
            dessin = dessin.replace(dessin[j], " ")
    return dessin

def charge_dictionnaire(dico : str):
    """Cette fonction charge les mots ligne par ligne d'un document
    texte puis retourne une liste de ces mots."""
    liste_mots = []
    with open(dico, "r") as f:
        for mot in f.readlines():
            mot = mot.strip().upper()
            if len(mot) >= LONGUEUR_MINIMALE:  #on vérifie que la longueur du mot soit supérieure ou égale à la longueur minimale
                liste_mots.append(mot)
    return liste_mots

DICO_MOTS = charge_dictionnaire("dico_fr.txt")

def genere_motif(secret : str, propositions : list):
    """Cette fonction génère un motif à partir du mot secret donné et des
    propositions de lettres qui ont été faites par l'utilisateur.
    Si la lettre est dans le mot secret et dans les propositions
    alors elle est affichée, si ce n'est pas le cas elle est remplacée
    par un symbole mystère
    (qui est défini par la variable globale : SYMBOLE_MYSTERE)."""
    for i in range(len(propositions)):
        propositions[i] = propositions[i].upper()
    motif = ""
    for lettre in secret:
        if lettre not in propositions:  #si la proposition n'est pas dans secret, elle sera remplacée par le symbole mystère
            motif += SYMOBOLE_MYSTERE
        elif lettre in propositions:
            motif += lettre  #si la lettre est bien dans le mot elle est ajoutée dans le motif
    return motif

def filtrer(motif : str, mot : str, deja_donnees : list):
    """Cette fonction cherche si oui ou non le motif pourrait être
    compatible avec un mot en fonction des propositions de lettres
    déjà faites. Elle renvoie un booléen et les lettres qui seraient
    possible de proposer."""
    reste_lettre = set()
    if len(motif) != len(mot):
        return (False, reste_lettre)
    rep = True
    longueur_motif = len(motif) - 1
    for i in range(0, longueur_motif):
        if motif[i] == "?":
            if mot[i] in deja_donnees:
                rep = False
        elif motif[i] != mot[i]:
            rep = False
    if rep == True:
        for j in range(0, longueur_motif):
            if motif[j] == SYMOBOLE_MYSTERE:
                reste_lettre.add(mot[j])
        return (True, reste_lettre)
    else:
        return (False, reste_lettre)

def trouver_mots_restants(motif : str, deja_donnees : list, liste_mots_restants : list):
    """D'après une liste de mots et une liste de lettres déjà données,
    cette fonction retourne un tuple qui contient le motif, les mots
    qui pourraient être la bonne réponse en fonction du motif et un
    dictionnaire des lettres qui pourraient être proposées."""
    dico_lettres = {l: 0 for l in ALPHABET if l not in deja_donnees}
    mots_possibles = []
    for mot in liste_mots_restants:
        ok, lettres_restantes = filtrer(motif, mot, deja_donnees)
        if ok == True:
            mots_possibles.append(mot)
    for l in dico_lettres:
        if l not in deja_donnees:
            if l in mots_possibles:
                dico_lettres[l] += 1
    return motif, mots_possibles, dico_lettres

def partie_avancee():
    """Cette fonction permet de jouer au pendu, elle a besoin des
    autres fonctions pour pouvoir s'éxecuter correctement et elle
    ne renvoie rien."""
    limite = ERREURS_POSSIBLES
    propositions_vraies = []
    propositions_fausses = []
    prop = []
    mot = random.choice(DICO_MOTS)
    rep = genere_motif(mot, propositions_vraies)
    dessin = ascii(7 - limite)
    print(f"{dessin}\nMot : {rep}; lettre(s) déjà essayée(s) : {propositions_fausses}; essai(s) restant(s) : "
          f"{limite} \nMot(s) possible(s) : {trouver_mots_restants(rep, prop, DICO_MOTS)[1]}")
    while mot != rep:  #s'éxecutera en boucle tant que le mot n'est pas deviné
        if limite == 0: #si la limite est atteinte
            print(f"Tu as perdu, le mot a trouver était : {mot} !")  #on affiche le mot qu'il fallait trouver
            return  #on arrête la boucle
        lettre = input("Choisir une lettre: ")  #on demande au joueur de proposer une lettre
        lettre = lettre.upper()
        if len(lettre) > 1 or type(lettre) != str or lettre not in ALPHABET:
            print("Vous devez utiliser une lettre sans accent !")  #si le joueur ne propose pas une lettre on lui revoie une erreur
        if lettre in prop:
            print(f"Vous avez déjà essayé la lettre {lettre} !")  #si la lettre a déjà été proposée on l'indique au joueur
        elif lettre in ALPHABET:
            prop.append(lettre)
            if lettre in mot:
                propositions_vraies.append(lettre)
                rep = genere_motif(mot, propositions_vraies)  #génère un motif du mot a chercher avec les propositions vraies
            else:
                limite -= 1
                propositions_fausses.append(lettre)
                rep = genere_motif(mot, propositions_vraies)
                print(f"Cette lettre n'est pas dans le mot ! Il vous reste {limite} essais.")
            dessin = ascii(7 - limite)
            print(f"{dessin}\nMot : {rep}; lettre(s) déjà essayée(s) : {propositions_fausses}; essai(s) restant(s) : "
                  f"{limite} \nMot(s) possible(s) : {trouver_mots_restants(rep, prop, DICO_MOTS)[1]}")
    print("Tu as gagné ! Bravo !")

partie_avancee()
