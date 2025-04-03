import React, { useState, FormEvent } from "react";
import axios from "axios";

interface Recommendation {
  contentId: number;
  title: string;
  summary: string;
}

interface ErrorResponse {
  error: string;
}

type RecommendationResponse = Recommendation[] | ErrorResponse[];

const RecommendationForm: React.FC = () => {
  const [contentId, setContentId] = useState<string>("");
  const [contentRecommendations, setContentRecommendations] =
    useState<RecommendationResponse>([]);
  const [collabRecommendations, setCollabRecommendations] =
    useState<RecommendationResponse>([]);
  const [azureRecommendations, setAzureRecommendations] = useState<string[]>(
    []
  );
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Fetch content-based recommendations
      const contentResponse = await axios.get<RecommendationResponse>(
        `http://127.0.0.1:5000/recommend/content?contentId=${contentId}`
      );
      setContentRecommendations(contentResponse.data);

      // Fetch collaborative recommendations
      const collabResponse = await axios.get<RecommendationResponse>(
        `http://127.0.0.1:5000/recommend/collaborative?contentId=${contentId}`
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

  const renderRecommendations = (
    recommendations: RecommendationResponse,
    title: string
  ) => {
    if (Array.isArray(recommendations) && recommendations.length > 0) {
      if ("error" in recommendations[0]) {
        // Error response
        return (
          <div>
            <h2>{title}</h2>
            <p>{recommendations[0].error}</p>
          </div>
        );
      }

      // Recommendations array
      return (
        <div>
          <h2>{title}</h2>
          <ul>
            {recommendations.map(
              (item) =>
                // Type guard to check if the item is a Recommendation
                "contentId" in item ? (
                  <li key={item.contentId}>
                    <strong>{item.title}</strong>
                    <p>{item.summary}</p>
                  </li>
                ) : null // If it's an ErrorResponse, do nothing
            )}
          </ul>
        </div>
      );
    }

    return null;
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
          {renderRecommendations(
            contentRecommendations,
            "Content Recommendations"
          )}
          {renderRecommendations(
            collabRecommendations,
            "Collaborative Recommendations"
          )}

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
