import React, { useEffect, useRef } from 'react'
import { MathJax, MathJaxContext } from 'better-react-mathjax'

export default function Message({ role, text }) {
  const isUser = role === 'user'
  const containerStyle = {
    display: 'flex',
    justifyContent: isUser ? 'flex-end' : 'flex-start',
    marginBottom: 8
  }
  const bubbleStyle = {
    background: isUser ? '#DCF8C6' : '#F1F1F1',
    padding: 10,
    borderRadius: 8,
    maxWidth: '80%',
    whiteSpace: 'pre-wrap'
  }

  // Use MathJax context to render math expressions inside message text.
  // Note: We use simple inline $$...$$ or \(..\) notation from the LLM outputs.
  return (
    <div style={containerStyle}>
      <div style={bubbleStyle}>
        <MathJaxContext>
          <MathJax dynamic>
            <div style={{ whiteSpace: 'pre-wrap' }}>{text}</div>
          </MathJax>
        </MathJaxContext>
      </div>
    </div>
  )
}
