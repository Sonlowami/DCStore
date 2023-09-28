import React from 'react'
import DashboardStatsGrid from './DashboardStatsGrid'
import TransactionChart from './TransactionChart'
import GenderProfileChart from './GenderProfileChart'
import RecentStudiesTable from './RecentData'

export default function Dashboard() {
  return (
    <div className="flex flex-col gap-4">
			<DashboardStatsGrid />
			<div className="flex flex-row gap-4 w-full">
				<TransactionChart />
				<GenderProfileChart />
			</div>
			<div className="flex flex-row gap-4 w-full">
				<RecentStudiesTable />
			</div>
		</div>
  )
}