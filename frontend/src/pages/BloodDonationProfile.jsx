import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaTint, FaSave } from 'react-icons/fa'

const BloodDonationProfile = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    bloodType: 'O+',
    weight: '70',
    lastDonation: '2025-01-15',
    canDonate: true,
    medicalConditions: '',
    allergies: '',
    medications: '',
    preferredCenter: 'Central Blood Bank',
  })
  const [saved, setSaved] = useState(false)

  const handleChange = (e) => {
    const { name, value, checked, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSave = () => {
    localStorage.setItem('donationProfile', JSON.stringify(formData))
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
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

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Blood Donation Profile</h1>
        <p className="text-gray-600 mb-8">Manage your donation information</p>

        {/* Success Message */}
        {saved && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6">
            ✓ Profile updated successfully!
          </div>
        )}

        {/* Form */}
        <div className="bg-white rounded-lg shadow-md p-8 space-y-6">
          {/* Blood Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Blood Type</label>
            <select
              name="bloodType"
              value={formData.bloodType}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="O+">O+</option>
              <option value="O-">O-</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
            </select>
          </div>

          {/* Weight */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Weight (kg)</label>
            <input
              type="number"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
              min="45"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <p className="text-xs text-gray-600 mt-1">Minimum weight for donation: 45 kg</p>
          </div>

          {/* Last Donation */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Last Donation Date</label>
            <input
              type="date"
              name="lastDonation"
              value={formData.lastDonation}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Can Donate */}
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="canDonate"
              name="canDonate"
              checked={formData.canDonate}
              onChange={handleChange}
              className="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary"
            />
            <label htmlFor="canDonate" className="text-sm font-medium text-gray-700">
              I am eligible to donate
            </label>
          </div>

          {/* Medical Conditions */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Medical Conditions</label>
            <textarea
              name="medicalConditions"
              value={formData.medicalConditions}
              onChange={handleChange}
              placeholder="List any medical conditions..."
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Allergies */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Allergies</label>
            <textarea
              name="allergies"
              value={formData.allergies}
              onChange={handleChange}
              placeholder="List any allergies..."
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Medications */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Current Medications</label>
            <textarea
              name="medications"
              value={formData.medications}
              onChange={handleChange}
              placeholder="List any medications..."
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Preferred Center */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Blood Bank</label>
            <input
              type="text"
              name="preferredCenter"
              value={formData.preferredCenter}
              onChange={handleChange}
              placeholder="Your preferred donation center"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            className="flex items-center justify-center space-x-2 w-full bg-primary text-white py-3 px-4 rounded-lg font-semibold hover:bg-primary-dark transition-all"
          >
            <FaSave />
            <span>Save Profile</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default BloodDonationProfile
