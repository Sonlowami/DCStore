import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';
import { useParams } from 'react-router-dom';


export default function Study() {
  const [series, setSeries] = useState([]);
  const { id } = useParams();

  const getSeries = async () => {
    try {
      const res = await getData(`/api/v1/study/${id}`);
      const data = res.data;
      setSeries(data);
    } catch (err) {
      console.log(`err: ${err}`);
      setSeries([]);
    }
  }

  useEffect(() => {
    getSeries();
  }
  , []);

  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Study: {id}</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Series description</th>
            <th>Series Number</th>
            <th>series ID</th>
            <th>Study ID</th>
            <th>Modality</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {series.map((sery) => (
            <tr key={sery.id}>
              <td>{series.seriesDescription || 'N/A'}</td>
              <td>{series.seriesNumber || 'N/A'}</td>
              <td>{series.seriesInstanceUID || 'N/A'}</td>
              <td>{series.studyID || 'N/A'}</td>
              <td>...</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
