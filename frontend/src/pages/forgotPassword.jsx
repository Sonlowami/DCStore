import React, { useState } from 'react';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // You can add your "forgot password" logic here
    console.log('Email:', email);
  };

  return (
    <div className="flex h-screen justify-center items-center bg-sky-500 w-full">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-1/3">
        <h2 className="text-2xl font-semibold mb-4">Forgot Password</h2>
        <p className='text-md my-4'>An email containing a link to a reset password page will be sent if your email is registered. Type your email below:</p>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 font-medium mb-2">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
            className="w-full px-3 py-3 border rounded-md focus:outline-none focus:border-blue-500"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <button type="submit" className="bg-sky-500 hover:bg-blue-500 text-white font-medium py-2 px-4 rounded focus:outline-none focus:shadow-outline-blue">
            Verify Email
          </button>
        </div>
      </form>
    </div>
  );
};

export default ForgotPassword;
