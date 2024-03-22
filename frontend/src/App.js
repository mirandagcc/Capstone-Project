import React, { useState} from 'react';import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './Components/LoginPage';
import MainPage from './Components/MainPage';
import StockSearchPage from './Components/StockSearchPage'; 


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn') === 'true');

  const handleLogin = (loginStatus) => {
    setIsLoggedIn(loginStatus);
    localStorage.setItem('isLoggedIn', loginStatus.toString()); // Persist login status
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
