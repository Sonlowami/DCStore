import axios from 'axios';

export async function getData(uri, pageNumber=0) {
  try {
    const token = localStorage.getItem('x-token');
    let res
    if (token) {
      const headers = {
        'x-token': token
      };

      res = await axios.get(uri, {
        headers: headers,
        params: { pageNumber }
      });
    }
    else {
      res = await axios.get(uri, { params: { pageNumber }});
    }
    data = res.data;
    return data;
  } catch (err) { console.log(err); }
}

export async function postData(uri, payload, pageNumber=0) {
  try {
    const token = localStorage.getItem('x-token');
    let res
    if (token) {
      const headers = {
        'x-token': token,
      };

      res = await axios.post(uri, payload, {
        headers: headers,
        params: { pageNumber }
      });
    }
    else {
      res = await axios.post(uri, payload, { params: { pageNumber }});
    }
    data = res.data;
    return data;
  } catch (err) { console.log(err); }
}

export async function updateData(uri, payload) {
  try {
    const token = localStorage.getItem('x-token');
    let res
    if (token) {
      const headers = {
        'x-token': token,
      };

      res = await axios.put(uri, payload, {
        headers: headers,
        params: { pageNumber }
      });
      data = res.data;
      return data;
    }
  } catch (err) { console.log(err); }
}
