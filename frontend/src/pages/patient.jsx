import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';
import { useParams, Link } from 'react-router-dom';


export default function Patient() {
  const [studies, setStudies] = useState([]);
  const { id } = useParams();

  const getStudies = async () => {
    try {
      const res = await getData(`/api/v1/patients/${id}/studies`);
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
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Patient {id}'s studies</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
        <tr>
            <th>Study description</th>
            <th>Study Date</th>
            <th>Patient ID</th>
            <th>Study ID</th>
            <th>Series</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {studies.map((study) => (
            <tr key={study.id}>
              <td>{study.studyDescription || 'N/A'}</td>
              <td>{new Date(study.studyDate).toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }) || 'N/A'}</td>
              <td>{study.patientID || 'N/A'}</td>
              <td>{study.studyInstanceUID || 'N/A'}</td>
              <td>{
                <Link to={`/studies/${study.studyInstanceUID}/series`}>
                  <button className='bg-sky-200 hover:bg-sky-300 text-gray-900 font-semibold py-1 px-2 rounded inline-flex items-center'>
                    <span>View Series</span>
                  </button>
                </Link>
              }</td>
          </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
