import React, { useState } from 'react';
import { API_BASE_URL } from './config';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/api/echo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });
      if (!res || !res.ok) {
        throw new Error(`HTTP error! status: ${res ? res.status : 'unknown'}`);
      }
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
      setResponse({ error: 'An error occurred' });
    }
  };

  return (
    <div className="App">
      <h1>MVC Template App</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter a message"
        />
        <button type="submit">Send</button>
      </form>
      {response && (
        <div>
          <h2>Response from server:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
