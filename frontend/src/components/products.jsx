import React from 'react'
import { Link } from 'react-router-dom'

export default function Products() {
  return (
    <>
      <p>This is products page</p>
      <Link to="/" className='underline'>Go to dashboard</Link>
    </>
  )
}