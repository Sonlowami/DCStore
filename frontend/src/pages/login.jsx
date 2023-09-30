import React, { useState } from 'react';
import { Link, redirect } from 'react-router-dom'
import { postData } from '../lib/helpers/queryFromApi';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // You can add your login logic here
    console.log('Email:', email);
    console.log('Password:', password);
    const credentials = { email, password };
    try {
      const resp = postData('/api/v1/login', credentials);
      const token = resp.json()['x-token'];
      localStorage.setItem('x-token', token);
      redirect('/');
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="flex h-screen justify-center items-center bg-sky-500">
      <form onSubmit={handleSubmit} className="bg-neutral-100 p-8 rounded shadow-md w-1/4 h-1/2">
        <h2 className="text-2xl font-semibold mb-4">Login</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 font-medium mb-2">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:border-blue-500"
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="password" className="block text-gray-700 font-medium mb-2">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:border-blue-500"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <button type="submit" className="bg-sky-500 hover:bg-blue-500 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline-blue">
            Login
          </button>
        </div>
        <div className="flex justify-between mt-4">
          <Link to="/register" className='hover:underline hover:font-semibold text-neutral-900'> Create an Account</Link> |
          <Link to="/forgot-password" className='hover:underline hover:font-semibold text-neutral-900'>Forgot Password</Link>
        </div>
      </form>
    </div>
  );
};

export default Login;
