import {
    useParams
  } from "react-router-dom";
function Puzzle(props) {
    let { puzzleId } = useParams();
    return <h3>Puzzle with id: {puzzleId}</h3>;
}

export default Puzzle;