import React, { useState, useEffect } from "react";
import "./TimeDisplay.css";

function TimeDisplay() {
  const [time, setTime] = useState<string>("");

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div className="time">{time}</div>;
}

export default TimeDisplay;
