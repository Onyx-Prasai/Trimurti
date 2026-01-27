import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import Logo from './Logo'
import { FaHome, FaTint, FaChartLine, FaRobot, FaBell, FaGift, FaUser } from 'react-icons/fa'

const Navbar = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/find-blood', label: 'Find Blood', icon: FaTint },
    { path: '/dashboard', label: 'Dashboard', icon: FaChartLine },
    { path: '/ai-health', label: 'AI Health', icon: FaRobot },
    { path: '/notification', label: 'Notification', icon: FaBell },
    { path: '/points', label: 'Points', icon: FaGift },
    { path: '/profile', label: 'Profile', icon: FaUser },
  ]

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

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-text">
              <FaHome className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

