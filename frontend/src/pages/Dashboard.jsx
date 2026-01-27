import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaHeart, FaTrophy, FaCalendarAlt, FaCheckCircle } from 'react-icons/fa'
import { getDonorProfile } from '../utils/api'

const Dashboard = () => {
  const [donor, setDonor] = useState(null)
  const [loading, setLoading] = useState(true)
  const donorId = 1 // In real app, get from auth context

  useEffect(() => {
    fetchDonorData()
  }, [])

  const fetchDonorData = async () => {
    try {
      const response = await getDonorProfile(donorId)
      setDonor(response.data)
    } catch (error) {
      console.error('Error fetching donor data:', error)
      // Mock data for demo
      setDonor({
        id: 1,
        total_donations: 3,
        lives_saved: 9,
        points: 320,
        can_donate: true,
        days_until_next: 0,
        last_donation_date: null,
        badges: ['First Drop'],
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  const canDonate = donor?.can_donate ?? true
  const daysUntilNext = donor?.days_until_next ?? 0
  const livesSaved = donor?.lives_saved ?? 0
  const totalDonations = donor?.total_donations ?? 0
  const points = donor?.points ?? 0
  const badges = donor?.badges ?? []

  // Calculate calendar days
  const calendarDays = []
  const today = new Date()
  for (let i = 0; i < 56; i++) {
    const date = new Date(today)
    date.setDate(today.getDate() + i)
    calendarDays.push(date)
  }

  const getDayStatus = (date) => {
    if (donor?.last_donation_date) {
      const lastDonation = new Date(donor.last_donation_date)
      const daysSince = Math.floor((date - lastDonation) / (1000 * 60 * 60 * 24))
      if (daysSince < 0) return 'past'
      if (daysSince < 56) return 'locked'
      return 'available'
    }
    return 'available'
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-primary to-red-600 text-white rounded-2xl p-8 mb-8"
        >
          <h1 className="text-3xl font-bold mb-2">Welcome Back!</h1>
          <p className="text-xl opacity-90">
            You have saved <span className="font-bold text-2xl">{livesSaved}</span> lives
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-text opacity-70 mb-1">Total Donations</p>
                <p className="text-3xl font-bold text-primary">{totalDonations}</p>
              </div>
              <FaHeart className="text-4xl text-primary opacity-20" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl p-6 shadow-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-text opacity-70 mb-1">Points Earned</p>
                <p className="text-3xl font-bold text-yellow-600">{points}</p>
              </div>
              <FaTrophy className="text-4xl text-yellow-600 opacity-20" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className={`rounded-2xl p-6 shadow-lg ${
              canDonate ? 'bg-green-100' : 'bg-yellow-100'
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-text opacity-70 mb-1">Donation Status</p>
                <p className={`text-2xl font-bold ${canDonate ? 'text-green-600' : 'text-yellow-600'}`}>
                  {canDonate ? 'Active' : 'Passive'}
                </p>
                {!canDonate && (
                  <p className="text-sm text-text opacity-70 mt-1">
                    {daysUntilNext} days remaining
                  </p>
                )}
              </div>
              <FaCalendarAlt className={`text-4xl opacity-20 ${canDonate ? 'text-green-600' : 'text-yellow-600'}`} />
            </div>
          </motion.div>
        </div>

        {/* Donation Calendar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-2xl p-6 shadow-lg mb-8"
        >
          <h2 className="text-2xl font-bold text-text mb-4 flex items-center">
            <FaCalendarAlt className="mr-3 text-primary" />
            Donation Calendar (56-Day Lockout)
          </h2>
          <div className="grid grid-cols-7 gap-2">
            {calendarDays.map((date, index) => {
              const status = getDayStatus(date)
              const isToday = date.toDateString() === today.toDateString()
              
              return (
                <div
                  key={index}
                  className={`aspect-square rounded-xl flex items-center justify-center text-xs font-semibold ${
                    status === 'past'
                      ? 'bg-gray-200 text-gray-400'
                      : status === 'locked'
                      ? 'bg-yellow-100 text-yellow-600'
                      : 'bg-green-100 text-green-600'
                  } ${isToday ? 'ring-2 ring-primary' : ''}`}
                  title={`${date.toLocaleDateString()} - ${status}`}
                >
                  {date.getDate()}
                </div>
              )
            })}
          </div>
          <div className="flex items-center space-x-4 mt-4 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-100 rounded mr-2"></div>
              <span className="text-text">Available</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-yellow-100 rounded mr-2"></div>
              <span className="text-text">Locked (56-day wait)</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-gray-200 rounded mr-2"></div>
              <span className="text-text">Past</span>
            </div>
          </div>
        </motion.div>

        {/* Badges Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <h2 className="text-2xl font-bold text-text mb-4 flex items-center">
            <FaTrophy className="mr-3 text-yellow-600" />
            Your Badges
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {['First Drop', 'Life Saver'].map((badge) => {
              const earned = badges.includes(badge)
              return (
                <div
                  key={badge}
                  className={`p-4 rounded-xl border-2 ${
                    earned
                      ? 'border-yellow-400 bg-yellow-50'
                      : 'border-gray-200 bg-gray-50 opacity-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <FaTrophy
                      className={`text-3xl ${earned ? 'text-yellow-600' : 'text-gray-400'}`}
                    />
                    <div>
                      <h3 className="font-semibold text-text">{badge}</h3>
                      <p className="text-sm text-text opacity-70">
                        {badge === 'First Drop'
                          ? 'Complete your first donation'
                          : 'Complete 5 donations'}
                      </p>
                      {earned && (
                        <span className="text-xs text-green-600 font-semibold mt-1 flex items-center">
                          <FaCheckCircle className="mr-1" />
                          Earned
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard

