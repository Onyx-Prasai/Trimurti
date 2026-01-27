import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import FindBlood from './pages/FindBlood'
import Dashboard from './pages/Dashboard'
import AIHealth from './pages/AIHealth'
import Notification from './pages/Notification'
import Points from './pages/Points'
import Profile from './pages/Profile'
import BloodStockDashboard from './pages/BloodStockDashboard'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/find-blood" element={<FindBlood />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/ai-health" element={<AIHealth />} />
          <Route path="/notification" element={<Notification />} />
          <Route path="/points" element={<Points />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/blood-stock" element={<BloodStockDashboard />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

