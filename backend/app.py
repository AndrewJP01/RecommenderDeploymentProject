from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load content model parts
cosine_sim, content_ids, content_index = joblib.load("content_model.sav")

# Load user interaction data
interactions = pd.read_csv("users_interactions.csv", dtype={'personId': str})

articles = pd.read_csv("shared_articles.csv")
articles = articles[articles['eventType'] == 'CONTENT SHARED']


# Define content-based recommender logic
def get_content_recommendations(user_id, top_n=5):
    try:
        user_id = str(user_id)

        user_data = interactions[interactions['personId'] == user_id]
        user_articles = user_data['contentId'].values

        article_indices = content_index[user_articles].dropna().astype(int)

        if article_indices.empty:
            return []

        sim_scores = cosine_sim[article_indices].mean(axis=0)
        recommendations = np.argsort(sim_scores)[::-1]
        recommended_ids = content_ids.iloc[recommendations].values
        filtered = [int(item) for item in recommended_ids if item not in user_articles]
        top_ids = filtered[:top_n]

        # 🔍 Match article metadata for recommended contentIds
        article_info = articles[articles['contentId'].isin(top_ids)][['contentId', 'title', 'text']]

        # ✅ Build JSON result in correct order
        result = [
            {
                'contentId': int(row['contentId']),
                'title': row['title'],
                'summary': row['text'][:200] + '...'  # Truncate to 200 characters
            }
            for cid in top_ids
            for _, row in article_info[article_info['contentId'] == cid].iterrows()
        ]


        return result
    except Exception as e:
        return [{"error": str(e)}]

# --- Routes ---

@app.route("/recommend/content", methods=["GET"])
def recommend_content():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    recommendations = get_content_recommendations(user_id)
    return jsonify(recommendations)

# Placeholder: collaborative route can stay as-is for now
@app.route("/recommend/collaborative", methods=["GET"])
def recommend_collaborative():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    return jsonify(["stub1", "stub2", "stub3", "stub4", "stub5"])

if __name__ == "__main__":
    app.run(debug=True)
