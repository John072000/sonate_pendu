from random import random

f = open("dictionnaire.txt", encoding="utf-8")

tableau_de_mots = []
longueur_du_tableau = 0

for ligne in f:
    mot_extrait = ligne.split(";")[0]
    tableau_de_mots.append(mot_extrait)
    longueur_du_tableau += 1

for s in tableau_de_mots:
    print(s)

print("-----------")

# Récupérer un mot au hasard:
j = int(random() * longueur_du_tableau)
print(tableau_de_mots[j])

f.close()