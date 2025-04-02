// src/components/RecommendationForm.tsx
import React, { useState, FormEvent } from "react";
import axios from "axios";

// Define the types for the recommendations
interface RecommendationResponse {
  collab: string[];
  content: string[];
  azure: string[];
}

const RecommendationForm: React.FC = () => {
  const [id, setId] = useState<string>("");
  const [collabRecommendations, setCollabRecommendations] = useState<string[]>(
    []
  );
  const [contentRecommendations, setContentRecommendations] = useState<
    string[]
  >([]);
  const [azureRecommendations, setAzureRecommendations] = useState<string[]>(
    []
  );
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Make requests to the backend
      const response = await axios.post<RecommendationResponse>(
        "http://127.0.0.1:5000/recommend",
        { id }
      );
      setCollabRecommendations(response.data.collab);
      setContentRecommendations(response.data.content);
      setAzureRecommendations(response.data.azure);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h1>Recommender System</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="id">Enter User or Item ID:</label>
        <input
          type="text"
          id="id"
          value={id}
          onChange={(e) => setId(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          Get Recommendations
        </button>
      </form>

      {loading && <p>Loading...</p>}

      {!loading && (
        <div>
          <h2>Collaborative Filtering Recommendations:</h2>
          <ul>
            {collabRecommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Content Filtering Recommendations:</h2>
          <ul>
            {contentRecommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Azure ML Endpoint Recommendations:</h2>
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
