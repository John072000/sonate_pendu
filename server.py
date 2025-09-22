from flask import Flask, render_template, request
from random import choice

app = Flask(__name__)

mot_a_trouver = ""
etat_actuel_du_mot = ""
nom_utilisateur = ""
tentatives_restantes = 5



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    if request.method == "POST":
        global nom_utilisateur
        # Si on recommence la partie, il n'est pas besoin de ré-assigner le nom d'utilisateur.
        if(request.form.__contains__("champ_nom")):
            nom_utilisateur = request.form["champ_nom"]
        global mot_a_trouver
        mot_a_trouver = choisir_un_mot_au_hasard().upper()
        global etat_actuel_du_mot
        etat_actuel_du_mot = '_' * len(mot_a_trouver)
        global tentatives_restantes
        tentatives_restantes = 5

    return render_template("play.html", nom_utilisateur=nom_utilisateur, etat_actuel_du_mot=etat_actuel_du_mot, tentatives=tentatives_restantes)

@app.route("/choix_lettre", methods=["POST"])
def choix_lettre():
    if request.method == "POST":
        global tentatives_restantes
        global etat_actuel_du_mot

        lettre_choisie = request.form["bouton_lettre"]
        lettre_choisie = lettre_choisie.upper()

        i = 0
        tentative_echouee = True
        for lettre in mot_a_trouver:
            if lettre == lettre_choisie:
                etat_actuel_du_mot = etat_actuel_du_mot[0:i] + lettre_choisie + etat_actuel_du_mot[i+1:]
                tentative_echouee = False
            i += 1

        if mot_a_trouver == etat_actuel_du_mot:
            return render_template("play.html", nom_utilisateur=nom_utilisateur,
                                   etat_actuel_du_mot=etat_actuel_du_mot, tentatives=tentatives_restantes,
                                   message_de_fin = "Vous avez gagné, " + nom_utilisateur + ", Bravo! Voulez-vous recommencer?")
        
        if tentative_echouee:
            tentatives_restantes -= 1
            if tentatives_restantes <= 0:
                return render_template("play.html", nom_utilisateur=nom_utilisateur, etat_actuel_du_mot=etat_actuel_du_mot,
                                       tentatives=tentatives_restantes, message_de_fin="Vous avez perdu! Recommencer?")

    return render_template("play.html", nom_utilisateur=nom_utilisateur, etat_actuel_du_mot=etat_actuel_du_mot, tentatives=tentatives_restantes)

def choisir_un_mot_au_hasard():
    with open("dictionnaire.txt", encoding="utf-8") as f:
        tableau_de_mots = [ligne.split(";")[0] for ligne in f]

    return choice(tableau_de_mots)