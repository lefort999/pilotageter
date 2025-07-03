import os
from flask import Flask, request, render_template

app = Flask(__name__)

def lire_texte(nom_fichier):
    """Lit le contenu d'un fichier texte."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return "Information non disponible."

@app.route("/")
def recherche():
    return render_template("index.html")

@app.route("/profession", methods=["GET", "POST"])
def profession():
    message = ""
    if request.method == "POST":
        prof = request.form.get("profession", "").lower()
        naissance = request.form.get("naissance", "")
        lieu = request.form.get("lieu", "").lower()
        msg = []

        # Récupérer texte principal selon la profession
        if prof in ["militaire", "fisc", "cadastre", "police", "notaire", "enregistrement"]:
            msg.append(f"Cette rubrique concerne le : {prof}. {lire_texte(prof + '.txt')}")
        else:
            msg.append(f"Cette rubrique n'existe pas : {prof}.")

        # Traitement des règles additionnelles
        try:
            naissance = int(naissance)
        except ValueError:
            naissance = None  # Si vide ou invalide

        if prof == "douanier" and naissance and 1760 < naissance < 1810:
            msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

        if "alsace" in lieu and naissance and 1870 < naissance < 1918:
            msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

        message = "<br>".join(msg)

    return render_template("index.html", message=message)
🪄 Suggestions bonus

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render attribue automatiquement un port
    app.run(host="0.0.0.0", port=port)
