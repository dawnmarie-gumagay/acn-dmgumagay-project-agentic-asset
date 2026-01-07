# Setup Instructions

## Prerequisites
- Python 3.10 or higher
- pip package manager
- Git
- Ollama Cloud account (for API key)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AgenticAI-DevOps
```

### 2. Create Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Windows
copy .env.template .env

# macOS/Linux
cp .env.template .env
```

Edit `.env` and replace `your_api_key_here` with your actual Ollama Cloud API key:
```env
OLLAMA_API_KEY=sk-your-actual-api-key-here
OLLAMA_BASE_URL=https://api.ollama.cloud
DEFAULT_MODEL=llama2:7b
VERBOSE_LEVEL=2
```

**Where to get API key:**
1. Sign up at https://ollama.cloud
2. Navigate to API settings
3. Generate a new API key
4. Copy it to your .env file

### 5. Test Connection
```bash
python test_connection.py
```

You should see:
```
✓ ALL TESTS PASSED - Connection is working!
```

If connection fails:
- Verify your API key is correct
- Check your internet connection
- Ensure OLLAMA_BASE_URL is correct

### 6. Run Your First Demo

**Quick Demo (5 seconds):**
```bash
python demo_healing_simple.py
```

**Full AI Demo (2-5 minutes):**
```bash
python main_with_healing.py
```

**Standard Mode (manifest generation only):**
```bash
python main.py
```

## Troubleshooting

### Issue: "OLLAMA_API_KEY is not set"
**Solution:** Make sure you created the `.env` file from `.env.template` and added your API key.

### Issue: "Connection failed"
**Solution:** 
- Verify API key is valid
- Check if Ollama Cloud service is accessible
- Try: `python test_connection.py` for detailed diagnostics

### Issue: "Module not found"
**Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Issue: "Virtual environment activation failed"
**Solution (Windows):** 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Project Structure
```
AgenticAI-DevOps/
├── agents.py              # AI agent definitions
├── tasks.py               # Task definitions
├── crew.py                # LLM connection factory
├── config.py              # Configuration management
├── main.py                # Standard execution mode
├── main_with_healing.py   # Self-healing mode
├── demo_healing_simple.py # Quick demo
├── test_connection.py     # Connection validator
├── test_healing.py        # Failure scenarios
├── requirements.txt       # Python dependencies
├── .env.template          # Environment template
├── .env                   # Your config (not in git)
└── outputs/               # Generated files

```

## Next Steps

1. ✅ Complete setup above
2. ✅ Run `test_connection.py`
3. ✅ Run `main_with_healing.py` for full demo with AI Agents
4. ✅ Run `main.py` for Standard Mode (just manifest generation)
5. ✅ Run `demo_healing_simple.py` for quick demo
6. ✅ Try custom prompts with `main_with_healing.py`
7. 📖 Read README.md for detailed documentation

## Custom Deployment Prompts

Try these examples:
```bash
python main_with_healing.py "Deploy a Node.js app with 5 replicas and 1Gi memory"
python main_with_healing.py "Create a Python Flask app with 2 replicas on port 8080"
python main_with_healing.py "Deploy nginx with 3 replicas, 256Mi memory, port 80"
```

## Support
- Check README.md for architecture details
- Review test_healing.py for supported failure scenarios
- Ensure Ollama Cloud service is active
