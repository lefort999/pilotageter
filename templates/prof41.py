
from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 🔹 Fonction utilitaire
def lire_texte(nom_fichier):
    """Lit le contenu d'un fichier texte."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return "⚠️ Information non disponible."

# 🔹 Route principale
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Traitement du formulaire d’analyse
@app.route("/analyse", methods=["POST"])
def analyse():
    msg = []

    # 🔎 Extraction des données du formulaire
    prof = request.form.get("profession", "").lower()
    naissance = request.form.get("naissance", type=int)
    lieu = request.form.get("lieu_naissance", "").lower()

    # ✅ Récupération des caractéristiques (select multiple)
    caracteristiques = request.form.getlist("caracteristiques")
    militaire = "militaire" in caracteristiques
    blesse = "blesse" in caracteristiques
    officier = "officier" in caracteristiques
    celibataire = "celibataire" in caracteristiques
    etatcivil = "etatcivil" in caracteristiques

    # 📚 Récupération des mots-clés documentaires (select multiple)
    doc_keywords = request.form.getlist("documentation")

    # 📜 Analyse des règles généalogiques
    if prof == "douanier" and naissance and 1760 < naissance < 1810:
        msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

    if "alsace" in lieu and naissance and 1870 < naissance < 1918:
        msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

    if prof == "orfèvre":
        msg.append("💎 Orfèvre : consulter les registres de poinçons.")

    if militaire or blesse or officier:
        msg.append("🎖️ Militaire blessé/officier : consulter les registres militaires.")

    if celibataire and etatcivil:
        msg.append("📜 Célibataire avec acte complet : voir actes notariés et mentions marginales.")

    

# 🔹 Exécution de l’application Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)