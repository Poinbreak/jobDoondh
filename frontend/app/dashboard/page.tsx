"use client";

import Layout from '@/components/layout';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  // Mock data for UI development before hooking up to backend
  const skillData = [
    { skill: 'Python', user: 100, job: 100 },
    { skill: 'React', user: 100, job: 80 },
    { skill: 'FastAPI', user: 0, job: 100 },
    { skill: 'Docker', user: 50, job: 80 },
    { skill: 'Postgres', user: 100, job: 50 },
    { skill: 'AWS', user: 0, job: 70 },
  ];

  return (
    <Layout>
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Dashboard</h1>
        <p className="text-gray-600 mb-8">Welcome back. Here is your current skill profile compared to your target jobs.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">Profile & Goals</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Target Role</label>
                <input type="text" defaultValue="Software Engineer" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Target Location</label>
                <input type="text" defaultValue="Remote" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                Save Profile
              </button>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-100 flex flex-col items-center">
            <h2 className="text-lg font-semibold mb-2">Skill Radar (Matched vs Missing)</h2>
            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={skillData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="skill" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="Your Skills" dataKey="user" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.5} />
                  <Radar name="Job Requirements" dataKey="job" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
