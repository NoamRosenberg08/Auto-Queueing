import { useState } from "react";
import "./App.css";
import MatchView from "./components/match/MatchView";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <MatchView
        matchNumber={1}
        blueAlliance={[2230, 4590, 3211]}
        redAlliance={[11001, 11011, 20119]}
      />

      <MatchView
        matchNumber={2}
        blueAlliance={[11011, 2230, 3211]}
        redAlliance={[4590, 11011, 20119]}
      />
    </>
  );
}

export default App;
