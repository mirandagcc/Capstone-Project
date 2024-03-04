import React, { useEffect, useState } from 'react';

function Portfolio() {
  const [portfolio, setPortfolio] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/portfolio')
      .then(response => response.json())
      .then(data => setPortfolio(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      {portfolio.map(stock => (
        <div key={stock.symbol}>{stock.name}: {stock.value}</div>
      ))}
    </div>
  );
}

export default Portfolio;
