import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';


export default function Studies() {
  const [studies, setStudies] = useState([]);

  const getStudies = async () => {
    try {
      const res = await getData('/api/v1/studies');
      const data = res.data;
      setStudies(data);
    } catch (err) {
      console.log(`err: ${err}`);
      setStudies([]);
    }
  }

  useEffect(() => {
    getStudies();
  }
  , []);

  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Studies</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Study description</th>
            <th>Study Date</th>
            <th>Study ID</th>
            <th>Patient ID</th>
            <th>Series</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {studies.map((study) => (
            <tr key={study.id}>
              <td>{study.studyDescription || 'N/A'}</td>
              <td>{new Date(study.studyDate).toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }) || 'N/A'}</td>
              <td>{study.studyInstanceUID || 'N/A'}</td>
              <td>{study.patientID || 'N/A'}</td>
              <td>...</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
