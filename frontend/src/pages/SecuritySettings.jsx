import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaLock, FaShieldAlt } from 'react-icons/fa'

const SecuritySettings = () => {
  const navigate = useNavigate()
  const [twoFAEnabled, setTwoFAEnabled] = useState(false)
  const [showPasswordForm, setShowPasswordForm] = useState(false)
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  })
  const [message, setMessage] = useState('')

  const handlePasswordChange = (e) => {
    const { name, value } = e.target
    setPasswordData(prev => ({ ...prev, [name]: value }))
  }

  const handlePasswordSubmit = () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage('Passwords do not match!')
      return
    }
    if (passwordData.newPassword.length < 8) {
      setMessage('Password must be at least 8 characters!')
      return
    }
    setMessage('Password changed successfully!')
    setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' })
    setTimeout(() => {
      setShowPasswordForm(false)
      setMessage('')
    }, 3000)
  }

  const handleTwoFAToggle = () => {
    setTwoFAEnabled(!twoFAEnabled)
    setMessage(twoFAEnabled ? '2FA disabled' : '2FA enabled')
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <button
          onClick={() => navigate('/settings')}
          className="flex items-center space-x-2 text-primary hover:text-primary-dark mb-4"
        >
          <FaArrowLeft />
          <span>Back to Settings</span>
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Privacy & Security</h1>
        <p className="text-gray-600 mb-8">Manage your account security</p>

        {/* Message */}
        {message && (
          <div className={`${message.includes('Error') || message.includes('not') ? 'bg-red-50 border-red-200 text-red-700' : 'bg-green-50 border-green-200 text-green-700'} border px-4 py-3 rounded-lg mb-6`}>
            {message}
          </div>
        )}

        {/* Security Options */}
        <div className="space-y-6">
          {/* Change Password */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center space-x-3 mb-4">
              <FaLock className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold text-gray-900">Change Password</h2>
            </div>

            {!showPasswordForm ? (
              <button
                onClick={() => setShowPasswordForm(true)}
                className="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-dark transition-all"
              >
                Change Password
              </button>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                  <input
                    type="password"
                    name="currentPassword"
                    value={passwordData.currentPassword}
                    onChange={handlePasswordChange}
                    placeholder="Enter current password"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                  <input
                    type="password"
                    name="newPassword"
                    value={passwordData.newPassword}
                    onChange={handlePasswordChange}
                    placeholder="Enter new password (min 8 characters)"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={passwordData.confirmPassword}
                    onChange={handlePasswordChange}
                    placeholder="Confirm new password"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>

                <div className="flex space-x-3">
                  <button
                    onClick={handlePasswordSubmit}
                    className="flex-1 bg-primary text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-dark transition-all"
                  >
                    Update Password
                  </button>
                  <button
                    onClick={() => {
                      setShowPasswordForm(false)
                      setMessage('')
                    }}
                    className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-all"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Two-Factor Authentication */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <FaShieldAlt className="w-5 h-5 text-primary" />
                <h2 className="text-xl font-semibold text-gray-900">Two-Factor Authentication</h2>
              </div>
              <button
                onClick={handleTwoFAToggle}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  twoFAEnabled
                    ? 'bg-primary text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {twoFAEnabled ? 'ENABLED' : 'DISABLED'}
              </button>
            </div>
            <p className="text-gray-600">
              {twoFAEnabled
                ? '✓ Two-factor authentication is enabled. You will be asked for a verification code when logging in.'
                : 'Two-factor authentication adds an extra layer of security to your account.'}
            </p>
          </div>

          {/* Login History */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Login Activity</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">Chrome on Windows</p>
                  <p className="text-sm text-gray-600">IP: 192.168.1.1 • Today</p>
                </div>
                <span className="text-green-600 text-sm">Current</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">Safari on iPhone</p>
                  <p className="text-sm text-gray-600">IP: 192.168.1.2 • Yesterday</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SecuritySettings
