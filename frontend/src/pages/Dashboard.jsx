import React, { useEffect, useState } from 'react'
import AISummaryCard from '../components/AISummaryCard'
import FlightTrendsChart from '../components/FlightTrendsChart'
import SentimentChart from '../components/SentimentChart'

export default function Dashboard(){
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Flight Fare & Sentiment Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 bg-white p-4 rounded shadow">
          <FlightTrendsChart />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <AISummaryCard />
          <SentimentChart />
        </div>
      </div>
    </div>
  )
}
