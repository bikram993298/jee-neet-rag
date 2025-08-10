// frontend/src/components/MathRenderer.jsx
import React, { useEffect, useRef } from "react";

export default function MathRenderer({ text }){
  const ref = useRef();
  useEffect(() => {
    // Use MathJax if available
    if (window.MathJax) {
      window.MathJax.typesetPromise([ref.current]);
    }
  }, [text]);

  return <div ref={ref} dangerouslySetInnerHTML={{ __html: text.replace(/\n/g, "<br/>") }} />;
}
