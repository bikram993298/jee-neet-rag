
# 📚 Hybrid JEE/NEET Tutor — AI-Powered Exam Prep with RAG + LoRA

A full-stack AI tutor for **JEE** and **NEET** exam preparation using **Retrieval-Augmented Generation (RAG)** over NCERT textbooks, past papers, and benchmark datasets — combined with a **hybrid LLM setup**:  
- **Local open-source model** for cost-efficient inference  
- **GPT-4 fallback** for complex queries  

Built with **FastAPI**, **LangChain**, **FAISS**, and **React**.

---

## 🚀 Features

- **RAG Pipeline** — Chunk, embed, and store NCERT + past paper content in FAISS.
- **Hybrid LLM Routing** — Offline inference (Ollama / GPT4All) with GPT-4 fallback.
- **Exam-ready Output** — Step-by-step solutions, MCQs, and concept explanations.
- **Frontend** — Chat-style React UI with MathJax for LaTeX equations.
- **Dataset Integration** — Supports [Reja1/jee-neet-benchmark](https://huggingface.co/datasets/Reja1/jee-neet-benchmark) for model evaluation & fine-tuning.
- **Deployable** — Works locally or in the cloud (Vercel + Render).

---

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, LangChain, FAISS, Sentence-Transformers, OpenAI API, pytesseract (OCR)  
**Frontend:** React, MathJax, TailwindCSS  
**Models:** Local (LLaMA, Mistral, GPT4All) + GPT-4 (fallback)  
**Dataset:** NCERT PDFs + [Hugging Face Dataset](https://huggingface.co/datasets/Reja1/jee-neet-benchmark)

---

## 📂 Project Structure

```

.
├── README.md
├── .env.example
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── admin.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   ├── ocr\_utils.py
│   │   ├── merge\_embeddings.py
│   ├── models/
│   │   ├── local\_llm.py
│   │   ├── openai\_llm.py
│   ├── requirements.txt
│   ├── config.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── Loader.jsx
│   │   ├── utils/mathjax.js
│   ├── package.json
│   ├── vite.config.js
│
├── data/
│   ├── ncert/
│   ├── jee\_papers/
│   ├── neet\_papers/
│   ├── embeddings/
│
└── scripts/
├── fine\_tune\_lora\_colab.ipynb

````

---

## ⚡ Quickstart

### 1️⃣ Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
````

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3️⃣ RAG Indexing

```bash
cd backend
python rag/ingest.py --source data/ncert
python rag/ingest.py --source data/jee_papers
python rag/merge_embeddings.py  # merge NCERT + JEE/NEET
```

---

## 🔍 Using the API

* **Chat:** `POST /api/chat`

  ```json
  {
    "query": "Explain the Bohr model for hydrogen atom."
  }
  ```
* **Reindex:** `POST /api/admin/reindex`

---

## 📦 Dataset

We integrate [Reja1/jee-neet-benchmark](https://huggingface.co/datasets/Reja1/jee-neet-benchmark):

* **JEE Advanced 2024**: 102 questions
* **NEET 2024 (Code T3)**: 200 questions
* **NEET 2025 (Code 45)**: 180 questions

Each question is stored as `.png` with metadata (exam, subject, type, answer).

---

## 🧪 Fine-tuning LLaMA 2 with LoRA (Google Colab)

We provide `scripts/fine_tune_lora_colab.ipynb` with:

1. OCR preprocessing of images → text
2. Tokenization (LLaMA 2 tokenizer)
3. LoRA config for low-cost fine-tuning
4. Model training and saving
5. Integration back into the RAG pipeline

---

## 📌 Notes & Next Steps

1. **Secrets**: Populate `.env` from `.env.example`. Keep secrets out of VCS.
2. **FAISS Merge**: `merge_embeddings.py` merges NCERT + JEE/NEET embeddings.
3. **OCR Tuning**: `ocr_utils.py` includes image preprocessing for better accuracy.
4. **Local LLM**: `local_llm.py` supports Ollama & GPT4All — adapt to your runtime.
5. **Evaluation**: Scripts in `scripts/` test accuracy on the HF dataset.
6. **Testing**: Unit tests available for ingestion, retrieval, and inference.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

