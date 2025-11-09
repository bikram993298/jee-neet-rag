import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

export default function Message({ role, text }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3 px-2`}>
      <div
        className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed shadow-md transition-all break-words ${
          isUser
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-gray-100 text-gray-900 border border-gray-300 rounded-bl-none"
        }`}
      >
        {isUser ? (
          // User message (plain)
          <div className="whitespace-pre-wrap">{text}</div>
        ) : (
          // Bot message (render markdown + math)
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              p: ({ node, ...props }) => <p className="mb-2" {...props} />,
              strong: ({ node, ...props }) => (
                <strong className="font-semibold text-gray-800" {...props} />
              ),
              code: ({ node, inline, className, children, ...props }) =>
                inline ? (
                  <code
                    className="bg-gray-200 px-1 rounded text-sm text-gray-800"
                    {...props}
                  >
                    {children}
                  </code>
                ) : (
                  <pre className="bg-gray-900 text-gray-100 p-3 rounded-xl overflow-x-auto text-sm">
                    <code>{children}</code>
                  </pre>
                ),
              h1: ({ node, ...props }) => (
                <h1 className="text-lg font-bold mb-2" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-base font-semibold mb-1" {...props} />
              ),
              li: ({ node, ...props }) => (
                <li className="ml-5 list-disc" {...props} />
              ),
            }}
          >
            {text}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}
