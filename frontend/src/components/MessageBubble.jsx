// frontend/src/components/MessageBubble.jsx
import React, { useEffect } from "react";
import MathRenderer from "./MathRenderer";

export default function MessageBubble({ msg }){
  const className = msg.sender === "user" ? "bubble user" : "bubble bot";
  return (
    <div className={className}>
      <MathRenderer text={msg.text} />
    </div>
  );
}
