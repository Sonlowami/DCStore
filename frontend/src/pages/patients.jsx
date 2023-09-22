import React from 'react'
import { Link } from 'react-router-dom'

export default function Patients() {
  return (
    <>
      <p>This is patients page</p>
      <Link to="/" className='underline'>Go to dashboard</Link>
    </>
  )
}