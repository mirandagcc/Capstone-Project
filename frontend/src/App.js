import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './Components/LoginPage';
import MainPage from './Components/MainPage';
import StockSearchPage from './Components/StockSearchPage'; 

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true); 
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Redirect based on login state */}
          <Route path="/" element={isLoggedIn ? <Navigate replace to="/main" /> : <LoginPage onLogin={handleLogin} />} />
          <Route path="/main" element={<MainPage />} />
          <Route path="/search" element={<StockSearchPage />} />
          {/* Redirects to login page if no exact route matches */}
          <Route path="*" element={<Navigate replace to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
