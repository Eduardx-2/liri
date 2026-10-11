from flask import Flask, request, jsonify
from back_api import ApisSession

app = Flask(__name__)


@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/api/consulta/number", methods=["POST", "OPTIONS"])
def main_session():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    numero = data.get("numero")
    if isinstance(numero, str) and len(numero) == 8:
        return jsonify(ApisSession().data_response(data))
    return jsonify({"errorLong": "Longitud incorrecta: 8 digitos longitud correcta"}), 500


if __name__ == "__main__":
    app.run(use_reloader=False, port=9081)
