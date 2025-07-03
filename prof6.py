import os
from flask import Flask, request, render_template

app = Flask(__name__)


def profession():
    message = ""
    if request.method == "POST":
        prof = request.form.get("profession", "").lower()
        naissance = request.form.get("naissance", "")
        lieu = request.form.get("lieu", "").lower()
        msg = []

        # 👉 Ici, mets cette condition :
        if prof in ["militaire", "fisc", "cadastre", "police", "notaire", "enregistrement", "douanier"]:
            msg.append(f"Cette rubrique concerne le : {prof}. {lire_texte(prof + '.txt')}")
        else:
            msg.append(f"Cette rubrique n'existe pas : {prof}.")

        # 🎯 Et ensuite, les règles spéciales :
        try:
            naissance = int(naissance)
        except ValueError:
            naissance = None

        if prof == "douanier" and naissance and 1760 < naissance < 1810:
            msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

        if "alsace" in lieu and naissance and 1870 < naissance < 1918:
            msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

        message = "<br>".join(msg)

    return render_template("index.html", message=message)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render attribue automatiquement un port
    app.run(host="0.0.0.0", port=port)
