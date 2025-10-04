from flask import Flask, request, jsonify, render_template
import pickle

# === Load Model ===
with open("phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

# === Inisialisasi Flask ===
app = Flask(__name__)

# === Route untuk Home ===
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# === Route untuk Prediksi ===
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        email_text = data.get("email_text", "")

        if not email_text:
            return jsonify({"error": "Field 'email_text' is required"}), 400

        # Prediksi
        prediction = model.predict([email_text])[0]
        probas = model.predict_proba([email_text])[0]

        # 0 = Phishing, 1 = Safe (sesuai label encoding tadi)
        label_map = {0: "Phishing Email", 1: "Safe Email"}
        result = {
            "prediction": label_map[prediction],
            "probability": {
                "Phishing Email": float(probas[0]),
                "Safe Email": float(probas[1])
            }
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Main ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
