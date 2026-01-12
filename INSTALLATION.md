# PBSC-Ignite Installation Guide

Complete step-by-step guide to set up and run the PBSC-Ignite AI-Powered Career Readiness Platform.

## 📋 Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **MongoDB**
   - **Option A - Local Installation:**
     - Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)
     - Default connection: `mongodb://localhost:27017/`
   - **Option B - Cloud (MongoDB Atlas):**
     - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
     - Create free cluster
     - Get connection string

3. **Redis (Optional but Recommended)**
   - Enables caching for better performance
   - **Windows:** [Redis for Windows](https://github.com/microsoftarchive/redis/releases)
   - **Linux/Mac:** `sudo apt-get install redis-server` or `brew install redis`
   - **Cloud:** [Redis Cloud](https://redis.com/try-free/)

### Required API Keys

You'll need the following API keys (free tiers available):

1. **Groq API** - For fast AI inference
   - Sign up: [https://console.groq.com](https://console.groq.com)
   - Get API key from dashboard

2. **Perplexity API** - For real-time research
   - Sign up: [https://www.perplexity.ai/api](https://www.perplexity.ai/api)
   - Get API key

3. **AWS Bedrock (Optional)** - For Claude Sonnet 4
   - AWS Account required
   - Enable Bedrock access
   - Create access keys

4. **Unipile API (Optional)** - For LinkedIn integration
   - Sign up: [https://unipile.com](https://unipile.com)
   - Get API key

## 🚀 Quick Start (Automated Setup)

### Windows

1. **Download/Clone the project**
   ```bash
   cd path/to/PBSC-Ignite
   ```

2. **Run automated setup**
   ```bash
   python setup.py
   ```

3. **Edit .env file with your API keys**
   ```bash
   notepad .env
   ```

4. **Start the application**
   ```bash
   start.bat
   ```

### Linux/Mac

1. **Download/Clone the project**
   ```bash
   cd path/to/PBSC-Ignite
   ```

2. **Run automated setup**
   ```bash
   python3 setup.py
   ```

3. **Edit .env file with your API keys**
   ```bash
   nano .env
   ```

4. **Make start script executable and run**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## 📝 Manual Setup (Step by Step)

If the automated setup doesn't work, follow these manual steps:

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter errors, try upgrading pip first:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file and add your API keys:**
   ```env
   # Required
   SECRET_KEY=your-secret-key-here
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=PBSC-Ignite-db
   GROQ_API_KEY=your-groq-api-key
   PERPLEXITY_API_KEY=your-perplexity-api-key

   # Optional
   REDIS_URL=redis://localhost:6379/0
   AWS_ACCESS_KEY_ID=your-aws-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret
   UNIPILE_API_KEY=your-unipile-key
   ```

### Step 4: Start MongoDB

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

**Verify MongoDB is running:**
```bash
mongosh
# or
mongo
```

### Step 5: Initialize Database

```bash
python init_db.py init
```

This creates all necessary collections and indexes.

### Step 6: Start the Application

```bash
python run.py
```

The application will be available at: **http://localhost:5000**

## 🔧 Configuration

### Database Configuration

**Using MongoDB Atlas (Cloud):**
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=PBSC-Ignite-db
```

**Using Local MongoDB:**
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=PBSC-Ignite-db
```

### Redis Configuration

**Local Redis:**
```env
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Redis Cloud:**
```env
REDIS_URL=redis://username:password@redis-host:port
```

## 🧪 Verify Installation

Run these commands to verify everything is set up correctly:

1. **Check Database Connection:**
   ```bash
   python init_db.py check
   ```

2. **Test Python Imports:**
   ```bash
   python -c "from app import create_app; app = create_app(); print('✅ App created successfully')"
   ```

3. **Check MongoDB Collections:**
   ```bash
   mongosh PBSC-Ignite-db --eval "db.getCollectionNames()"
   ```

## 🐛 Troubleshooting

### Issue: "No module named 'flask'"
**Solution:** Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "MongoDB connection failed"
**Solution:** 
1. Check if MongoDB is running: `mongosh` or `mongo`
2. Verify MONGO_URI in .env file
3. Check firewall settings

### Issue: "Redis connection failed"
**Solution:** 
- The app will work without Redis (caching disabled)
- To fix: Install and start Redis, or comment out Redis-related code

### Issue: Port 5000 already in use
**Solution:** Change port in run.py:
```python
app.run(debug=True, port=5001)
```

### Issue: API key errors
**Solution:** 
1. Verify API keys are correctly set in .env
2. Check API key quotas/limits
3. Ensure no extra spaces in .env file

## 📱 Accessing the Application

After successful installation:

1. **Open browser:** http://localhost:5000
2. **Sign Up:** Create a new account
3. **Set Profile:** Complete your career goals
4. **Start Learning:** Generate your personalized roadmap

## 🔄 Database Management

**Reset Database (WARNING: Deletes all data):**
```bash
python init_db.py reset
```

**Re-initialize Database:**
```bash
python init_db.py init
```

**Health Check:**
```bash
python init_db.py check
```

## 🚢 Production Deployment

For production deployment, consider:

1. **Use Gunicorn (Linux/Mac):**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```

2. **Set Production Environment:**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=generate-a-strong-secret-key
   ```

3. **Use Production Database:**
   - MongoDB Atlas for cloud database
   - Redis Cloud for caching

4. **Set Up Reverse Proxy:**
   - Use Nginx or Apache
   - Configure SSL/TLS

## 📚 Additional Resources

- **MongoDB Docs:** https://docs.mongodb.com
- **Flask Docs:** https://flask.palletsprojects.com
- **Redis Docs:** https://redis.io/docs
- **Groq API:** https://console.groq.com/docs
- **Perplexity API:** https://docs.perplexity.ai

## 💡 Getting API Keys

### Groq API Key
1. Visit https://console.groq.com
2. Sign up/Sign in
3. Go to API Keys section
4. Create new API key
5. Copy and paste in .env

### Perplexity API Key
1. Visit https://www.perplexity.ai/api
2. Sign up for API access
3. Get your API key from dashboard
4. Copy and paste in .env

### AWS Bedrock (Optional)
1. Create AWS account
2. Enable Bedrock service
3. Create IAM user with Bedrock permissions
4. Generate access keys
5. Add to .env

## ✅ Post-Installation Checklist

- [ ] Python 3.8+ installed
- [ ] MongoDB running and accessible
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file configured with API keys
- [ ] Database initialized (python init_db.py init)
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can create user account
- [ ] Can generate learning roadmap

## 🆘 Need Help?

If you encounter issues:

1. Check the error messages carefully
2. Verify all prerequisites are installed
3. Review the troubleshooting section
4. Check that all services (MongoDB, Redis) are running
5. Verify API keys are valid and have quota remaining

---

**Congratulations! You're ready to use PBSC-Ignite! 🎉**
