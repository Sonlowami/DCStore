import React, { useState } from 'react';
import { postData } from '../lib/helpers/queryFromApi'

export default function Upload() {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState('initial');

  function handleMultipleFiles(e) {
    setStatus('initial');
    setFiles(e.target.files);
  }

  function handleFile() {
    setStatus('uploading');
    const form = new FormData();
    for (file of files) {
      form.append('files', file);
    }
    try {
      const response = postData('/upload', form);
    } catch (err) { console.log(err); }
  }
  console.log('uploading processed!');

  return (
    <div className='mt-2'>
      <form>
        <p className='m-2 text-lg'>Upload files. Supported formats: .dcm, .zip if zipped files are .dcm format</p>
        <input type="file" id='file' multiple onChange={handleMultipleFiles} className='m-4 font-23 text-lg flex justify-center items-center'/>
        <button type="button" onClick={handleFile} className='bg-sky-500 border border-2 hover:border-4 hover:bg-sky-300 border-orange-500 rounded-md p-2 my-2'>Upload</button>
      </form>
    </div>
  )
}

