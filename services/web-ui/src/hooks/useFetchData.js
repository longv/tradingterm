import { useState, useEffect, useCallback } from "react";
import _ from "lodash";
import axios from "axios";

const useFetchData = (url) => {
  const [data, setData] = useState({
    symbolTradeEvents: [],
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  /**
   * fetchData
   *
   * Asynchronously fetches chartData from the API and updates the state with the labels and values.
   */
  const fetchData = useCallback(async () => {
    setLoading(true);

    try {
      const response = await axios.get(url);

      const processed = _.chain(response.data)
        .groupBy("symbol")
        .map((items, symbol) => ({
          labels: _.map(items, "timestamp"),
          dataset: {
            label: symbol,
            data: _.map(items, "ema")
          }
        }))
        // .reduce((acc, item) => {
        //   acc.labels = _.union(acc.labels, item.labels); // Merge unique labels
        //   acc.datasets.push(item.dataset); // Add dataset to datasets array
        //   return acc;
        // }, { labels: [], datasets: [] })
        .value()

      setData({ symbolTradeEvents: processed });
    } catch (error) {
      setError("Error fetching chartData");
    } finally {
      setLoading(false);
    }
  }, [url]);

  // Fetch chartData when the component mounts
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, error, loading };
};

export default useFetchData;
