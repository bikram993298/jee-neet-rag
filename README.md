👉 `jee-neet-rag` — your **AI-Powered JEE/NEET Tutor using RAG + Google Gemini**.

This version includes everything:

* Overview of what the project *does*
* Detailed local setup (backend + frontend)
* API explanation
* RAG architecture diagram (in text form)
* Contribution guide
* Deployment & environment setup
* And best practices

You can copy this directly into your `jee-neet-rag/README.md` file 👇

---

# 📚 JEE/NEET AI Tutor — RAG + Google Gemini

> 🧠 An AI-powered tutoring platform built using **Retrieval-Augmented Generation (RAG)** and **Google Gemini API** to help students prepare for **JEE** and **NEET** by answering questions using real NCERT and past paper data.

---

## 🚀 Overview

**JEE-NEET-RAG** is a full-stack project that combines **AI + Search + Education**.
It lets students ask questions (theory or numerical) from their syllabus, and the AI answers them with **step-by-step reasoning** based on **NCERT content** and **past paper data**.

The backend uses:

* **FastAPI** + **FAISS** + **Sentence Transformers** for the RAG pipeline.
  The frontend uses:
* **React**, **TailwindCSS**, and **Framer Motion** for a modern chat interface.

The AI model is:

* **Google Gemini 1.5 Flash** — free, fast, and intelligent.

---

## 🧠 What the Project Does

Here’s how the system works behind the scenes 👇

### 🧩 Retrieval-Augmented Generation (RAG) Pipeline

```
1️⃣ User asks a question (e.g., "Explain Bohr’s model of atom")
2️⃣ The system retrieves the most relevant text chunks from NCERT using FAISS
3️⃣ Combines those chunks into a contextual prompt
4️⃣ Sends the context + question to the Gemini model
5️⃣ Gemini generates a step-by-step, syllabus-accurate explanation
6️⃣ Response is displayed beautifully on the frontend
```

This ensures **accurate, syllabus-based** answers instead of random LLM responses.

---

## ⚙️ Features

✅ **RAG Pipeline** — retrieves context from NCERT and past paper data
✅ **AI Tutor Chatbot** — Chat-style interface for question-answering
✅ **Gemini API** — Uses Google’s free Gemini API (no OpenAI key required)
✅ **FAISS Vector DB** — Efficient and local semantic search
✅ **React UI** — Modern, mobile-friendly chat design
✅ **Environment-based config** — Works locally or in production easily
✅ **Easy Dataset Expansion** — Just drop `.txt` files to add new chapters

---

## 🧰 Tech Stack

| Layer          | Technology                                          |
| -------------- | --------------------------------------------------- |
| **Frontend**   | React, TailwindCSS, Framer Motion, Lucide Icons     |
| **Backend**    | FastAPI, Uvicorn, Python 3.10+                      |
| **AI Model**   | Google Gemini 1.5 Flash (Free via Google AI Studio) |
| **Vector DB**  | FAISS                                               |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`)          |
| **Data**       | NCERT + JEE/NEET past papers (as text files)        |

---

## 🛠️ Local Setup Guide

### 🧩 1️⃣ Clone the repository

```bash
git clone https://github.com/bikram993298/jee-neet-rag.git
cd jee-neet-rag
```

---

### 🧩 2️⃣ Backend Setup

#### Create a virtual environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # (on Windows)
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### `requirements.txt`

```text
fastapi
uvicorn[standard]
sentence-transformers
faiss-cpu
google-generativeai
python-dotenv
pydantic
tqdm
```

#### Create `.env` file inside `backend/`

```ini
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=models/gemini-2.5-pro
FAISS_INDEX_PATH=data/embeddings/faiss_index.idx
ID_MAP_PATH=data/embeddings/id_to_text.pkl
EMBEDDING_MODEL=all-MiniLM-L6-v2
HOST=0.0.0.0
PORT=8000
```

> 🎯 Get your free API key from:
> [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

### 🧩 3️⃣ Prepare Data for RAG

Create folders:

```
jee-neet-rag/data/ncert/
```

Add `.txt` files:

```
data/ncert/physics_ch1.txt
data/ncert/chemistry_ch1.txt
```

Each file should contain plain text (you can copy content from NCERT PDFs).

---

### 🧩 4️⃣ Generate FAISS Embeddings

Run:

```bash
python rag/ingest.py
```

You’ll see:

```
Embedding 120 chunks with all-MiniLM-L6-v2 ...
Building FAISS index...
Saving index -> data/embeddings/faiss_index.idx
Saving id->text map -> data/embeddings/id_to_text.pkl
Done.
```

---

### 🧩 5️⃣ Start Backend

Run from project root (`jee-neet-rag/`):

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

Now open the API docs:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🧩 6️⃣ Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install --legacy-peer-deps
npm install framer-motion lucide-react better-react-mathjax
npm run dev
```

