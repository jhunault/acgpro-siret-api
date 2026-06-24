from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def siret():
    nom = request.args.get("nom", "")
    cp = request.args.get("cp", "")

    if nom == "" or cp == "":
        return "Paramètres manquants"

    url = f"https://api.annuaire-entreprises.data.gouv.fr/search?q={nom}&code_postal={cp}"
    r = requests.get(url)
    data = r.json()

    try:
        siret = data["results"][0]["siret"]
        return siret
    except:
        return "Aucun résultat"

@app.route("/health")
def health():
    return "OK"
