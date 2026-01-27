import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaTint, FaPhone, FaMapMarkerAlt, FaCheckCircle } from 'react-icons/fa'

const BloodRequest = () => {
  const [requests, setRequests] = useState([
    { id: 30, hospital_name: 'Arghakhanchi Emergency Request', city: 'Arghakhanchi', blood_type: 'B-', blood_product: 'Plasma', urgency: 'Critical', location: 'Arghakhanchi, Nepal (Request ID: 30)', contact_number: '+977-1-XXXXXX' },
    { id: 29, hospital_name: 'Gulmi Emergency Request', city: 'Gulmi', blood_type: 'B+', blood_product: 'Platelets', urgency: 'Critical', location: 'Gulmi, Nepal (Request ID: 29)', contact_number: '+977-1-XXXXXX' },
    { id: 27, hospital_name: 'Bara Emergency Request', city: 'Bara', blood_type: 'AB-', blood_product: 'Whole Blood', urgency: 'Critical', location: 'Bara, Nepal (Request ID: 27)', contact_number: '+977-1-XXXXXX' },
    { id: 24, hospital_name: 'Chitwan Emergency Request', city: 'Chitwan', blood_type: 'B-', blood_product: 'Platelets', urgency: 'Critical', location: 'Chitwan, Nepal (Request ID: 24)', contact_number: '+977-1-XXXXXX' },
    { id: 23, hospital_name: 'Tanahu Emergency Request', city: 'Tanahu', blood_type: 'O+', blood_product: 'Whole Blood', urgency: 'Critical', location: 'Tanahu, Nepal (Request ID: 23)', contact_number: '+977-1-XXXXXX' },
    { id: 21, hospital_name: 'Gorkha Emergency Request', city: 'Gorkha', blood_type: 'AB-', blood_product: 'Whole Blood', urgency: 'Critical', location: 'Gorkha, Nepal (Request ID: 21)', contact_number: '+977-1-XXXXXX' },
    { id: 20, hospital_name: 'Sindhupalchok Emergency Request', city: 'Sindhupalchok', blood_type: 'AB+', blood_product: 'Platelets', urgency: 'Critical', location: 'Sindhupalchok, Nepal (Request ID: 20)', contact_number: '+977-1-XXXXXX' },
    { id: 18, hospital_name: 'Udayapur Emergency Request', city: 'Udayapur', blood_type: 'O-', blood_product: 'Plasma', urgency: 'Critical', location: 'Udayapur, Nepal (Request ID: 18)', contact_number: '+977-1-XXXXXX' },
    { id: 16, hospital_name: 'Terhathum Emergency Request', city: 'Terhathum', blood_type: 'AB-', blood_product: 'Platelets', urgency: 'Critical', location: 'Terhathum, Nepal (Request ID: 16)', contact_number: '+977-1-XXXXXX' },
    { id: 14, hospital_name: 'Sunsari Emergency Request', city: 'Sunsari', blood_type: 'AB-', blood_product: 'Whole Blood', urgency: 'Critical', location: 'Sunsari, Nepal (Request ID: 14)', contact_number: '+977-1-XXXXXX' },
    { id: 13, hospital_name: 'Morang Emergency Request', city: 'Morang', blood_type: 'A+', blood_product: 'Platelets', urgency: 'Critical', location: 'Morang, Nepal (Request ID: 13)', contact_number: '+977-1-XXXXXX' },
    { id: 11, hospital_name: 'Ilam Emergency Request', city: 'Ilam', blood_type: 'O+', blood_product: 'Plasma', urgency: 'Critical', location: 'Ilam, Nepal (Request ID: 11)', contact_number: '+977-1-XXXXXX' },
    { id: 8, hospital_name: 'Ramechhap Emergency Request', city: 'Ramechhap', blood_type: 'B-', blood_product: 'Plasma', urgency: 'Critical', location: 'Ramechhap, Nepal (Request ID: 8)', contact_number: '+977-1-XXXXXX' },
    { id: 7, hospital_name: 'Sindhuli Emergency Request', city: 'Sindhuli', blood_type: 'O+', blood_product: 'Platelets', urgency: 'Critical', location: 'Sindhuli, Nepal (Request ID: 7)', contact_number: '+977-1-XXXXXX' },
    { id: 6, hospital_name: 'Rasuwa Emergency Request', city: 'Rasuwa', blood_type: 'A+', blood_product: 'Plasma', urgency: 'Critical', location: 'Rasuwa, Nepal (Request ID: 6)', contact_number: '+977-1-XXXXXX' },
    { id: 5, hospital_name: 'Nuwakot Emergency Request', city: 'Nuwakot', blood_type: 'A-', blood_product: 'Platelets', urgency: 'Critical', location: 'Nuwakot, Nepal (Request ID: 5)', contact_number: '+977-1-XXXXXX' },
    { id: 1, hospital_name: 'Kathmandu Emergency Request', city: 'Kathmandu', blood_type: 'A+', blood_product: 'Platelets', urgency: 'Critical', location: 'Kathmandu, Nepal (Request ID: 1)', contact_number: '+977-1-XXXXXX' },
    { id: 28, hospital_name: 'Rautahat Emergency Request', city: 'Rautahat', blood_type: 'A-', blood_product: 'Plasma', urgency: 'High', location: 'Rautahat, Nepal (Request ID: 28)', contact_number: '+977-1-XXXXXX' },
    { id: 26, hospital_name: 'Parsa Emergency Request', city: 'Parsa', blood_type: 'O+', blood_product: 'Plasma', urgency: 'High', location: 'Parsa, Nepal (Request ID: 26)', contact_number: '+977-1-XXXXXX' },
    { id: 25, hospital_name: 'Nawalpur Emergency Request', city: 'Nawalpur', blood_type: 'O+', blood_product: 'Platelets', urgency: 'High', location: 'Nawalpur, Nepal (Request ID: 25)', contact_number: '+977-1-XXXXXX' },
  ])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    blood_type: '',
    urgency: '',
    city: '',
  })

  useEffect(() => {
    // Requests are loaded from local state, filtering happens in real-time
  }, [filters])

  const handleRequest = (requestId) => {
    // Handle blood request donation logic
    console.log('Donating to request:', requestId)
    alert('Your donation request has been submitted!')
  }

  const getUrgencyColor = (urgency) => {
    if (urgency === 'Critical') return 'bg-red-100 text-red-800 border-red-300'
    if (urgency === 'High') return 'bg-orange-100 text-orange-800 border-orange-300'
    if (urgency === 'Medium') return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    return 'bg-green-100 text-green-800 border-green-300'
  }

  // Filter requests
  const filteredRequests = requests.filter((request) => {
    return (
      (filters.blood_type === '' || request.blood_type === filters.blood_type) &&
      (filters.urgency === '' || request.urgency === filters.urgency) &&
      (filters.city === '' || request.city.toLowerCase().includes(filters.city.toLowerCase()))
    )
  })

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-4xl font-bold text-text mb-4 text-center flex items-center justify-center">
            <FaTint className="mr-3 text-primary" />
            Blood Donation Requests
          </h1>
          <p className="text-text opacity-70 text-center max-w-2xl mx-auto">
            View active blood donation requests from hospitals and blood banks. Help save lives by responding to urgent needs.
          </p>
        </motion.div>

        {/* Filter Section */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-xl font-semibold text-text mb-4">Filter Requests</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-text mb-2">Blood Type</label>
              <select
                value={filters.blood_type}
                onChange={(e) => setFilters({ ...filters, blood_type: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
              >
                <option value="">All Types</option>
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
            <div>
              <label className="block text-sm font-medium text-text mb-2">Urgency Level</label>
              <select
                value={filters.urgency}
                onChange={(e) => setFilters({ ...filters, urgency: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
              >
                <option value="">All Levels</option>
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-text mb-2">City</label>
              <input
                type="text"
                value={filters.city}
                onChange={(e) => setFilters({ ...filters, city: e.target.value })}
                placeholder="Enter city name"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
              />
            </div>
          </div>
        </motion.div>

        {/* Requests Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12"
        >
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <p className="text-text mt-4">Loading requests...</p>
            </div>
          ) : requests.length === 0 ? (
            <div className="bg-white rounded-2xl p-12 text-center text-text shadow-lg">
              <FaCheckCircle className="w-16 h-16 mx-auto text-green-400 mb-4" />
              <p className="text-lg font-semibold mb-2">No Active Requests</p>
              <p className="text-text opacity-70">All current blood needs have been met. Check back later for new requests.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredRequests.map((request) => (
                <motion.div
                  key={request.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow border-l-4 border-primary"
                >
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="text-xl font-semibold text-text">{request.hospital_name}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getUrgencyColor(request.urgency)}`}>
                          {request.urgency}
                        </span>
                      </div>
                      <p className="text-sm text-text opacity-70 mb-4">{request.location}</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <p className="text-text opacity-70">Blood Type Needed</p>
                          <p className="text-lg font-bold text-primary">{request.blood_type}</p>
                        </div>
                        <div>
                          <p className="text-text opacity-70">Product</p>
                          <p className="text-lg font-bold">{request.blood_product}</p>
                        </div>
                        <div>
                          <p className="text-text opacity-70">Units Needed</p>
                          <p className="text-lg font-bold">{request.units_needed}</p>
                        </div>
                        <div className="flex items-center gap-2 text-text opacity-70">
                          <FaMapMarkerAlt className="text-primary" />
                          {request.city}
                        </div>
                      </div>
                    </div>
                    <div className="flex flex-col gap-2 w-full md:w-auto">
                      <button
                        onClick={() => handleRequest(request.id)}
                        className="bg-primary text-white px-6 py-2 rounded-xl hover:bg-red-700 transition-colors font-semibold flex items-center justify-center gap-2"
                      >
                        <FaTint />
                        Donate Now
                      </button>
                      <a
                        href={`tel:${request.contact_number}`}
                        className="bg-gray-100 text-text px-6 py-2 rounded-xl hover:bg-gray-200 transition-colors font-semibold flex items-center justify-center gap-2"
                      >
                        <FaPhone />
                        Call Now
                      </a>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default BloodRequest
