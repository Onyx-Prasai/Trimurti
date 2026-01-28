import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaSearch, FaMap, FaList } from 'react-icons/fa'
import { getStock } from '../utils/api'
import BloodMapView from '../components/BloodMapView'
import { mockStockData, mockPredictionsData } from './FindBlood.test'

const FindBlood = () => {
  const [viewMode, setViewMode] = useState('list') // 'list' or 'map'
  const [stock, setStock] = useState([])
  const [stockFilters, setStockFilters] = useState({ 
    blood_group: '', 
    city: '', 
    blood_product_type: '', 
    sort_by: '', 
    order: 'asc' 
  })
  const [stockLoading, setStockLoading] = useState(false)

  useEffect(() => {
    fetchStock()
    const interval = setInterval(fetchStock, 15000)
    return () => clearInterval(interval)
  }, [stockFilters])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (searchType === 'hospitals') {
        const response = await getHospitals(filters)
        const data = response.data.results || (Array.isArray(response.data) ? response.data : [])
        setHospitals(data)
      } else {
        const response = await getBloodBanks({ city: filters.city })
        const data = response.data.results || (Array.isArray(response.data) ? response.data : [])
        setBloodBanks(data)
      }
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPredictions = async () => {
    setPredictionsLoading(true)
    try {
      const response = await getBloodPredictions()
      setPredictions(response.data)
    } catch (error) {
      console.error('Error fetching predictions:', error)
      // Use mock data as fallback
      setPredictions(mockPredictionsData)
    } finally {
      setPredictionsLoading(false)
    }
  }

  const fetchStock = async () => {
    setStockLoading(true)
    try {
      const response = await getStock(stockFilters)
      setStock(Array.isArray(response.data) ? response.data : [])
    } catch (error) {
      console.error('Error fetching stock:', error)
      // Use mock data as fallback
      setStock(mockStockData)
    } finally {
      setStockLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    // Filter removed, no longer used
  }

  const handleStockFilterChange = (key, value) => {
    setStockFilters({ ...stockFilters, [key]: value })
  }

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-text mb-8 text-center"
        >
          Find Blood
        </motion.h1>

        {/* Live Stock Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-lg mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
            <h2 className="text-2xl font-semibold text-text">Live Blood Availability</h2>
            <div className="flex flex-wrap gap-3">
              <select
                value={stockFilters.blood_group}
                onChange={(e) => handleStockFilterChange('blood_group', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Blood Groups</option>
                {bloodTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
              <select
                value={stockFilters.blood_product_type}
                onChange={(e) => handleStockFilterChange('blood_product_type', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Product Types</option>
                <option value="whole_blood">Whole Blood</option>
                <option value="plasma">Plasma</option>
                <option value="platelets">Platelets</option>
              </select>
              <input
                type="text"
                value={stockFilters.city}
                onChange={(e) => handleStockFilterChange('city', e.target.value)}
                placeholder="Filter by district"
                className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              <select
                value={stockFilters.sort_by}
                onChange={(e) => handleStockFilterChange('sort_by', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">Sort By</option>
                <option value="hospital__name">Hospital Name</option>
                <option value="blood_group">Blood Group</option>
                <option value="blood_product_type">Product Type</option>
                <option value="units_available">Units Available</option>
              </select>
              <select
                value={stockFilters.order}
                onChange={(e) => handleStockFilterChange('order', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
              <button
                onClick={fetchStock}
                className="flex items-center space-x-2 px-4 py-2 bg-primary text-white rounded-xl hover:bg-red-600 transition-all"
              >
                <FaSearch />
                <span>Refresh</span>
              </button>
            </div>
          </div>

          {stockLoading ? (
            <div className="text-center py-4">Loading live stock...</div>
          ) : stock.length === 0 ? (
            <div className="text-center py-4 text-text">No stock records yet.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Hospital</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">District</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Blood Group</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Product Type</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Units</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Updated</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {stock.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <p className="font-semibold text-text">{item.hospital?.name || item.hospital_name}</p>
                        <p className="text-sm text-gray-500">{item.hospital?.address || ''}</p>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">{item.hospital?.city || item.city}</td>
                      <td className="px-4 py-3">
                        <span className="px-3 py-1 bg-primary text-white rounded-full text-sm">
                          {item.blood_group}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">
                        {item.blood_product_type === 'whole_blood' ? 'Whole Blood' :
                         item.blood_product_type === 'plasma' ? 'Plasma' :
                         item.blood_product_type === 'platelets' ? 'Platelets' : 'Unknown'}
                      </td>
                      <td className="px-4 py-3 text-lg font-bold text-text">{item.units_available || item.units}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {new Date(item.updated_at || item.last_updated).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>

        {/* Search Type Toggle - Removed, moved to Blood Request */}

        {/* View Mode Toggle */}
        <div className="flex justify-center mb-6">
          <div className="bg-white rounded-2xl p-1 shadow-lg inline-flex">
            <button
              onClick={() => setViewMode('list')}
              className={`px-6 py-2 rounded-xl transition-all flex items-center space-x-2 ${
                viewMode === 'list'
                  ? 'bg-primary text-white'
                  : 'text-text hover:bg-gray-100'
              }`}
            >
              <FaList />
              <span>Stock Table</span>
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-6 py-2 rounded-xl transition-all flex items-center space-x-2 ${
                viewMode === 'map'
                  ? 'bg-primary text-white'
                  : 'text-text hover:bg-gray-100'
              }`}
            >
              <FaMap />
              <span>Map View</span>
            </button>
          </div>
        </div>

        {/* Stock Table View */}
        {viewMode === 'list' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {/* Stock table already displayed above in Live Stock Section */}
          </motion.div>
        )}

        {/* Map View */}
        {viewMode === 'map' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <BloodMapView 
              bloodGroup={stockFilters.blood_group}
              selectedCity={stockFilters.city}
            />
          </motion.div>
        )}

        {/* Blood Prediction Section */}
        {/* Moved to separate BloodPrediction page */}
      </div>
    </div>
  )
}

export default FindBlood

