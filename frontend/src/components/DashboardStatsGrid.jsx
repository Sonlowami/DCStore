import React from 'react'
import { FaImages, FaBookMedical } from 'react-icons/fa'
import { FaPeopleLine } from 'react-icons/fa6'
import { SiSteelseries } from 'react-icons/si'

export default function DashboardStatsGrid() {
  return (
    <div className="flex gap-4 w-full">
      <BoxWrapper>
        <div className='rounded-full h-12 w-12 flex items-center justify-center bg-sky-500'>
        <FaPeopleLine className='text-2xl text-white'/>
        </div>
        <div className='pl-4'>
          <span className='text-sm text-gray-500 font-light'>Total Patients</span>
          <div className="flex items-center gap-2">
            <strong className='text-xl text-gray-700 font-semibold'>4000</strong>
            <span className='text-sm text-red-500 -pl-2'>-150</span>
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
      <div className='rounded-full h-12 w-12 flex items-center justify-center bg-green-500'>
        <FaBookMedical className='text-2xl text-white'/>
        </div>
        <div className='pl-4'>
          <span className='text-sm text-gray-500 font-light'>Total Studies</span>
          <div className="flex items-center gap-2">
            <strong className='text-xl text-gray-700 font-semibold'>4000</strong>
            <span className='text-sm text-green-500 -pl-2'>+10</span>
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
      <div className='rounded-full h-12 w-12 flex items-center justify-center bg-orange-500'>
        <SiSteelseries className='text-2xl text-white'/>
        </div>
        <div className='pl-4'>
          <span className='text-sm text-gray-500 font-light'>Total Series</span>
          <div className="flex items-center gap-2">
            <strong className='text-xl text-gray-700 font-semibold'>4000</strong>
            <span className='text-sm text-green-500 -pl-2'>+10</span>
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
      <div className='rounded-full h-12 w-12 flex items-center justify-center bg-neutral-500'>
        <FaImages className='text-2xl text-white'/>
        </div>
        <div className='pl-4'>
          <span className='text-sm text-gray-500 font-light'>Total Images</span>
          <div className="flex items-center gap-2">
            <strong className='text-xl text-gray-700 font-semibold'>400000</strong>
            <span className='text-sm text-green-500 -pl-2'>+1500</span>
          </div>
        </div>
      </BoxWrapper>
    </div>
  )
}

function BoxWrapper({ children }) {
  return (
    <div className="bg-white rounded-sm p-4 flex-1 border border-gray-200 flex items-center">
      { children }
    </div>
  )
}
