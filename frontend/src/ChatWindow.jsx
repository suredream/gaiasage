import React, { useState, useRef, useEffect } from 'react'
import './ChatWindow.css'

function ChatWindow() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setIsLoading(true)

    // Add user message to chat
    const newUserMessage = { role: 'user', content: userMessage }
    setMessages((prev) => [...prev, newUserMessage])

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      })

      if (!response.ok) {
        // Try to get error details from response
        let errorDetail = `HTTP error! status: ${response.status}`
        try {
          const errorData = await response.json()
          if (errorData.detail) {
            errorDetail = errorData.detail
          }
        } catch (e) {
          // If response is not JSON, use status text
          errorDetail = response.statusText || errorDetail
        }
        throw new Error(errorDetail)
      }

      const data = await response.json()
      const assistantMessage = { role: 'assistant', content: data.response }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      // Show detailed error in development, generic message in production
      const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      const errorContent = isDevelopment
        ? `Error: ${error.message}`
        : 'Sorry, I encountered an error. Please try again.'
      const errorMessage = {
        role: 'assistant',
        content: errorContent,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h1>GaiaSage</h1>
        <p className="subtitle">Geospatial Analysis Co-pilot</p>
      </div>
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>Welcome to GaiaSage! I can help you with geospatial analysis tasks.</p>
            <p className="example">Try asking: "Conduct deforestation analysis in Borneo"</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <span className="loading">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-input-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about geospatial analysis..."
          disabled={isLoading}
          className="chat-input"
        />
        <button type="submit" disabled={isLoading || !input.trim()} className="send-button">
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow

