import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';
import { useParams } from 'react-router-dom';


export default function SingleSeries() {
  const [instances, setInstances] = useState([]);
  const { id } = useParams();

  const getInstances = async () => {
    try {
      const res = await getData(`/api/v1/series/${id}`);
      const data = res.data;
      setInstances(data);
    } catch (err) {
      console.log(`err: ${err}`);
      setInstances([]);
    }
  }

  useEffect(() => {
    getInstances();
  }
  , []);

  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Series: {id}</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Instance ID</th>
            <th>Instances Number</th>
            <th>Series ID</th>
            <th>Download</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {instances.map((sery) => (
            <tr key={sery.id}>
              <td>{instances.sopInstanceUID || 'N/A'}</td>
              <td>{instances.instancesNumber || 'N/A'}</td>
              <td>{instances.seriesId || 'N/A'}</td>
              <td>{instances.filepath || 'N/A'}</td>
              <td>...</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
