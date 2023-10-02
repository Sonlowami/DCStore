import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AuthService from '../lib/helpers/authService';
import { redirect } from '../lib/helpers/queryFromApi';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(''); // Clear any previous error message
    // You can add your login logic here
    try {
      const res = await AuthService.login(email, password);
      if (res['x-token']) {
        redirect('/');
      } else {
        setErrorMessage('Invalid credentials'); // Set error message
      }
    } catch (err) {
      console.log(err.response.data.error);
      setErrorMessage('Invalid credentials'); // Set error message
    }
  };

  return (
    <div className="flex h-screen justify-center items-center bg-sky-500">
      <form onSubmit={handleSubmit} className="bg-neutral-100 p-8 rounded shadow-md w-1/4 h-1/2">
        <h2 className="text-2xl font-semibold mb-4">Login</h2>
        {errorMessage && (
          <div className="mb-4 p-3 bg-red-400 text-white rounded">{errorMessage}</div>
        )}
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
