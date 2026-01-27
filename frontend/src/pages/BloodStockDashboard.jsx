import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaHospital, FaTint, FaMapMarkerAlt, FaSearch, FaFilter, FaExclamationTriangle } from 'react-icons/fa'

const BloodStockDashboard = () => {
  const [bloodStock, setBloodStock] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    city: '',
    bloodGroup: '',
    minUnits: 0
  })
  const [cities, setCities] = useState([])

  const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

  useEffect(() => {
    fetchBloodStock()
  }, [filters])

  const fetchBloodStock = async () => {
    setLoading(true)
    try {
      const queryParams = new URLSearchParams()
      if (filters.city) queryParams.append('city', filters.city)
      if (filters.bloodGroup) queryParams.append('blood_group', filters.bloodGroup)
      if (filters.minUnits > 0) queryParams.append('min_units', filters.minUnits)

      const response = await fetch(
        `http://localhost:8000/api/v1/public/blood-stock/?${queryParams}`
      )
      const data = await response.json()
      
      setBloodStock(data.results || [])
      
      // Extract unique cities
      const uniqueCities = [...new Set(data.results.map(item => item.hospital.city))]
      setCities(uniqueCities)
    } catch (error) {
      console.error('Error fetching blood stock:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStockStatus = (units) => {
    if (units < 5) return { label: 'CRITICAL', color: 'text-red-600 bg-red-100' }
    if (units < 15) return { label: 'LOW', color: 'text-orange-600 bg-orange-100' }
    if (units < 30) return { label: 'MODERATE', color: 'text-yellow-600 bg-yellow-100' }
    return { label: 'GOOD', color: 'text-green-600 bg-green-100' }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            BloodSync Nepal Dashboard
          </h1>
          <p className="text-gray-600">
            Real-time blood inventory across Nepal's hospitals and blood banks
          </p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-8"
        >
          <div className="flex items-center mb-4">
            <FaFilter className="text-primary mr-2" />
            <h2 className="text-xl font-semibold">Search & Filter</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* City Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FaMapMarkerAlt className="inline mr-1" /> City
              </label>
              <select
                value={filters.city}
                onChange={(e) => handleFilterChange('city', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Cities</option>
                <option value="Kathmandu">Kathmandu</option>
                <option value="Lalitpur">Lalitpur</option>
                <option value="Bhaktapur">Bhaktapur</option>
                <option value="Pokhara">Pokhara</option>
                <option value="Chitwan">Chitwan</option>
              </select>
            </div>

            {/* Blood Group Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FaTint className="inline mr-1" /> Blood Group
              </label>
              <select
                value={filters.bloodGroup}
                onChange={(e) => handleFilterChange('bloodGroup', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Blood Groups</option>
                {bloodGroups.map(bg => (
                  <option key={bg} value={bg}>{bg}</option>
                ))}
              </select>
            </div>

            {/* Minimum Units Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Units
              </label>
              <input
                type="number"
                value={filters.minUnits}
                onChange={(e) => handleFilterChange('minUnits', parseInt(e.target.value) || 0)}
                min="0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="0"
              />
            </div>
          </div>
        </motion.div>

        {/* Results */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading blood stock data...</p>
          </div>
        ) : bloodStock.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
            <FaExclamationTriangle className="text-5xl text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No Results Found</h3>
            <p className="text-gray-600">Try adjusting your filters to see more results.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {bloodStock.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg overflow-hidden"
              >
                {/* Hospital Header */}
                <div className="bg-gradient-to-r from-primary to-red-600 text-white p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center">
                      <FaHospital className="text-3xl mr-4" />
                      <div>
                        <h3 className="text-2xl font-bold">{item.hospital.name}</h3>
                        <p className="opacity-90 flex items-center mt-1">
                          <FaMapMarkerAlt className="mr-2" />
                          {item.hospital.city}
                        </p>
                        {item.hospital.address && (
                          <p className="text-sm opacity-75 mt-1">{item.hospital.address}</p>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm opacity-75">Last Updated</p>
                      <p className="font-semibold">
                        {new Date(item.last_updated).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Blood Stock Grid */}
                <div className="p-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
                    {bloodGroups.map(bg => {
                      const stock = item.stock[bg]
                      const units = stock ? stock.units : 0
                      const status = getStockStatus(units)

                      return (
                        <div
                          key={bg}
                          className="text-center p-4 rounded-xl border-2 border-gray-200 hover:border-primary transition-all"
                        >
                          <div className="text-2xl font-bold text-gray-800 mb-1">{bg}</div>
                          <div className="text-3xl font-bold text-primary mb-2">{units}</div>
                          <div className={`text-xs font-semibold px-2 py-1 rounded-full ${status.color}`}>
                            {status.label}
                          </div>
                          {stock && (
                            <div className="text-xs text-gray-500 mt-2">
                              {new Date(stock.updated_at).toLocaleTimeString()}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>

                  {/* Total Units */}
                  <div className="mt-6 pt-6 border-t border-gray-200 flex justify-between items-center">
                    <span className="text-gray-600 font-medium">Total Units Available:</span>
                    <span className="text-3xl font-bold text-primary">
                      {Object.values(item.stock).reduce((sum, s) => sum + (s.units || 0), 0)}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {/* Summary Stats */}
        {!loading && bloodStock.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-8 bg-white rounded-2xl shadow-lg p-6"
          >
            <h3 className="text-xl font-bold mb-4">Summary Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-primary">{bloodStock.length}</div>
                <div className="text-gray-600 mt-2">Hospitals Found</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600">
                  {bloodStock.reduce((sum, item) => 
                    sum + Object.values(item.stock).reduce((s, stock) => s + (stock.units || 0), 0), 0
                  )}
                </div>
                <div className="text-gray-600 mt-2">Total Units Available</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600">
                  {new Set(bloodStock.map(item => item.hospital.city)).size}
                </div>
                <div className="text-gray-600 mt-2">Cities Covered</div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default BloodStockDashboard
