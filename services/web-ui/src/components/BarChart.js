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
import "../styles/BarChart.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

/**
 * BarChart Component
 *
 * This component renders a bar chart using Chart.js with the provided labels and values.
 *
 * Props:
 * - labels: Array of strings representing the labels for the x-axis.
 * - values: Array of numbers representing the values for each label.
 */

const BarChart = ({ labels, dataset }) => {
  // Handle empty data case
  if (!labels.length) return null;

  // This is the chart data structure
  const chartData = {
    labels: labels,
    datasets: [dataset],

    // [
    //   {
    //     label: "Values",
    //     data: values, // Array of values for the dataset
    //     backgroundColor: "#007bff", // Here can be changed color of the bars
    //   },
    // ],
  };
  // const data = {
  //   labels: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
  //   datasets: [{
  //     label: 'My First Dataset',
  //     data: [65, 59, 80, 81, 56, 55, 40],
  //     fill: false,
  //     borderColor: 'rgb(75, 192, 192)',
  //     tension: 0.1
  //   }]
  // };

  return (
    <div className="barchart-container">
      <Line data={chartData} />
    </div>
  );
};

export default BarChart;
