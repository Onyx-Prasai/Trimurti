import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaUser, FaShieldAlt, FaBell, FaTint, FaCreditCard, FaLanguage, FaMoon, FaQuestionCircle, FaFileAlt } from 'react-icons/fa'

const Settings = () => {
  const navigate = useNavigate()
  const [darkMode, setDarkMode] = useState(localStorage.getItem('darkMode') === 'true')
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en')
  const [notifications, setNotifications] = useState(localStorage.getItem('notifications') !== 'false')

  const handleDarkModeToggle = () => {
    const newDarkMode = !darkMode
    setDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode)
    document.documentElement.classList.toggle('dark', newDarkMode)
  }

  const handleLanguageChange = (lang) => {
    setLanguage(lang)
    localStorage.setItem('language', lang)
    console.log(`Language changed to: ${lang}`)
  }

  const handleNotificationsToggle = () => {
    const newNotifications = !notifications
    setNotifications(newNotifications)
    localStorage.setItem('notifications', newNotifications)
  }

  const settingsSections = [
    { id: 'account', label: 'Account Settings', icon: FaUser, description: 'Manage your profile' },
    { id: 'security', label: 'Privacy & Security', icon: FaShieldAlt, description: 'Security settings' },
    { id: 'donation', label: 'Blood Donation Profile', icon: FaTint, description: 'Donation information' },
    { id: 'payment', label: 'Payment Methods', icon: FaCreditCard, description: 'Payment details' },
    { id: 'help', label: 'Help & Support', icon: FaQuestionCircle, description: 'Get help' },
    { id: 'legal', label: 'Legal & Privacy', icon: FaFileAlt, description: 'Legal documents' },
  ]

  const handleNavigate = (section) => {
    navigate(`/settings/${section}`)
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center space-x-2 text-primary hover:text-primary-dark mb-4"
          >
            <FaArrowLeft />
            <span>Back</span>
          </button>
          <h1 className="text-4xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-2">Manage your account and preferences</p>
        </div>

        {/* Quick Settings */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Quick Settings</h2>

          {/* Dark Mode */}
          <div className="flex items-center justify-between py-4 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <FaMoon className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium text-gray-900">Dark Mode</p>
                <p className="text-sm text-gray-600">Enable dark theme</p>
              </div>
            </div>
            <button
              onClick={handleDarkModeToggle}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                darkMode
                  ? 'bg-primary text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {darkMode ? 'ON' : 'OFF'}
            </button>
          </div>

          {/* Notifications */}
          <div className="flex items-center justify-between py-4 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <FaBell className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium text-gray-900">Notifications</p>
                <p className="text-sm text-gray-600">Enable push notifications</p>
              </div>
            </div>
            <button
              onClick={handleNotificationsToggle}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                notifications
                  ? 'bg-primary text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {notifications ? 'ON' : 'OFF'}
            </button>
          </div>

          {/* Language */}
          <div className="py-4">
            <div className="flex items-center space-x-3 mb-4">
              <FaLanguage className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium text-gray-900">Language</p>
                <p className="text-sm text-gray-600">Choose your preferred language</p>
              </div>
            </div>
            <div className="flex space-x-2">
              {[
                { code: 'en', label: 'English' },
                { code: 'ne', label: 'Nepali' },
                { code: 'hi', label: 'Hindi' },
              ].map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageChange(lang.code)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    language === lang.code
                      ? 'bg-primary text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Settings Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {settingsSections.map((section) => {
            const Icon = section.icon
            return (
              <button
                key={section.id}
                onClick={() => handleNavigate(section.id)}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all text-left hover:translate-y-[-2px]"
              >
                <div className="flex items-center space-x-4">
                  <div className="bg-primary bg-opacity-10 p-3 rounded-lg">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{section.label}</h3>
                    <p className="text-sm text-gray-600">{section.description}</p>
                  </div>
                </div>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default Settings
