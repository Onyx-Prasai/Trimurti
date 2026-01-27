import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Donor API
export const getDonorStats = () => api.get('/donors/stats/')
export const getDonorProfile = (id) => api.get(`/donors/${id}/`)
export const registerDonation = (id, data) => api.post(`/donors/${id}/register_donation/`, data)

// Hospital API
export const getHospitals = (params) => api.get('/hospitals/', { params })
export const getBloodPredictions = () => api.get('/hospitals/predictions/')
export const getHospitalRegistry = (params) => api.get('/hospital-registry/', { params })
export const getStock = (params) => api.get('/stock/', { params })
export const ingestTransaction = (data, apiKey) =>
  api.post('/ingest/transactions/', data, {
    headers: { 'X-API-Key': apiKey },
  })

// Blood Bank API
export const getBloodBanks = (params) => api.get('/bloodbanks/', { params })

// Store API
export const getStoreItems = () => api.get('/store/')
export const redeemItem = (data) => api.post('/redemptions/', data)

// AI Health API
export const chatWithAI = (message) => api.post('/ai-health/chat/', { message })
export const analyzeReport = (data) => api.post('/ai-health/analyze_report/', data)

export default api

