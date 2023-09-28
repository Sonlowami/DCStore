import React, { useState } from 'react';

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    phoneNumber: '',
    dateOfBirth: '',
    gender: 'male', // Default to male
    role: 'patient', // Default to patient
  });

  const [formErrors, setFormErrors] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    gender: '',
    role: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (validateForm()) {
      const resp = postData(formData)
      console.log('Form submitted:', formData);
    }
  };

  const validateForm = () => {
    const { firstName, lastName, email, password, gender, role } = formData;
    let errors = {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      gender: '',
      role: '',
    };
    let isValid = true;

    if (!firstName) {
      errors.firstName = 'First Name is required';
      isValid = false;
    }

    if (!lastName) {
      errors.lastName = 'Last Name is required';
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

    if (!gender) {
      errors.gender = 'Gender is required';
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
     <div className='w-full h-full bg-sky-500 flex items-center justify-center'>
      <div className="mx-auto w-1/2 my-6 p-4 bg-neutral-100 border shadow-lg rounded">
        <h2 className="text-2xl font-bold mb-4">Create Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">
              First Name<span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.firstName}</div>
          </div>

          <div className="mb-4">
            <label htmlFor="lastName" className="block text-sm font-medium text-gray-700">
              Last Name<span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
            <div className="text-red-600 text-xs mt-1">{formErrors.lastName}</div>
          </div>

          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
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
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
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
            <label className="block text-sm font-medium text-gray-700">Phone Number</label>
            <input
              type="tel"
              id="phoneNumber"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
            <input
              type="date"
              id="dateOfBirth"
              name="dateOfBirth"
              value={formData.dateOfBirth}
              onChange={handleInputChange}
              className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Gender<span className="text-red-600">*</span></label>
            <div className="mt-2">
              <label className="inline-flex items-center mr-4">
                <input
                  type="radio"
                  name="gender"
                  value="male"
                  checked={formData.gender === 'male'}
                  onChange={handleInputChange}
                  className="form-radio text-blue-500 focus:ring-0"
                />
                <span className="ml-2">Male</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="gender"
                  value="female"
                  checked={formData.gender === 'female'}
                  onChange={handleInputChange}
                  className="form-radio text-blue-500 focus:ring-0"
                />
                <span className="ml-2">Female</span>
              </label>
            </div>
            <div className="text-red-600 text-xs mt-1">{formErrors.gender}</div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Role<span className="text-red-600">*</span></label>
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