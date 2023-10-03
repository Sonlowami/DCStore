import React, { useState, useEffect } from 'react';
import { FaImages, FaBookMedical } from 'react-icons/fa';
import { FaPeopleLine } from 'react-icons/fa6';
import { SiSteelseries } from 'react-icons/si';
import { getData } from '../lib/helpers/queryFromApi'

export default function DashboardStatsGrid() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await getData('/api/v1/dicom_info');
        setStats(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="flex gap-4 w-full">
      <BoxWrapper>
        <div className="rounded-full h-12 w-12 flex items-center justify-center bg-sky-500">
          <FaPeopleLine className="text-2xl text-white" />
        </div>
        <div className="pl-4">
          <span className="text-sm text-gray-500 font-light">Total Patients</span>
          <div className="flex items-center gap-2">
            <strong className="text-xl text-gray-700 font-semibold">{stats.total_patients}</strong>
            {/* <span className={`text-sm ${stats.patients_change > 0 ? 'text-green-500' : 'text-red-500'} -pl-2`}>{stats.patients_change || 'N/A'}</span> */}
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
        <div className="rounded-full h-12 w-12 flex items-center justify-center bg-green-500">
          <FaBookMedical className="text-2xl text-white" />
        </div>
        <div className="pl-4">
          <span className="text-sm text-gray-500 font-light">Total Studies</span>
          <div className="flex items-center gap-2">
            <strong className="text-xl text-gray-700 font-semibold">{stats.total_studies}</strong>
            {/* <span className={`text-sm ${stats.studies_change > 0 ? 'text-green-500' : 'text-red-500'} -pl-2`}>{stats.studies_change || 'N/A'}</span> */}
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
        <div className="rounded-full h-12 w-12 flex items-center justify-center bg-orange-500">
          <SiSteelseries className="text-2xl text-white" />
        </div>
        <div className="pl-4">
          <span className="text-sm text-gray-500 font-light">Total Series</span>
          <div className="flex items-center gap-2">
            <strong className="text-xl text-gray-700 font-semibold">{stats.total_series}</strong>
            {/* <span className={`text-sm ${stats.series_change > 0 ? 'text-green-500' : 'text-red-500'} -pl-2`}>{stats.series_change || 'N/A'}</span> */}
          </div>
        </div>
      </BoxWrapper>
      <BoxWrapper>
        <div className="rounded-full h-12 w-12 flex items-center justify-center bg-neutral-500">
          <FaImages className="text-2xl text-white" />
        </div>
        <div className="pl-4">
          <span className="text-sm text-gray-500 font-light">Total Images</span>
          <div className="flex items-center gap-2">
            <strong className="text-xl text-gray-700 font-semibold">{stats.total_instances}</strong>
            {/* <span className={`text-sm ${stats.images_change > 0 ? 'text-green-500' : 'text-red-500'} -pl-2`}>{stats.images_change || 'N/A'}</span> */}
          </div>
        </div>
      </BoxWrapper>
    </div>
  );
}

function BoxWrapper({ children }) {
  return (
    <div className="bg-white rounded-sm p-4 flex-1 border border-gray-200 flex items-center">
      {children}
    </div>
  );
}
