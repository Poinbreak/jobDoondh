"use client";

import { useState } from 'react';
import Layout from '@/components/layout';
import { UploadCloud, CheckCircle, AlertTriangle } from 'lucide-react';

export default function ResumeHub() {
  const [isUploading, setIsUploading] = useState(false);
  const [scoreData, setScoreData] = useState<{score: number, feedback: string[]} | null>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setIsUploading(true);
      // Mock upload and scoring
      setTimeout(() => {
        setIsUploading(false);
        setScoreData({
          score: 75,
          feedback: [
            "Good resume length (300-800 words).",
            "All core sections (Education, Experience, Skills, Projects) are present.",
            "Good use of action verbs, but could use more impactful words.",
            "Some quantified achievements found. Try to add more numbers to prove your impact.",
            "Good use of bullet points for readability."
          ]
        });
      }, 1500);
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Resume Hub</h1>
        
        <div className="bg-white rounded-lg shadow p-8 mb-8 text-center border-2 border-dashed border-gray-300">
          <UploadCloud className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h2 className="text-lg font-medium text-gray-900 mb-2">Upload your latest resume</h2>
          <p className="text-gray-500 mb-6">Supports PDF and DOCX files up to 5MB.</p>
          
          <label className="cursor-pointer bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 transition-colors inline-block">
            {isUploading ? "Uploading & Analyzing..." : "Select File"}
            <input type="file" className="hidden" accept=".pdf,.docx" onChange={handleUpload} disabled={isUploading} />
          </label>
        </div>

        {scoreData && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Resume Analysis</h3>
              <div className="flex items-center">
                <span className="text-sm text-gray-500 mr-2">Rule-based Score:</span>
                <span className={`text-xl font-bold ${scoreData.score >= 80 ? 'text-green-600' : scoreData.score >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
                  {scoreData.score}/100
                </span>
              </div>
            </div>
            
            <div className="p-6">
              <h4 className="text-sm font-medium text-gray-900 uppercase tracking-wider mb-4">Feedback & Suggestions</h4>
              <ul className="space-y-3">
                {scoreData.feedback.map((item, idx) => (
                  <li key={idx} className="flex items-start">
                    {item.includes('Try') || item.includes('Consider') || item.includes('more') ? (
                      <AlertTriangle className="w-5 h-5 text-yellow-500 mr-3 flex-shrink-0 mt-0.5" />
                    ) : (
                      <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                    )}
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
