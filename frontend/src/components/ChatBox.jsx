import React, { useState, useRef, useEffect } from 'react'
import Message from './Message'
import Loader from './Loader'

export default function ChatBox() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function sendMessage() {
    if (!input.trim()) return

    const userMsg = { role: 'user', text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}/api/chat`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: userMsg.text }),
        }
      )

      if (!res.ok) throw new Error(`Server error: ${res.status}`)

      const data = await res.json()
      const botMsg = { role: 'assistant', text: data.answer }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: '⚠️ Error: ' + err.message },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div style={{ minHeight: 300, maxHeight: '65vh', overflowY: 'auto', padding: 12, border: '1px solid #eee', borderRadius: 8, background: '#fafafa', marginBottom: 12 }}>
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}
        {loading && <Loader />}
        <div ref={chatEndRef} />
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your JEE/NEET question..."
          style={{ flex: 1, padding: 8, borderRadius: 8, border: '1px solid #ddd' }}
          rows={2}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          style={{ padding: '8px 12px', borderRadius: 8, background: '#2563eb', color: '#fff', border: 'none' }}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
