// frontend/src/utils/api.js
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export async function askQuestion(question, mode="explain", k=3) {
  const resp = await axios.post(`${API_BASE}/chat`, { question, mode, k });
  return resp.data;
}
