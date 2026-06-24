from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def siret():
    # Récupération des paramètres
    nom = request.args.get("nom", "").strip()
    cp = request.args.get("cp", "").strip()

    # Vérification des paramètres
    if not nom or not cp:
        return "Paramètres manquants"

    # Appel de l'API publique Annuaire Entreprises
    url = f"https://api.annuaire-entreprises.data.gouv.fr/search?q={nom}&code_postal={cp}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except Exception as e:
        return f"Erreur de requête API : {e}"

    # Extraction du premier SIRET trouvé
    results = data.get("results", [])
    if not results:
        return "Aucun résultat"

    siret = results[0].get("siret", "SIRET non trouvé")
    return siret

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
