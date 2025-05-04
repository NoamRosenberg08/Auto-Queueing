import { useEffect, useState } from "react";
import "./QueueAlerting.css";

function QueueAlert() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/team/should_queue");
        const result = await response.json();
        setData(result); // Refresh the entire object with new data
      } catch (error) {
        console.error("Error fetching or parsing data:", error);
      }
    };

    // Fetch data initially
    fetchData();

    // Set up an interval to fetch data every 5 seconds (5000ms)
    const intervalId = setInterval(fetchData, 2500);

    // Clean up the interval when the component unmounts
    return () => {
      clearInterval(intervalId);
    };
  }, []); // Empty dependency array ensures the effect runs only once on mount

  if (data === null) {
    return <div className="queue-alert">Loading...</div>;
  }

  // Render different content based on the data
  if (data["should_queue"] === "True") {
    return <div className="box queueing-time">QUEUE!</div>;
  } else {
    return <div className="box resting-time">NO QUEUE!</div>;
  }
}

export default QueueAlert;
