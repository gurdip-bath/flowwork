// commenting out import for now 
// import { useState } from 'react'
import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import AppHeader from './components/AppHeader/AppHeader'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <div className="w-full min-h-screen">
      <AppHeader/>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </div>
  )
}

export default App
