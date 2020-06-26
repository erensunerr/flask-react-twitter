import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
    var a;
   fetch('/time').then(res => res.json()).then(a)
   console.log(a)

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The current time is {a.time}.</p>
      </header>
    </div>
  );
}

export default App;
