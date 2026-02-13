# Code Architect - Gemini 3 Hackathon Project

An autonomous code analysis system powered by **Gemini 3 Pro** that intelligently analyzes software repositories across multiple iterations with Marathon Agent capabilities.

## 🎯 Project Overview

**Code Architect** is designed to showcase Gemini 3's multimodal reasoning and autonomous agent capabilities by building a sophisticated system that:

- **Analyzes** entire codebases using Gemini's 1M token context window
- **Reasons** about architecture, performance, security, and code quality
- **Autonomously** executes multi-step analysis across iterations
- **Self-corrects** when exploring deeper insights
- **Generates** actionable recommendations with code examples
- **Maintains continuity** across long-running analysis sessions (Marathon Agent track)

## 🏗️ Architecture

```
Code Architect Hackathon/
├── backend/                    # Python Flask backend (Deploy on Render)
│   ├── main.py                # Flask application entry
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variable template
│   ├── routes/
│   │   ├── gemini_routes.py   # Gemini API endpoints
│   │   └── analysis_routes.py # Analysis endpoints
│   ├── services/
│   │   └── gemini_service.py  # Gemini 3 integration logic
│   └── models/
│       └── schemas.py         # Pydantic models
│
├── frontend/                   # Next.js frontend (Deploy on Vercel)
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx       # Main dashboard
│   │   │   ├── layout.tsx     # Root layout
│   │   │   └── globals.css    # Global styles
│   │   ├── components/
│   │   │   ├── AnalysisForm.tsx      # Repository input form
│   │   │   └── ResultsPanel.tsx      # Results display
│   │   └── lib/
│   │       ├── api.ts         # API client
│   │       └── store.ts       # Zustand state management
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js      # PostCSS / Tailwind plugin config
│   ├── next.config.mjs        # Next.js configuration (ESM)
│   └── vercel.json            # Vercel deployment config
│
├── render.yaml                # Render deployment config
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Gemini 3 API Key (from Google AI Studio)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Linux/macOS: source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

5. **Run the backend:**
   ```bash
   python main.py
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create .env.local:**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

## 🔧 How It Works

### 1. Repository Input
User provides a repository URL, branch, focus areas, and analysis depth.

### 2. Autonomous Analysis Loop
- **Iteration 1-N**: Gemini 3 analyzes code at each iteration level
- **Thinking Mode**: Uses Marathon Agent capabilities to maintain context across iterations
- **Self-Correction**: Refines findings based on previous analysis
- **Extraction**: Pulls out recommendations and findings automatically

### 3. Results Processing
- Aggregates findings from all iterations
- Extracts actionable recommendations
- Generates code improvement examples

### 4. Real-time Status Updates
- Frontend polls backend every 3 seconds
- Updates UI with progress and results
- Displays findings and recommendations as they're generated

## 📊 Key Features

### Marathon Agent Track
- ✅ Multi-iteration analysis (1-5 depths configurable)
- ✅ Thought Signature maintenance across iterations
- ✅ Self-correction capabilities
- ✅ Long-running autonomous tasks (hours capable)

### Gemini 3 Capabilities Utilized
- 🧠 Extended context window (1M tokens) for large codebases
- 🔄 Deep reasoning with thinking levels
- 🎯 Multimodal understanding of code + documentation
- 🤖 Autonomous decision making within analysis loops

### User Experience
- 🎨 Modern dark-themed dashboard
- ⚡ Real-time analysis progress
- 📈 Detailed findings visualization
- 💡 Actionable recommendations

## 🌐 Deployment

### Deploy Backend to Render

1. **Create Render account** at https://render.com
2. **Connect GitHub repository**
3. **Create Web Service:**
   - Build command: `pip install --only-binary=:all: -r backend/requirements.txt`
   - Start command: `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT main:app`
   - Environment: Add `GEMINI_API_KEY`, `FRONTEND_URL`
   - Runtime: Python 3.11.7

4. **Your backend URL** is `https://code-architect.onrender.com`

### Deploy Frontend to Vercel

1. **Create Vercel account** at https://vercel.com
2. **Import project** from GitHub
3. **Set Root Directory** to `frontend`
4. **Set environment variables:**
   - `NEXT_PUBLIC_API_URL`: Your Render backend URL (e.g. `https://code-architect.onrender.com`)
5. **Deploy** (automatic on push to main)

## 📝 API Endpoints

### Health Check
```
GET /health
```

### Start Analysis
```
POST /api/gemini/analyze
Body: {
  "repository_url": "https://github.com/user/repo",
  "branch": "main",
  "focus_areas": ["architecture", "performance", "security"],
  "depth": 3
}
```

### Get Analysis Status
```
GET /api/gemini/analyze/{analysis_id}
```

## 🔐 Security Notes

- **API Keys**: Never commit `.env` file to version control
- **CORS**: Configure allowed origins in backend config
- **Rate Limiting**: Consider adding in production
- **Input Validation**: All inputs are validated with Pydantic

## 🚦 Testing

### Backend
```bash
# Run with logging
python main.py --log-level debug

# Test endpoints
curl http://localhost:8000/health
```

### Frontend
```bash
npm run lint
npm run build
```

## 📚 Tech Stack

**Backend:**
- Flask - Lightweight Python web framework
- Google Generative AI SDK - Gemini integration
- Pydantic - Data validation
- Gunicorn - WSGI production server
- GitPython - Repository handling

**Frontend:**
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Zustand - State management
- Axios - HTTP client

## 🎓 Hackathon Compliance

✅ **Follows Hackathon Requirements:**
- Uses Gemini 3 API for core functionality
- Marathon Agent track (multi-step autonomous reasoning)
- NOT just a prompt wrapper (complex orchestration)
- NOT basic chatbot (sophisticated analysis system)
- Autonomous verification and self-correction
- Real business value (code quality analysis)

❌ **Avoids Discouraged Patterns:**
- Multi-step orchestration required (not single-prompt)
- Deep reasoning with code understanding (beyond basic RAG)
- Autonomous agents with self-correction
- Real-time continuous verification

## 🤝 Contributing

Feel free to extend this project:
- Add more analysis dimensions (test coverage, documentation)
- Implement git diff generation
- Add caching layer with Redis
- Create CLI tool for local analysis
- Build GitHub integration

## 📄 License

MIT License - Feel free to use for hackathon submission!

## 🙋 Support

For issues or questions:
1. Check the `.env` setup
2. Verify Gemini API key is valid
3. Ensure backend is running before frontend
4. Check browser console for client-side errors
