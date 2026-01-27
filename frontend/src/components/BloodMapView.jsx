import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet'
import { motion } from 'framer-motion'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { FaMapMarkerAlt, FaTint } from 'react-icons/fa'
import axios from 'axios'

// Fix Leaflet default marker icon issue
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const createCustomIcon = (stockLevel) => {
  const color = stockLevel === 'CRITICAL' ? '#ef4444' :
                stockLevel === 'LOW' ? '#f97316' :
                stockLevel === 'MODERATE' ? '#eab308' : '#22c55e'
  
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        width: 32px;
        height: 32px;
        background-color: ${color};
        border: 3px solid white;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
        </svg>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  })
}

const BloodMapView = ({ bloodGroup, selectedCity, showRadiusDemo = false }) => {
  const [hospitals, setHospitals] = useState([])
  const [loading, setLoading] = useState(true)
  const [mapCenter, setMapCenter] = useState([27.7172, 85.3240]) // Kathmandu default
  const [mapZoom, setMapZoom] = useState(12)

  // City coordinates
  const cityCoordinates = {
    Kathmandu: [27.7172, 85.3240],
    Bhaktapur: [27.6710, 85.4298],
    Lalitpur: [27.6588, 85.3247],
    Pokhara: [28.2096, 83.9856],
  }

  useEffect(() => {
    if (selectedCity && cityCoordinates[selectedCity]) {
      setMapCenter(cityCoordinates[selectedCity])
      setMapZoom(13)
    }
  }, [selectedCity])

  useEffect(() => {
    fetchMapData()
  }, [bloodGroup, selectedCity])

  const fetchMapData = async () => {
    setLoading(true)
    try {
      const cities = selectedCity ? selectedCity : 'Kathmandu,Bhaktapur,Lalitpur,Pokhara'
      const response = await axios.get(
        `http://localhost:8000/api/v1/public/map-data/?cities=${cities}`
      )
      setHospitals(response.data.hospitals || [])
    } catch (error) {
      console.error('Error fetching map data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStockLevel = (totalUnits) => {
    if (totalUnits < 5) return 'CRITICAL'
    if (totalUnits < 15) return 'LOW'
    if (totalUnits < 30) return 'MODERATE'
    return 'GOOD'
  }

  const getStockColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'text-red-600'
      case 'LOW': return 'text-orange-600'
      case 'MODERATE': return 'text-yellow-600'
      case 'GOOD': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  const filteredHospitals = hospitals.filter(hospital => {
    if (!bloodGroup) return true
    return hospital.stock[bloodGroup] !== undefined && hospital.stock[bloodGroup] > 0
  })

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
      <div className="p-4 bg-gradient-to-r from-primary to-red-600 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FaMapMarkerAlt className="text-2xl" />
            <h3 className="text-xl font-bold">Blood Availability Map</h3>
          </div>
          {bloodGroup && (
            <div className="flex items-center space-x-2 bg-white/20 px-3 py-1 rounded-lg">
              <FaTint />
              <span className="font-semibold">{bloodGroup}</span>
            </div>
          )}
        </div>
        <p className="text-sm mt-1 text-white/80">
          {filteredHospitals.length} hospital{filteredHospitals.length !== 1 ? 's' : ''} found
          {selectedCity && ` in ${selectedCity}`}
        </p>
      </div>

      {loading ? (
        <div className="h-[500px] flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-2"></div>
            <p className="text-gray-600">Loading map data...</p>
          </div>
        </div>
      ) : (
        <div className="relative">
          <MapContainer
            center={mapCenter}
            zoom={mapZoom}
            className="h-[500px] w-full"
            scrollWheelZoom={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {filteredHospitals.map((hospital) => {
              const stockLevel = getStockLevel(hospital.total_units)
              const hasBloodGroup = bloodGroup ? hospital.stock[bloodGroup] > 0 : true
              
              if (!hasBloodGroup) return null

              return (
                <Marker
                  key={hospital.id}
                  position={[hospital.position.lat, hospital.position.lng]}
                  icon={createCustomIcon(stockLevel)}
                >
                  <Popup>
                    <div className="p-2 min-w-[250px]">
                      <h4 className="font-bold text-lg text-gray-800 mb-2">
                        {hospital.name}
                      </h4>
                      <p className="text-sm text-gray-600 mb-3">
                        <FaMapMarkerAlt className="inline mr-1" />
                        {hospital.city}, {hospital.address}
                      </p>
                      
                      <div className="mb-3">
                        <p className={`text-sm font-semibold ${getStockColor(stockLevel)}`}>
                          Stock Level: {stockLevel}
                        </p>
                        <p className="text-xs text-gray-500">
                          Total Units: {hospital.total_units}
                        </p>
                      </div>

                      <div className="border-t pt-2">
                        <p className="text-xs font-semibold text-gray-700 mb-1">
                          Available Blood Groups:
                        </p>
                        <div className="grid grid-cols-4 gap-1">
                          {Object.entries(hospital.stock).map(([group, units]) => (
                            <div
                              key={group}
                              className={`text-center p-1 rounded ${
                                units > 0 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-400'
                              } ${bloodGroup === group ? 'ring-2 ring-primary' : ''}`}
                            >
                              <div className="text-xs font-semibold">{group}</div>
                              <div className="text-xs">{units}</div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <button
                        onClick={() => {
                          const url = `https://www.google.com/maps/dir/?api=1&destination=${hospital.position.lat},${hospital.position.lng}`
                          window.open(url, '_blank')
                        }}
                        className="mt-3 w-full bg-primary text-white py-2 rounded-lg text-sm hover:bg-red-600 transition-colors"
                      >
                        Get Directions
                      </button>
                    </div>
                  </Popup>
                </Marker>
              )
            })}

            {showRadiusDemo && mapCenter && (
              <>
                <Circle
                  center={mapCenter}
                  radius={500}
                  pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.1 }}
                />
                <Circle
                  center={mapCenter}
                  radius={2000}
                  pathOptions={{ color: 'orange', fillColor: 'orange', fillOpacity: 0.05 }}
                />
              </>
            )}
          </MapContainer>

          {/* Legend */}
          <div className="absolute bottom-4 right-4 bg-white/95 backdrop-blur-sm p-3 rounded-lg shadow-lg z-[1000]">
            <p className="text-xs font-semibold mb-2 text-gray-700">Stock Levels</p>
            <div className="space-y-1">
              {[
                { label: 'Critical (<5)', color: '#ef4444' },
                { label: 'Low (5-14)', color: '#f97316' },
                { label: 'Moderate (15-29)', color: '#eab308' },
                { label: 'Good (30+)', color: '#22c55e' },
              ].map(({ label, color }) => (
                <div key={label} className="flex items-center space-x-2">
                  <div
                    className="w-4 h-4 rounded-full border-2 border-white shadow-sm"
                    style={{ backgroundColor: color }}
                  ></div>
                  <span className="text-xs text-gray-700">{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="p-4 bg-gray-50 border-t">
        <p className="text-xs text-gray-600 text-center">
          Click on markers to view detailed blood stock information and get directions
        </p>
      </div>
    </div>
  )
}

export default BloodMapView
