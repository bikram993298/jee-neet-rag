import React from "react";
import { MathJaxContext } from "better-react-mathjax";
import ChatBox from "./components/ChatBox";

const mathConfig = {
  loader: { load: ["input/tex", "output/chtml"] },
  tex: { inlineMath: [["$", "$"], ["\\(", "\\)"]] },
};

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
        JEE / NEET AI Assistant 🤖
      </h1>

      <MathJaxContext config={mathConfig}>
        <ChatBox />
      </MathJaxContext>

      <footer className="mt-6 text-gray-500 text-xs">
        Built with ❤️ by Bikram Barman
      </footer>
    </div>
  );
}
