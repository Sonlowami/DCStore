import React, { useState } from 'react';
import { postData } from '../lib/helpers/queryFromApi'

export default function Upload() {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState('initial');
  const [message, setMessage] = useState('');

  function handleMultipleFiles(e) {
    setStatus('initial');
    setFiles(e.target.files);
  }

  async function handleFile() {
    setStatus('uploading');
    setMessage('');
    const form = new FormData();
    for (const file of files) {
      form.append('files', file);
    }
    try {
      const response = await postData('/api/v1/files', form);
      setStatus('success');
      setMessage('File uploaded successfully');
      console.log(JSON.stringify(response));
    } catch (err) {
      setStatus('failure');
      setMessage('Failed to upload file');
      console.log(err);
    }
  }

  return (
    <div className='mt-2'>
      <form>
        <p className='m-2 text-lg'>Upload files. Supported formats: .dcm, .zip if zipped files are .dcm format</p>
        <input type="file" id='file' multiple onChange={handleMultipleFiles} className='m-4 font-23 text-lg flex justify-center items-center'/>
        <button type="button" onClick={handleFile} className='bg-sky-500 border border-2 hover:border-4 hover:bg-sky-300 border-orange-500 rounded-md p-2 my-2'>Upload</button>
        {status === 'uploading' && <div className='text-lg'>Uploading file...</div>}
        {status === 'success' && <div className='text-lg text-green-500'>{message}</div>}
        {status === 'failure' && <div className='text-lg text-red-500'>{message}</div>}
      </form>
    </div>
  )
}
