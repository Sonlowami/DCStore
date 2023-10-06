import {
  HiOutlineViewGrid,
  HiOutlineQuestionMarkCircle,
  HiOutlineCog,
  HiOutlineAnnotation
} from 'react-icons/hi'

import {
  FaBookMedical,
  FaShareAltSquare,
  FaHistory
} from 'react-icons/fa'

import {FaPersonHalfDress} from 'react-icons/fa6'
export const DASHBOARD_SIDEBAR_LINKS = [
  {
    key: 'dashboard',
    label: 'Dashboard',
    path: '/',
    icon: <HiOutlineViewGrid/>
  },
  {
    key: 'patients',
    label: 'Patients',
    path: '/patients',
    icon: <FaPersonHalfDress/>
  },
  {
    key: 'studies',
    label: 'Studies',
    path: '/studies',
    icon: <FaBookMedical/>
  },
  {
    key: 'series',
    label: 'Series',
    path: '/series',
    icon: <FaBookMedical/>
  },
  {
    key: 'instances',
    label: 'Instances',
    path: 'instances',
    icon: <FaBookMedical/>
  },
  // {
  //   key: 'history',
  //   label: 'History',
  //   path: '/history',
  //   icon: <FaHistory/>
  // },
  // {
  //   key: 'messages',
  //   label: 'Messages',
  //   path: '/messages',
  //   icon: <HiOutlineAnnotation/>
  // }
]

export const DASHBOARD_SIDEBAR_BOTTOM_LINKS = [
  // {
  //   key: 'settings',
  //   label: 'Settings',
  //   path: '/settings',
  //   icon: <HiOutlineCog/>
  // },
  // {
  //   key: 'support',
  //   label: 'Help & Support',
  //   path: '/support',
  //   icon: <HiOutlineQuestionMarkCircle/>
  // },
]
