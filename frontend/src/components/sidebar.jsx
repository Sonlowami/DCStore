import React from 'react'
import { FaHospitalSymbol } from 'react-icons/fa'
import { DASHBOARD_SIDEBAR_BOTTOM_LINKS, DASHBOARD_SIDEBAR_LINKS } from '../lib/consts/navigation'
import { Link, useLocation } from 'react-router-dom'
import classNames from 'classnames'
import { HiOutlineLogout } from 'react-icons/hi'

const linkClasses = 'flex align-center font-light px-3 py-2 hover:bg-neutral-700 active: bg-neutral-900 hover:no-underline rounded-sm text-base'

export default function Sidebar() {
  return (
    <div className='p-3 mr-10 flex flex-col bg-neutral-900 text-white'>
      <div className="flex items-center gap-3 px-1 py-3">
        <FaHospitalSymbol fontSize={24}/>
        <span className='text-lg'>DCStore</span>
      </div>
      <div className='flex-1 p-2'>
        { DASHBOARD_SIDEBAR_LINKS.map((item) => {
          return <SidebarLink key={item.key} item={item}/>
        })}
      </div>
      <div>
        {DASHBOARD_SIDEBAR_BOTTOM_LINKS.map((item) => {
          return <SidebarLink key={item.key} item={item}/>
        })}
        <div className={classNames('text-red-400 cursor-pointer', linkClasses)}>
          <span className='text-xl'><HiOutlineLogout/></span> Log Out
        </div>
      </div>
    </div>
  )
}

function SidebarLink ({ item }) {
  const {pathname} = useLocation()
  return (
    <Link to={ item.path } className={
        classNames(pathname === item.path ? "text-white bg-neutral-600" : 'text-neutral-500', linkClasses)
      }>
      <span className='text-xl pr-2'>{ item.icon } </span>
      { item.label }
    </Link>
  )
}