Open in browser:
👉 [http://localhost:5173](http://localhost:5173)

---

## 📦 Folder Structure

```
jee-neet-rag/
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/chat.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── merge_embeddings.py
│   ├── models/
│   │   └── gemini_llm.py
│   └── config.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Message.jsx
│   │   │   └── Loader.jsx
│   ├── vite.config.js
│   └── package.json
├── data/ncert/
│   ├── physics_ch1.txt
│   ├── chemistry_ch1.txt
└── README.md
```

---

## 🌐 API Endpoints

### `/api/chat` → POST

**Description:** Accepts a query and returns a context-based AI-generated answer.

#### Example Request

```json
{
  "query": "Explain Bohr's model of hydrogen atom."
}
```

#### Example Response

```json
{
  "answer": "According to Bohr's model, electrons revolve in discrete orbits..."
}
```

---

## 🧠 RAG Flow Diagram (Text Form)

```
User Question
   ↓
Sentence Transformer → Embedding Vector
   ↓
FAISS → Retrieve top 5 relevant chunks
   ↓
Combine context + question → Prompt
   ↓
Gemini Model → Generate Answer
   ↓
Frontend → Display Chat Response
```

---

## ☁️ Deployment Guide

### 🟢 Deploy Backend (Render)

* Go to [https://render.com](https://render.com)
* Create a new **Web Service**
* Connect your GitHub repo
* Add Environment Variables:

  ```
  GEMINI_API_KEY=your_google_api_key_here
  GEMINI_MODEL=gemini-1.5-flash
  ```

### 🟣 Deploy Frontend (Vercel)

* Go to [https://vercel.com](https://vercel.com)
* Import the repo
* Add:

  ```
  VITE_API_URL=https://your-backend.onrender.com
  ```
* Deploy 🚀

---

## 🤝 Contributing

Contributions are welcome! 🎉
To contribute:

1. **Fork** the repository
2. **Create** a new branch

   ```bash
   git checkout -b feature/my-feature
   ```
3. **Commit** your changes

   ```bash
   git commit -m "Added new feature"
   ```
4. **Push** to your fork

   ```bash
   git push origin feature/my-feature
   ```
5. **Submit a Pull Request**

### 💡 Suggestions

* Improve RAG retrieval ranking
* Add support for image-based question answering (Gemini Vision)
* Enhance UI animations or add dark mode
* Add quiz/question generator using the RAG database

---

## 🧾 License

MIT License © 2025
Developed with ❤️ by **[Bikram Barman](https://github.com/bikram993298)**

---

## 🌟 Demo Preview (Example)

**Question:**

> “Explain Bohr’s model of the hydrogen atom.”

**Answer (AI):**

> According to Niels Bohr, electrons revolve around the nucleus in stable orbits.
> The angular momentum is quantized as
> ( mvr = n \frac{h}{2\pi} ).
> Energy levels are given by ( E_n = -13.6/n^2 \text{ eV} ).
> Transitions between levels emit or absorb photons.

---

