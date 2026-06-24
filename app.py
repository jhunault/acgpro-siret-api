from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def siret():
    nom = request.args.get("nom", "").strip()
    cp = request.args.get("cp", "").strip()

    if not nom or not cp:
        return "Paramètres manquants"

    url = f"https://api.annuaire-entreprises.data.gouv.fr/search?q={nom}&code_postal={cp}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        return f"Erreur de requête API : {e}"
    except ValueError:
        return "Erreur de décodage JSON"

    results = data.get("results", [])
    if not results:
        return "Aucun résultat"

    siret = results[0].get("siret")
    if not siret:
        return "SIRET non trouvé"

    return siret

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
