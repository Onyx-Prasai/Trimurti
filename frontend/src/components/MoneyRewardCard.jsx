import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaCoins, FaWallet } from 'react-icons/fa'
import { redeemMoneyReward } from '../utils/api'

const MoneyRewardCard = ({ donor, onRedeem }) => {
  const [selectedAmount, setSelectedAmount] = useState(100)
  const [redeeming, setRedeeming] = useState(false)
  const [message, setMessage] = useState(null)

  const handleRedeem = async () => {
    if (redeeming) return

    setRedeeming(true)
    setMessage(null)

    try {
      const response = await redeemMoneyReward({
        donor_id: donor.id,
        points: selectedAmount,
      })

      setMessage({
        type: 'success',
        text: `Successfully redeemed ${selectedAmount} points for ${response.data.esewa_amount} RS Esewa!`,
      })
      onRedeem()
      setTimeout(() => setSelectedAmount(100), 2000)
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to redeem reward',
      })
    } finally {
      setRedeeming(false)
    }
  }

  const esewaBenefits = [
    'Fast and secure payment gateway',
    'Instantly redeemable',
    'No processing fees',
    'Available on mobile and web',
  ]

  const pointsAmounts = [100, 200, 500, 1000]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-8 shadow-lg"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold mb-2 flex items-center text-gray-800">
            <FaWallet className="mr-3 text-green-600" />
            Points to Money
          </h3>
          <p className="text-sm text-gray-600">Convert your points to Esewa credit</p>
        </div>
        <FaCoins className="text-6xl text-gray-200" />
      </div>

      {/* Conversion Rate */}
      <div className="bg-green-50 rounded-xl p-4 mb-6 border border-green-200">
        <p className="text-sm text-gray-700 mb-1">Conversion Rate</p>
        <p className="text-3xl font-bold text-green-600">100 Points = 1 RS</p>
      </div>

      {/* Amount Selection */}
      <div className="mb-6">
        <p className="text-sm text-gray-700 mb-3 font-semibold">Select Points Amount</p>
        <div className="grid grid-cols-2 gap-3">
          {pointsAmounts.map((amount) => (
            <button
              key={amount}
              onClick={() => setSelectedAmount(amount)}
              disabled={donor?.points < amount}
              className={`p-3 rounded-lg font-semibold transition-all ${
                selectedAmount === amount
                  ? 'bg-green-600 text-white shadow-lg scale-105'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {amount} pts
              <br />
              <span className="text-sm">{(amount / 100).toFixed(2)} RS</span>
            </button>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="bg-gray-50 rounded-xl p-4 mb-6 border border-gray-200">
        <div className="flex justify-between items-center mb-3">
          <span className="text-gray-700">Points to Redeem:</span>
          <span className="font-bold text-lg text-gray-800">{selectedAmount}</span>
        </div>
        <div className="flex justify-between items-center border-t border-gray-300 pt-3">
          <span className="text-gray-700">Esewa Amount:</span>
          <span className="font-bold text-2xl text-green-600">{(selectedAmount / 100).toFixed(2)} RS</span>
        </div>
      </div>

      {/* Redeem Button */}
      <button
        onClick={handleRedeem}
        disabled={redeeming || donor?.points < selectedAmount}
        className="w-full bg-green-600 text-white font-bold py-3 rounded-xl hover:bg-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-4"
      >
        {redeeming ? 'Processing...' : 'Redeem to Esewa'}
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

      {/* Benefits */}
      <div className="mt-6 border-t border-gray-200 pt-6">
        <p className="text-sm font-semibold mb-3 text-gray-700">Why Esewa?</p>
        <ul className="space-y-2 text-sm text-gray-700">
          {esewaBenefits.map((benefit, idx) => (
            <li key={idx} className="flex items-center">
              <span className="w-2 h-2 bg-green-600 rounded-full mr-2"></span>
              {benefit}
            </li>
          ))}
        </ul>
      </div>
    </motion.div>
  )
}

export default MoneyRewardCard
