import { useState } from "react";
import "./App.css";
import MatchView from "./components/match/MatchView";
import QueueAlert from "./components/queue/QueueAlert";
import MatchList from "./components/match/MatchList";
import TimeDisplay from "./components/time/TimeDisplay";
function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div className="main-container">
        <MatchList />
        <div>
          <QueueAlert />
          <TimeDisplay />
        </div>
      </div>
    </>
  );
}

export default App;
