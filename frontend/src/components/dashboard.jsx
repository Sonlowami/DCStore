import React from 'react'
import DashboardStatsGrid from './DashboardStatsGrid'
import TransactionChart from './TransactionChart'
import GenderProfileChart from './GenderProfileChart'
import RecentDataTable from './RecentData'

export default function Dashboard() {
  return (
    <div className="flex flex-col gap-4">
			<DashboardStatsGrid />
			<div className="flex flex-row gap-4 w-full">
				<TransactionChart />
				<GenderProfileChart />
			</div>
			<div className="flex flex-row gap-4 w-full">
				<RecentDataTable />
			</div>
		</div>
  )
}