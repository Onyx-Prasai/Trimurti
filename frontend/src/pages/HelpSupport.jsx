import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaQuestionCircle, FaEnvelope, FaPhone } from 'react-icons/fa'

const HelpSupport = () => {
  const navigate = useNavigate()
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [showContactForm, setShowContactForm] = useState(false)
  const [contactData, setContactData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  })

  const faqs = [
    {
      category: 'General',
      questions: [
        { q: 'How do I create an account?', a: 'Click on Register and fill in your details.' },
        { q: 'How do I reset my password?', a: 'Click Forgot Password on the login page.' },
        { q: 'Is my data secure?', a: 'Yes, we use encryption and follow security best practices.' },
      ],
    },
    {
      category: 'Blood Donation',
      questions: [
        { q: 'Who can donate blood?', a: 'Generally, healthy individuals aged 18-65 with minimum weight of 45kg.' },
        { q: 'How often can I donate?', a: 'Usually every 3-6 months depending on the type of donation.' },
        { q: 'What are the eligibility criteria?', a: 'Check our detailed eligibility guidelines on the donation page.' },
      ],
    },
    {
      category: 'Payment',
      questions: [
        { q: 'What payment methods do you accept?', a: 'We accept credit cards, debit cards, and digital wallets.' },
        { q: 'Is it safe to use my card?', a: 'Yes, all transactions are encrypted and secure.' },
        { q: 'Can I get a refund?', a: 'Yes, refunds are processed within 5-7 business days.' },
      ],
    },
  ]

  const handleContactChange = (e) => {
    const { name, value } = e.target
    setContactData(prev => ({ ...prev, [name]: value }))
  }

  const handleContactSubmit = () => {
    if (!contactData.name || !contactData.email || !contactData.subject || !contactData.message) {
      alert('Please fill in all fields')
      return
    }
    alert('Your message has been sent! We will get back to you soon.')
    setContactData({ name: '', email: '', subject: '', message: '' })
    setShowContactForm(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      <div className="max-w-3xl mx-auto px-4">
        {/* Header */}
        <button
          onClick={() => navigate('/settings')}
          className="flex items-center space-x-2 text-primary hover:text-primary-dark mb-4"
        >
          <FaArrowLeft />
          <span>Back to Settings</span>
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Help & Support</h1>
        <p className="text-gray-600 mb-8">Find answers to your questions</p>

        {/* Contact Support Button */}
        <div className="mb-8 flex space-x-4">
          <button
            onClick={() => setShowContactForm(!showContactForm)}
            className="flex items-center space-x-2 bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-all"
          >
            <FaEnvelope />
            <span>Contact Support</span>
          </button>
          <a
            href="tel:+977-1234567890"
            className="flex items-center space-x-2 bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-all"
          >
            <FaPhone />
            <span>Call Us</span>
          </a>
        </div>

        {/* Contact Form */}
        {showContactForm && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Send us a Message</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  name="name"
                  value={contactData.name}
                  onChange={handleContactChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  name="email"
                  value={contactData.email}
                  onChange={handleContactChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                <input
                  type="text"
                  name="subject"
                  value={contactData.subject}
                  onChange={handleContactChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Message</label>
                <textarea
                  name="message"
                  value={contactData.message}
                  onChange={handleContactChange}
                  rows="5"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={handleContactSubmit}
                  className="flex-1 bg-primary text-white py-2 px-4 rounded-lg font-medium hover:bg-primary-dark transition-all"
                >
                  Send Message
                </button>
                <button
                  onClick={() => setShowContactForm(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-all"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* FAQ Section */}
        <div className="space-y-6">
          {faqs.map((category) => (
            <div key={category.category} className="bg-white rounded-lg shadow-md overflow-hidden">
              <button
                onClick={() => setSelectedCategory(selectedCategory === category.category ? null : category.category)}
                className="w-full flex items-center justify-between p-6 hover:bg-gray-50 transition-all"
              >
                <div className="flex items-center space-x-3">
                  <FaQuestionCircle className="w-5 h-5 text-primary" />
                  <h2 className="text-lg font-semibold text-gray-900">{category.category}</h2>
                </div>
                <span className="text-2xl text-gray-500">
                  {selectedCategory === category.category ? '−' : '+'}
                </span>
              </button>

              {selectedCategory === category.category && (
                <div className="border-t border-gray-200 p-6 bg-gray-50 space-y-4">
                  {category.questions.map((item, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg">
                      <p className="font-medium text-gray-900 mb-2">{item.q}</p>
                      <p className="text-gray-600">{item.a}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default HelpSupport
