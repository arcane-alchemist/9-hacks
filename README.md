# LegalSaathi ⚖️
**Apna Haq Jaano — Know Your Rights**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![React](https://img.shields.io/badge/React-19-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

LegalSaathi is an intelligent, multi-lingual legal assistance platform designed to empower individuals with accessible legal knowledge. By leveraging a Retrieval-Augmented Generation (RAG) architecture running on top of real legal statutes, it provides actionable steps, extracts critical deadlines, and delivers clear responses to complex legal scenarios.

## 🌟 Key Features

- **Conversational AI Interface**: An intuitive React-based chat application for guided legal inquiry.
- **RAG-Powered Knowledge Base**: Context-aware legal answers drawing directly from statutes (e.g., IPC, Minimum Wages Act, Atrocities Act, Domestic Violence Act).
- **Multi-lingual Support**: Native translation and language detection allowing users to interact in languages like English, Hindi, Bengali, Tamil, and Telugu without switching apps.
- **Deadline Extraction**: Automatically parses generated legal advice to highlight important legal deadlines and timeframes so users don't miss critical action windows.
- **Responsive UI**: Sleek, accessible, mobile-friendly design built with TailwindCSS.

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19 + Vite
- **Styling**: TailwindCSS 4
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI + Uvicorn
- **AI / LLM Integration**: OpenAI / Google Generative AI
- **Vector DB / RAG**: ChromaDB
- **Utilities**: Pydantic, Python-dotenv, Deep-Translator, Langdetect, Dateparser

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- Valid API keys for the chosen LLM providers (e.g., OpenAI or Google Gemini).

### 1. Backend Setup

Navigate to the `backend` directory:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up Environment Variables:
Create a `.env` file in the `backend` directory and add your API keys:
```env
# Example .env file mapping
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```
*The backend API will now be running on `http://localhost:8000`.*

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
*The React app will be served locally, typically on `http://localhost:5173` or `5174`.*

## 📂 Project Structure
```text
LegalSaathi/
├── backend/                  # FastAPI Application
│   ├── main.py               # Core API router and logic
│   ├── config.py             # LLM Prompts and constants
│   ├── deadline.py           # Legal deadline extraction engine
│   ├── language_detector.py  # User locale detection fallback logic
│   ├── requirements.txt      # Python dependencies
│   └── statutes/             # Text files forming the RAG Database
└── frontend/                 # React + Vite UI
    ├── src/
    │   ├── components/       # UI Elements (ChatInterface, Header, etc.)
    │   ├── i18n/             # Dictionary translation packs (hi, bn, ta, te, en)
    │   └── App.jsx           # Main application shell
    └── package.json          # Node dependencies
```

## � How It Works

1. **User Input & Localization**: A user submits a query in their native language. The system automatically detects the language and standardizes the processing pipeline.
2. **Context Retrieval (RAG)**: The backend queries a locally run, lightweight ChromaDB vector database which holds chunked, embedded versions of core Indian legal acts and statutes.
3. **LLM Generation**: Top-matching legal documents are injected into the system prompt of our LLM (OpenAI/Gemini). It generates legal advice matching heavily enforced safety constraints.
4. **Deadline Interception**: The response is intercepted by a custom Python regex and dateparser module to extract any strict deadlines (e.g., "15 days to file an FIR") which are bundled as metadata.
5. **Frontend Rendering**: The React frontend visually displays the advice, pulling out important timeframes into a distinct red "Alert" card.

## 📈 Future Roadmap

- [ ] **Voice Support:** Audio-to-text input to further improve accessibility for rural users.
- [ ] **Automated Legal Document Drafting:** Auto-fill standardized legal notices and RTIs based on chat context.
- [ ] **Lawyer Connect Platform:** Enable users to seamlessly transfer their AI conversation context to a verified pro-bono lawyer.
- [ ] **Broader Legal Database:** Ingesting additional civil, corporate, and family law statutes.

## �🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
This project is open-source and available under the MIT License.
