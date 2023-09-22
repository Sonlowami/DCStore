import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from '../sidebar'
import Header from '../header'

export default function Layout() {
  return (
    <div className='flex flex-row bg-neutral-100 h-screen w-screen overflow-hidden'>
      { <Sidebar/> }
      <div className='p-4 w-full'>
        <Header/>
        <div>{ <Outlet/> }</div>
      </div>
    </div>
  )
}