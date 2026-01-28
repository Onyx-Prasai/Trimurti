import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaSearch, FaMap, FaList } from 'react-icons/fa'
import { getStock } from '../utils/api'
import BloodMapView from '../components/BloodMapView'
import { mockStockData, mockPredictionsData } from './FindBlood.test'

const FindBlood = () => {
  const [viewMode, setViewMode] = useState('list') // 'list' or 'map'
  const [stock, setStock] = useState([])
  const [stockPage, setStockPage] = useState(1)
  const [stockFilters, setStockFilters] = useState({ 
    blood_group: '', 
    city: '', 
    blood_product_type: '', 
    sort_by: '', 
    order: 'asc' 
  })
  const [stockLoading, setStockLoading] = useState(false)
  const PAGE_SIZE = 5

  useEffect(() => {
    fetchStock()
    const interval = setInterval(fetchStock, 15000)
    return () => clearInterval(interval)
  }, [stockFilters])

  useEffect(() => {
    // Reset pagination whenever filters change
    setStockPage(1)
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
  const formatProductType = (t) => {
    // Default to Whole Blood if backend doesn't send a specific product type
    if (!t) return 'Whole Blood'
    const normalized = String(t).toLowerCase().replace(/\s+/g, '_')
    if (normalized === 'whole_blood') return 'Whole Blood'
    if (normalized === 'plasma') return 'Plasma'
    if (normalized === 'platelets') return 'Platelets'
    // Fallback: show the raw value in a nicer way instead of "Unknown"
    return String(t)
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (ch) => ch.toUpperCase())
  }

  // Group stock rows by hospital so "Live Blood Availability" shows hospitals (not a long table)
  const hospitalGroups = Object.values(
    (stock || []).reduce((acc, item) => {
      const hospitalName = item.hospital?.name || item.hospital_name || 'Unknown Hospital'
      const city = item.hospital?.city || item.city || ''
      const address = item.hospital?.address || ''
      const key = `${hospitalName}__${city}__${address}`
      if (!acc[key]) {
        acc[key] = {
          key,
          hospitalName,
          city,
          address,
          updated_at: item.updated_at || item.last_updated || null,
          items: [],
        }
      }
      acc[key].items.push(item)
      const itemUpdated = item.updated_at || item.last_updated || null
      if (itemUpdated) {
        const cur = acc[key].updated_at ? new Date(acc[key].updated_at).getTime() : 0
        const nxt = new Date(itemUpdated).getTime()
        if (nxt > cur) acc[key].updated_at = itemUpdated
      }
      return acc
    }, {})
  )

  const totalPages = Math.max(1, Math.ceil(hospitalGroups.length / PAGE_SIZE))
  const safePage = Math.min(Math.max(stockPage, 1), totalPages)
  const pagedHospitals = hospitalGroups.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE)

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

          {/* View Mode Toggle */}
          <div className="flex justify-center mb-6">
            <div className="bg-gray-50 rounded-2xl p-1 shadow-sm inline-flex">
              <button
                onClick={() => setViewMode('list')}
                className={`px-6 py-2 rounded-xl transition-all flex items-center space-x-2 ${
                  viewMode === 'list'
                    ? 'bg-primary text-white'
                    : 'text-text hover:bg-gray-100'
                }`}
              >
                <FaList />
                <span>List</span>
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
                <span>Map</span>
              </button>
            </div>
          </div>

          {viewMode === 'map' ? (
            <div className="mb-2">
              <BloodMapView 
                bloodGroup={stockFilters.blood_group}
                selectedCity={stockFilters.city?.trim() || ''}
              />
            </div>
          ) : stockLoading ? (
            <div className="text-center py-6">Loading live stock...</div>
          ) : hospitalGroups.length === 0 ? (
            <div className="text-center py-6 text-text">No stock records yet.</div>
          ) : (
            <>
              <div className="space-y-4">
                {pagedHospitals.map((group) => (
                  <div key={group.key} className="border border-gray-200 rounded-2xl p-5 hover:shadow-md transition-all">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-2">
                      <div>
                        <p className="text-lg font-bold text-text">{group.hospitalName}</p>
                        <p className="text-sm text-gray-600">{group.city}{group.address ? ` • ${group.address}` : ''}</p>
                      </div>
                      <div className="text-sm text-gray-500">
                        {group.updated_at ? `Updated: ${new Date(group.updated_at).toLocaleString()}` : ''}
                      </div>
                    </div>

                    <div className="mt-4 flex flex-wrap gap-2">
                      {group.items.map((item) => (
                        <div
                          key={item.id || `${item.blood_group}-${item.blood_product_type}-${item.units_available || item.units}`}
                          className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-2"
                        >
                          <span className="px-2 py-1 bg-primary text-white rounded-full text-xs font-semibold">
                            {item.blood_group}
                          </span>
                          <span className="text-xs text-gray-700">{formatProductType(item.blood_product_type)}</span>
                          <span className="text-xs font-bold text-text">
                            {item.units_available ?? item.units ?? 0} units
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination ("scroll wheel" style page buttons) */}
              <div className="mt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div className="text-sm text-gray-600">
                  Page <span className="font-semibold text-text">{safePage}</span> of{' '}
                  <span className="font-semibold text-text">{totalPages}</span>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setStockPage((p) => Math.max(1, p - 1))}
                    disabled={safePage === 1}
                    className="px-3 py-2 rounded-xl border border-gray-300 text-text disabled:opacity-50 hover:bg-gray-50"
                  >
                    Prev
                  </button>

                  <div className="max-w-full overflow-x-auto">
                    <div className="flex gap-2">
                      {Array.from({ length: totalPages }).map((_, idx) => {
                        const page = idx + 1
                        const active = page === safePage
                        return (
                          <button
                            key={page}
                            onClick={() => setStockPage(page)}
                            className={`min-w-10 px-3 py-2 rounded-xl border transition-all ${
                              active
                                ? 'bg-primary text-white border-primary'
                                : 'border-gray-300 text-text hover:bg-gray-50'
                            }`}
                          >
                            {page}
                          </button>
                        )
                      })}
                    </div>
                  </div>

                  <button
                    onClick={() => setStockPage((p) => Math.min(totalPages, p + 1))}
                    disabled={safePage === totalPages}
                    className="px-3 py-2 rounded-xl border border-gray-300 text-text disabled:opacity-50 hover:bg-gray-50"
                  >
                    Next
                  </button>
                </div>
              </div>
            </>
          )}
        </motion.div>

        {/* Search Type Toggle - Removed, moved to Blood Request */}

        {/* Blood Prediction Section */}
        {/* Moved to separate BloodPrediction page */}
      </div>
    </div>
  )
}

export default FindBlood

