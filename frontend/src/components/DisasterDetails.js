import React from "react";

function DisasterDetails({ data }) {
    // Check if data is available, if not display a message
    if (!data) {
        return <p>No data available.</p>;
    }

    return (
        <div className="disaster-details">
            <h3>{data.name}</h3> {/* Display disaster name */}
            <p><strong>Location:</strong> {data.location}</p> {/* Display location */}
            <p><strong>Severity:</strong> {data.severity}</p> {/* Display severity level */}
            <p><strong>Description:</strong> {data.description}</p> {/* Display description */}
        </div>
    );
}

export default DisasterDetails;
