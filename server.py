import random, string, re, unicodedata
from flask import Flask, render_template, request, redirect, url_for, session

appli = Flask(__name__)
appli.config["SECRET_KEY"] = "secret"

nb_max_essais = 5
mots = []
entrees_max = 5 # Nombre d'entrées maximum dans le fichier highscores.txt.

string.ascii_lowercase
with open("dictionnaire.txt", encoding="utf-8") as f:
    tableau_de_mots = [ligne.strip().split(";")[0] for ligne in f if ligne.strip()]

for mot in tableau_de_mots:
    mots.append(mot.upper())


def demarrer_nouvelle_partie():
    session["mot"] = random.choice(mots) if mots else "PYTHON"
    session["lettres_trouvees"] = []
    session["essais_restants"] = nb_max_essais
    statut = session.get("statut", "")
    if statut == "en_cours" or statut == "perdu":
        session["victoires_consecutives"] = 0
    session["statut"] = "en_cours"  # en_cours / gagne / perdu
    highscores = lire_scores()
    session["highscores"] = highscores


@appli.route("/")
def accueil():
    return render_template("accueil.html")

@appli.route("/demarrer", methods=["POST"])
def demarrer():
    nom = request.form.get("nom", "")
    session["nom"] = nom
    return redirect(url_for("jeu"))

@appli.route("/jeu")
def jeu():
    if "mot" not in session:
        demarrer_nouvelle_partie()
    mot_avec_accent = session.get("mot", "PYTHON")
    lettres_trouvees = session.get("lettres_trouvees", [])
    essais_restants = session.get("essais_restants", nb_max_essais)
    statut = session.get("statut", "en_cours")
    nom = session.get("nom", "")
    highscores = session.get("highscores", [])
    victoires_consecutives = session.get("victoires_consecutives", 0)

    liste_masquee = []
    mot_sans_accent = unicodedata.normalize('NFKD', mot_avec_accent)  
    mot_sans_accent = ''.join([c for c in mot_sans_accent if not unicodedata.combining(c)])
    i = 0
    for caractere in mot_sans_accent:
        if caractere in lettres_trouvees:
            caractere_avec_accent = mot_avec_accent[i]
            liste_masquee.append(caractere_avec_accent)
        else:
            liste_masquee.append("_")
        i += 1
    mot_masque = " ".join(liste_masquee)

    erreurs = nb_max_essais - essais_restants
    etapes_pendu = [
        """
 +---+
 |   |
     |
     |
     |
     |
=======
""",
        """
 +---+
 |   |
 O   |
     |
     |
     |
=======
""",
        """
 +---+
 |   |
 O   |
 |   |
     |
     |
=======
""",
        """
 +---+
 |   |
 O   |
/|\\  |
     |
     |
=======
""",
        """
 +---+
 |   |
 O   |
/|\\  |
/    |
     |
=======
""",
        """
 +---+
 |   |
 O   |
/|\\  |
/ \\  |
     |
=======
""",
    ]
    if erreurs < 0:
        erreurs = 0
    if erreurs >= len(etapes_pendu):
        erreurs = len(etapes_pendu) - 1
    potence_ascii = etapes_pendu[erreurs]
    
    return render_template(
        'jeu.html',
        mot_masque=mot_masque,
        lettres_trouvees=lettres_trouvees,
        essais_restants=essais_restants,
        statut=statut,
        nb_max_essais=nb_max_essais,
        potence_ascii=potence_ascii,
        mot=mot_avec_accent,
        nom=nom,
        highscores=highscores,
        alphabet = string.ascii_lowercase,
        victoires_consecutives = victoires_consecutives
    )


@appli.route("/proposer", methods=["POST"])
def proposer():
    mot_avec_accent = session.get("mot")
    mot_sans_accent = unicodedata.normalize('NFKD', mot_avec_accent)  
    mot_sans_accent = ''.join([c for c in mot_sans_accent if not unicodedata.combining(c)])  
    lettres_trouvees = session.get("lettres_trouvees", [])
    essais_restants = session.get("essais_restants", nb_max_essais)
    statut = session.get("statut", "en_cours")
    victoires_consecutives = session.get("victoires_consecutives", 0)

    if statut == "en_cours" and mot_sans_accent:
        lettre = request.form.get("lettre", "").strip().upper()

        if len(lettre) == 1 and lettre.isalpha():
            if lettre not in lettres_trouvees:
                lettres_trouvees.append(lettre)
                if lettre not in mot_sans_accent:
                    essais_restants -= 1
                else:
                    tout_trouve = True
                    for c in mot_sans_accent:
                        if c not in lettres_trouvees:
                            tout_trouve = False
                            break
                    if tout_trouve:
                        statut = "gagne"
                        victoires_consecutives += 1
                if essais_restants <= 0:
                    statut = "perdu"
                    highscores = session.get("highscores", [])
                    nom = session.get("nom")
                    if victoires_consecutives > 0:
                        nouvelle_entree = (nom, victoires_consecutives)
                        nom_deja_enregistre = False
                        i = 0
                        for entree in highscores:
                            if entree[0] == nom and entree[1] > victoires_consecutives:
                                nom_deja_enregistre = True
                                highscores[i] = nouvelle_entree
                                break
                            i+= 1
                        if not nom_deja_enregistre:
                            highscores.append(nouvelle_entree)
                        print(highscores)
                        if highscores:
                            highscores.sort(key=lambda x: x[1], reverse=True)
                        while len(highscores) > entrees_max:
                            highscores.pop()
                        sauvegarder_scores(highscores)
                    victoires_consecutives = 0

                

    session["lettres_trouvees"] = lettres_trouvees
    session["essais_restants"] = essais_restants
    session["statut"] = statut
    session["victoires_consecutives"] = victoires_consecutives

    return redirect(url_for("jeu"))


@appli.route("/nouveau")
def nouveau():
    demarrer_nouvelle_partie()
    return redirect(url_for("jeu"))


def lire_scores():
    highscores = []
    try:
        with open("highscores.txt", "r") as f:
            i = 0
            for ligne in f:
                if i >= entrees_max:
                    break
                i += 1
                ligne = re.sub(r"\d+. ", "", ligne, 1) # Efface l'index
                nom = ligne.split(";")[0].strip()
                score = int(ligne.split(";")[1].strip())
                highscores.append((nom, score))
            highscores.sort(key=lambda x: x[1], reverse=True)    
    except FileNotFoundError:
        f = open("highscores.txt", "x")
        f.close()
    return highscores

def sauvegarder_scores(highscores):
    with open("highscores.txt", "w") as f:
        i = 1
        for ligne in highscores:
            f.write((str)(i) + ". " + ligne[0] + "; " + str(ligne[1]) + "\n")
            i += 1
    

if __name__ == "__main__":
    appli.run(debug=True)