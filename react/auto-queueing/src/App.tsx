import { useState } from "react";
import "./App.css";
import TeamNumber from "./components/match/TeamNumber";

function App() {
  const [count, setCount] = useState(0);

  return <TeamNumber teamNumber={4590} />;
}

export default App;
