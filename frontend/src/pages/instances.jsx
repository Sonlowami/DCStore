import React from 'react';
import { useState, useEffect } from 'react';
import { getData } from '../lib/helpers/queryFromApi';


export default function Instances() {
  const [instances, setInstances] = useState([]);

  const getInstances = async () => {
    try {
      const res = await getData('/api/v1/instances');
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

  async function downloadInstance(instance) {
    try {
      const res = await getData(`/api/v1/instances/${instance.sopInstanceUID}/download`);
      const data = res.data;
      console.log(`data: ${JSON.stringify(data)}`);

      const blob = new Blob([data], { type: 'application/dicom' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${instance.sopInstanceUID}.dcm`);
      document.body.appendChild(link);
      link.click();

      // Clean up
      window.URL.revokeObjectURL(url);
      link.parentNode.removeChild(link);
    } catch (err) {
      console.log(`err: ${err}`);
    }
  }

  return (
    <div>
      <h1 className='font-semibold text-gray-900 text-xl py-3 mt-2'>Instances</h1>
      <table className='my-3 w-full'>
        <thead className='px-2 bg-sky-100'>
          <tr>
            <th>Instance Number</th>
            <th>Image type</th>
            <th>Instance ID</th>
            <th>Download</th>
          </tr>
        </thead>
        <tbody className='px-2'>
          {instances.map((instance) => (
            <tr key={instance.id}>
              <td>{instance.instanceNumber || 'N/A'}</td>
              <td>{instance.imageType.join(' - ')}</td>
              <td>{instance.sopInstanceUID || 'N/A'}</td>
              <td>
                {instance.sopInstanceUID ? <button 
                style={{backgroundColor: '#4CAF50', color: 'white', padding: '10px 24px', border: 'none', borderRadius: '4px', cursor: 'pointer'}}
                onClick={() => downloadInstance(instance)}>Click here</button> : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
