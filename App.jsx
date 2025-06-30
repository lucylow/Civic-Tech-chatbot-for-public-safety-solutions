import { useState, useEffect, useRef } from 'react'
import { Send, AlertTriangle, Phone, MapPin, Shield } from 'lucide-react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Send initial greeting
    handleQuickAction('greeting')
  }, [])

  const sendMessage = async (message) => {
    if (!message.trim()) return

    const userMessage = { type: 'user', content: message, timestamp: new Date() }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: sessionId })
      })

      const data = await response.json()
      setSessionId(data.session_id)

      const botMessage = {
        type: 'bot',
        content: data.response.message,
        quickActions: data.response.quick_actions,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(inputMessage)
    setInputMessage('')
  }

  const handleQuickAction = (action) => {
    const actionMessages = {
      'greeting': 'Hello',
      'emergency': 'I need emergency help',
      'report_hazard': 'I want to report a hazard',
      'view_alerts': 'Show me current alerts',
      'safety_info': 'I need safety information',
      'call_911': 'Call 911 immediately',
      'emergency_contacts': 'Show emergency contacts',
      'safety_tips': 'Give me safety tips'
    }
    
    const message = actionMessages[action] || action
    sendMessage(message)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">SafeIndy AI</h1>
              <p className="text-sm text-gray-600">24/7 Public Safety Assistant for Indianapolis</p>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
          
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.type === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-900'
                }`}>
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  
                  {/* Quick Actions */}
                  {message.quickActions && (
                    <div className="mt-3 space-y-2">
                      {message.quickActions.map((action, actionIndex) => (
                        <button
                          key={actionIndex}
                          onClick={() => handleQuickAction(action.action)}
                          className="block w-full text-left px-3 py-2 text-sm bg-white text-gray-700 rounded border hover:bg-gray-50 transition-colors"
                        >
                          {action.text}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span>SafeIndy AI is typing...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            <form onSubmit={handleSubmit} className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message or describe your safety concern..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send className="h-5 w-5" />
              </button>
            </form>
          </div>
        </div>

        {/* Emergency Banner */}
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <div className="flex-1">
              <p className="text-sm text-red-800">
                <strong>Emergency?</strong> For life-threatening emergencies, call 911 immediately.
              </p>
            </div>
            <button
              onClick={() => window.open('tel:911')}
              className="flex items-center space-x-1 px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 transition-colors"
            >
              <Phone className="h-4 w-4" />
              <span>Call 911</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

