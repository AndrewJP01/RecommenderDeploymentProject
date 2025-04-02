from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS  # Allows frontend to call the API

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load saved models (Add these files later)
collab_model = joblib.load("collaborative_model.sav")
content_model = joblib.load("content_model.sav")

def get_recommendations(model, user_id):
    # Dummy logic: Replace with actual model prediction later
    return [f"article_{i}" for i in np.random.choice(range(100), 5, replace=False)]

@app.route("/recommend/collaborative", methods=["GET"])
def recommend_collaborative():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    recommendations = get_recommendations(collab_model, user_id)
    return jsonify(recommendations)

@app.route("/recommend/content", methods=["GET"])
def recommend_content():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    recommendations = get_recommendations(content_model, user_id)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
