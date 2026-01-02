# 🧠 CodeMind  
### Structural Code Intelligence with AST-Powered RAG

> **CodeMind is not a generic LLM wrapper.  
> It is a structural, code-aware RAG system that understands your codebase the way a senior engineer does.**

---

## 🚀 What is CodeMind?

**CodeMind** is an AI-powered assistant that enables natural-language querying over real-world codebases with **high precision and zero hallucination**.

Unlike standard RAG systems that treat code as plain text, CodeMind **preserves code structure**, reconstructs full logical units, and answers **only using verified code context**.

---

## 🔥 Why CodeMind is Different

### ❌ Typical Code RAG Systems
- Random token chunking  
- Broken functions & methods  
- Lost class context  
- Hallucinated logic  
- Poor scalability  

### ✅ CodeMind’s Structural RAG
CodeMind treats code as **structured data**, not text.

> **RAG is a data engineering problem — CodeMind solves it structurally.**

---

## 🧩 Core Capabilities

### 🧠 AST-Driven Code Parsing
Leverages Python’s native `ast` module to traverse syntax trees and extract:
- `ClassDef`
- `FunctionDef`
- `AsyncFunctionDef`
- Class methods
- Module-level code  

Parent-child relationships are preserved to enable **accurate contextual reconstruction**.

---

### 🧱 Semantic Code Chunking
- Code is chunked by **logical boundaries**, not token limits  
- Large functions are safely split  
- All splits remain symbol-linked for reconstruction  

---

### 🔁 Smart Reconstruction
- Split chunks are **reassembled before LLM inference**  
- The model always sees **complete functions or methods**  
- Eliminates partial-context hallucinations  

---

### 🏗️ Class-Aware Retrieval
- Class methods automatically attach their class headers  
- Missing headers are dynamically fetched  
- Ensures state and design context is preserved  

---

### 🎯 Symbol-Level Deduplication
- Results are grouped by `symbol`  
- Prevents duplicate fragments  
- One symbol → one coherent context block  

---

### 📦 Context Budget Enforcement
- Retrieved chunks are scored, sorted, and trimmed  
- Guarantees LLM context limits are respected  
- Works on large codebases  

---

## 🏗️ Architecture
<img width="1076" height="3630" alt="Untitled diagram-2026-01-02-155834" src="https://github.com/user-attachments/assets/68688416-7cab-4665-8595-5921c57df4e8" />

```
![flowchart TD
    A[User Codebase ZIP] --> B[AST Parsing]
    B --> C[Structural Code Chunks]
    C --> D[Embeddings]
    D --> E[Qdrant Vector DB]
    E --> F[Symbol-Aware Retrieval]
    F --> G[Chunk Reconstruction]
    G --> H["LLM Answer (Grounded)"]](flowchart.png)

    
```

🛠️ Tech Stack
Backend

Python 3.10+

FastAPI

Python AST

SentenceTransformers (nomic-embed-text-v1.5)

Qdrant

Frontend

Streamlit (intentionally minimal)

▶️ How to Run (CRITICAL)
Prerequisites

Python 3.10+

Docker (for Qdrant)

Git

1️⃣ Clone Repository
git clone https://github.com/your-username/CodeMind.git
cd CodeMind

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

5️⃣ Start Backend
uvicorn backend.main:app --reload

6️⃣ Start Frontend
streamlit run frontend/app.py

🖼️ Visual Proof

📸 Streamlit UI with complex query and reconstructed context

(Add screenshot here)

🧪 Example Queries

“What does the BankAccount class do?”

“Improve the withdrawal logic”

“Explain this module in simple terms”

“Where is error handling missing?”

“Refactor this function safely”

🧠 Technical Challenges Solved
Handling Async AST Nodes

Python’s AST represents async functions differently (AsyncFunctionDef).
Ensuring consistent extraction and reconstruction across sync/async functions required separate traversal logic and symbol normalization.

Class Context Reconstruction

Class headers and methods are indexed separately for retrieval quality, then re-attached at query time — balancing recall accuracy with context integrity.

Chunk Explosion Control

Symbol-level deduplication was required to prevent redundant chunks from overwhelming the LLM context window.

🚧 Roadmap

Multi-language support

Dependency graph reasoning

Call-chain tracing

IDE plugin

💼 Why This Matters to Clients

Faster onboarding

Zero hallucination risk

Private codebase safe

Scales to large repos

Designed like a production system

👨‍💻 Built By

Prithvi Raj
Focused on structural correctness, data engineering, and production-grade AI systems.

⭐ Final Thought

CodeMind doesn’t just retrieve code.
It reconstructs intent.
