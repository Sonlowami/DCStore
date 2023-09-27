import React from 'react';
import { Link } from 'react-router-dom';

const studies = [
{
  id: 101,
  description: 'MRI Brain Scan',
  patientId: 1,
  referringPhysician: 'Dr. Smith',
  recentSeriesId: 201,
  series: 3,
},
{
  id: 102,
  description: 'X-ray Chest',
  patientId: 2,
  referringPhysician: 'Dr. Johnson',
  recentSeriesId: 202,
  series: 2,
},
{
  id: 103,
  description: 'CT Abdomen',
  patientId: 3,
  referringPhysician: 'Dr. Anderson',
  recentSeriesId: 203,
  series: 4,
},
{
  id: 104,
  description: 'Ultrasound Heart',
  patientId: 4,
  referringPhysician: 'Dr. Williams',
  recentSeriesId: 204,
  series: 1,
},
];

export default function Studies() {
  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Studies</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Study ID</th>
            <th>Study description</th>
            <th>Patient ID</th>
            <th>Series</th>
            <th>Recent Series ID</th>
            <th>Referring Physician</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {studies.map((study) => (
            <tr key={study.id}>
              <td>{study.id}</td>
              <td>{study.description}</td>
              <td>{study.patientId}</td>
              <td>{study.series}</td>
              <td>{study.recentSeriesId}</td>
              <td>{study.referringPhysician}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}