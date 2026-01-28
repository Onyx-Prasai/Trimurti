import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaUser, FaEdit, FaSave, FaSignOutAlt } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'
import { getDonorProfile } from '../utils/api'

const Profile = ({ setIsAuthenticated }) => {
  const [loading, setLoading] = useState(false)
  const [editing, setEditing] = useState(false)
  const [donor, setDonor] = useState(null)
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

  // Get user data from localStorage (set during login/registration)
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    // Initialize form data with user data from localStorage
    if (user?.id) {
      setFormData(prev => ({
        ...prev,
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone: user.phone_number || user.phone || '',
        address: user.address || '',
        city: user.city || 'Kathmandu',
        blood_group: user.blood_group || 'O+',
      }))
      // Fetch donor profile data including points and stats
      fetchDonorData()
    } else {
      navigate('/login')
    }
  }, [])

  const fetchDonorData = async () => {
    try {
      const response = await getDonorProfile(user.id)
      setDonor(response.data)

      // Prefer server truth for blood group (keeps Profile in sync with login modal selection)
      const serverBloodGroup = response?.data?.blood_group
      if (serverBloodGroup) {
        setFormData((prev) => ({ ...prev, blood_group: serverBloodGroup }))
        const existingUser = JSON.parse(localStorage.getItem('user') || '{}')
        localStorage.setItem(
          'user',
          JSON.stringify({ ...existingUser, blood_group: serverBloodGroup })
        )
      }
    } catch (error) {
      console.error('Error fetching donor data:', error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      // Update user in localStorage
      const updatedUser = {
        ...user,
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        phone_number: formData.phone,
        phone: formData.phone,
        address: formData.address,
        city: formData.city,
        blood_group: formData.blood_group,
      }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      // In real app, make API call to update profile
      // const response = await updateProfile(formData)
      // if (response.ok) { ... }
      
      setEditing(false)
      alert('Profile updated successfully!')
    } catch (error) {
      console.error('Error saving profile:', error)
      alert('Error updating profile. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/')
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading profile...</div>
  }

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
  // Keep this aligned with backend `DonorProfile.DISTRICTS`
  const cities = [
    // Bagmati Province
    'Kathmandu',
    'Bhaktapur',
    'Lalitpur',
    'Kavre',
    'Nuwakot',
    'Rasuwa',
    'Sindhuli',
    'Ramechhap',
    'Dolakha',
    'Makwanpur',
    // Eastern Region
    'Ilam',
    'Jhapa',
    'Morang',
    'Sunsari',
    'Dhankuta',
    'Terhathum',
    'Panchthar',
    'Udayapur',
    'Sankhuwasabha',
    'Sindhupalchok',
    // Central Region
    'Gorkha',
    'Lamjung',
    'Tanahu',
    'Chitwan',
    'Nawalpur',
    'Parsa',
    'Bara',
    'Rautahat',
    'Gulmi',
    'Arghakhanchi',
    // Western Region
    'Palpa',
    'Dang',
    'Banke',
    'Bardiya',
    'Surkhet',
    // Mid-Western Region
    'Salyan',
    'Pyuthan',
    'Rolpa',
    'Rukum',
    'Dailekh',
    'Jumla',
    'Kalikot',
    'Dolpa',
    // Far-Western Region
    'Jajarkot',
    'Achham',
    'Bajura',
    'Bajhang',
    'Doti',
    'Kailali',
    'Kanchanpur',
  ]

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
                District
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

