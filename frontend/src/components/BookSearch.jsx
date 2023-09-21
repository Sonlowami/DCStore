import React, { useState, useRef, useCallback } from 'react'
import useSearch from '../hooks/useSearch'

export default function BookSearch() {
  const [query, setQuery] = useState('');
  const [pageNumber, setPageNumber] = useState(1);

  const { loading, data, hasmore, error } = useSearch(query, pageNumber)

  const observer = useRef()
  const lastItem = useCallback((item) => {
    if (loading) return
    if (observer.current) observer.current.disconnect()
    observer.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasmore) {
        setPageNumber((prevPage) => prevPage + 1)
      }
  })
    if (item) observer.current.observe(item)
  }, [loading, hasmore])

  function handleSearch(e) {
    setQuery(e.target.value);
    setPageNumber(1);
  }

  return (
    <div>
      <input type="text" value={query} onChange={handleSearch}/>
      {data.map((item, index) => {
        if (data.length == index + 1)
          return <div key={item} ref={lastItem}>{item}</div>
        return <div key={item}>{item}</div>
      })}
      <div>{loading && 'loading'}</div>
      <div>{error && 'error'}</div>
    </div>
  );
}
