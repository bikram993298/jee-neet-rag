// frontend/src/components/ChatBox.jsx
import React, { useState } from "react";
import { askQuestion } from "../utils/api";
import MessageBubble from "./MessageBubble";

export default function ChatBox(){
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(){
    if(!text.trim()) return;
    const userMsg = { sender: "user", text };
    setMessages(prev => [...prev, userMsg]);
    setText("");
    setLoading(true);
    try{
      const res = await askQuestion(text, "explain", 3);
      setMessages(prev => [...prev, userMsg, { sender: "bot", text: res.answer }]);
    }catch(err){
      setMessages(prev => [...prev, { sender: "bot", text: "Error: " + (err.message || "Request failed") }]);
    }finally{
      setLoading(false);
    }
  }

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((m, i) => <MessageBubble key={i} msg={m} />)}
      </div>
      <div className="composer">
        <textarea value={text} onChange={(e) => setText(e.target.value)} rows={2}/>
        <button onClick={send} disabled={loading}>{loading ? "Thinking..." : "Send"}</button>
      </div>
    </div>
  );
}
