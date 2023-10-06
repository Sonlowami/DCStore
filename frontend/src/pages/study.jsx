import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';
import { useParams, Link } from 'react-router-dom';


export default function Study() {
  const [series, setSeries] = useState([]);
  const { id } = useParams();

  const getSeries = async () => {
    try {
      const res = await getData(`/api/v1/studies/${id}/series`);
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
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Series for study ID {id}</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Series Number</th>
            <th>Modality</th>
            <th>Series description</th>
            <th>Series ID</th>
            <th>Images</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {series.map((sery) => (
            <tr key={sery.id}>
              <td>{sery.seriesNumber || 'N/A'}</td>
              <td>{sery.modality || 'N/A'}</td>
              <td>{sery.seriesDescription || 'N/A'}</td>
              <td>{sery.seriesInstanceUID || 'N/A'}</td>
              <td>
                {sery.seriesInstanceUID ? <Link to={`/series/${sery.seriesInstanceUID}/instances`}>View Images</Link> : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
