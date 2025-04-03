import React, { useState, FormEvent } from "react";
import axios from "axios";

interface Recommendation {
  contentId: number;
  title: string;
  summary: string;
}

const RecommendationForm: React.FC = () => {
  const [contentId, setContentId] = useState<string>("");
  const [contentRecommendations, setContentRecommendations] = useState<
    Recommendation[]
  >([]);
  const [collabRecommendations, setCollabRecommendations] = useState<string[]>(
    []
  );
  const [azureRecommendations, setAzureRecommendations] = useState<string[]>(
    []
  );
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Fetch content-based recommendations
      const contentResponse = await axios.get<Recommendation[]>(
        `http://127.0.0.1:5000/recommend/content?contentId=${contentId}`
      );
      setContentRecommendations(contentResponse.data);

      // Fetch collaborative recommendations (using a hardcoded user ID for now)
      const collabResponse = await axios.get<string[]>(
        `http://127.0.0.1:5000/recommend/collaborative?userId=123` // Using a default user ID
      );
      setCollabRecommendations(collabResponse.data);

      // Set Azure ML recommendations to a default message since there's no actual endpoint
      setAzureRecommendations(["No Azure ML recommendations available."]);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Recommender System</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="contentId">Enter Content ID:</label>
        <input
          type="text"
          id="contentId"
          value={contentId}
          onChange={(e) => setContentId(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          Get Recommendations
        </button>
      </form>

      {loading && <p>Loading...</p>}

      {!loading && (
        <div>
          {/* Content Recommendations */}
          <h2>Content Recommendations:</h2>
          <ul>
            {contentRecommendations.map((item) => (
              <li key={item.contentId}>
                <strong>{item.title}</strong>
                <p>{item.summary}</p>
              </li>
            ))}
          </ul>

          {/* Collaborative Recommendations */}
          <h2>Collaborative Recommendations:</h2>
          <ul>
            {collabRecommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          {/* Azure ML Recommendations */}
          <h2>Azure ML Recommendations (Placeholder):</h2>
          <ul>
            {azureRecommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RecommendationForm;
