import TeamNumber from "./TeamNumber";
import config from "../../config";
import "./MatchViewing.css";

interface MatchViewProps {
  matchNumber: number;
  blueAlliance: number[];
  redAlliance: number[];
}

function MatchView({ matchNumber, blueAlliance, redAlliance }: MatchViewProps) {
  const isBlueHighlighted = blueAlliance.includes(config.TeamNumber);
  const isRedHighlighted = redAlliance.includes(config.TeamNumber);

  return (
    <div className="match-view">
      <div className="match-number">{matchNumber}</div>

      <div className="alliances">
        <div
          className={`alliance blue-alliance ${
            isBlueHighlighted ? "filled" : "outlined"
          }`}
        >
          {blueAlliance.map((teamNumber, index) => (
            <div
              key={index}
              className={`team-box blue-team ${
                teamNumber === config.TeamNumber ? "highlighted" : ""
              }`}
            >
              <TeamNumber teamNumber={teamNumber} />
            </div>
          ))}
        </div>

        <div
          className={`alliance red-alliance ${
            isRedHighlighted ? "filled" : "outlined"
          }`}
        >
          {redAlliance.map((teamNumber, index) => (
            <div
              key={index}
              className={`team-box red-team ${
                teamNumber === config.TeamNumber ? "highlighted" : ""
              }`}
            >
              <TeamNumber teamNumber={teamNumber} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default MatchView;
