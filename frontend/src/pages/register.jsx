import React, { useState } from 'react';
import { postData } from '../lib/helpers/queryFromApi';
import { redirect } from '../lib/helpers/queryFromApi';
import AuthService from '../lib/helpers/authService';

const Register = () => {
  const [formData, setFormData] = useState({
    fullname: '',
    username: '',
    email: '',
    password: '',
    role: 'patient', // Default to patient
  });

  const [ status, setStatus ] = useState(0);

  const [formErrors, setFormErrors] = useState({
    fullname: '',
    username: '',
    email: '',
    password: '',
    role: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (validateForm()) {
      try {
        await AuthService.register(formData);
        redirect('/login');
      } catch (err) {
        if (err.response.status === 400) {
          if (err.response.data.error === 'Username already exists') {
            setFormErrors({ ...formErrors, username: 'Username already exists' });
          } else if (err.response.data.error === 'User already exists') {
            setFormErrors({ ...formErrors, email: 'Email already exists' });
          }
        }
      }
    }
  };

  const validateForm = () => {
    const { fullname, username, email, password, role } = formData;
    let errors = {
      fullname: '',
      username: '',
      email: '',
      password: '',
      role: '',
    };
    let isValid = true;

    if (!fullname) {
      errors.lastName = 'Last Name is required';
      isValid = false;
    }

    if (!username) {
      errors.username = 'Username is required';
      isValid = false;
    }

    if (!email) {
      errors.email = 'Email is required';
      isValid = false;
    }

    if (!password) {
      errors.password = 'Password is required';
      isValid = false;
    }

    if (!role) {
      errors.role = 'Role is required';
      isValid = false;
    }

    setFormErrors(errors);
    return isValid;
  };

  return (
     <div className='w-full h-screen bg-sky-500 flex items-center justify-center'>
      <div className="mx-auto w-1/3 my-6 p-4 bg-neutral-100 border shadow-lg rounded">
        <h2 className="text-2xl font-bold mb-4">Create Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="firstName" className="block text-md font-medium text-gray-700">
              Full Name<span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              id="fullname"
              name="fullname"
              value={formData.fullname}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.fullname}</div>
          </div>

          <div className="mb-4">
            <label htmlFor="username" className="block text-md font-medium text-gray-700">
              Username<span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.username}</div>
          </div>

          <div className="mb-4">
            <label htmlFor="email" className="block text-md font-medium text-gray-700">
              Email<span className="text-red-600">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.email}</div>
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="block text-md font-medium text-gray-700">
              Password<span className="text-red-600">*</span>
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.password}</div>
          </div>

          <div className="mb-4">
            <label className="block text-md font-medium text-gray-700">Role<span className="text-red-600">*</span></label>
            <div className="mt-2">
              <label className="inline-flex items-center mr-4">
                <input
                  type="radio"
                  name="role"
                  value="doctor"
                  checked={formData.role === 'doctor'}
                  onChange={handleInputChange}
                  className="form-radio text-blue-500 focus:ring-0"
                />
                <span className="ml-2">Doctor</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="role"
                  value="patient"
                  checked={formData.role === 'patient'}
                  onChange={handleInputChange}
                  className="form-radio text-blue-500 focus:ring-0"
                />
                <span className="ml-2">Patient</span>
              </label>
            </div>
            <div className="text-red-600 text-xs mt-1">{formErrors.role}</div>
          </div>

          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
