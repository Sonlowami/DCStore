import React from 'react'
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';
import { Link } from 'react-router-dom';


export default function Patients() {
  const [patients, setPatients] = useState([])

  const getPatients = async () => {
    try {
      const res = await getData('/api/v1/patients');
      const data = res.data;
      setPatients(data);
    } catch (err) {
      console.log(`err: ${err}`);
      setPatients([]);
    }
  }

  useEffect(() => {
    getPatients();
  }
  , []);

  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Patients</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Patient ID</th>
            <th>Full Name</th>
            <th>Age</th>
            <th>Sex</th>
            <th>Birth Date</th>
            <th>Studies</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.patientID || 'N/A'}</td>
              <td>{patient.patientName || 'N/A'}</td>
              <td>{patient.patientAge || 'N/A'}</td>
              <td>{patient.patientSex || 'N/A'}</td>
              <td>{patient.patientBirthDate || 'N/A'}</td>
              <td>
                {patient.patientID ? <Link to={`/patients/${patient.patientID}/studies`}>View Studies</Link> : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
