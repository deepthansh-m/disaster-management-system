import React from "react";
import DisasterDetails from "../components/DisasterDetails";

function DetailsPage({ disasterData }) {
    return (
        <div className="details-page">
            <h2>Disaster Details</h2>
            <DisasterDetails data={disasterData} />
        </div>
    );
}

export default DetailsPage;
