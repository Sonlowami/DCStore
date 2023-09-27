import React from 'react'
import { format } from 'date-fns'
import { Link } from 'react-router-dom'
import { getStudyStatus } from '../lib/helpers'

const recentStudiesData = [
	{
    studyId: 301,
    patientId: 1,
    referringPhysician: 'Dr. Adams',
    date_taken: '2023-09-25',
    time_taken: '10:30 AM',
    action: 'uploaded',
    description: 'X-ray Chest',
  },
  {
    studyId: 302,
    patientId: 2,
    referringPhysician: 'Dr. Smith',
    date_taken: '2023-09-26',
    time_taken: '9:45 AM',
    action: 'downloaded',
    description: 'MRI Brain Scan',
  },
  {
    studyId: 303,
    patientId: 3,
    referringPhysician: 'Dr. Johnson',
    date_taken: '2023-09-27',
    time_taken: '3:15 PM',
    action: 'modified',
    description: 'CT Abdomen',
  },
  {
    studyId: 304,
    patientId: 4,
    referringPhysician: 'Dr. Anderson',
    date_taken: '2023-09-24',
    time_taken: '11:20 AM',
    action: 'uploaded',
    description: 'Ultrasound Heart',
  },
];


export default function RecentStudiesTable() {
	return (
		<div className="bg-white px-4 pt-3 pb-4 rounded-sm bstudy bstudy-gray-200 flex-1">
			<strong className="text-gray-700 font-medium">Recent Studies</strong>
			<div className="bstudy-x bstudy-gray-200 rounded-sm mt-3">
				<table className="w-full text-gray-700">
					<thead>
						<tr>
							<th>ID</th>
							<th>Patient ID</th>
							<th>Referring Physician</th>
							<th>Taken Date</th>
							<th>Taken Time</th>
							<th>Description</th>
							<th>Action</th>
						</tr>
					</thead>
					<tbody>
						{recentStudiesData.map((study) => (
							<tr key={study.id}>
								<td>
									<Link to={`/study/${study.id}`}>#{study.id}</Link>
								</td>
								<td>
									<Link to={`/product/${study.patientId}`}>#{study.patientId}</Link>
								</td>
								<td>
									<Link to={`/customer/${study.referringPhysician}`}>{study.referringPhysician}</Link>
								</td>
								<td>{format(new Date(study.date_taken), 'dd MMM yyyy')}</td>
								<td>{study.time_taken}</td>
								<td>{study.description}</td>
								<td>{getStudyStatus(study.action)}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}