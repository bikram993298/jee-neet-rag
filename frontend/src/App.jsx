import React from 'react'
import ChatBox from './components/ChatBox'

export default function App() {
  return (
    <div style={{ minHeight: '100vh', padding: 24, background: '#f8fafc' }}>
      <div style={{ maxWidth: 900, margin: '0 auto', background: '#fff', padding: 20, borderRadius: 12, boxShadow: '0 6px 18px rgba(0,0,0,0.06)' }}>
        <h1 style={{ fontSize: 22, marginBottom: 12 }}>JEE/NEET Tutor (RAG only)</h1>
        <ChatBox />
      </div>
    </div>
  )
}
