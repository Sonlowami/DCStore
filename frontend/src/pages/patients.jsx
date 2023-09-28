import React from 'react'
import { Link } from 'react-router-dom'

const patients = [
  {
    id: 1,
    firstName: 'John',
    lastName: 'Doe',
    age: 30,
    sex: 'Male',
    studies: 1,
    recentStudy: {
      id: 101,
      date: '2023-09-25',
    },
  },
  {
    id: 2,
    firstName: 'Jane',
    lastName: 'Smith',
    age: 25,
    sex: 'Female',
    studies: 1,
    recentStudy: {
      id: 102,
      date: '2023-09-26',
    },
  },
  {
    id: 3,
    firstName: 'Bob',
    lastName: 'Johnson',
    age: 45,
    sex: 'Male',
    studies: 4,
    recentStudy: {
      id: 103,
      date: '2023-09-27',
    },
  },
  {
    id: 4,
    firstName: 'Alice',
    lastName: 'Williams',
    age: 35,
    sex: 'Female',
    studies: 3,
    recentStudy: {
      id: 104,
      date: '2023-09-24',
    },
  },
];

export default function Patients() {
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
            <th>Studies</th>
            <th>Recent Study ID</th>
            <th>Recent Study Date</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.id}</td>
              <td>{`${patient.firstName} ${patient.lastName}`}</td>
              <td>{patient.age}</td>
              <td>{patient.sex}</td>
              <td>{patient.studies}</td>
              <td>{patient.recentStudy.id}</td>
              <td>{patient.recentStudy.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
