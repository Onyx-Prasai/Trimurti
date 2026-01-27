import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaBell, FaExclamationCircle, FaInfoCircle, FaCheckCircle } from 'react-icons/fa'
import { getHospitals } from '../utils/api'

const Notification = () => {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCriticalRequests()
  }, [])

  const fetchCriticalRequests = async () => {
    try {
      const response = await getHospitals({})
      // Filter critical hospitals from response
      const allHospitals = response.data.results || (Array.isArray(response.data) ? response.data : [])
      const criticalHospitals = allHospitals.filter(h => h.is_critical)
      
      const notifs = criticalHospitals.map((hospital) => ({
        id: hospital.id,
        type: 'critical',
        title: `Critical Blood Need: ${hospital.blood_type_needed}`,
        message: `${hospital.hospital_name} in ${hospital.city} urgently needs ${hospital.blood_type_needed} blood.`,
        hospital: hospital,
        timestamp: new Date(hospital.created_at),
        read: false,
      }))
      
      setNotifications(notifs)
    } catch (error) {
      console.error('Error fetching notifications:', error)
      // Mock data for demo
      setNotifications([
        {
          id: 1,
          type: 'critical',
          title: 'Critical Blood Need: O+',
          message: 'Kathmandu Hospital urgently needs O+ blood.',
          timestamp: new Date(),
          read: false,
        },
        {
          id: 2,
          type: 'info',
          title: 'Donation Reminder',
          message: 'You can donate again in 5 days!',
          timestamp: new Date(Date.now() - 86400000),
          read: false,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = (id) => {
    setNotifications(
      notifications.map((notif) =>
        notif.id === id ? { ...notif, read: true } : notif
      )
    )
  }

  const getIcon = (type) => {
    switch (type) {
      case 'critical':
        return <FaExclamationCircle className="text-red-500" />
      case 'info':
        return <FaInfoCircle className="text-blue-500" />
      case 'success':
        return <FaCheckCircle className="text-green-500" />
      default:
        return <FaBell className="text-gray-500" />
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-text mb-8 text-center flex items-center justify-center"
        >
          <FaBell className="mr-3 text-primary" />
          Notifications
        </motion.h1>

        {notifications.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-12 text-center shadow-lg"
          >
            <FaBell className="text-6xl text-gray-300 mx-auto mb-4" />
            <p className="text-text text-xl">No notifications yet</p>
          </motion.div>
        ) : (
          <div className="space-y-4">
            {notifications.map((notif) => (
              <motion.div
                key={notif.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className={`bg-white rounded-2xl p-6 shadow-lg cursor-pointer transition-all ${
                  notif.read ? 'opacity-60' : 'border-l-4 border-primary'
                }`}
                onClick={() => markAsRead(notif.id)}
              >
                <div className="flex items-start space-x-4">
                  <div className="text-2xl mt-1">{getIcon(notif.type)}</div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-text mb-1">
                      {notif.title}
                    </h3>
                    <p className="text-text opacity-70 mb-2">{notif.message}</p>
                    <p className="text-sm text-text opacity-50">
                      {notif.timestamp.toLocaleString()}
                    </p>
                  </div>
                  {!notif.read && (
                    <div className="w-3 h-3 bg-primary rounded-full"></div>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Notification

