import React from 'react';
import { ResponsiveContainer, BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Bar } from 'recharts';

const data = [
  {Patients:489, Studies:1412, Series:1620, Month:5},
  {Patients:254, Studies:6558, Series:596, Month:10},
  {Patients:56, Studies:4200, Series:939, Month:11},
  {Patients:306, Studies:6748, Series:1088, Month:4},
  {Patients:469, Studies:3306, Series:3103, Month:3},
  {Patients:61, Studies:3599, Series:3347, Month:6},
  {Patients:286, Studies:1630, Series:9375, Month:8},
  {Patients:98, Studies:5206, Series:3623, Month:2},
]

export default function TransactionChart() {
  return (
    <div className='h-[22rem] bg-white p-4 border border-gray-200 flex flex-cols flex-1'>
      <strong className='text-gray-700 font-medium'>Patient Chart</strong>
      <div className="w-full mt-3">
        <ResponsiveContainer  width={750} height={300}>
        <BarChart width={730} height={250} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Patients" fill="#8884d8" />
          <Bar dataKey="Studies" fill="#82ca9d" />
        </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
