import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaRobot, FaPaperclip, FaSpinner } from 'react-icons/fa'
import { chatWithAI, analyzeReport } from '../utils/api'

const AIHealth = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI Health Assistant. I can help you with blood donation questions, health tips, and analyze medical reports. How can I assist you today?',
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [reportText, setReportText] = useState('')
  const [reportType, setReportType] = useState('general')
  const [analyzing, setAnalyzing] = useState(false)

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    const userInput = input
    setMessages((prevMessages) => [...prevMessages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await chatWithAI(userInput)
      console.log('API Response:', response)
      
      if (response.data && response.data.response) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: 'assistant', content: response.data.response },
        ])
      } else {
        throw new Error('Invalid response format from API')
      }
    } catch (error) {
      console.error('Error chatting with AI:', error)
      console.error('Error details:', error.response?.data || error.message)
      
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzeReport = async () => {
    if (!reportText.trim() || analyzing) return

    setAnalyzing(true)
    try {
      const response = await analyzeReport({
        report_text: reportText,
        report_type: reportType,
      })
      console.log('Report Analysis Response:', response)
      
      if (response.data && response.data.analysis) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            role: 'assistant',
            content: `Report Analysis:\n\n${response.data.analysis}`,
          },
        ])
        setReportText('')
      } else {
        throw new Error('Invalid response format from API')
      }
    } catch (error) {
      console.error('Error analyzing report:', error)
      console.error('Error details:', error.response?.data || error.message)
      
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error analyzing your report. Please try again.',
        },
      ])
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-text mb-8 text-center flex items-center justify-center"
        >
          <FaRobot className="mr-3 text-primary" />
          AI Health Assistant
        </motion.h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl shadow-lg h-[600px] flex flex-col"
            >
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((message, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl p-4 ${
                        message.role === 'user'
                          ? 'bg-primary text-white'
                          : 'bg-gray-100 text-text'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                  </motion.div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-2xl p-4">
                      <FaSpinner className="animate-spin text-primary" />
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="p-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Ask me anything about health..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                    disabled={loading}
                  />
                  <button
                    type="button"
                    onClick={() => {
                      if (input.trim() && !loading) {
                        handleSend()
                      }
                    }}
                    className="bg-primary text-white px-6 py-2 rounded-xl hover:bg-red-600 transition-all cursor-pointer active:opacity-80"
                  >
                    Send
                  </button>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Report Analysis */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl p-6 shadow-lg sticky top-24"
            >
              <h3 className="text-xl font-semibold text-text mb-4 flex items-center">
                <FaPaperclip className="mr-2 text-primary" />
                Analyze Medical Report
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-text mb-2">
                    Report Type
                  </label>
                  <select
                    value={reportType}
                    onChange={(e) => setReportType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option value="general">General Health</option>
                    <option value="blood_test">Blood Test</option>
                    <option value="hemoglobin">Hemoglobin</option>
                    <option value="iron">Iron Levels</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">
                    Report Content
                  </label>
                  <textarea
                    value={reportText}
                    onChange={(e) => setReportText(e.target.value)}
                    placeholder="Paste your report text here..."
                    rows="8"
                    className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => {
                    console.log('Button clicked. reportText:', reportText, 'analyzing:', analyzing)
                    if (reportText.trim() && !analyzing) {
                      console.log('Calling handleAnalyzeReport with:', reportText, reportType)
                      handleAnalyzeReport()
                    } else {
                      console.log('Condition not met: reportText.trim()=', reportText.trim(), '!analyzing=', !analyzing)
                    }
                  }}
                  className="w-full bg-primary text-white px-4 py-2 rounded-xl hover:bg-red-600 transition-all flex items-center justify-center space-x-2 cursor-pointer active:opacity-80"
                >
                  {analyzing ? (
                    <>
                      <FaSpinner className="animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <FaPaperclip />
                      <span>Analyze Report</span>
                    </>
                  )}
                </button>
                <p className="text-xs text-text opacity-70">
                  The AI will analyze your report and provide specific Nepalese dietary recommendations (iron-rich foods like spinach, lentils, etc.)
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AIHealth

