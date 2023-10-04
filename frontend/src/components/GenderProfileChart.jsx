import React, { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'
import { getData } from '../lib/helpers/queryFromApi'


const RADIAN = Math.PI / 180
const COLORS = ['#00C49F', '#FFBB28', '#FF8042']

const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
	const radius = innerRadius + (outerRadius - innerRadius) * 0.5
	const x = cx + radius * Math.cos(-midAngle * RADIAN)
	const y = cy + radius * Math.sin(-midAngle * RADIAN)

	return (
		<text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
			{`${(percent * 100).toFixed(0)}%`}
		</text>
	)
}

export default function GenderProfilePieChart() {
	const [data, setData] = useState([])

	useEffect(() => {
		const fetchStats = async () => {
			try {
				const response = await getData('/api/v1/patients_gender_count');
				const new_data = [
					{ name: 'Male', value: response.data['males'] },
					{ name: 'Female', value: response.data['females'] },
					{ name: 'Other', value: response.data['others'] }
				]
				setData(new_data)
			} catch (error) {
				console.error(error)
			}
		}
		fetchStats()
	}
		, [])
	
	return (
		<div className="w-[20rem] h-[22rem] bg-white p-4 rounded-sm border border-gray-200 flex flex-col">
			<strong className="text-gray-700 font-medium">Patient Profile</strong>
			<div className="mt-3 w-full flex-1 text-xs">
				<ResponsiveContainer width="100%" height="100%">
					<PieChart width={400} height={300}>
						<Pie
							data={data}
							cx="50%"
							cy="45%"
							labelLine={false}
							label={renderCustomizedLabel}
							outerRadius={105}
							fill="#8884d8"
							dataKey="value"
						>
							{data.map((_, index) => (
								<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
							))}
						</Pie>
						<Legend />
					</PieChart>
				</ResponsiveContainer>
			</div>
		</div>
	)
}
