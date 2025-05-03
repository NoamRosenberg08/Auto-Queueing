import { useEffect, useState } from "react";
import "./QueueAlerting.css";

function QueueAlert() {
  const [data, setData] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/team/should_queue");
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching or parsing data:", error);
      }
    };

    fetchData();
  }, []);

  if (data === null) {
    return <div className="queue-alert">Loading...</div>;
  }
  if (data["should_queue"] === "True") {
    return <div className="box queueing-time">QUEUE!</div>;
  } else {
    return <div className="box resting-time">NO QUEUE!</div>;
  }
}

export default QueueAlert;
