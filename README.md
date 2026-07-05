<fsWrite>
<path>README.md</path>
<content># 🛢️ Production Engineering Assistant (PEA)

<div align="center">

**AI-Powered Troubleshooting & Decision Support System for Production Engineers**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://langchain.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live Demo](#) · [Report Bug](https://github.com/ifulxploit/production-engineering-assistant/issues) · [Request Feature](https://github.com/ifulxploit/production-engineering-assistant/issues)

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [System Flow](#-system-flow)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

**Production Engineering Assistant (PEA)** adalah aplikasi chatbot berbasis **Large Language Model (LLM)** yang dirancang khusus untuk membantu **Production Engineer**, **mahasiswa Teknik Perminyakan**, dan **Production Supervisor** dalam menganalisis dan troubleshooting masalah produksi sumur migas.

### 🎓 Background

Project ini dikembangkan sebagai **Final Project** untuk program **Maju Bareng AI - Hacktiv8**  
Kelas: *LLM-Based Tools and Gemini API Integration for Data Scientists*

### 💡 Why This Project?

Dalam industri minyak dan gas, Production Engineer sering menghadapi berbagai masalah kompleks seperti:
- Penurunan produksi sumur yang drastis
- Water cut yang naik tiba-tiba
- Masalah pada sistem artificial lift (ESP, Gas Lift)
- Flow assurance issues (hydrate, wax, scale)
- Dan banyak lagi...

PEA hadir sebagai **Decision Support Assistant** yang:
- ✅ Menganalisis masalah berdasarkan **Knowledge Base** (PDF teknis)
- ✅ Memberikan kemungkinan penyebab secara terstruktur
- ✅ Menjelaskan alasan engineering di balik setiap masalah
- ✅ Merekomendasikan tindakan troubleshooting yang tepat
- ✅ Menyediakan referensi dari dokumen teknis

**PENTING:** Aplikasi ini **BUKAN** bertujuan menggantikan engineer, melainkan menjadi **asisten cerdas** yang mempercepat proses diagnosis dan pengambilan keputusan.

---

## ✨ Features

### 🤖 Core Features

| Feature | Description |
|---------|-------------|
| **🧠 AI-Powered Analysis** | Menggunakan Gemini 2.5 Flash untuk analisis masalah yang cerdas dan kontekstual |
| **📚 RAG Pipeline** | Retrieval-Augmented Generation dengan FAISS untuk jawaban berbasis dokumen |
| **💬 Conversation Memory** | AI mengingat konteks percakapan untuk follow-up questions |
| **📄 PDF Knowledge Base** | Upload dan proses dokumen PDF sebagai sumber pengetahuan |
| **🎯 Structured Response** | Format jawaban profesional: Problem → Causes → Explanation → Action |

### 🎨 UI/UX Features

| Feature | Description |
|---------|-------------|
| **🎨 Modern Dark Theme** | Desain modern dengan gradient purple & cyan |
| **💡 Click-to-Ask Chips** | Suggestion questions yang bisa diklik langsung |
| **👤 Personal Branding** | Profile card dengan foto dan informasi developer |
| **🔗 Social Media Links** | Quick access ke GitHub, LinkedIn, Instagram |
| **🗑️ Reset Chat** | Tombol untuk memulai sesi troubleshooting baru |
| **📱 Responsive Design** | Tampilan optimal di desktop dan mobile |

### 🛠️ Technical Features

| Feature | Description |
|---------|-------------|
| **🔒 Secure API Key** | Environment variables untuk keamanan API key |
| **📊 Logging System** | Centralized logging untuk debugging dan monitoring |
| **⚡ Auto-Build Vector DB** | FAISS database otomatis dibangun saat pertama kali run |
| **🔄 Modular Architecture** | Kode terstruktur dengan separation of concerns |
| **🎯 Type Hints** | Python type hints untuk code quality |

---

## 🛠️ Tech Stack

### Core Technologies

- **Language:** Python 3.10+
- **UI Framework:** Streamlit 1.30+
- **LLM:** Google Gemini 2.5 Flash
- **Orchestration:** LangChain 0.2+
- **Vector Database:** FAISS
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Document Loader:** PyPDF

### Libraries & Tools

```
streamlit>=1.30.0
langchain>=0.2.0
langchain-google-genai>=1.0.0
langchain-community>=0.2.0
langchain-huggingface>=0.1.0
faiss-cpu>=1.8.0
sentence-transformers>=2.7.0
pypdf>=4.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                    (Streamlit Web App)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                        │
│                  (LangChain Framework)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│   LLM ENGINE     │          │   RAG PIPELINE   │
│  (Gemini API)    │          │                  │
│                  │          │  ┌────────────┐  │
│  - Chat Model    │          │  │  Retriever │  │
│  - Temperature   │          │  │   (FAISS)  │  │
│  - Max Tokens    │          │  └─────┬──────┘  │
└──────────────────┘          │        │         │
                              │        ▼         │
                              │  ┌────────────┐  │
                              │  │  Embedding │  │
                              │  │   Model    │  │
                              │  └─────┬──────┘  │
                              │        │         │
                              │        ▼         │
                              │  ┌────────────┐  │
                              │  │   Vector   │  │
                              │  │ Database   │  │
                              │  └────────────┘  │
                              └──────────────────┘
                                         │
                                         ▼
                              ┌──────────────────┐
                              │  KNOWLEDGE BASE  │
                              │   (PDF Files)    │
                              └──────────────────┘
```

### Component Description

1. **User Interface (Streamlit)**
   - Chat interface dengan modern UI/UX
   - Sidebar dengan personal branding
   - Suggestion chips untuk quick questions

2. **Orchestration Layer (LangChain)**
   - Menghubungkan semua komponen
   - Mengelola conversation flow
   - Handling RAG pipeline

3. **LLM Engine (Gemini 2.5 Flash)**
   - Model bahasa besar dari Google
   - Temperature rendah (0.2) untuk akurasi
   - Max tokens 2048 untuk respons detail

4. **RAG Pipeline**
   - **Retriever:** Mencari dokumen relevan dari FAISS
   - **Embedding Model:** Sentence Transformers untuk vectorization
   - **Vector Database:** FAISS untuk similarity search

5. **Knowledge Base**
   - PDF documents (Well Troubleshooting, ESP Manual, dll)
   - Chunking strategy: 1000 characters, 200 overlap
   - Stored as vectors in FAISS

---

## 🔄 System Flow

### Pseudocode: How PEA Works

```python
# ============================================
# MAIN APPLICATION FLOW
# ============================================

def main():
    # 1. INITIALIZATION
    load_environment_variables()  # Load .env (API keys)
    initialize_logger()           # Setup logging
    check_vector_db_exists()      # Check if FAISS DB exists
    
    if not vector_db_exists:
        build_knowledge_base()    # Build FAISS from PDFs
    
    # 2. USER INTERACTION LOOP
    while True:
        user_input = get_user_input()  # Get question from UI
        
        # 3. RETRIEVAL PHASE (RAG)
        relevant_docs = retrieve_from_faiss(user_input)
        # - Convert question to vector using Sentence Transformers
        # - Search FAISS for top 4 similar chunks
        # - Return document chunks with metadata
        
        # 4. CONTEXT BUILDING
        context = format_documents(relevant_docs)
        # - Combine chunks into single context string
        # - Add metadata (source, page number)
        
        # 5. PROMPT CONSTRUCTION
        system_prompt = build_system_prompt(context)
        # - Include professional response format
        # - Inject retrieved context
        # - Add conversation history (memory)
        
        # 6. LLM INFERENCE
        response = call_gemini_api(system_prompt)
        # - Send prompt to Gemini 2.5 Flash
        # - Get structured response
        # - Temperature: 0.2 (factual, not creative)
        
        # 7. RESPONSE DISPLAY
        display_response(response)
        # - Render in chat interface
        # - Format with markdown
        # - Show references if available
        
        # 8. MEMORY UPDATE
        save_to_conversation_history(user_input, response)
        # - Store in session state
        # - Enable follow-up questions

# ============================================
# KNOWLEDGE BASE BUILDING (One-time Setup)
# ============================================

def build_knowledge_base():
    # 1. LOAD PDFs
    documents = load_pdfs_from_directory("knowledge/pdf/")
    # - Read all PDF files
    # - Extract text from each page
    
    # 2. CHUNKING
    chunks = split_documents(documents, chunk_size=1000, overlap=200)
    # - Split long documents into smaller chunks
    # - Overlap to maintain context
    
    # 3. EMBEDDING
    vectors = embed_chunks(chunks, model="all-MiniLM-L6-v2")
    # - Convert text chunks to vector embeddings
    # - Each chunk → 384-dimensional vector
    
    # 4. STORE IN FAISS
    faiss_index = create_faiss_index(vectors)
    save_faiss_index(faiss_index, "knowledge/vector_db/")
    # - Build FAISS index for fast similarity search
    # - Save to disk for persistence

# ============================================
# RETRIEVAL PROCESS
# ============================================

def retrieve_from_faiss(query):
    # 1. EMBED QUERY
    query_vector = embed_text(query, model="all-MiniLM-L6-v2")
    
    # 2. SIMILARITY SEARCH
    top_k_chunks = faiss_index.search(query_vector, k=4)
    # - Find 4 most similar chunks
    # - Return chunks with similarity scores
    
    # 3. RETURN DOCUMENTS
    return top_k_chunks

# ============================================
# PROFESSIONAL RESPONSE FORMAT
# ============================================

PROFESSIONAL_RESPONSE_FORMAT = """
**Problem Summary**
[Rangkuman masalah 1-2 kalimat]

**Possible Causes**
- Penyebab 1
- Penyebab 2
- Penyebab 3

**Engineering Explanation**
[Penjelasan teknis mendalam]

**Recommended Inspection**
- Inspeksi 1
- Inspeksi 2

**Recommended Action**
- Tindakan 1
- Tindakan 2

**Additional Notes**
[Peringatan keselamatan, dll]

**References**
[Rujukan dari Knowledge Base]
"""
```

### Flow Diagram

```
User Question
     │
     ▼
┌─────────────────┐
│  Embed Query    │ ← Sentence Transformers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Search FAISS   │ ← Top 4 Similar Chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Context  │ ← Combine Chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Construct      │ ← System Prompt + Context + History
│  Prompt         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Call Gemini    │ ← Gemini 2.5 Flash API
│  API            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Display        │ ← Streamlit UI
│  Response       │
└─────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Git
- Google Gemini API Key ([Get it here](https://aistudio.google.com/apikey))

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone https://github.com/ifulxploit/production-engineering-assistant.git
cd production-engineering-assistant
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> **⚠️ IMPORTANT:** Never commit `.env` file to Git! It's already in `.gitignore`.

#### 5. Add PDF Documents

Place your PDF documents in the `knowledge/pdf/` folder:

```bash
# Example PDFs to add:
# - Well_Troubleshooting_Guide.pdf
# - ESP_Manual.pdf
# - Artificial_Lift_Handbook.pdf
```

**Supported PDF Topics:**
- Well Troubleshooting
- Artificial Lift Systems (ESP, Gas Lift, Beam Pump)
- Flow Assurance
- Well Testing & Analysis
- Production Optimization

#### 6. Run the Application

```bash
streamlit run app.py
```

The application will:
1. ✅ Check if Vector DB exists
2. ✅ Build FAISS database from PDFs (first time only)
3. ✅ Start Streamlit server
4. ✅ Open browser at `http://localhost:8501`

---

## 🚀 Usage

### Basic Usage

1. **Open the application** in your browser (auto-opened after `streamlit run`)

2. **Ask a question** in the chat input:
   ```
   Produksi sumur minyak saya turun 30% dalam seminggu, apa yang harus saya lakukan?
   ```

3. **Get structured response** with:
   - Problem Summary
   - Possible Causes
   - Engineering Explanation
   - Recommended Inspection
   - Recommended Action
   - References

4. **Click suggestion chips** for quick questions:
   - 💧 Water Cut Naik Drastis
   - ⚙️ ESP Underload
   - 📉 Penurunan Tekanan Reservoir

5. **Follow-up questions** (AI remembers context):
   ```
   Jelaskan lebih detail tentang penyebab pertama yang kamu sebutkan.
   ```

6. **Reset chat** when needed:
   - Click "🗑️ Reset Chat Session" in sidebar

### Example Questions

#### Well Troubleshooting
```
Water cut naik dari 20% menjadi 60%, apa penyebabnya?
```

#### Artificial Lift
```
ESP mengalami underload, apa langkah troubleshootingnya?
```

#### Flow Assurance
```
Terjadi hydrate blockage di flowline, bagaimana cara mengatasinya?
```

#### Well Testing
```
Bagaimana cara melakukan Pressure Buildup Test (PBU)?
```

---

## 📂 Project Structure

```
production-engineering-assistant/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (NOT in Git)
├── .env.example                    # Template for .env
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── config/                         # Configuration files
│   ├── __init__.py
│   ├── settings.py                 # App settings (API, LLM params)
│   ├── prompt.py                   # System prompts
│   └── constants.py                # Constants & format templates
│
├── core/                           # Core business logic
│   ├── __init__.py
│   ├── llm.py                      # Gemini API integration
│   ├── chatbot.py                  # Chat logic & RAG chain
│   ├── rag.py                      # RAG pipeline (PDF → FAISS)
│   ├── retriever.py                # FAISS retriever
│   ├── memory.py                   # Conversation memory
│   └── formatter.py                # Response formatting
│
├── knowledge/                      # Knowledge base
│   ├── pdf/                        # PDF documents (input)
│   │   ├── well_troubleshooting.pdf
│   │   ├── esp_manual.pdf
│   │   └── ...
│   └── vector_db/                  # FAISS index (auto-generated)
│       ├── index.faiss
│       └── index.pkl
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── helpers.py                  # Helper functions
│   └── logger.py                   # Logging configuration
│
├── data/                           # Data files
│   └── sample_questions.json       # Suggestion questions
│
├── assets/                         # Static assets
│   ├── profile.png                 # Developer photo
│   └── logo.png                    # App logo
│
└── docs/                           # Documentation
    ├── architecture.md
    ├── roadmap.md
    └── prompt-design.md
```

---

## 📸 Screenshots

<div align="center">

### Main Chat Interface
![Main Interface](https://raw.githubusercontent.com/ifulxploit/production-engineering-assistant/refs/heads/main/assets/screenshots/1.png)

### Suggestion Chips
![Suggestion Chips](https://raw.githubusercontent.com/ifulxploit/production-engineering-assistant/refs/heads/main/assets/screenshots/2.png)

### Professional Response Format
![Response Format](https://raw.githubusercontent.com/ifulxploit/production-engineering-assistant/refs/heads/main/assets/screenshots/3.png)

### Sidebar with Personal Branding
![Sidebar](https://raw.githubusercontent.com/ifulxploit/production-engineering-assistant/refs/heads/main/assets/screenshots/4.png)

</div>


---

## 🗺️ Roadmap

### ✅ Completed (v1.0)

- [x] Basic chatbot with Gemini API
- [x] Conversation memory
- [x] Professional prompt engineering
- [x] PDF knowledge base (RAG)
- [x] FAISS vector database
- [x] Modern UI/UX with purple/cyan theme
- [x] Click-to-ask suggestion chips
- [x] Personal branding in sidebar
- [x] Social media links
- [x] Centralized logging system
- [x] Auto-build vector DB

### 🚧 Future Enhancements (v2.0)

- [ ] **Engineering Calculator**
  - Nodal Analysis calculator
  - PIPESIM integration
  - Well performance calculator

- [ ] **Advanced Features**
  - Excel upload for production data
  - Production dashboard analytics
  - Multi-agent system
  - Voice assistant

- [ ] **Integration**
  - SCADA integration
  - Real-time data monitoring
  - Well report generator

- [ ] **Deployment**
  - Azure deployment
  - API service
  - Docker containerization

See the [open issues](https://github.com/ifulxploit/production-engineering-assistant/issues) for a full list of proposed features.

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

**Saiful Miqdar**  
Production Engineer | S1 Teknik Perminyakan (2025)  
Universitas Proklamasi 45

- 📧 Email: [your-email@example.com](mailto:miqdarsaiful@gmail.com)
- 💼 LinkedIn: [Saiful Miqdar](https://www.linkedin.com/in/saiful-miqdar-7050511b1/)
- 🐙 GitHub: [@ifulxploit](https://github.com/ifulxploit)
- 📷 Instagram: [@saiful_miqdar](https://www.instagram.com/saiful_miqdar)

Project Link: [https://github.com/ifulxploit/production-engineering-assistant](https://github.com/ifulxploit/production-engineering-assistant)

---

## 🙏 Acknowledgments

- [Hacktiv8 Indonesia](https://hacktiv8.com/) - Maju Bareng AI Program
- [Google Gemini API](https://ai.google.dev/) - LLM Provider
- [LangChain](https://langchain.com/) - LLM Orchestration Framework
- [Streamlit](https://streamlit.io/) - Web App Framework
- [FAISS](https://faiss.ai/) - Vector Database
- [Sentence Transformers](https://www.sbert.net/) - Embedding Models
- [SVG Repo](https://www.svgrepo.com/) - Icons

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by **Saiful Miqdar**

*Production Engineering Assistant - Empowering Engineers with AI*

</div>
</content>
</fsWrite>
