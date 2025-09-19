from flask import Flask, render_template, request

app = Flask(__name__)


mot_a_trouver = "arc"

mot_en_cours = "___"

mot_evolutif = "b"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    if request.method == "POST":
        mon_champ = request.form["mon_champ"]
        print(mon_champ)
    
    return render_template("play.html", nom=mon_champ, mot=mot_en_cours)

@app.route("/test")
def test():
    return render_template("test.html")



@app.route("/a")
def a():
    f = open("templates/play.html")

    mot_du_pendu = "___"

    mon_html = f.read()
    index_debut_de_balise = mon_html.find("id=\"pendu\"") + len("id=\"pendu\">")
    j = 0
    current_mot = ""
    while j < len("{{ mot }}"):
        current_mot += mon_html[index_debut_de_balise + j]
        j += 1
    print("1ere méthode: " + current_mot)

    index_fin_de_balise = mon_html.find('<', index_debut_de_balise)

    print("2eme méthode: " + mon_html[index_debut_de_balise:index_fin_de_balise])
    
    global mot_evolutif
    mot_evolutif += 'a'

    return render_template("play.html", mot=mot_evolutif)


mot_en_cours = "_____"

def ma_fonction():

    mot_en_cours = 'a' + mot_en_cours[1:]

