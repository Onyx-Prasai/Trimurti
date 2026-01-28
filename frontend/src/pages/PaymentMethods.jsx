import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaCreditCard, FaTrash } from 'react-icons/fa'

const PaymentMethods = () => {
  const navigate = useNavigate()
  const [paymentMethods, setPaymentMethods] = useState([
    { id: 1, type: 'credit', last4: '4242', brand: 'Visa', expiry: '12/25' },
    { id: 2, type: 'debit', last4: '5555', brand: 'Mastercard', expiry: '08/24' },
  ])
  const [showAddForm, setShowAddForm] = useState(false)
  const [newPayment, setNewPayment] = useState({
    cardNumber: '',
    cardName: '',
    expiry: '',
    cvv: '',
  })

  const handleAddPayment = () => {
    if (!newPayment.cardNumber || !newPayment.cardName || !newPayment.expiry || !newPayment.cvv) {
      alert('Please fill in all fields')
      return
    }
    const last4 = newPayment.cardNumber.slice(-4)
    setPaymentMethods([
      ...paymentMethods,
      {
        id: Date.now(),
        type: 'credit',
        last4: last4,
        brand: 'Card',
        expiry: newPayment.expiry,
      },
    ])
    setNewPayment({ cardNumber: '', cardName: '', expiry: '', cvv: '' })
    setShowAddForm(false)
    alert('Payment method added successfully!')
  }

  const handleDeletePayment = (id) => {
    setPaymentMethods(paymentMethods.filter(m => m.id !== id))
    alert('Payment method removed')
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <button
          onClick={() => navigate('/settings')}
          className="flex items-center space-x-2 text-primary hover:text-primary-dark mb-4"
        >
          <FaArrowLeft />
          <span>Back to Settings</span>
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Payment Methods</h1>
        <p className="text-gray-600 mb-8">Manage your payment information</p>

        {/* Payment Methods List */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Saved Cards</h2>
          <div className="space-y-3">
            {paymentMethods.map((method) => (
              <div key={method.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center space-x-4">
                  <FaCreditCard className="w-6 h-6 text-primary" />
                  <div>
                    <p className="font-medium text-gray-900">
                      {method.brand} •••• {method.last4}
                    </p>
                    <p className="text-sm text-gray-600">Expires {method.expiry}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeletePayment(method.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-all"
                >
                  <FaTrash className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Add Payment Method */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Card</h2>

          {!showAddForm ? (
            <button
              onClick={() => setShowAddForm(true)}
              className="w-full bg-primary text-white py-3 px-4 rounded-lg font-semibold hover:bg-primary-dark transition-all flex items-center justify-center space-x-2"
            >
              <span>+ Add Payment Method</span>
            </button>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Card Number</label>
                <input
                  type="text"
                  placeholder="1234 5678 9012 3456"
                  value={newPayment.cardNumber}
                  onChange={(e) => setNewPayment({ ...newPayment, cardNumber: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  maxLength="16"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cardholder Name</label>
                <input
                  type="text"
                  placeholder="John Doe"
                  value={newPayment.cardName}
                  onChange={(e) => setNewPayment({ ...newPayment, cardName: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Expiry Date</label>
                  <input
                    type="text"
                    placeholder="MM/YY"
                    value={newPayment.expiry}
                    onChange={(e) => setNewPayment({ ...newPayment, expiry: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    maxLength="5"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">CVV</label>
                  <input
                    type="password"
                    placeholder="123"
                    value={newPayment.cvv}
                    onChange={(e) => setNewPayment({ ...newPayment, cvv: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    maxLength="4"
                  />
                </div>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleAddPayment}
                  className="flex-1 bg-primary text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-dark transition-all"
                >
                  Add Card
                </button>
                <button
                  onClick={() => {
                    setShowAddForm(false)
                    setNewPayment({ cardNumber: '', cardName: '', expiry: '', cvv: '' })
                  }}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-all"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PaymentMethods
