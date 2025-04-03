# import pandas as pd
# from flask import Flask, request, jsonify
# import joblib
# from flask_cors import CORS
# import ast

# app = Flask(__name__)
# CORS(app)

# # Load content model parts
# cosine_sim, content_ids, content_index = joblib.load("content_model.sav")

# # Load article metadata
# articles = pd.read_csv("shared_articles.csv")
# articles = articles[articles['eventType'] == 'CONTENT SHARED']

# # Load user interactions
# interactions = pd.read_csv("users_interactions.csv")

# # Load pre-computed collaborative recommendations
# try:
#     collaborative_recommendations_df = pd.read_csv("collaborative_recommendations.csv")
#     print("✅ Pre-computed collaborative recommendations loaded successfully.")
# except Exception as e:
#     print(f"❌ Error loading collaborative recommendations: {e}")
#     collaborative_recommendations_df = None

# # --- Content-Based Recommender: Based on a given article ---
# def get_similar_articles(content_id, top_n=5):
#     try:
#         content_id = int(content_id)
#         if content_id not in content_index:
#             return [{"error": f"Content ID {content_id} not found"}]
#         idx = content_index[content_id]
#         sim_scores = list(enumerate(cosine_sim[idx]))
#         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#         # Get top N similar articles excluding itself
#         top_indices = [i for i, _ in sim_scores[1:top_n+1]]
#         top_ids = content_ids.iloc[top_indices].values
#         article_info = articles[articles['contentId'].isin(top_ids)][['contentId', 'title', 'text']]
#         result = [
#             {
#                 'contentId': int(row['contentId']),
#                 'title': row['title'],
#                 'summary': row['text'][:200] + '...'
#             }
#             for cid in top_ids
#             for _, row in article_info[article_info['contentId'] == cid].iterrows()
#         ]
#         return result
#     except Exception as e:
#         return [{"error": str(e)}]

# # --- Collaborative Filtering Recommender: Based on pre-computed data using contentId to find users ---
# def get_collaborative_recommendations(content_id, top_n=5):
#     global collaborative_recommendations_df
#     try:
#         content_id = int(content_id)

#         # Find users who have interacted with the given contentId
#         user_ids = interactions[interactions['contentId'] == content_id]['personId'].unique()

#         if collaborative_recommendations_df is not None and len(user_ids) > 0:
#             all_recs = pd.DataFrame()
#             for user_id in user_ids:
#                 # Ensure user_id is a float to match the CSV
#                 user_id = float(user_id)
#                 # Filter for the given user
#                 user_recs = collaborative_recommendations_df[collaborative_recommendations_df['userId'] == user_id].sort_values(by='rank').head(top_n)
#                 if not user_recs.empty:
#                     all_recs = pd.concat([all_recs, user_recs])

#             if not all_recs.empty:
#                 # Aggregate and get top N recommended item IDs
#                 top_content_ids = all_recs['recommendedItemId'].unique()[:top_n]

#                 # Fetch article info for the top content IDs
#                 article_info = articles[articles['contentId'].isin(top_content_ids)][['contentId', 'title', 'text']]

#                 # Prepare the result
#                 result = [
#                     {
#                         'contentId': int(row['contentId']),
#                         'title': row['title'],
#                         'summary': row['text'][:200] + '...'
#                     }
#                     for cid in top_content_ids
#                     for _, row in article_info[article_info['contentId'] == cid].iterrows()
#                 ]
#                 return result
#             else:
#                 return [{"error": f"No pre-computed recommendations found for any users who interacted with content {content_id}"}]
#         else:
#             return [{"error": "Pre-computed recommendations not loaded or no users interacted with this content"}]
#     except Exception as e:
#         return [{"error": str(e)}]

# # --- Routes ---
# @app.route("/recommend/content", methods=["GET"])
# def recommend_content():
#     content_id = request.args.get("contentId")
#     if not content_id:
#         return jsonify({"error": "Missing contentId"}), 400
#     recommendations = get_similar_articles(content_id)
#     return jsonify(recommendations)

# @app.route("/recommend/collaborative", methods=["GET"])
# def recommend_collaborative():
#     content_id = request.args.get("contentId")
#     if not content_id:
#         return jsonify({"error": "Missing contentId"}), 400
#     recommendations = get_collaborative_recommendations(content_id)
#     return jsonify(recommendations)

# if __name__ == "__main__":
#     app.run(debug=True)

import pandas as pd
from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
import ast

app = Flask(__name__)
CORS(app)

# Load content model parts
cosine_sim, content_ids, content_index = joblib.load("content_model.sav")

# Load article metadata
articles = pd.read_csv("shared_articles.csv")
articles = articles[articles['eventType'] == 'CONTENT SHARED']

# Load user interactions
interactions = pd.read_csv("users_interactions.csv")

# Load pre-computed collaborative recommendations
try:
    collaborative_recommendations_df = pd.read_csv("collaborative_recommendations.csv")
    print("✅ Pre-computed collaborative recommendations loaded successfully.")
except Exception as e:
    print(f"❌ Error loading collaborative recommendations: {e}")
    collaborative_recommendations_df = None

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

# --- Collaborative Filtering Recommender: Based on pre-computed data using contentId to find users ---
def get_collaborative_recommendations(content_id, top_n=5):
    global collaborative_recommendations_df
    try:
        content_id = int(content_id)

        # Find users who have interacted with the given contentId
        user_ids = interactions[interactions['contentId'] == content_id]['personId'].unique()

        if collaborative_recommendations_df is not None and len(user_ids) > 0:
            all_recs = pd.DataFrame()
            for user_id in user_ids:
                # Ensure user_id is a float to match the CSV
                user_id = float(user_id)
                # Filter for the given user
                user_recs = collaborative_recommendations_df[collaborative_recommendations_df['userId'] == user_id].sort_values(by='rank').head(top_n)
                if not user_recs.empty:
                    all_recs = pd.concat([all_recs, user_recs])

            if not all_recs.empty:
                # Aggregate and get top N recommended item IDs
                top_content_ids = all_recs['recommendedItemId'].unique()[:top_n]

                # Fetch article info for the top content IDs
                article_info = articles[articles['contentId'].isin(top_content_ids)][['contentId', 'title', 'text']]
                if article_info.empty:
                     return [{"error": f"Article info not found for  {top_content_ids}"}]
                # Prepare the result
                result = [
                    {
                        'contentId': int(row['contentId']),
                        'title': row['title'],
                        'summary': row['text'][:200] + '...'
                    }
                    for cid in top_content_ids
                    for _, row in article_info[article_info['contentId'] == cid].iterrows()
                ]
                return result
            else:
                return [{"error": f"No pre-computed recommendations found for any users who interacted with content {content_id}"}]
        else:
            return [{"error": "Pre-computed recommendations not loaded or no users interacted with this content"}]
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
    content_id = request.args.get("contentId")
    if not content_id:
        return jsonify({"error": "Missing contentId"}), 400
    recommendations = get_collaborative_recommendations(content_id)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
