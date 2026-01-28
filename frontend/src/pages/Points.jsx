import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaGift, FaCoins, FaShareAlt, FaCopy, FaWallet, FaTag, FaPills } from 'react-icons/fa'
import {
  getDonorProfile,
  getAvailableDiscounts,
  getAvailableMedicines,
  getMoneyRewards,
} from '../utils/api'
import MoneyRewardCard from '../components/MoneyRewardCard'
import DiscountCard from '../components/DiscountCard'
import MedicineRewardCard from '../components/MedicineRewardCard'

const Points = () => {
  const [donor, setDonor] = useState(null)
  const [discountRewards, setDiscountRewards] = useState([])
  const [medicineRewards, setMedicineRewards] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('money') // money, discounts, medicine
  const donorId = 1 // In real app, get from auth context

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [donorRes, discountRes, medicineRes] = await Promise.all([
        getDonorProfile(donorId).catch(() => null),
        getAvailableDiscounts().catch(() => null),
        getAvailableMedicines().catch(() => null),
      ])

      if (donorRes) {
        setDonor(donorRes.data)
      } else {
        // Mock data
        setDonor({
          id: 1,
          points: 850,
          referral_code: 'REF123456',
          address: '123 Main Street, Kathmandu',
          phone: '9841234567',
        })
      }

      if (discountRes) {
        setDiscountRewards(
          Array.isArray(discountRes.data)
            ? discountRes.data
            : discountRes.data.results || []
        )
      } else {
        // Mock data
        setDiscountRewards([
          {
            id: 1,
            name: 'Premium Coffee',
            business_name: 'Himalayan Java',
            business_type: 'Coffee Shop',
            description: '25% off on all beverages and pastries',
            discount_percentage: 25,
            points_cost: 150,
            coupon_code: 'HJAVA25',
            valid_until: '2026-03-31',
            stock: 15,
            days_remaining: 63,
          },
          {
            id: 2,
            name: 'Fresh Baked Goods',
            business_name: 'Brobakery',
            business_type: 'Bakery',
            description: '30% off on all cakes, breads and pastries',
            discount_percentage: 30,
            points_cost: 180,
            coupon_code: 'BROBAKE30',
            valid_until: '2026-03-15',
            stock: 12,
            days_remaining: 47,
          },
          {
            id: 3,
            name: 'Food Discount',
            business_name: 'Pizza Hut Nepal',
            business_type: 'Restaurant',
            description: '30% off on all pizzas and sides',
            discount_percentage: 30,
            points_cost: 200,
            coupon_code: 'BLOOD30',
            valid_until: '2026-02-28',
            stock: 10,
            days_remaining: 32,
          },
          {
            id: 5,
            name: 'FastFood Deal',
            business_name: 'Burger King Nepal',
            business_type: 'Fast Food',
            description: 'Buy 1 Get 1 Free on selected burgers',
            discount_percentage: 50,
            points_cost: 250,
            coupon_code: 'BKG50',
            valid_until: '2026-03-10',
            stock: 8,
            days_remaining: 42,
          },
          {
            id: 6,
            name: 'Tea & Snacks',
            business_name: 'Potters Coffee House',
            business_type: 'Café',
            description: '20% off on all items including tea and snacks',
            discount_percentage: 20,
            points_cost: 120,
            coupon_code: 'POTTERS20',
            valid_until: '2026-03-25',
            stock: 20,
            days_remaining: 57,
          },
          {
            id: 7,
            name: 'Restaurant Special',
            business_name: 'Nepali Chulo',
            business_type: 'Nepali Restaurant',
            description: '35% off on traditional Nepali meals',
            discount_percentage: 35,
            points_cost: 220,
            coupon_code: 'CHULO35',
            valid_until: '2026-03-20',
            stock: 7,
            days_remaining: 52,
          },
          {
            id: 8,
            name: 'Health & Wellness',
            business_name: 'Wellness Store Nepal',
            business_type: 'Health Shop',
            description: '40% off on organic products and supplements',
            discount_percentage: 40,
            points_cost: 200,
            coupon_code: 'WELLNESS40',
            valid_until: '2026-04-05',
            stock: 10,
            days_remaining: 69,
          },
        ])
      }

      if (medicineRes) {
        setMedicineRewards(
          Array.isArray(medicineRes.data)
            ? medicineRes.data
            : medicineRes.data.results || []
        )
      } else {
        // Mock data
        setMedicineRewards([
          {
            id: 1,
            name: 'Paracetamol 500mg',
            description: 'Effective pain relief and fever reducer',
            category: 'Pain Relief',
            points_cost: 50,
            provider: 'Zandu Pharma',
            stock: 15,
          },
          {
            id: 2,
            name: 'Multi-Vitamin Tablets',
            description: 'Complete daily nutrition',
            category: 'Supplement',
            points_cost: 100,
            provider: 'Himalaya Wellness',
            stock: 8,
          },
          {
            id: 3,
            name: 'First Aid Kit',
            description: 'Complete first aid kit with bandages and antiseptic',
            category: 'Medical Kit',
            points_cost: 250,
            provider: 'HealthCare Plus',
            stock: 3,
          },
        ])
      }
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRedeemSuccess = () => {
    fetchData()
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

  const tabConfig = [
    {
      id: 'money',
      label: 'Money',
      icon: FaWallet,
      color: 'from-green-400 to-emerald-600',
    },
    {
      id: 'discounts',
      label: 'Discounts',
      icon: FaTag,
      color: 'from-yellow-400 to-orange-500',
    },
    {
      id: 'medicine',
      label: 'Medicine',
      icon: FaPills,
      color: 'from-blue-400 to-blue-600',
    },
  ]

  return (
    <div className="min-h-screen py-8 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-gray-800 mb-8 text-center flex items-center justify-center"
        >
          <FaGift className="mr-3 text-red-500" />
          Points & Rewards
        </motion.h1>

        {/* Points Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-yellow-400 to-yellow-600 text-white rounded-2xl p-8 mb-8 shadow-lg"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xl opacity-90 mb-2">Your Points Balance</p>
              <p className="text-5xl font-bold">{points}</p>
              <p className="text-sm opacity-80 mt-2">
                Earn 500 points per donation • 100 bonus points per referral
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
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <FaShareAlt className="mr-3 text-red-500" />
            Referral Program
          </h2>
          <div className="bg-gray-50 rounded-xl p-4 mb-4">
            <p className="text-sm text-gray-700 opacity-70 mb-2">Your Referral Code</p>
            <div className="flex items-center space-x-3">
              <code className="flex-1 bg-white px-4 py-2 rounded-lg font-mono text-lg font-bold text-red-500">
                {referralCode}
              </code>
              <button
                onClick={copyReferralLink}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-all flex items-center space-x-2"
              >
                <FaCopy />
                <span>Copy Link</span>
              </button>
            </div>
          </div>
          <p className="text-gray-700 opacity-70">
            Share your referral link with friends. When they register and make their first
            donation, you'll earn 100 bonus points!
          </p>
        </motion.div>

        {/* Reward Categories */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          {/* Tab Navigation */}
          <div className="flex gap-3 mb-8 overflow-x-auto pb-2">
            {tabConfig.map((tab) => {
              const IconComponent = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold whitespace-nowrap transition-all ${
                    activeTab === tab.id
                      ? `bg-gradient-to-r ${tab.color} text-white shadow-lg`
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <IconComponent />
                  {tab.label}
                </button>
              )
            })}
          </div>

          {/* Money Rewards Tab */}
          {activeTab === 'money' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <MoneyRewardCard donor={donor} onRedeem={handleRedeemSuccess} />
            </motion.div>
          )}

          {/* Discount Rewards Tab */}
          {activeTab === 'discounts' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Exclusive Discounts</h2>
              {discountRewards.length === 0 ? (
                <div className="bg-white rounded-2xl p-8 text-center">
                  <FaTag className="text-6xl text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-600">No discounts available yet</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {discountRewards.map((discount) => (
                    <DiscountCard
                      key={discount.id}
                      discount={discount}
                      donor={donor}
                      onRedeem={handleRedeemSuccess}
                    />
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {/* Medicine Rewards Tab */}
          {activeTab === 'medicine' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Medicine & Healthcare</h2>
              {medicineRewards.length === 0 ? (
                <div className="bg-white rounded-2xl p-8 text-center">
                  <FaPills className="text-6xl text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-600">No medicine rewards available yet</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {medicineRewards.map((medicine) => (
                    <MedicineRewardCard
                      key={medicine.id}
                      medicine={medicine}
                      donor={donor}
                      onRedeem={handleRedeemSuccess}
                    />
                  ))}
                </div>
              )}
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default Points

