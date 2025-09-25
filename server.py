import random, string
from flask import Flask, render_template, request, redirect, url_for, session

appli = Flask(__name__)
appli.config["SECRET_KEY"] = "secret"

nb_max_essais = 7
mots = []

string.ascii_lowercase
with open("dictionnaire.txt", encoding="utf-8") as f:
    tableau_de_mots = [ligne.strip().split(";")[0] for ligne in f if ligne.strip()]

for mot in tableau_de_mots:
    mots.append(mot.upper())


def demarrer_nouvelle_partie():
    session["mot"] = random.choice(mots) if mots else "PYTHON"
    session["lettres_trouvees"] = []
    session["essais_restants"] = nb_max_essais
    session["statut"] = "en_cours"  # en_cours / gagne / perdu


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

    mot = session.get("mot", "PYTHON")
    lettres_trouvees = session.get("lettres_trouvees", [])
    essais_restants = session.get("essais_restants", nb_max_essais)
    statut = session.get("statut", "en_cours")
    nom = session.get("nom", "")

    liste_masquee = []
    for caractere in mot:
        if caractere in lettres_trouvees:
            liste_masquee.append(caractere)
        else:
            liste_masquee.append("_")
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
/|   |
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

    highscores = []
    highscores.append(("John", 7))
    highscores.append(("Bob", 6))
    highscores.append(("Jack", 5))
    
    return render_template(
        'jeu.html',
        mot_masque=mot_masque,
        lettres_trouvees=lettres_trouvees,
        essais_restants=essais_restants,
        statut=statut,
        nb_max_essais=nb_max_essais,
        potence_ascii=potence_ascii,
        mot=mot,
        nom=nom,
        highscores=highscores,
        alphabet = string.ascii_lowercase
    )


@appli.route("/proposer", methods=["POST"])
def proposer():
    mot = session.get("mot")
    lettres_trouvees = session.get("lettres_trouvees", [])
    essais_restants = session.get("essais_restants", nb_max_essais)
    statut = session.get("statut", "en_cours")

    if statut == "en_cours" and mot:
        lettre = request.form.get("lettre", "").strip().upper()

        if len(lettre) == 1 and lettre.isalpha():
            if lettre not in lettres_trouvees:
                lettres_trouvees.append(lettre)
                if lettre not in mot:
                    essais_restants -= 1

                tout_trouve = True
                for c in mot:
                    if c not in lettres_trouvees:
                        tout_trouve = False
                        break

                if tout_trouve:
                    statut = "gagne"
                elif essais_restants <= 0:
                    statut = "perdu"

    session["lettres_trouvees"] = lettres_trouvees
    session["essais_restants"] = essais_restants
    session["statut"] = statut

    return redirect(url_for("jeu"))


@appli.route("/nouveau")
def nouveau():
    demarrer_nouvelle_partie()
    return redirect(url_for("jeu"))


GABARIT_HTML_JEU = r"""
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Pendu</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div class="barre">
    <p> Bienvenue {{ nom }} </p>
    <p> Tableau des scores: </p>
    <table id="highscores">
      <tr><td>1. {{ highscores[0][0] }}: {{ highscores[0][1] }} </td></tr>
      <tr><td>2. {{ highscores[1][0] }}: {{ highscores[1][1] }} </td></tr>
      <tr><td>3. {{ highscores[2][0] }}: {{ highscores[2][1] }}</td></tr>
    </table>
  </div>
  <div class="content">
    <h1>Jeu du Pendu</h1>
    <p><a href="{{ url_for('nouveau') }}">Nouvelle partie</a></p>

    <pre>{{ potence_ascii }}</pre>

    <p>Mot : <strong>{{ mot_masque }}</strong></p>
    <p>Tentatives restantes : <strong>{{ essais_restants }}</strong> / {{ nb_max_essais }}</p>

    {% if statut == 'en_cours' %}

        <form action="{{ url_for('proposer') }}" method="post">
            <table id="lettres">
                <tr>
                    <td><input name="lettre" type="submit" value="a"></td>
                    <td><input name="lettre" type="submit" value="b"></td>
                    <td><input name="lettre" type="submit" value="c"></td>
                    <td><input name="lettre" type="submit" value="d"></td>
                    <td><input name="lettre" type="submit" value="e"></td>
                    <td><input name="lettre" type="submit" value="f"></td>
                    <td><input name="lettre" type="submit" value="g"></td>
                </tr>
                <tr>
                    <td><input name="lettre" type="submit" value="h"></td>
                    <td><input name="lettre" type="submit" value="i"></td>
                    <td><input name="lettre" type="submit" value="j"></td>
                    <td><input name="lettre" type="submit" value="k"></td>
                    <td><input name="lettre" type="submit" value="l"></td>
                    <td><input name="lettre" type="submit" value="m"></td>
                    <td><input name="lettre" type="submit" value="n"></td>
                </tr>
                <tr>
                    <td><input name="lettre" type="submit" value="o"></td>
                    <td><input name="lettre" type="submit" value="p"></td>
                    <td><input name="lettre" type="submit" value="q"></td>
                    <td><input name="lettre" type="submit" value="r"></td>
                    <td><input name="lettre" type="submit" value="s"></td>
                    <td><input name="lettre" type="submit" value="t"></td>
                    <td><input name="lettre" type="submit" value="u"></td>
                </tr>
                <tr>
                    <td><input name="lettre" type="submit" value="v"></td>
                    <td><input name="lettre" type="submit" value="w"></td>
                    <td><input name="lettre" type="submit" value="x"></td>
                    <td><input name="lettre" type="submit" value="y"></td>
                    <td><input name="lettre" type="submit" value="z"></td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        </form>

    {% elif statut == 'gagne' %}
        <p>Bravo ! Vous avez gagné. Le mot était : <strong>{{ mot }}</strong></p>
    {% else %}
        <p>Dommage ! Vous avez perdu. Le mot était : <strong>{{ mot }}</strong></p>
    {% endif %}

    <p>Lettres essayées : {{ lettres_trouvees|join(', ') if lettres_trouvees else '—' }}</p>
  </div>
</body>
</html>
"""

GABARIT_HTML_ACCUEIL = r"""
<!doctype html>
<html lang="fr">
<head>
 <meta charset="utf-8">
 <title>Pendu</title>
 <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div class="content" id="accueil">
  <h1 class="title">Jeu du pendu - Accueil</h1>
  <p>Bienvenue !<p>

  <form action="/demarrer" method="post">
    <label>Entrez votre nom: <input type="text" id="nom" name="nom" autofocus/></label>
    <button type="submit">Démarrer</button>
  </form>
  </div>
  
</body>
</html>
"""

if __name__ == "__main__":
    appli.run(debug=True)