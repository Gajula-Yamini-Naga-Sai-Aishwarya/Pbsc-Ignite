# 🚀 PBSC-Ignite Quick Start Guide

Get up and running with PBSC-Ignite in 5 minutes!

## ⚡ Prerequisites (Do This First!)

1. **Install Python 3.8+** → [Download](https://www.python.org/downloads/)
2. **Install MongoDB** → [Download](https://www.mongodb.com/try/download/community) OR use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free cloud option)
3. **Get API Keys** (Free tiers available):
   - [Groq API Key](https://console.groq.com) - **Required**
   - [Perplexity API Key](https://www.perplexity.ai/api) - **Required**

## 🎯 3-Step Installation

### Step 1: Automated Setup
```bash
python setup.py
```
This will:
- ✅ Check Python version
- ✅ Install all dependencies
- ✅ Create .env file
- ✅ Initialize database

### Step 2: Add Your API Keys
Open `.env` file and add your keys:
```env
GROQ_API_KEY=your-groq-key-here
PERPLEXITY_API_KEY=your-perplexity-key-here
MONGO_URI=mongodb://localhost:27017/
```

### Step 3: Run the App
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Or manually:**
```bash
python run.py
```

## 🌐 Access Your Platform

Open browser → **http://localhost:5000**

That's it! You're ready to go! 🎉

---

## 🔧 Manual Setup (If Automated Fails)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env
# Edit .env with your API keys

# 5. Initialize database
python init_db.py init

# 6. Run the app
python run.py
```

## 🆘 Common Issues

### MongoDB not running?
**Windows:**
```bash
net start MongoDB
```
**Linux:**
```bash
sudo systemctl start mongod
```
**Mac:**
```bash
brew services start mongodb-community
```

### Port 5000 already in use?
Edit `run.py` and change the port:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Missing dependencies?
```bash
pip install -r requirements.txt --upgrade
```

## 📖 What's Next?

1. **Create Account** - Sign up at http://localhost:5000/sign_up
2. **Set Career Goal** - Complete your profile
3. **Generate Roadmap** - Get your AI-powered learning path
4. **Start Learning** - Begin with LEO AI Tutor

## 🔑 Get Free API Keys

### Groq (Required)
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy to .env file

### Perplexity (Required)
1. Go to https://www.perplexity.ai/api
2. Sign up (free tier available)
3. Get API key
4. Copy to .env file

## 💡 Quick Tips

- **No Redis?** App works without it (caching disabled)
- **Cloud MongoDB?** Update MONGO_URI in .env with Atlas connection string
- **API Limits?** Free tiers have rate limits; upgrade if needed

## ✅ Verify Everything Works

```bash
# Check database
python init_db.py check

# Test application
python -c "from app import create_app; print('✅ Success!')"
```

---

Need detailed setup? See [INSTALLATION.md](INSTALLATION.md)

**Ready to transform your career journey! 🚀**
