import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
    setLoading(false)
  }, [])

  useEffect(() => {
    const handleUnauthorized = () => setIsAuthenticated(false)
    window.addEventListener('auth:unauthorized', handleUnauthorized)
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized)
  }, [])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
        <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/signup" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Signup />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  )
}

export default App
