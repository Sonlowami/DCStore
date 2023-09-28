import React, { useState } from 'react';

const ResetPassword = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setconfirmPassword] = useState('');

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };
  const handleconfirmPasswordChange = (e) => {
    setconfirmPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // You can add your login logic here
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className="flex h-screen justify-center items-center bg-sky-500">
      <form onSubmit={handleSubmit} className="bg-neutral-100 p-8 rounded shadow-md w-1/4 h-1/2">
        <h2 className="text-2xl font-semibold mb-4">Reset Password</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 font-medium mb-2">New Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:border-blue-500"
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-gray-700 font-medium mb-2">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={handleconfirmPasswordChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:border-blue-500"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <button type="submit" className="bg-sky-500 hover:bg-blue-500 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline-blue">
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default ResetPassword;
