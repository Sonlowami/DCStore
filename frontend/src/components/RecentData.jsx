import React from 'react'

const data = [
  {
    firstName: "John",
    lastName: "Doe",
    age: 30,
    city: "New York",
  },
  {
    firstName: "Jane",
    lastName: "Smith",
    age: 28,
    city: "Los Angeles",
  },
  {
    firstName: "Bob",
    lastName: "Johnson",
    age: 35,
    city: "Chicago",
  },
];

export default function RecentDataTable() {
  return (
    <div className='w-full'>
      <table className="table">
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Age</th>
            <th>City</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.firstName}</td>
              <td>{row.lastName}</td>
              <td>{row.age}</td>
              <td>{row.city}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
