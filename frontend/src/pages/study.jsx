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
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Study: {id}</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Study ID</th>
            <th>Series ID</th>
            <th>Series Description</th>
            <th>Number</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {series.map((sery) => (
            <tr key={sery.id}>
              <td>{id}</td>
              <td>{<Link to={`/series/${sery.seriesInstanceUID}`}>{ sery.seriesInstanceUID }</Link> || 'N/A'}</td>
              <td>{sery.seriesDescription || 'N/A'}</td>
              <td>{sery.seriesNumber || 'N/A'}</td>
              <td>...</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
