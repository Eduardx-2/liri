"""Sirve el front estático de LIRI. El backend real lo conecta Eduardo después."""
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

ROOT = Path(__file__).resolve().parent
STATIC = {"index.html", "styles.css", "script.js", "api.js", "logo.png"}

app = Flask(__name__)


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:name>")
def archivo(name):
    if name not in STATIC:
        return ("", 404)
    return send_from_directory(ROOT, name)


@app.post("/api/number/data")
def number_data():
    # Stub hasta que exista el backend. Con USAR_PRUEBAS=true el front
    # no llega acá en los 4 números de prueba.
    return jsonify({
        "errorNumero": "Backend aún no conectado."
    }), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
