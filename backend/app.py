from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load content model parts
cosine_sim, content_ids, content_index = joblib.load("content_model.sav")

# Load article metadata
articles = pd.read_csv("shared_articles.csv")
articles = articles[articles['eventType'] == 'CONTENT SHARED']

# --- Content-Based Recommender: Based on a given article ---
def get_similar_articles(content_id, top_n=5):
    try:
        content_id = int(content_id)

        if content_id not in content_index:
            return [{"error": f"Content ID {content_id} not found"}]

        idx = content_index[content_id]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top N similar articles excluding itself
        top_indices = [i for i, _ in sim_scores[1:top_n+1]]
        top_ids = content_ids.iloc[top_indices].values

        article_info = articles[articles['contentId'].isin(top_ids)][['contentId', 'title', 'text']]

        result = [
            {
                'contentId': int(row['contentId']),
                'title': row['title'],
                'summary': row['text'][:200] + '...'
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
    content_id = request.args.get("contentId")
    if not content_id:
        return jsonify({"error": "Missing contentId"}), 400
    recommendations = get_similar_articles(content_id)
    return jsonify(recommendations)

@app.route("/recommend/collaborative", methods=["GET"])
def recommend_collaborative():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    return jsonify(["stub1", "stub2", "stub3", "stub4", "stub5"])

if __name__ == "__main__":
    app.run(debug=True)
