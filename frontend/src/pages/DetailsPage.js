import React from "react";
import { useLocation } from "react-router-dom";

function DetailsPage() {
  const location = useLocation();
  const disasterData = location.state?.prediction;

  if (!disasterData) {
    return <div>No data available. Please try again.</div>;
  }

  return (
    <div className="details-page">
      <h2>Disaster Prediction Details</h2>
      <p><strong>Location:</strong> {disasterData.region || "N/A"}</p>
      <p><strong>Disaster Type:</strong> {disasterData.result || "N/A"}</p>
      <p><strong>Confidence:</strong> {disasterData.confidence || "N/A"}</p>
      <p><strong>Rainfall:</strong> {disasterData.parameters?.rainfall || "N/A"}</p>
      <p><strong>Temperature:</strong> {disasterData.parameters?.temperature || "N/A"}</p>
    </div>
  );
}

export default DetailsPage;
