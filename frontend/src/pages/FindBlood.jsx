import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaSearch, FaPhone, FaMapMarkerAlt, FaExclamationCircle, FaChartLine, FaUniversity, FaMap, FaList } from 'react-icons/fa'
import { getHospitals, getBloodBanks, getBloodPredictions, getStock } from '../utils/api'
import BloodMapView from '../components/BloodMapView'

const FindBlood = () => {
  const [searchType, setSearchType] = useState('hospitals')
  const [viewMode, setViewMode] = useState('list') // 'list' or 'map'
  const [filters, setFilters] = useState({
    blood_type: '',
    blood_product: '',
    city: '',
    hospital_name: '',
  })
  const [hospitals, setHospitals] = useState([])
  const [bloodBanks, setBloodBanks] = useState([])
  const [predictions, setPredictions] = useState([])
  const [stock, setStock] = useState([])
  const [stockFilters, setStockFilters] = useState({ 
    blood_group: '', 
    city: '', 
    blood_product_type: '', 
    sort_by: '', 
    order: 'asc' 
  })
  const [loading, setLoading] = useState(false)
  const [predictionsLoading, setPredictionsLoading] = useState(false)
  const [stockLoading, setStockLoading] = useState(false)
  const [eligibilityChecklist, setEligibilityChecklist] = useState({
    age: false,
    weight: false,
    health: false,
    no_tattoo: false,
    no_pregnancy: false,
  })

  useEffect(() => {
    fetchData()
  }, [filters, searchType])

  useEffect(() => {
    fetchPredictions()
  }, [])

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
    } finally {
      setStockLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
  }

  const handleStockFilterChange = (key, value) => {
    setStockFilters({ ...stockFilters, [key]: value })
  }

  const getGoogleMapsLink = (lat, lng, name) => {
    if (lat && lng) {
      return `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&destination_place_id=${encodeURIComponent(name)}`
    }
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}`
  }

  const isEligible = () => {
    return Object.values(eligibilityChecklist).every(v => v === true)
  }

  const getUrgencyClass = (urgency) => {
    switch (urgency) {
      case 'High': return 'border-red-500 bg-red-50';
      case 'Medium': return 'border-yellow-500 bg-yellow-50';
      case 'Low': return 'border-green-500 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  }

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
  const districts = [
    // Bagmati Province
    'Kathmandu', 'Bhaktapur', 'Lalitpur', 'Kavre', 'Nuwakot', 'Rasuwa', 
    'Sindhuli', 'Ramechhap', 'Dolakha', 'Makwanpur',
    // Eastern Region
    'Ilam', 'Jhapa', 'Morang', 'Sunsari', 'Dhankuta', 'Terhathum', 'Panchthar', 
    'Udayapur', 'Sankhuwasabha', 'Sindhupalchok',
    // Central Region
    'Gorkha', 'Lamjung', 'Tanahu', 'Chitwan', 'Nawalpur', 'Parsa', 'Bara', 
    'Rautahat', 'Gulmi', 'Arghakhanchi',
    // Western Region
    'Palpa', 'Dang', 'Banke', 'Bardiya', 'Surkhet',
    // Mid-Western Region
    'Salyan', 'Pyuthan', 'Rolpa', 'Rukum', 'Dailekh', 'Jumla', 'Kalikot', 'Dolpa',
    // Far-Western Region
    'Jajarkot', 'Achham', 'Bajura', 'Bajhang', 'Doti', 'Kailali', 'Kanchanpur'
  ]

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
                        <p className="font-semibold text-text">{item.hospital?.name}</p>
                        <p className="text-sm text-gray-500">{item.hospital?.address}</p>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-700">{item.hospital?.city}</td>
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
                      <td className="px-4 py-3 text-lg font-bold text-text">{item.units_available}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {new Date(item.updated_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>

        {/* Search Type Toggle */}
        <div className="flex justify-center mb-6 space-x-4">
          <div className="bg-white rounded-2xl p-1 shadow-lg inline-flex">
            <button
              onClick={() => setSearchType('hospitals')}
              className={`px-6 py-2 rounded-xl transition-all ${
                searchType === 'hospitals'
                  ? 'bg-primary text-white'
                  : 'text-text hover:bg-gray-100'
              }`}
            >
              Hospitals in Need
            </button>
            <button
              onClick={() => setSearchType('banks')}
              className={`px-6 py-2 rounded-xl transition-all ${
                searchType === 'banks'
                  ? 'bg-primary text-white'
                  : 'text-text hover:bg-gray-100'
              }`}
            >
              Blood Banks
            </button>
          </div>

          {/* View Mode Toggle */}
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
              <span>List View</span>
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

        {/* Search Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-lg mb-8"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Blood Type
              </label>
              <select
                value={filters.blood_type}
                onChange={(e) => handleFilterChange('blood_type', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Blood Types</option>
                {bloodTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Product Type
              </label>
              <select
                value={filters.blood_product}
                onChange={(e) => handleFilterChange('blood_product', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Products</option>
                <option value="whole_blood">Whole Blood</option>
                <option value="plasma">Plasma</option>
                <option value="platelets">Platelets</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-text mb-2">
                District
              </label>
              <select
                value={filters.city}
                onChange={(e) => handleFilterChange('city', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">All Districts</option>
                {districts.map((district) => (
                  <option key={district} value={district}>{district}</option>
                ))}
              </select>
            </div>

            {searchType === 'hospitals' && (
              <div>
                <label className="block text-sm font-medium text-text mb-2">
                  Hospital Name
                </label>
                <input
                  type="text"
                  value={filters.hospital_name}
                  onChange={(e) => handleFilterChange('hospital_name', e.target.value)}
                  placeholder="Search hospitals..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
            )}
          </div>
        </motion.div>

        {/* Map View */}
        {viewMode === 'map' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <BloodMapView 
              bloodGroup={stockFilters.blood_group || filters.blood_type}
              selectedCity={filters.city}
            />
          </motion.div>
        )}

        {/* Results */}
        {viewMode === 'list' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            {loading ? (
              <div className="text-center py-12">Loading...</div>
            ) : searchType === 'hospitals' ? (
              <div className="space-y-4">
                {hospitals.length === 0 ? (
                  <div className="bg-white rounded-2xl p-8 text-center text-text">
                    No hospitals found matching your criteria.
                  </div>
                ) : (
                  hospitals.map((hospital) => (
                    <motion.div
                      key={hospital.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className={`bg-white rounded-2xl p-6 shadow-lg ${
                        hospital.is_critical ? 'border-l-4 border-primary' : ''
                      }`}
                    >
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-xl font-semibold text-text mb-2">
                            {hospital.hospital_name}
                          </h3>
                          <div className="flex items-center space-x-4 text-sm text-text opacity-70">
                            <span className="flex items-center">
                              <FaMapMarkerAlt className="mr-2" />
                              {hospital.district}
                            </span>
                            <span className="px-3 py-1 bg-primary text-white rounded-full">
                              {hospital.blood_type_needed}
                            </span>
                            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">
                              {hospital.blood_product_needed === 'whole_blood' ? 'Whole Blood' :
                               hospital.blood_product_needed === 'plasma' ? 'Plasma' :
                               hospital.blood_product_needed === 'platelets' ? 'Platelets' : 'Unknown'}
                            </span>
                            {hospital.is_critical && (
                              <span className="flex items-center text-primary">
                                <FaExclamationCircle className="mr-1" />
                                Critical
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <p className="text-text mb-4">{hospital.address}</p>
                      <div className="flex space-x-3">
                        <a
                          href={`tel:${hospital.contact_phone}`}
                          className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-xl hover:bg-red-600 transition-all"
                        >
                          <FaPhone />
                          <span>Call Now</span>
                        </a>
                        <a
                          href={getGoogleMapsLink(hospital.latitude, hospital.longitude, hospital.hospital_name)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center space-x-2 bg-gray-100 text-text px-4 py-2 rounded-xl hover:bg-gray-200 transition-all"
                        >
                          <FaMapMarkerAlt />
                          <span>Get Directions</span>
                        </a>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>
            ) : (
              <div className="space-y-4">
                {bloodBanks.length === 0 ? (
                  <div className="bg-white rounded-2xl p-8 text-center text-text">
                    No blood banks found.
                  </div>
                ) : (
                  bloodBanks.map((bank) => (
                    <motion.div
                      key={bank.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="bg-white rounded-2xl p-6 shadow-lg"
                    >
                      <h3 className="text-xl font-semibold text-text mb-2">
                        {bank.name}
                      </h3>
                      <div className="flex items-center space-x-4 text-sm text-text opacity-70 mb-4">
                        <span className="flex items-center">
                          <FaMapMarkerAlt className="mr-2" />
                          {bank.city}
                        </span>
                        <span>{bank.operating_hours}</span>
                      </div>
                      <p className="text-text mb-4">{bank.address}</p>
                      <div className="flex space-x-3">
                        <a
                          href={`tel:${bank.phone}`}
                          className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-xl hover:bg-red-600 transition-all"
                        >
                          <FaPhone />
                          <span>Call Now</span>
                        </a>
                        <a
                          href={getGoogleMapsLink(bank.latitude, bank.longitude, bank.name)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center space-x-2 bg-gray-100 text-text px-4 py-2 rounded-xl hover:bg-gray-200 transition-all"
                        >
                          <FaMapMarkerAlt />
                          <span>Get Directions</span>
                        </a>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Eligibility Tool */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl p-6 shadow-lg sticky top-24"
            >
              <h3 className="text-xl font-semibold text-text mb-4">
                Donor Eligibility Checklist
              </h3>
              <div className="space-y-3">
                {[
                  { key: 'age', label: 'Age between 18-65 years' },
                  { key: 'weight', label: 'Weight at least 50 kg' },
                  { key: 'health', label: 'Good general health' },
                  { key: 'no_tattoo', label: 'No tattoos in last 6 months' },
                  { key: 'no_pregnancy', label: 'Not pregnant (if applicable)' },
                ].map((item) => (
                  <label key={item.key} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={eligibilityChecklist[item.key]}
                      onChange={(e) =>
                        setEligibilityChecklist({
                          ...eligibilityChecklist,
                          [item.key]: e.target.checked,
                        })
                      }
                      className="w-5 h-5 text-primary rounded focus:ring-primary"
                    />
                    <span className="text-text">{item.label}</span>
                  </label>
                ))}
              </div>
              <div className={`mt-6 p-4 rounded-xl ${
                isEligible()
                  ? 'bg-green-100 text-green-700'
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                <p className="font-semibold">
                  {isEligible()
                    ? '✓ You are eligible to donate!'
                    : 'Complete the checklist to check eligibility'}
                </p>
              </div>
            </motion.div>
          </div>
        </div>
        
        {/* Blood Prediction Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-16"
        >
          <h2 className="text-3xl font-bold text-text mb-8 text-center flex items-center justify-center">
            <FaChartLine className="mr-3 text-primary" />
            Blood Prediction for Future
          </h2>
          {predictionsLoading ? (
            <div className="text-center py-12">Loading predictions...</div>
          ) : predictions.length === 0 ? (
            <div className="bg-white rounded-2xl p-8 text-center text-text shadow-lg">
              Not enough data to make predictions. Please check back later.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {predictions.map((pred, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className={`rounded-2xl p-6 shadow-lg border-l-4 ${getUrgencyClass(pred.urgency)}`}
                >
                  <div className="flex items-center mb-3">
                    <FaUniversity className="text-xl text-text opacity-70 mr-3" />
                    <h3 className="text-lg font-semibold text-text">{pred.hospital_name}</h3>
                  </div>
                  <p className="text-sm text-text opacity-70 mb-4">{pred.district}</p>
                  
                  <div className="text-center my-4">
                    <p className="text-sm text-text mb-1">Predicted Need</p>
                    <p className="text-4xl font-bold text-primary">{pred.predicted_blood_type}</p>
                    <p className="text-xs text-text opacity-60 mt-2">
                      {pred.predicted_blood_product === 'whole_blood' ? 'Whole Blood' :
                       pred.predicted_blood_product === 'plasma' ? 'Plasma' :
                       pred.predicted_blood_product === 'platelets' ? 'Platelets' : 'Unknown'}
                    </p>
                  </div>

                  <div className="text-center">
                    <p className="text-sm text-text mb-1">Urgency Level</p>
                    <p className={`text-lg font-bold ${
                      pred.urgency === 'High' ? 'text-red-600' :
                      pred.urgency === 'Medium' ? 'text-yellow-600' : 'text-green-600'
                    }`}>{pred.urgency}</p>
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

export default FindBlood

