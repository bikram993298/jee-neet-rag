// frontend/src/App.jsx
import React from "react";
import ChatBox from "./components/ChatBox";

export default function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Hybrid JEE/NEET Tutor</h1>
      </header>
      <main>
        <ChatBox />
      </main>
    </div>
  );
}
