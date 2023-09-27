import React from 'react'
import { Link } from 'react-router-dom'

const shared = [
  {
    id: 101,
    description: 'MRI Brain Scan',
    patientId: 1,
    referringPhysician: 'Dr. Smith',
    recentSeriesId: 201,
    series: 3,
    from: 'Dr. Emmanuel'
  },
  {
    id: 102,
    description: 'X-ray Chest',
    patientId: 2,
    referringPhysician: 'Dr. Johnson',
    recentSeriesId: 202,
    series: 2,
    from: 'Dr. Smith'
  },
  {
    id: 103,
    description: 'CT Abdomen',
    patientId: 3,
    referringPhysician: 'Dr. Anderson',
    recentSeriesId: 203,
    series: 4,
    from: 'Dr. Jonhson'
  },
  {
    id: 104,
    description: 'Ultrasound Heart',
    patientId: 4,
    referringPhysician: 'Dr. Williams',
    recentSeriesId: 204,
    series: 1,
    from: 'Lowami'
  },
];
export default function Shared() {
  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Shared Studies</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Study ID</th>
            <th>Study description</th>
            <th>Patient ID</th>
            <th>Series</th>
            <th>Recent Series ID</th>
            <th>Referring Physician</th>
            <th>Shared by</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {shared.map((study) => (
            <tr key={study.id}>
              <td>{study.id}</td>
              <td>{study.description}</td>
              <td>{study.patientId}</td>
              <td>{study.series}</td>
              <td>{study.recentSeriesId}</td>
              <td>{study.referringPhysician}</td>
              <td>{study.from}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}