import React from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

// Register necessary Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function DisasterPredictionChart() {
    // Sample data for the chart
    const data = {
        labels: ["2020", "2021", "2022", "2023", "2024"], // X-axis labels
        datasets: [
            {
                label: "Predicted Disasters",
                data: [5, 10, 7, 12, 15], // Replace with dynamic data
                borderColor: "rgba(75, 192, 192, 1)", // Line color
                backgroundColor: "rgba(75, 192, 192, 0.2)", // Fill under the line
                tension: 0.4, // Smooth line
            },
            {
                label: "Past Disasters",
                data: [4, 8, 6, 10, 14], // Replace with dynamic data
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                tension: 0.4,
            },
        ],
    };

    // Chart options
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: "Disaster Prediction Chart",
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: "Year",
                },
            },
            y: {
                title: {
                    display: true,
                    text: "Number of Disasters",
                },
                beginAtZero: true,
            },
        },
    };

    return (
        <div className="prediction-chart">
            <Line data={data} options={options} />
        </div>
    );
}

export default DisasterPredictionChart;
