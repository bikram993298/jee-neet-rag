import React, { useState, useRef, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { LogOut } from "lucide-react";
import Message from "./Message";
import Loader from "./Loader";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  const { user, logout } = useAuth();

  // Auto-scroll when new messages appear
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // =====================================================
  // Send Message Handler
  // =====================================================
  async function sendMessage() {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    const newMessages = [...messages, userMsg]; // full conversation history

    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      // ✅ Send updated history with auth token
      const res = await fetch(`${import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${user?.accessToken}`,
        },
        body: JSON.stringify({ messages: newMessages }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const data = await res.json();

      const botMsg = {
        role: "assistant",
        text: data.answer || "No response received.",
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "⚠️ Error: " + err.message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // Keyboard Shortcut: Send on Enter
  // =====================================================
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // =====================================================
  // UI Layout
  // =====================================================
  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 bg-gray-900 text-white rounded-2xl shadow-lg border border-gray-700">
      {/* Header with User Info */}
      <div className="flex justify-between items-center mb-4 pb-4 border-b border-gray-700">
        <div>
          <h2 className="text-lg font-semibold">{user?.full_name}</h2>
          <p className="text-xs text-gray-400">{user?.email}</p>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-800 rounded-xl space-y-3 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-900">
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}
        {loading && <Loader />}
        <div ref={chatEndRef} />
      </div>

      {/* Input Section */}
      <div className="flex items-end gap-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your JEE/NEET question..."
          rows={2}
          className="flex-1 resize-none rounded-lg p-3 bg-gray-800 border border-gray-600 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className={`px-5 py-2.5 rounded-lg font-semibold transition ${
            loading
              ? "bg-blue-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 active:scale-95"
          }`}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}
