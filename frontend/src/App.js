import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  

  return (
    <div>
      <h1>{message}</h1>
    </div>
  );
}

export default App;
