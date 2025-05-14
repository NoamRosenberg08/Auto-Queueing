import { useEffect, useState } from "react";
import MatchView from "./MatchView";

interface MatchData {
  [matchNumber: number]: number[];
}

function MatchList() {
  const [matchData, setMatchData] = useState<MatchData>({});
  const [currentMatchNumber, setCurrentMatchNumber] = useState<number | null>(
    null
  );

  useEffect(() => {
    const fetchData = () => {
      fetch("http://localhost:5000/schedule/team")
        .then((res) => res.json())
        .then((data) => setMatchData(data))
        .catch((err) => console.error("Failed to fetch match data:", err));

      fetch("http://localhost:5000/match/number")
        .then((res) => res.json())
        .then((data) =>
          data.MatchNumber == -1
            ? console.log("no match number")
            : setCurrentMatchNumber(data.MatchNumber)
        )
        .catch((err) =>
          console.error("Failed to fetch current match number:", err)
        );
    };

    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 1000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <div className="match-list">
      {Object.entries(matchData)
        .filter(([matchNumberStr]) =>
          currentMatchNumber === null
            ? true
            : Number(matchNumberStr) >= currentMatchNumber
        )
        .sort(([a], [b]) => Number(a) - Number(b))
        .map(([matchNumberStr, teams]) => {
          const matchNumber = Number(matchNumberStr);
          const redAlliance = teams.slice(0, 3);
          const blueAlliance = teams.slice(3, 6);

          return (
            <MatchView
              key={matchNumber}
              matchNumber={matchNumber}
              redAlliance={redAlliance}
              blueAlliance={blueAlliance}
            />
          );
        })}
    </div>
  );
}

export default MatchList;
