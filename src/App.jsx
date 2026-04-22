
// STARTER CODE
// import * as React from 'react'
// import * as ReactBootstrap from 'react-bootstrap'

// const { Badge, Button, Card } = ReactBootstrap

// export default function App() {
//   const [name, setName] = React.useState('World')

//   return (
//     <div className="container py-4">
//       <Card className="starter-card shadow-sm">
//         <Card.Body className="p-4">
//           <h1 className="greeting display-6 fw-bold">Hello, {name}!</h1>
//           <p className="mb-3 text-secondary">
//             This starter is set up to match the React Essentials notes more closely.
//             For the assignment, build the tic-tac-toe tutorial in this file and leave
//             mounting to <code>src/main.jsx</code>.
//           </p>
//           <div className="d-flex gap-2 flex-wrap align-items-center">
//             <Button variant="primary" onClick={() => setName('CS 35L')}>
//               Set example name
//             </Button>
//             <Badge bg="secondary" pill>
//               ReactBootstrap ready
//             </Badge>
//           </div>
//         </Card.Body>
//       </Card>
//     </div>
//   )
// }


// TIC-TAC-TOE CODE
import { useState } from 'react';

function Square() {
  const [value, setValue] = useState(null);

  function handleClick() {
    setValue('X');
  }

  return (
    <button
      className="square"
      onClick={handleClick}
    >
      {value}
    </button>
  );
}

export default function Board() {
  return (
    <>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
    </>
  );
}

