import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaFileAlt } from 'react-icons/fa'

const LegalPrivacy = () => {
  const navigate = useNavigate()
  const [selectedTab, setSelectedTab] = useState('terms')

  const termsContent = `
Terms and Conditions

1. Acceptance of Terms
By using BloodHub, you agree to these terms and conditions. If you do not agree, please do not use our service.

2. User Responsibilities
- You must be at least 18 years old to use this service
- You are responsible for maintaining the confidentiality of your account
- You must provide accurate information during registration
- You are responsible for all activities under your account

3. Blood Donation Guidelines
- Donors must meet health and eligibility criteria
- False information about health status may result in account suspension
- BloodHub is not responsible for adverse reactions to donation
- Always consult with medical professionals before donating

4. Limitation of Liability
BloodHub is provided "as-is" without warranties. We are not liable for:
- Damages from use or inability to use the service
- Loss of data or information
- Medical complications from donation

5. Changes to Terms
We reserve the right to modify these terms at any time. Changes will be effective immediately upon posting.

6. Termination
We may terminate your account for violations of these terms.
  `

  const privacyContent = `
Privacy Policy

1. Information We Collect
- Personal information (name, email, phone, date of birth)
- Health information (blood type, medical history, allergies)
- Payment information (processed securely)
- Usage data and analytics

2. How We Use Your Information
- To provide and improve our services
- To process donations and payments
- To send notifications and updates
- To comply with legal requirements
- For research and analytics

3. Data Protection
- We use encryption to protect sensitive data
- We follow GDPR and local privacy laws
- We do not sell your data to third parties
- You can request data deletion anytime

4. Cookies
We use cookies to:
- Remember your preferences
- Improve user experience
- Track analytics
- Personalize content

5. Third-Party Sharing
We may share information with:
- Blood banks and hospitals (for donation purposes)
- Payment processors (for transactions)
- Law enforcement (when legally required)

6. Your Rights
You have the right to:
- Access your personal data
- Request corrections
- Request deletion
- Opt out of marketing emails
- Port your data to another service

7. Changes to Privacy Policy
We may update this policy. Continued use means you accept the changes.

8. Contact Us
For privacy concerns: privacy@bloodhub.com
  `

  const cookieContent = `
Cookie Policy

1. What Are Cookies?
Cookies are small files stored on your device to remember preferences and track usage.

2. Types of Cookies We Use
- Essential: Required for basic functionality
- Performance: Track how you use our site
- Functional: Remember your preferences
- Targeting: Show relevant advertisements

3. Managing Cookies
You can control cookies through your browser settings:
- Chrome: Settings > Privacy and security > Cookies
- Firefox: Preferences > Privacy > Cookies
- Safari: Preferences > Privacy > Manage Website Data

4. Cookie List
- Session ID: Maintains your login session
- User Preferences: Language, theme settings
- Analytics: Google Analytics for traffic analysis
- Marketing: Facebook, Google tracking

5. Third-Party Cookies
Third-party services (Google, Facebook) may set their own cookies.
See their privacy policies for details.
  `

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-10">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <button
          onClick={() => navigate('/settings')}
          className="flex items-center space-x-2 text-primary hover:text-primary-dark mb-4"
        >
          <FaArrowLeft />
          <span>Back to Settings</span>
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Legal & Privacy</h1>
        <p className="text-gray-600 mb-8">Important information about our policies</p>

        {/* Tabs */}
        <div className="flex space-x-4 mb-8 bg-white rounded-lg shadow-md p-2">
          <button
            onClick={() => setSelectedTab('terms')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              selectedTab === 'terms'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            Terms & Conditions
          </button>
          <button
            onClick={() => setSelectedTab('privacy')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              selectedTab === 'privacy'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            Privacy Policy
          </button>
          <button
            onClick={() => setSelectedTab('cookies')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              selectedTab === 'cookies'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            Cookie Policy
          </button>
        </div>

        {/* Content */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center space-x-3 mb-6">
            <FaFileAlt className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-semibold text-gray-900">
              {selectedTab === 'terms' && 'Terms & Conditions'}
              {selectedTab === 'privacy' && 'Privacy Policy'}
              {selectedTab === 'cookies' && 'Cookie Policy'}
            </h2>
          </div>

          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-line text-gray-700 leading-relaxed">
              {selectedTab === 'terms' && termsContent}
              {selectedTab === 'privacy' && privacyContent}
              {selectedTab === 'cookies' && cookieContent}
            </div>
          </div>

          {/* Acceptance Checkbox */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                defaultChecked
                className="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">
                I have read and accept these terms and policies
              </span>
            </label>
          </div>

          {/* Download Button */}
          <button className="mt-6 flex items-center space-x-2 bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-dark transition-all">
            <FaFileAlt />
            <span>Download PDF</span>
          </button>
        </div>

        {/* Contact for Concerns */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-2">Questions About Our Policies?</h3>
          <p className="text-blue-800 text-sm">
            Contact our legal team at{' '}
            <a href="mailto:legal@bloodhub.com" className="font-medium underline">
              legal@bloodhub.com
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}

export default LegalPrivacy
