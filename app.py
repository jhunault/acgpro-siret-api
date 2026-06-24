from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def siret():
    nom = request.args.get("nom", "")
    cp = request.args.get("cp", "")

    url = f"https://api.annuaire-entreprises.data.gouv.fr/search?q={nom}&code_postal={cp}"
    r = requests.get(url)

    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
