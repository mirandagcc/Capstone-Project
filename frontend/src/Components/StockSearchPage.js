import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './StockSearchPage.css';

function StockSearchPage() {
  const [symbol, setSymbol] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [results, setResults] = useState(null); 
  const navigate = useNavigate();

  const handleSearch = async () => {
    try {
      const url = `https://mcsbt-integration-miranda.ew.r.appspot.com/api/portfolio/${symbol}?start=${startDate}&end=${endDate}`;
      const response = await fetch(url);
      const data = await response.json();
      if (response.ok) {
        setResults(data); 
      } else {
        throw new Error(data.error || 'Unknown error');
      }
    } catch (error) {
      console.error('Error fetching stock history:', error);
      setResults({ error: error.toString() }); 
    }
  };

  return (
    <div>
      <h1>Search Historical Stock Data</h1>
      <div>
        <label>
          Stock Symbol:
          <input
            className="stock-input"
            type="text"
            placeholder="Enter stock symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Start Date:
          <input
            className="stock-input"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          End Date:
          <input
            className="stock-input"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
      </div>
      <button onClick={handleSearch}>Search</button>
      <button onClick={() => navigate('/')}>Back to Main</button>
      {/* Display the search results or error message */}
      {results && (
        <div>
          <h2>Results:</h2>
          {results.error ? (
            <p>Error: {results.error}</p>
          ) : (
            <ul>
              {Object.entries(results).map(([date, details], index) => (
                <li key={index}>{date}: {details['4. close']}</li> 
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default StockSearchPage;
