import React, { Fragment, useState } from 'react'
import { BiUpload } from 'react-icons/bi'
import { HiOutlineSearch, HiOutlineBell, HiOutlineChat} from 'react-icons/hi'
import { Popover, Transition, Menu } from '@headlessui/react'
import classNames from 'classnames'
import { useNavigate } from 'react-router-dom'
import Upload from './Upload'

export default function Header() {
  const { navigate } = useNavigate();
  const [ loading, setLoading] = useState(false);

  function loadUpload() {
    console.log('upload called');
    (loading) ? setLoading(false): setLoading(true);
  }

  return (
    <div className='h-16 px-3 flex justify-between w-full items-center bg-white'>
      <div className='relative'>
        { <HiOutlineSearch fontSize={16} className='absolute top-1/3 -translate-1/2 left-3'/> }
        <input
          type="text"
          placeholder='search'
          className='text-sm active: outline-none hover: outline-none h-10 w-[24rem] border border-gray-200 rounded-md pl-11 pr-4'/>
      </div>
      <div className='flex items-center gap-2 pr-2'>
        <Popover className="relative">
          {({ open }) => {
            return <>
              <Popover.Button
                className={classNames(
                  open && 'bg-gray-200',
                  'p-2 inline-flex items-center text-gray-700 hover:text-opacify-200 focus: outline-none')}>
                  <BiUpload fontSize={24}/>
              </Popover.Button>
              <Transition
                as={Fragment}
                enter='transition ease-out duration-200'
                enterFrom='opacity-0 translate-y-1'
                enterTo='opacity-100 translate-y-8'
                leave='transition ease-in duration-150'
                leaveFrom='opacity-100 translate-y-0'
                leaveTo='opacity-0 translate-y-1'
              >
                <Popover.Panel className='absolute -right-3 z-10'>
                  <div className='bg-sky-100 round-sm border-2 round-md p-3 z-10'>
                    <strong className="font-medium text-gray-900 font-semibold text-xl">Upload Images</strong>
                    <div className='mt-2 py-1 text-sm'><Upload/></div>
                  </div>
                </Popover.Panel>
              </Transition>
            </>
          }}
        </Popover>
        <Popover className="relative">
          {({ open }) => {
            return <>
              <Popover.Button
                className={classNames(
                  open && 'bg-gray-200',
                  'p-2 inline-flex items-center text-gray-700 hover:text-opacify-200 focus: outline-none')}>
                  <HiOutlineChat fontSize={24}/>
              </Popover.Button>
              <Transition
                as={Fragment}
                enter='transition ease-out duration-200'
                enterFrom='opacity-0 translate-y-1'
                enterTo='opacity-100 translate-y-8'
                leave='transition ease-in duration-150'
                leaveFrom='opacity-100 translate-y-0'
                leaveTo='opacity-0 translate-y-1'
              >
                <Popover.Panel className='absolute -right-3 w-60'>
                  <div className='bg-sky-100 round-sm'>
                    <strong className="font-medium text-gray-700">Messages</strong>
                    <div className='mt-2 py-1 text-sm'>Load messages in this pane!</div>
                  </div>
                </Popover.Panel>
              </Transition>
            </>
          }}
        </Popover>
        <Popover className='relative'>
        {({ open }) => {
            return <>
              <Popover.Button
                className={classNames(
                  open && 'bg-gray-200',
                  'p-2 inline-flex items-center text-gray-700 hover:text-opacify-200 focus: outline-none')}>
                 <HiOutlineBell fontSize={24}/>
              </Popover.Button>
              <Transition
                as={Fragment}
                enter='transition ease-out duration-200'
                enterFrom='opacity-0 translate-y-1'
                enterTo='opacity-100 translate-y-8'
                leave='transition ease-in duration-150'
                leaveFrom='opacity-100 translate-y-0'
                leaveTo='opacity-0 translate-y-1'
              >
                <Popover.Panel className='absolute -right-3 w-60'>
                  <div className="bg-sky-100 rounded-sm">
                    <strong className="font-medium text-gray-700">Notifications</strong>
                    <div className='mt-2 py-1 text-sm'>Load notifications in this pane!</div>
                  </div>
                </Popover.Panel>
              </Transition>
            </>
          }}
        </Popover>
        <Menu as='div' className='relative inline-block text-left'>
          <Menu.Button className='inline-flex w-full justify-center'>
            <div className='h-10 w-10 rounded-full bg-sky-500 bg-color bg-no-repeat bg-center' style={{backgroundImage: 'url("https://source.unsplash.com/80x80?face")'}}>
              <span className='sr-only'>User profile</span>
            </div>
          </Menu.Button>
          <Menu.Items className='origin-top-right z-10 absolute right-0 mt-2 w-48 bg-sky-100 rounded-sm ring-black ring-1ring-opacity-5 focus: bg-gray-200'>
            <Menu.Item as='div'>
              {({active}) => {
                return <button className={classNames(active && 'bg-blue-300', 'px-4 py-2 w-full')} onClick={() => navigate('/profile')}>
                  Profile
                </button>
                }}
            </Menu.Item>
            <Menu.Item as='div'>
              {({active}) => {
                return <button className={classNames(active && 'bg-blue-300', 'px-4 py-2 w-full')} onClick={() => navigate('/settings')}>
                  Settings
                </button>
              }}
            </Menu.Item>
            <Menu.Item as='div'>
              {({active}) => {
                return <button className={classNames(active && 'bg-blue-300', 'px-4 py-2 w-full')} onClick={() => navigate('/logout')}>
                  Log Out
                </button>
              }}
            </Menu.Item>
          </Menu.Items>
        </Menu>
      </div>
    </div>
  )
}
 