// commenting out import for now 
// import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import AppHeader from './components/AppHeader/AppHeader'

function App() {
  return (
    <>
    <div className ="w-full min-h screen">
      <AppHeader/>
      <LoginPage />
    </div>
    </>
  )
}

export default App
