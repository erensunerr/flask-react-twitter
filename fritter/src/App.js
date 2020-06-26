import React from 'react';

function App() {
  fetch('/time')
  .then(response => response.json())
  .then(commits => );
  return (
    <h1>
      HELLO, time = {x}
    </h1>
  )

}

export default App;
