import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 
import './MainPage.css';

function MainPage() {
  const navigate = useNavigate(); 

  const [username, setUsername] = useState('Loading...');
  const [totalValue, setTotalValue] = useState('Calculating...');
  const [stocks, setStocks] = useState([]);
  const userId = '2'; 

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const userDetailsResponse = await fetch(`http://127.0.0.1:5000/api/user-details?userId=${userId}`);
        const userDetails = await userDetailsResponse.json();
        setUsername(userDetails.username); 
      } catch (error) {
        console.error('Error fetching user details:', error);
        setUsername('User details not available'); 
      }
    };

    const fetchPortfolioValue = async () => {
      try {
        const portfolioValueResponse = await fetch(`http://127.0.0.1:5000/api/portfolio/value?userId=${userId}`);
        const portfolioValueData = await portfolioValueResponse.json();
        setTotalValue(portfolioValueData.total_portfolio_value);
      } catch (error) {
        console.error('Error fetching portfolio value:', error);
        setTotalValue('Value not available'); 
      }
    };

    const fetchStocks = async () => {
      try {
        const portfolioResponse = await fetch(`http://127.0.0.1:5000/api/portfolio?userId=${userId}`);
        const portfolioData = await portfolioResponse.json();
        setStocks(Object.entries(portfolioData.stocks).map(([symbol, quantity]) => ({ symbol, quantity })));
      } catch (error) {
        console.error('Error fetching stocks:', error);
        setStocks([]); 
      }
    };

    fetchUserDetails();
    fetchPortfolioValue();
    fetchStocks();
  }, [userId]);

  return (
    <div className="main-container">
      <h1>Hi, {username}!</h1>
      <p>Total Portfolio Value: $ {totalValue}</p>
      <h2>Your Stocks:</h2>
      <ul>
        {stocks.map((stock, index) => (
          <li key={index}>
            {stock.symbol}: {stock.quantity} shares
          </li>
        ))}
      </ul>
      {/* Button to navigate to the stock search page */}
      <button onClick={() => navigate('/search')} style={{ marginTop: '20px' }}>Search Historical Data</button>
    </div>
  );
}

export default MainPage;
