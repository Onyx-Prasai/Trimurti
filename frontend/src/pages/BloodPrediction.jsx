import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaChartLine, FaUniversity } from 'react-icons/fa'
import { getBloodPredictions } from '../utils/api'

const BloodPrediction = () => {
  const [predictions, setPredictions] = useState([])
  const [predictionsLoading, setPredictionsLoading] = useState(false)

  useEffect(() => {
    fetchPredictions()
  }, [])

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

  const getUrgencyClass = (urgency) => {
    if (urgency === 'High') return 'border-red-500 bg-red-50'
    if (urgency === 'Medium') return 'border-yellow-500 bg-yellow-50'
    return 'border-green-500 bg-green-50'
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-4xl font-bold text-text mb-4 text-center flex items-center justify-center">
            <FaChartLine className="mr-3 text-primary" />
            Blood Prediction for Future
          </h1>
          <p className="text-text opacity-70 text-center max-w-2xl mx-auto">
            Stay informed about predicted blood shortages and hospital needs. Plan your donations in advance to help save lives.
          </p>
        </motion.div>

        {/* Predictions Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12"
        >
          {predictionsLoading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <p className="text-text mt-4">Loading predictions...</p>
            </div>
          ) : predictions.length === 0 ? (
            <div className="bg-white rounded-2xl p-12 text-center text-text shadow-lg">
              <FaChartLine className="w-16 h-16 mx-auto text-gray-300 mb-4" />
              <p className="text-lg">Not enough data to make predictions. Please check back later.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {predictions.map((pred, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  className={`rounded-2xl p-6 shadow-lg border-l-4 transition-transform hover:scale-105 ${getUrgencyClass(pred.urgency)}`}
                >
                  <div className="flex items-center mb-3">
                    <FaUniversity className="text-xl text-text opacity-70 mr-3" />
                    <h3 className="text-lg font-semibold text-text">{pred.hospital_name}</h3>
                  </div>
                  <p className="text-sm text-text opacity-70 mb-4">{pred.district}</p>
                  
                  <div className="text-center my-6 p-4 bg-white rounded-xl">
                    <p className="text-sm text-text mb-2 font-semibold">Predicted Need</p>
                    <p className="text-4xl font-bold text-primary">{pred.predicted_blood_type}</p>
                    <p className="text-xs text-text opacity-60 mt-2">
                      {pred.predicted_blood_product === 'whole_blood' ? 'Whole Blood' :
                       pred.predicted_blood_product === 'plasma' ? 'Plasma' :
                       pred.predicted_blood_product === 'platelets' ? 'Platelets' : 'Unknown'}
                    </p>
                  </div>

                  <div className="text-center">
                    <p className="text-sm text-text mb-2 font-semibold">Urgency Level</p>
                    <span className={`inline-block px-4 py-2 rounded-lg font-bold text-sm ${
                      pred.urgency === 'High' ? 'bg-red-200 text-red-700' :
                      pred.urgency === 'Medium' ? 'bg-yellow-200 text-yellow-700' : 'bg-green-200 text-green-700'
                    }`}>{pred.urgency}</span>
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

export default BloodPrediction
