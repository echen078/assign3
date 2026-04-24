// TIC-TAC-TOE CODE
// import { useState } from 'react';

// function Square({value, onSquareClick}) {
//   return (
//     <button className="square" onClick={onSquareClick}>
//       {value}
//     </button>
//   );
// }

// export default function Board() {
//   const [xIsNext, setXIsNext] = useState(true);
//   const [squares, setSquares] = useState(Array(9).fill(null));

//   function handleClick(i) {
//     if (calculateWinner(squares) || squares[i]) {
//       return;
//     }
//     const nextSquares = squares.slice();
//     if (xIsNext) {
//       nextSquares[i] = 'X';
//     } else {
//       nextSquares[i] = 'O';
//     }
//     setSquares(nextSquares);
//     setXIsNext(!xIsNext);
//   }

//   const winner = calculateWinner(squares);
//   let status;
//   if (winner) {
//     status = 'Winner: ' + winner;
//   } else {
//     status = 'Next player: ' + (xIsNext ? 'X' : 'O');
//   }

//   return (
//     <>
//       <div className="status">{status}</div>
//       <div className="board-row">
//         <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
//         <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
//         <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
//       </div>
//       <div className="board-row">
//         <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
//         <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
//         <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
//       </div>
//       <div className="board-row">
//         <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
//         <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
//         <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
//       </div>
//     </>
//   );
// }

// function calculateWinner(squares) {
//   const lines = [
//     [0, 1, 2],
//     [3, 4, 5],
//     [6, 7, 8],
//     [0, 3, 6],
//     [1, 4, 7],
//     [2, 5, 8],
//     [0, 4, 8],
//     [2, 4, 6],
//   ];
//   for (let i = 0; i < lines.length; i++) {
//     const [a, b, c] = lines[i];
//     if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
//       return squares[a];
//     }
//   }
//   return null;
// }


// CHORUS LAPILLI CODE
import { useState } from 'react';

function Square({ value, onSquareClick, isSelected }) {
  let cls;
  if (isSelected) {
    cls = 'square selected';
  } else {
    cls = 'square';
  }
  return (
    <button
      className={cls}
      onClick={onSquareClick}
    >
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [selectedSquare, setSelectedSquare] = useState(null);

  const xCount = squares.filter(s => s === 'X').length;
  const oCount = squares.filter(s => s === 'O').length;
  const fullBoard = xCount >= 3 && oCount >= 3;

  function handleClick(i) {
    if (calculateWinner(squares)) return;

    let currentPlayer;
    if (xIsNext) {
      currentPlayer = 'X';
    } else {
      currentPlayer = 'O';
    }

    // [GenAI Use] Prompt: "I have a fullBoard boolean (true when both players have placed 3 pieces). Inside handleClick(i), write the logic: if (!fullBoard) keep the original tic-tac-toe placement logic (block occupied squares, place currentPlayer's symbol, flip xIsNext). Otherwise if full board: when no piece is selected and the clicked square belongs to currentPlayer, select it; if the same square is clicked again, deselect; if another own piece is clicked, switch selection; if an empty adjacent square is clicked, move the piece there. However, first enforce the center constraint: if currentPlayer already has a piece at index 4, the move is only allowed if it selects and moves index 4 or results in a win."
    // [GenAI Use] LLM Response Start
    if (!fullBoard) {
      if (squares[i]) return;
      const nextSquares = squares.slice();
      nextSquares[i] = currentPlayer;
      setSquares(nextSquares);
      setXIsNext(!xIsNext);
    } else {
      if (selectedSquare === null) {
        if (squares[i] !== currentPlayer) return;
        setSelectedSquare(i);
      } else if (i === selectedSquare) {
        setSelectedSquare(null);
      } else if (squares[i] === currentPlayer) {
        setSelectedSquare(i);
      } else if (squares[i] === null && isAdjacent(selectedSquare, i)) {
        const nextSquares = squares.slice();
        nextSquares[selectedSquare] = null;
        nextSquares[i] = currentPlayer;

        // If current player has a piece at center, the move must win or vacate center.
        if (squares[4] === currentPlayer) {
          const vacatesCenter = selectedSquare === 4;
          if (!vacatesCenter && !calculateWinner(nextSquares)) return;
        }

        setSquares(nextSquares);
        setSelectedSquare(null);
        setXIsNext(!xIsNext);
      }
    }
    // [GenAI Use] LLM Response End
    // [GenAI Use] Reflection: I traced through the given code of the conditions, the four-way else-if for full board phase covers every case I had prompted (no selection, deselect, switch selection, execute move). The center constraint check correctly reads from the original squares (before the move) to detect whether center is occupied, then tests two escape conditions. I verified the logic manually in the browser — blocked moves, valid moves, and the center constraint all behaved as expected.
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else if (fullBoard) {
    if (xIsNext) {
      status = 'Move a piece: X';
    } else {
      status = 'Move a piece: O';
    }
  } else {
    if (xIsNext) {
      status = 'Next player: X';
    } else {
      status = 'Next player: O';
    }
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} isSelected={selectedSquare === 0} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} isSelected={selectedSquare === 1} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} isSelected={selectedSquare === 2} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} isSelected={selectedSquare === 3} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} isSelected={selectedSquare === 4} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} isSelected={selectedSquare === 5} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} isSelected={selectedSquare === 6} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} isSelected={selectedSquare === 7} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} isSelected={selectedSquare === 8} />
      </div>
    </>
  );
}

// [GenAI Use] Prompt: "I'm building Chorus Lapilli in React. I need a helper function that checks whether two board squares (given as flat indices 0–8 on a 3x3 grid) are adjacent, including diagonals."
// [GenAI Use] LLM Response Start
function isAdjacent(a, b) {
  const rowA = Math.floor(a / 3), colA = a % 3;
  const rowB = Math.floor(b / 3), colB = b % 3;
  return Math.abs(rowA - rowB) <= 1 && Math.abs(colA - colB) <= 1 && a !== b;
}
// [GenAI Use] LLM Response End
// [GenAI Use] Reflection: The logic converts flat indices to (row, col) using integer division and modulo, then checks that both row and column distances are at most 1 and the squares are distinct. I traced through a few cases (e.g. index 0 vs 1, 0 vs 4, 0 vs 5) to confirm it handles corners, edges, and diagonals correctly.

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}