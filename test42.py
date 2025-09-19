f = open("dictionnaire.txt", encoding="utf-8")

tableau_de_mots = []

for ligne in f:
    mot_extrait = ligne.split(";")[0]
    tableau_de_mots.append(mot_extrait)

for s in tableau_de_mots:
    print(s)