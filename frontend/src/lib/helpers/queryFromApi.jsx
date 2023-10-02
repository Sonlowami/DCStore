import axios from 'axios';


// change base url to localhost:5000 for API
axios.defaults.baseURL = 'http://localhost:5000';


export async function getData(uri, pageNumber=0) {
  const token = localStorage.getItem('x-token');
  const headers = {
    'x-token': token
  };
  const res = await axios.get(uri, {
    headers: headers,
    params: { pageNumber }
  });
  return res;
}

export async function postData(uri, payload, pageNumber=0) {
  const token = localStorage.getItem('x-token');
  const headers = {
    'x-token': token,
  };

  const res = await axios.post(uri, payload, {
    headers: headers,
    params: { pageNumber }
  });
  return res;
}

export async function updateData(uri, payload) {
  const token = localStorage.getItem('x-token');
  const headers = {
    'x-token': token,
  };

  const res = await axios.put(uri, payload, {
    headers: headers,
  });
  return res;
}

export function redirect(path) {
  window.location.href = path;
}
