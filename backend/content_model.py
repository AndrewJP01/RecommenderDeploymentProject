import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load your data
interactions = pd.read_csv('users_interactions.csv')
articles = pd.read_csv('shared_articles.csv')

# Filter only shared articles
# Filter only shared articles
articles = articles[articles['eventType'] == 'CONTENT SHARED'].reset_index(drop=True)

# TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(articles['text'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Mapping
content_ids = articles['contentId']
content_index = pd.Series(articles.index, index=articles['contentId'])  # this is now 0 to len(articles)

# Save
joblib.dump((cosine_sim, content_ids, content_index), 'content_model.sav')

