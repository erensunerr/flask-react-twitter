import React, {useState, useEffect} from "react"
import randomcolor from 'randomcolor'


/**
 * App - creates fritter
 *
 * @param {int} argA Not a real thing
 * @return {int} Not a real thing
 */
function App() {


  var [count, setCount] = useState(0);
  var [color, setColor] = useState("#000000");

  useEffect(() => {
    setColor(randomcolor());
  }, [count]);

  return (
    <div style={{color: color}}>
      <h1>{count}</h1>
      <button onClick={() => setCount(prevCount => prevCount-1)}>DEC</button>
      <button onClick={() => setCount(prevCount => prevCount+1)}>INC</button>
    </div>
  )
}

export default App
