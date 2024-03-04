import React, { useState } from 'react';
import './LoginPage.css'; 

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  function handleSubmit(event) {
    event.preventDefault();
    console.log(email, password);
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
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Email or Phone"
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
