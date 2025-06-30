from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse():
    msg = []

    prof = request.form.get("profession", "").lower()
    naissance = request.form.get("naissance", type=int)
    lieu = request.form.get("lieu_naissance", "").lower()
    militaire = "militaire" in request.form
    blesse = "blesse" in request.form
    officier = "officier" in request.form
    celibataire = "celibataire" in request.form
    etatcivil = "etatcivil" in request.form

    # Exemple de quelques règles simples
    if prof == "douanier" and naissance and 1760 < naissance < 1810:
        msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

    if "alsace" in lieu and naissance and 1870 < naissance < 1918:
        msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : administration prussienne, consulter ANOM ou archives allemandes.")

    if prof == "orfèvre":
        msg.append("💎 Orfèvre : consulter les registres de poinçons (Minerve, Coq, Vieillard).")

    if militaire and officier and blesse:
        msg.append("🎖️ Militaire blessé/officier : consulter les états de service ou registres de pensions militaires.")

    if celibataire and etatcivil:
        msg.append("📜 Célibataire avec état civil complet : regarder les mentions marginales et les actes notariés.")

    if not msg:
        msg.append("🤷 Aucune règle déclenchée. Essayez d’élargir ou croiser d'autres critères.")

    return render_template("index.html", message="<br>".join(msg))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)