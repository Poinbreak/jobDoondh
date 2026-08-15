"use client";

import { useState } from 'react';
import Layout from '@/components/layout';
import { Briefcase, MapPin, Building, Calendar, Star, FileText } from 'lucide-react';

export default function JobsFeed() {
  const [quotaRemaining, setQuotaRemaining] = useState(5);
  
  // Mock data for UI
  const jobs = [
    {
      id: "1",
      title: "Senior Full Stack Engineer",
      company: "TechCorp India",
      location: "Bangalore",
      description: "Looking for an experienced engineer with strong Python and React skills to lead our core product team...",
      match_score: 92,
      posted_at: "2 hours ago"
    },
    {
      id: "2",
      title: "Backend Developer (FastAPI)",
      company: "StartupInc",
      location: "Remote",
      description: "Join our fast-growing startup to build scalable microservices using FastAPI and Postgres.",
      match_score: 85,
      posted_at: "1 day ago"
    }
  ];

  const handleGeneratePitch = (jobId: string) => {
    if (quotaRemaining > 0) {
      setQuotaRemaining(prev => prev - 1);
      alert(`Generating AI Pitch for job ${jobId}... (Mock)`);
    } else {
      alert("Daily pitch limit reached. Please try again tomorrow.");
    }
  };

  return (
    <Layout>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Recommended Jobs</h1>
        <div className="bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">
          Pitch Quota: {quotaRemaining}/5 remaining today
        </div>
      </div>
      
      <div className="space-y-6">
        {jobs.map(job => (
          <div key={job.id} className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-1">{job.title}</h2>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
                    <div className="flex items-center"><Building className="w-4 h-4 mr-1" /> {job.company}</div>
                    <div className="flex items-center"><MapPin className="w-4 h-4 mr-1" /> {job.location}</div>
                    <div className="flex items-center"><Calendar className="w-4 h-4 mr-1" /> {job.posted_at}</div>
                  </div>
                </div>
                <div className="flex flex-col items-end">
                  <div className="bg-green-100 text-green-800 text-lg font-bold px-3 py-1 rounded flex items-center">
                    <Star className="w-4 h-4 mr-1 fill-current" />
                    {job.match_score}% Match
                  </div>
                </div>
              </div>
              
              <p className="text-gray-700 mb-6">{job.description}</p>
              
              <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                <button className="text-blue-600 hover:text-blue-800 font-medium text-sm flex items-center">
                  View full details
                </button>
                <button 
                  onClick={() => handleGeneratePitch(job.id)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium text-sm flex items-center transition-colors"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Generate AI Pitch
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
