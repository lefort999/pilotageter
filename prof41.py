from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 🔧 Lecture de texte brut
def lire_texte(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ Fichier non trouvé."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse():
    msg = []

    # 🔍 Champs principaux
    prof = request.form.get("profession", "").lower()
    naissance = request.form.get("naissance", type=int)
    mariage = request.form.get("mariage", type=int)
    deces = request.form.get("deces", type=int)

    lieu_naissance = request.form.get("lieu_naissance", "").lower()
    cp_naissance = request.form.get("cp_naissance", "")
    lieu_mariage = request.form.get("lieu_mariage", "").lower()
    cp_mariage = request.form.get("cp_mariage", "")
    lieu_deces = request.form.get("lieu_deces", "").lower()
    cp_deces = request.form.get("cp_deces", "")

    # 🎛️ Cases à cocher
    caracteristiques = request.form.getlist("caracteristiques")
    documentation = request.form.getlist("documentation")

    # 🧠 Exemples de règles
    if prof == "douanier" and naissance and 1760 < naissance < 1810:
        msg.append("📁 Douanier entre 1760–1810 : voir les Archives nationales (F/12, F/14).")

    if "alsace" in lieu_naissance and naissance and 1870 < naissance < 1918:
        msg.append("🪖 Né en Alsace entre 1870 et 1918 : consulter ANOM ou les archives allemandes.")

    if prof == "orfèvre":
        msg.append("💍 Orfèvre : consulter les registres des poinçons.")

    if "militaire" in caracteristiques and "officier" in caracteristiques and "blesse" in caracteristiques:
        msg.append("🎖️ Militaire blessé et officier : dossier militaire approfondi recommandé.")

    if "etatcivil" in caracteristiques and "celibataire" in caracteristiques:
        msg.append("📜 Célibataire avec acte complet : vérifier les mentions marginales ou notariées.")

    # 📂 Chargement des fichiers documentaires
    for doc in documentation:
        fichier = f"{doc}.txt"
        contenu = lire_texte(fichier).replace("\n", "<br>")
        msg.append(f"📘 <strong>{fichier}</strong><br>{contenu}")

    if not msg:
        msg.append("🤷 Aucune règle détectée.")

    return render_template("index.html", message="<br>".join(msg))

@app.route("/profession", methods=["POST"])
def profession():
    rubrique = request.form.get("lecture", "").lower()
    if rubrique in ["militaire", "fisc", "cadastre", "police", "notaire", "administration", "enigme"]:
        contenu = lire_texte(f"{rubrique}.txt").replace("\n", "<br>")
        message = f"📘 Rubrique : <strong>{rubrique}</strong><br>{contenu}"
    else:
        message = f"❌ Rubrique inconnue : <strong>{rubrique}</strong>"

    return render_template("index.html", lecture_result=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
