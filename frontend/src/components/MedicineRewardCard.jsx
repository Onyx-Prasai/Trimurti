import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaPills, FaBox, FaTruck } from 'react-icons/fa'
import { redeemMedicineReward } from '../utils/api'

const MedicineRewardCard = ({ medicine, donor, onRedeem }) => {
  const [redeeming, setRedeeming] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [deliveryInfo, setDeliveryInfo] = useState({
    address: donor?.address || '',
    phone: donor?.phone || '',
  })
  const [message, setMessage] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setDeliveryInfo(prev => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleRedeem = async () => {
    if (redeeming || !deliveryInfo.address || !deliveryInfo.phone) {
      setMessage({
        type: 'error',
        text: 'Please fill in delivery address and phone number',
      })
      return
    }

    setRedeeming(true)
    setMessage(null)

    try {
      await redeemMedicineReward({
        donor_id: donor.id,
        medicine_reward_id: medicine.id,
        delivery_address: deliveryInfo.address,
        delivery_phone: deliveryInfo.phone,
      })

      setMessage({
        type: 'success',
        text: `Successfully redeemed! ${medicine.name} will be delivered to your address.`,
      })
      onRedeem()
      setTimeout(() => setShowForm(false), 2000)
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to redeem medicine',
      })
    } finally {
      setRedeeming(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ shadow: 'lg' }}
      className="bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <FaPills className="text-blue-600 mr-2 text-2xl" />
            <h3 className="text-xl font-bold text-gray-800">{medicine.name}</h3>
          </div>
          <p className="text-sm text-gray-600 ml-8">{medicine.category}</p>
          <p className="text-xs text-gray-500 ml-8">By {medicine.provider}</p>
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-700 mb-4 px-2">{medicine.description}</p>

      {/* Points and Stock */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-blue-50 rounded-lg p-3 text-center">
          <p className="text-xs text-gray-600 mb-1">Points Required</p>
          <p className="text-2xl font-bold text-blue-600">{medicine.points_cost}</p>
        </div>
        <div className={`rounded-lg p-3 text-center ${
          medicine.stock > 0 ? 'bg-green-50' : 'bg-red-50'
        }`}>
          <p className="text-xs text-gray-600 mb-1">Availability</p>
          <p className={`text-2xl font-bold ${
            medicine.stock > 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {medicine.stock > 0 ? medicine.stock : '0'}
          </p>
        </div>
      </div>

      {/* Redeem Button */}
      {!showForm ? (
        <button
          onClick={() => setShowForm(true)}
          disabled={
            redeeming ||
            donor?.points < medicine.points_cost ||
            medicine.stock <= 0
          }
          className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold py-3 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-3"
        >
          {redeeming ? 'Processing...' : 'Redeem Medicine'}
        </button>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-3 mb-3"
        >
          <div>
            <label className="text-sm font-semibold text-gray-700 block mb-1">
              Delivery Address
            </label>
            <textarea
              name="address"
              value={deliveryInfo.address}
              onChange={handleInputChange}
              placeholder="Enter your full delivery address"
              className="w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500"
              rows={3}
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-gray-700 block mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              name="phone"
              value={deliveryInfo.phone}
              onChange={handleInputChange}
              placeholder="10-digit phone number"
              className="w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleRedeem}
              disabled={redeeming || !deliveryInfo.address || !deliveryInfo.phone}
              className="flex-1 bg-green-500 text-white font-semibold py-2 rounded-lg hover:bg-green-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {redeeming ? 'Confirming...' : 'Confirm'}
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="flex-1 bg-gray-300 text-gray-800 font-semibold py-2 rounded-lg hover:bg-gray-400 transition-all"
            >
              Cancel
            </button>
          </div>
        </motion.div>
      )}

      {/* Message */}
      {message && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`p-3 rounded-lg text-sm ${
            message.type === 'success'
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          {message.text}
        </motion.div>
      )}

      {/* Delivery Info */}
      {!showForm && (
        <div className="bg-blue-50 rounded-lg p-3">
          <p className="text-xs text-gray-600 mb-2 flex items-center">
            <FaTruck className="mr-2 text-blue-600" />
            Delivery Information
          </p>
          <ul className="text-xs text-gray-700 space-y-1 ml-5">
            <li>• Fast delivery to your address</li>
            <li>• Trackable shipment</li>
            <li>• Authentic medicines from verified providers</li>
          </ul>
        </div>
      )}
    </motion.div>
  )
}

export default MedicineRewardCard
