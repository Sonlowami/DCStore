import React, { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { Link } from 'react-router-dom'
import { getStudyStatus } from '../lib/helpers'
import { getData } from '../lib/helpers/queryFromApi'


export default function RecentStudiesTable() {
	const [recentStudiesData, setRecentStudiesData] = useState([])

	useEffect(() => {
		const fetchRecentStudies = async () => {
			try {
				const response = await getData('/api/v1/recent_files')
				setRecentStudiesData(response.data)
			} catch (error) {
				console.error(error)
			}
		}
		fetchRecentStudies()
	}
		, [])
	return (
		<div className="bg-white px-4 pt-3 pb-4 rounded-sm bstudy bstudy-gray-200 flex-1">
			<strong className="text-gray-700 font-medium">Recent Activities</strong>
			<div className="bstudy-x bstudy-gray-200 rounded-sm mt-3">
				<table className="w-full text-gray-700">
					<thead>
						<tr>
							<th>File Name</th>
							<th>Action</th>
							<th>At</th>
							<th>Patient Name</th>
							<th>Instance Number</th>
							<th>Study Description</th>
							<th>Series Description</th>
						</tr>
					</thead>
					<tbody>
						{recentStudiesData.map((study) => (
							<tr key={study.fileID}>
								<td>{study.info.filename}</td>
								<td>{study.info.action}</td>
								<td>{new Date(study.info.datetime).toLocaleString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true })}</td>
								<td>{study.info.patientName}</td>
								<td>{study.info.instanceNumber}</td>
								<td>{study.info.studyDescription}</td>
								<td>{study.info.seriesDescription}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}
