import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './MainPage.css';

function MainPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('Loading...');
  const [totalValue, setTotalValue] = useState('Calculating...');
  const [stocks, setStocks] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [stockSymbol, setStockSymbol] = useState('');
  const [stockQuantity, setStockQuantity] = useState(0);
  const [modifyType, setModifyType] = useState('add');

  const user_id = '1';

  useEffect(() => {
    fetchUserDetails();
    fetchPortfolioData();
  }, [user_id]); 

  async function fetchUserDetails() {
    try {
      const userDetailsResponse = await fetch(`https://mcsbt-integration-miranda4.ew.r.appspot.com/user-details?user_id=${user_id}`);
      const userDetails = await userDetailsResponse.json();
      setUsername(userDetails.username);
    } catch (error) {
      console.error('Error fetching user details:', error);
      setUsername('User details not available');
    }
  }

  async function fetchPortfolioData() {
    try {
      const portfolioResponse = await fetch(`https://mcsbt-integration-miranda4.ew.r.appspot.com/api/portfolio?user_id=${user_id}`);
      const portfolioData = await portfolioResponse.json();
      setTotalValue(portfolioData.total_portfolio_value);
      setStocks(portfolioData.stocks);
    } catch (error) {
      console.error('Error fetching portfolio data:', error);
      setTotalValue('Value not available');
      setStocks([]);
    }
  }

  const updatePortfolio = async () => {
    const data = {
      user_id: user_id,
      [modifyType]: [{ symbol: stockSymbol.toUpperCase(), quantity: parseInt(stockQuantity, 10) }]
    };
  
    try {
      const response = await fetch('https://mcsbt-integration-miranda4.ew.r.appspot.com/update_user', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error + ': ' + result.details.join(' '));
      }
      alert('Portfolio updated successfully! Refresh to see changes!');
      setShowModal(false);
      fetchPortfolioData(); 
    } catch (error) {
      console.error('Error updating portfolio:', error);
      alert(error.message); 
    }
  };
  

  return (
    <div className="main-container">
      <h1>Hi, {username}!</h1>
      <p>Total Portfolio Value: ${totalValue}</p>
      <h2>Your Stocks:</h2>
      <ul>
        {stocks.map((stock, index) => (
          <li key={index}>
            {stock.symbol}: {stock.quantity} shares
          </li>
        ))}
      </ul>
      <button onClick={() => navigate('/search')} style={{ margin: '20px 0' }}>Search Historical Data</button>
      
      {/* Portfolio Modification Button */}
      <button onClick={() => setShowModal(true)}>Modify Portfolio</button>

      {/* Modal for Portfolio Modification */}
      {showModal && (
        <div className="modal">
          <div>
            <label>Symbol: <input type="text" value={stockSymbol} onChange={(e) => setStockSymbol(e.target.value)} /></label>
          </div>
          <div>
            <label>Quantity: <input type="number" value={stockQuantity} onChange={(e) => setStockQuantity(e.target.value)} /></label>
          </div>
          <div>
            <label>
              Modify Type:
              <select value={modifyType} onChange={(e) => setModifyType(e.target.value)}>
                <option value="add">Add</option>
                <option value="remove">Remove</option>
              </select>
            </label>
          </div>
          <button onClick={updatePortfolio}>Submit</button>
          <button onClick={() => setShowModal(false)}>Cancel</button>
        </div>
      )}
    </div>
  );
}

export default MainPage;
