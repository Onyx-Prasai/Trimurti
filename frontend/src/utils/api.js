import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
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

// Money Reward API (Points to Esewa)
export const getMoneyRewards = () => api.get('/rewards/money/')
export const getActiveMoneyRewards = () => api.get('/rewards/money/active/')
export const redeemMoneyReward = (data) => api.post('/rewards/money/redeem/', data)

// Discount Reward API
export const getDiscountRewards = () => api.get('/rewards/discounts/')
export const getAvailableDiscounts = () => api.get('/rewards/discounts/available/')
export const getDiscountRedemptions = () => api.get('/rewards/discount-redemptions/')
export const redeemDiscountReward = (data) => api.post('/rewards/discount-redemptions/redeem/', data)
export const markDiscountAsUsed = (discountRedemptionId) => 
  api.post(`/rewards/discount-redemptions/${discountRedemptionId}/mark_used/`)

// Medicine Reward API
export const getMedicineRewards = () => api.get('/rewards/medicine/')
export const getAvailableMedicines = () => api.get('/rewards/medicine/available/')
export const getMedicineRedemptions = () => api.get('/rewards/medicine-redemptions/')
export const redeemMedicineReward = (data) => api.post('/rewards/medicine-redemptions/redeem/', data)

// AI Health API
export const chatWithAI = (message) => api.post('/ai-health/chat/', { message })
export const analyzeReport = (data) => api.post('/ai-health/analyze_report/', data)
export const analyzeBloodReportImage = (imageFile) => {
  const formData = new FormData()
  formData.append('image', imageFile)
  return api.post('/ai-health/analyze_image/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export default api

