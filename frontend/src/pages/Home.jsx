import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { FaTint, FaGift, FaChartLine, FaRobot, FaHeart } from 'react-icons/fa'
import { getDonorStats } from '../utils/api'

const Home = () => {
  const [stats, setStats] = useState({
    lives_saved: 0,
    active_donors: 0,
    blood_banks: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await getDonorStats()
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const Counter = ({ value, label, delay = 0 }) => {
    const [count, setCount] = useState(0)

    useEffect(() => {
      const duration = 2000
      const steps = 60
      const increment = value / steps
      let current = 0

      const timer = setTimeout(() => {
        const interval = setInterval(() => {
          current += increment
          if (current >= value) {
            setCount(value)
            clearInterval(interval)
          } else {
            setCount(Math.floor(current))
          }
        }, duration / steps)

        return () => clearInterval(interval)
      }, delay)

      return () => clearTimeout(timer)
    }, [value, delay])

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: delay / 1000 }}
        className="text-center"
      >
        <div className="text-4xl font-bold text-primary mb-2">{count.toLocaleString()}+</div>
        <div className="text-text">{label}</div>
      </motion.div>
    )
  }

  const features = [
    {
      icon: FaTint,
      title: 'Find Blood',
      description: 'Search for blood banks and hospitals in need',
      link: '/find-blood',
      color: 'bg-red-100 text-primary',
    },
    {
      icon: FaGift,
      title: 'Earn Points',
      description: 'Get rewarded for every donation you make',
      link: '/points',
      color: 'bg-yellow-100 text-yellow-600',
    },
    {
      icon: FaChartLine,
      title: 'Track Impact',
      description: 'See how many lives you\'ve saved',
      link: '/dashboard',
      color: 'bg-green-100 text-green-600',
    },
    {
      icon: FaRobot,
      title: 'AI Insights',
      description: 'Get personalized health recommendations',
      link: '/ai-health',
      color: 'bg-blue-100 text-blue-600',
    },
    
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary to-red-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-6xl font-bold mb-6"
          >
            Save Lives, One Drop of Blood at a Time
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl md:text-2xl mb-8 opacity-90"
          >
            Join thousands of heroes making a difference in Nepal
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Link
              to="/profile"
              className="inline-block bg-white text-primary px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-100 transition-all shadow-lg"
            >
              Join the Movement
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Counter value={stats.lives_saved || 1250} label="Lives Saved" delay={0} />
            <Counter value={stats.active_donors || 450} label="Active Donors" delay={200} />
            <Counter value={stats.blood_banks || 25} label="Blood Banks" delay={400} />
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-text mb-12">
            How You Can Help
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all"
                >
                  <Link to={feature.link}>
                    <div className={`${feature.color} w-16 h-16 rounded-2xl flex items-center justify-center mb-4`}>
                      <Icon className="text-2xl" />
                    </div>
                    <h3 className="text-xl font-semibold text-text mb-2">{feature.title}</h3>
                    <p className="text-text opacity-70">{feature.description}</p>
                  </Link>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            <FaHeart className="text-6xl mx-auto mb-6 pulse-heartbeat" />
            <h2 className="text-4xl font-bold mb-4">Ready to Make a Difference?</h2>
            <p className="text-xl mb-8 opacity-90">
              Every donation counts. Start your journey today.
            </p>
            <Link
              to="/find-blood"
              className="inline-block bg-white text-primary px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-100 transition-all shadow-lg"
            >
              Find Blood Banks Near You
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home

