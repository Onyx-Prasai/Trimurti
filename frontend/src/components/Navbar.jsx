import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'
import Logo from './Logo'
import { FaHome, FaTint, FaChartLine, FaRobot, FaBell, FaGift, FaUser, FaSignInAlt, FaSignOutAlt, FaBars, FaTimes, FaCog } from 'react-icons/fa'

const Navbar = ({ isAuthenticated, setIsAuthenticated }) => {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const authenticatedNavItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/find-blood', label: 'Find Blood', icon: FaTint },
    { path: '/dashboard', label: 'Dashboard', icon: FaChartLine },
    { path: '/ai-health', label: 'AI Health', icon: FaRobot },
    { path: '/notification', label: 'Notification', icon: FaBell },
    { path: '/points', label: 'Points', icon: FaGift },
    { path: '/profile', label: 'Profile', icon: FaUser },
  ]

  const hamburgerMenuItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/find-blood', label: 'Find Blood', icon: FaTint },
    { path: '/blood-prediction', label: 'Blood Prediction', icon: FaChartLine },
    { path: '/blood-request', label: 'Blood Request', icon: FaTint },
    { path: '/profile', label: 'Profile', icon: FaUser },
    { path: '/settings', label: 'Settings', icon: FaCog },
  ]

  const publicNavItems = [
    { path: '/', label: 'Home', icon: FaHome },
  ]

  const navItems = isAuthenticated ? authenticatedNavItems : publicNavItems

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    window.location.href = '/'
  }

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3">
            <Logo />
            <span className="text-xl font-bold text-primary">Blood Hub Nepal</span>
          </Link>
          
          <div className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${
                    isActive
                      ? 'bg-primary text-white'
                      : 'text-text hover:bg-gray-100'
                  }`}
                >
                  <Icon />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>

          {/* Auth buttons */}
          <div className="hidden md:flex space-x-2">
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700 transition-all"
              >
                <FaSignOutAlt />
                <span>Logout</span>
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${
                    location.pathname === '/login'
                      ? 'bg-primary text-white'
                      : 'text-text hover:bg-gray-100'
                  }`}
                >
                  <FaSignInAlt />
                  <span>Login</span>
                </Link>
                <Link
                  to="/register"
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all ${
                    location.pathname === '/register'
                      ? 'bg-primary text-white'
                      : 'text-text hover:bg-gray-100'
                  }`}
                >
                  <FaUser />
                  <span>Register</span>
                </Link>
              </>
            )}
          </div>

          {/* Hamburger menu button */}
          {isAuthenticated && (
            <div>
              <button 
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="text-black p-2 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {mobileMenuOpen ? (
                  <FaTimes className="w-6 h-6" />
                ) : (
                  <FaBars className="w-6 h-6" />
                )}
              </button>
            </div>
          )}
        </div>

        {/* Hamburger Menu */}
        {isAuthenticated && mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-gray-200 bg-white"
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              {hamburgerMenuItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`block px-4 py-2 rounded-lg transition-colors flex items-center space-x-3 ${
                      isActive
                        ? 'bg-primary text-white'
                        : 'text-text hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
              <button
                onClick={() => {
                  handleLogout()
                  setMobileMenuOpen(false)
                }}
                className="w-full text-left px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors flex items-center space-x-3"
              >
                <FaSignOutAlt className="w-5 h-5" />
                <span>Logout</span>
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  )
}

export default Navbar

