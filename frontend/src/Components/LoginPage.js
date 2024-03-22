import React, { useState } from 'react';
import './LoginPage.css'; 
import { useNavigate } from 'react-router-dom';


function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    console.log("Log In button clicked");
    fetch('https://mcsbt-integration-miranda.ew.r.appspot.com/login', { 
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
      onLogin(true);  
      navigate('/main');
    })
    .catch(error => {
      console.error('ERROR But not CORS:', error);
    });
  }

  return (
    <div className="background">
      <div className="shape"></div>
      <div className="shape"></div>
      <form onSubmit={handleSubmit} className="form">
        <div className="logo-container">
            <img src="logo_capstone.png" alt="Logo" style={{textAlign: 'center', marginBottom: '20px', width: '100px', height: 'auto'}} />
        </div>
        <h3>Login Here</h3>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Username"
            id="username"
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Password"
            id="password"
            required
          />
        </div>
        <button type="submit">Log In</button>
      </form>
    </div>
  );
}

export default Login;

