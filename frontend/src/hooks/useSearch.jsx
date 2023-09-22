import { useEffect, useState } from "react";
import axios from 'axios';

export default function useSearch(query, pageNumber) {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState([]);
  const [hasmore, setHasmore] = useState(false)

  useEffect(() => { setData([]) }, [query])

  useEffect( () => { return async () => {
    let cancel;
    try {
      const resp = await axios({
        method: 'GET',
        url: '',
        params: { q: query, page: pageNumber },
        cancelToken: new axios.CancelToken((c) => cancel = c),
      })
      setData((prevData) => [...new Set(...prevData, ...resp.data.docs)]);
      setHasmore(resp.data.length > 0);
      setLoading(false)
      console.log(resp.data);
      return () => cancel();
    } catch (e) {
      if (axios.isCancel(e)) return;
      setError(true)
    }
  }
  }, [query, pageNumber]);
  console.log(data)
  return { loading, data, error, hasmore };
}
