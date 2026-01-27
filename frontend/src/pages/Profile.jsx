import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaUser, FaEdit, FaSave, FaSignOutAlt } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'
import { getDonorProfile } from '../utils/api'

const Profile = ({ setIsAuthenticated }) => {
  const [donor, setDonor] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address: '',
    city: 'Kathmandu',
    blood_group: 'O+',
  })
  const donorId = 1 // In real app, get from auth context

  useEffect(() => {
    fetchDonorData()
  }, [])

  const fetchDonorData = async () => {
    try {
      const response = await getDonorProfile(donorId)
      const data = response.data
      setDonor(data)
      setFormData({
        first_name: data.user?.first_name || '',
        last_name: data.user?.last_name || '',
        email: data.user?.email || '',
        phone: data.phone || '',
        address: data.address || '',
        city: data.city || 'Kathmandu',
        blood_group: data.blood_group || 'O+',
      })
    } catch (error) {
      console.error('Error fetching donor data:', error)
      // Mock data for demo
      setDonor({
        id: 1,
        user: { first_name: 'John', last_name: 'Doe', email: 'john@example.com' },
        phone: '+977-9841234567',
        address: 'Kathmandu, Nepal',
        city: 'Kathmandu',
        blood_group: 'O+',
        points: 320,
        total_donations: 3,
      })
      setFormData({
        first_name: 'John',
        last_name: 'Doe',
        email: 'john@example.com',
        phone: '+977-9841234567',
        address: 'Kathmandu, Nepal',
        city: 'Kathmandu',
        blood_group: 'O+',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSave = () => {
    // In real app, make API call to update profile
    console.log('Saving profile:', formData)
    setEditing(false)
    alert('Profile updated successfully!')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/')
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
  const cities = ['Kathmandu', 'Bhaktapur', 'Lalitpur']

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-text mb-8 text-center flex items-center justify-center"
        >
          <FaUser className="mr-3 text-primary" />
          Profile
        </motion.h1>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-8 shadow-lg"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-text">Personal Information</h2>
            <div className="flex space-x-2">
              {!editing ? (
                <button
                  onClick={() => setEditing(true)}
                  className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-xl hover:bg-red-600 transition-all"
                >
                  <FaEdit />
                  <span>Edit</span>
                </button>
              ) : (
                <button
                  onClick={handleSave}
                  className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-xl hover:bg-green-700 transition-all"
                >
                  <FaSave />
                  <span>Save</span>
                </button>
              )}
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-xl hover:bg-red-700 transition-all"
              >
                <FaSignOutAlt />
                <span>Logout</span>
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-text mb-2">
                First Name
              </label>
              {editing ? (
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              ) : (
                <p className="text-text">{formData.first_name || 'N/A'}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Last Name
              </label>
              {editing ? (
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              ) : (
                <p className="text-text">{formData.last_name || 'N/A'}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Email
              </label>
              {editing ? (
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              ) : (
                <p className="text-text">{formData.email || 'N/A'}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Phone
              </label>
              {editing ? (
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              ) : (
                <p className="text-text">{formData.phone || 'N/A'}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Blood Group
              </label>
              {editing ? (
                <select
                  value={formData.blood_group}
                  onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  {bloodTypes.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              ) : (
                <p className="text-text font-semibold text-primary">{formData.blood_group}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                City
              </label>
              {editing ? (
                <select
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  {cities.map((city) => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </select>
              ) : (
                <p className="text-text">{formData.city}</p>
              )}
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-text mb-2">
                Address
              </label>
              {editing ? (
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              ) : (
                <p className="text-text">{formData.address || 'N/A'}</p>
              )}
            </div>
          </div>

          {/* Stats Section */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <h3 className="text-xl font-bold text-text mb-4">Your Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-text opacity-70 mb-1">Total Donations</p>
                <p className="text-2xl font-bold text-primary">{donor?.total_donations || 0}</p>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-text opacity-70 mb-1">Lives Saved</p>
                <p className="text-2xl font-bold text-green-600">{donor?.lives_saved || 0}</p>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-text opacity-70 mb-1">Points</p>
                <p className="text-2xl font-bold text-yellow-600">{donor?.points || 0}</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Profile

