import React from "react";
import BarChart from "./BarChart";
import useFetchData from "../hooks/useFetchData";
import ErrorMessage from "./common/ErrorMessage";
import LoadingSpinner from "./common/LoadingSpinner";

const DataFetcher = () => {
  const { data, error, loading } = useFetchData(
    "http://localhost:8000/trade/"
  );

  // Show loading spinner while data is fetching
  if (loading) return <LoadingSpinner />;

  // Show error box if eny error comes from data fetching
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      {
        data.symbolTradeEvents.map(({ labels, dataset }, index) =>
          <BarChart key={index} labels={labels} dataset={dataset} />
        )
      }
    </div>
  )
  // return <BarChart labels={data.labels} datasets={data.datasets} />;
};

export default React.memo(DataFetcher);
