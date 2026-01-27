import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaGift, FaCoins, FaShareAlt, FaCopy } from 'react-icons/fa'
import { getStoreItems, redeemItem, getDonorProfile } from '../utils/api'

const Points = () => {
  const [donor, setDonor] = useState(null)
  const [storeItems, setStoreItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [redeeming, setRedeeming] = useState(null)
  const donorId = 1 // In real app, get from auth context

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [donorRes, storeRes] = await Promise.all([
        getDonorProfile(donorId).catch(() => null),
        getStoreItems(),
      ])
      
      if (donorRes) {
        setDonor(donorRes.data)
      } else {
        // Mock data
        setDonor({ id: 1, points: 320, referral_code: 'REF123456' })
      }
      
      const storeData = storeRes.data.results || (Array.isArray(storeRes.data) ? storeRes.data : [])
      setStoreItems(storeData)
    } catch (error) {
      console.error('Error fetching data:', error)
      // Mock data
      setDonor({ id: 1, points: 320, referral_code: 'REF123456' })
      setStoreItems([
        { id: 1, name: 'Paracetamol', description: 'Pain relief medicine', points_cost: 50, stock: 10 },
        { id: 2, name: 'First Aid Kit', description: 'Complete first aid kit', points_cost: 200, stock: 5 },
        { id: 3, name: 'Health Checkup Voucher', description: 'Free health checkup', points_cost: 300, stock: 3 },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleRedeem = async (itemId) => {
    if (redeeming) return
    
    setRedeeming(itemId)
    try {
      await redeemItem({
        donor_id: donorId,
        item_id: itemId,
      })
      // Refresh data
      await fetchData()
      alert('Item redeemed successfully!')
    } catch (error) {
      console.error('Error redeeming item:', error)
      alert(error.response?.data?.error || 'Failed to redeem item')
    } finally {
      setRedeeming(null)
    }
  }

  const copyReferralLink = () => {
    const link = `${window.location.origin}/register?ref=${donor?.referral_code}`
    navigator.clipboard.writeText(link)
    alert('Referral link copied!')
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  const points = donor?.points ?? 0
  const referralCode = donor?.referral_code ?? 'N/A'

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-text mb-8 text-center flex items-center justify-center"
        >
          <FaGift className="mr-3 text-primary" />
          Points & Rewards
        </motion.h1>

        {/* Points Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-yellow-400 to-yellow-600 text-white rounded-2xl p-8 mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xl opacity-90 mb-2">Your Points</p>
              <p className="text-5xl font-bold">{points}</p>
              <p className="text-sm opacity-80 mt-2">
                Earn 100 points per donation • 20 bonus points per referral
              </p>
            </div>
            <FaCoins className="text-8xl opacity-20" />
          </div>
        </motion.div>

        {/* Referral Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 shadow-lg mb-8"
        >
          <h2 className="text-2xl font-bold text-text mb-4 flex items-center">
            <FaShareAlt className="mr-3 text-primary" />
            Referral Program
          </h2>
          <div className="bg-gray-50 rounded-xl p-4 mb-4">
            <p className="text-sm text-text opacity-70 mb-2">Your Referral Code</p>
            <div className="flex items-center space-x-3">
              <code className="flex-1 bg-white px-4 py-2 rounded-lg font-mono text-lg font-bold text-primary">
                {referralCode}
              </code>
              <button
                onClick={copyReferralLink}
                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-all flex items-center space-x-2"
              >
                <FaCopy />
                <span>Copy Link</span>
              </button>
            </div>
          </div>
          <p className="text-text opacity-70">
            Share your referral link with friends. When they register and make their first donation, you'll both earn 20 bonus points!
          </p>
        </motion.div>

        {/* Store */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold text-text mb-6">Redeem Points</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {storeItems.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all"
              >
                <div className="text-center mb-4">
                  <FaGift className="text-5xl text-primary mx-auto mb-3" />
                  <h3 className="text-xl font-semibold text-text mb-2">{item.name}</h3>
                  <p className="text-text opacity-70 text-sm mb-4">{item.description}</p>
                </div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-2xl font-bold text-yellow-600">
                    {item.points_cost} pts
                  </span>
                  <span className={`text-sm ${
                    item.stock > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {item.stock > 0 ? `Stock: ${item.stock}` : 'Out of Stock'}
                  </span>
                </div>
                <button
                  onClick={() => handleRedeem(item.id)}
                  disabled={points < item.points_cost || item.stock <= 0 || redeeming === item.id}
                  className="w-full bg-primary text-white px-4 py-2 rounded-xl hover:bg-red-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {redeeming === item.id ? 'Redeeming...' : 'Redeem Now'}
                </button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Points

