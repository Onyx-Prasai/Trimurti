import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import FindBlood from './pages/FindBlood'
import BloodPrediction from './pages/BloodPrediction'
import BloodRequest from './pages/BloodRequest'
import Dashboard from './pages/Dashboard'
import AIHealth from './pages/AIHealth'
import Notification from './pages/Notification'
import Points from './pages/Points'
import Profile from './pages/Profile'
import BloodStockDashboard from './pages/BloodStockDashboard'
import Login from './pages/Login'
import Register from './pages/Register'
import Settings from './pages/Settings'
import AccountSettings from './pages/AccountSettings'
import SecuritySettings from './pages/SecuritySettings'
import BloodDonationProfile from './pages/BloodDonationProfile'
import PaymentMethods from './pages/PaymentMethods'
import HelpSupport from './pages/HelpSupport'
import LegalPrivacy from './pages/LegalPrivacy'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/find-blood" element={isAuthenticated ? <FindBlood /> : <Navigate to="/login" />} />
          <Route path="/blood-prediction" element={isAuthenticated ? <BloodPrediction /> : <Navigate to="/login" />} />
          <Route path="/blood-request" element={isAuthenticated ? <BloodRequest /> : <Navigate to="/login" />} />
          <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/ai-health" element={isAuthenticated ? <AIHealth /> : <Navigate to="/login" />} />
          <Route path="/notification" element={isAuthenticated ? <Notification /> : <Navigate to="/login" />} />
          <Route path="/points" element={isAuthenticated ? <Points /> : <Navigate to="/login" />} />
          <Route path="/profile" element={isAuthenticated ? <Profile setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" />} />
          <Route path="/blood-stock" element={isAuthenticated ? <BloodStockDashboard /> : <Navigate to="/login" />} />
          <Route path="/settings" element={isAuthenticated ? <Settings /> : <Navigate to="/login" />} />
          <Route path="/settings/account" element={isAuthenticated ? <AccountSettings /> : <Navigate to="/login" />} />
          <Route path="/settings/security" element={isAuthenticated ? <SecuritySettings /> : <Navigate to="/login" />} />
          <Route path="/settings/donation" element={isAuthenticated ? <BloodDonationProfile /> : <Navigate to="/login" />} />
          <Route path="/settings/payment" element={isAuthenticated ? <PaymentMethods /> : <Navigate to="/login" />} />
          <Route path="/settings/help" element={isAuthenticated ? <HelpSupport /> : <Navigate to="/login" />} />
          <Route path="/settings/legal" element={isAuthenticated ? <LegalPrivacy /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

