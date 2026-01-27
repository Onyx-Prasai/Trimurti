import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaTag, FaCopy, FaCheck } from 'react-icons/fa'
import { redeemDiscountReward, markDiscountAsUsed } from '../utils/api'

const DiscountCard = ({ discount, donor, onRedeem }) => {
  const [redeeming, setRedeeming] = useState(false)
  const [copied, setCopied] = useState(false)
  const [message, setMessage] = useState(null)

  const handleRedeem = async () => {
    if (redeeming) return

    setRedeeming(true)
    setMessage(null)

    try {
      const response = await redeemDiscountReward({
        donor_id: donor.id,
        discount_reward_id: discount.id,
      })

      setMessage({
        type: 'success',
        text: `Successfully unlocked discount! Coupon: ${discount.coupon_code}`,
      })
      onRedeem()
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to redeem discount',
      })
    } finally {
      setRedeeming(false)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(discount.coupon_code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const getStatusColor = () => {
    if (discount.stock === 0) return 'bg-red-50'
    if (discount.days_remaining <= 7) return 'bg-yellow-50'
    return 'bg-white'
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ shadow: 'lg' }}
      className={`${getStatusColor()} rounded-2xl p-6 shadow-md hover:shadow-xl transition-all`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-800 mb-1">{discount.name}</h3>
          <p className="text-sm text-gray-600 flex items-center">
            <FaTag className="mr-2 text-yellow-500" />
            {discount.business_name}
          </p>
          <p className="text-xs text-gray-500 mt-1">{discount.business_type}</p>
        </div>
        <div className="text-right">
          <p className="text-3xl font-bold text-green-600">{discount.discount_percentage}%</p>
          <p className="text-xs text-gray-500">OFF</p>
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-700 mb-4">{discount.description}</p>

      {/* Coupon Code */}
      <div className="bg-gray-100 rounded-xl p-3 mb-4">
        <p className="text-xs text-gray-600 mb-1">Coupon Code</p>
        <div className="flex items-center justify-between">
          <code className="font-mono font-bold text-gray-800">{discount.coupon_code}</code>
          <button
            onClick={copyToClipboard}
            className="ml-2 p-2 hover:bg-gray-200 rounded transition-all"
            title="Copy coupon code"
          >
            {copied ? (
              <FaCheck className="text-green-600" />
            ) : (
              <FaCopy className="text-gray-600" />
            )}
          </button>
        </div>
      </div>

      {/* Points Cost and Validity */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-blue-50 rounded-lg p-3">
          <p className="text-xs text-gray-600 mb-1">Points Required</p>
          <p className="text-lg font-bold text-blue-600">{discount.points_cost} pts</p>
        </div>
        <div className={`rounded-lg p-3 ${
          discount.days_remaining <= 0 ? 'bg-red-50' : 'bg-green-50'
        }`}>
          <p className="text-xs text-gray-600 mb-1">Valid For</p>
          <p className={`text-lg font-bold ${
            discount.days_remaining <= 0 ? 'text-red-600' : 'text-green-600'
          }`}>
            {discount.days_remaining} days
          </p>
        </div>
      </div>

      {/* Stock Status */}
      {discount.stock !== -1 && (
        <div className="mb-4 p-2 bg-gray-100 rounded-lg text-center">
          <p className={`text-sm font-semibold ${
            discount.stock > 5 ? 'text-green-600' : 'text-orange-600'
          }`}>
            {discount.stock > 0 ? `${discount.stock} available` : 'Out of stock'}
          </p>
        </div>
      )}

      {/* Redeem Button */}
      <button
        onClick={handleRedeem}
        disabled={
          redeeming ||
          donor?.points < discount.points_cost ||
          discount.days_remaining <= 0 ||
          discount.stock === 0
        }
        className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-bold py-3 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-3"
      >
        {redeeming ? 'Unlocking...' : 'Unlock Discount'}
      </button>

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

      {/* Status Tags */}
      <div className="flex gap-2 mt-3">
        {discount.days_remaining <= 7 && discount.days_remaining > 0 && (
          <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
            Ending Soon
          </span>
        )}
        {discount.days_remaining <= 0 && (
          <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
            Expired
          </span>
        )}
        {discount.stock === 0 && (
          <span className="text-xs bg-gray-200 text-gray-800 px-2 py-1 rounded">
            Out of Stock
          </span>
        )}
      </div>
    </motion.div>
  )
}

export default DiscountCard
