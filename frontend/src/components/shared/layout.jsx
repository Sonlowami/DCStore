import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from '../sidebar'
import Header from '../header'

export default function Layout() {
  return (
    <div className='flex flex-row bg-neutral-200 h-screen w-screen overflow-y-scroll'>
      { <Sidebar className='overflow-y-hidden h-screen'/> }
      <div className='p-4 w-full'>
        <Header/>
        <div>{ <Outlet/> }</div>
      </div>
    </div>
  )
}