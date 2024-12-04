import React from "react";

function DisasterDetails({ data }) {
    if (!data) {
        return <p>No data available.</p>;
    }

    return (
        <div className="disaster-details">
            <h3>{data.name}</h3>
            <p>Location: {data.location}</p>
            <p>Severity: {data.severity}</p>
            <p>Description: {data.description}</p>
        </div>
    );
}

export default DisasterDetails;
