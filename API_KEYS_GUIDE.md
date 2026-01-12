# 🔑 API Keys Guide - PBSC-Ignite

Complete guide to obtaining all required and optional API keys for the PBSC-Ignite platform.

## 📋 Overview

PBSC-Ignite uses multiple AI services to provide comprehensive career readiness features. Here's what you need:

### Required (Free Tiers Available)
- ✅ **Groq API** - Fast AI inference
- ✅ **Perplexity API** - Real-time research

### Optional (Enhanced Features)
- 🔹 **AWS Bedrock** - Claude Sonnet 4 (premium AI)
- 🔹 **Unipile API** - LinkedIn integration
- 🔹 **Redis** - Performance caching

---

## 🚀 Required API Keys

### 1. Groq API Key (REQUIRED)

**Purpose:** Fast AI inference for roadmaps, tutoring, and content generation

**Cost:** FREE tier available (generous limits)

**How to Get:**

1. Visit [https://console.groq.com](https://console.groq.com)

2. Click **"Sign Up"** or **"Sign In"**
   - Use Google/GitHub account or email

3. Go to **API Keys** section in dashboard

4. Click **"Create API Key"**
   - Give it a name (e.g., "PBSC-Ignite")
   - Copy the key immediately (shown only once)

5. Add to `.env` file:
   ```env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
   ```

**Free Tier Limits:**
- ~14,400 requests per day
- ~6,000 requests per minute
- More than enough for learning platform

**Pricing (if needed):**
- Pay-as-you-go: ~$0.05-0.10 per 1M tokens
- Very affordable

**Documentation:** [https://console.groq.com/docs](https://console.groq.com/docs)

---

### 2. Perplexity API Key (REQUIRED)

**Purpose:** Real-time research, current information, and enhanced roadmap generation

**Cost:** FREE trial, then affordable pricing

**How to Get:**

1. Visit [https://www.perplexity.ai](https://www.perplexity.ai)

2. Click **"API"** or go to [https://www.perplexity.ai/api](https://www.perplexity.ai/api)

3. Sign up for API access
   - Provide email and basic information
   - May require waitlist approval (usually quick)

4. Access your API keys in dashboard

5. Copy your API key

6. Add to `.env` file:
   ```env
   PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxx
   ```

**Free Trial:**
- $5 credit to start
- About 1,000+ queries

**Pricing:**
- Sonar models: ~$0.20-1.00 per 1M tokens
- Sonar Online (with search): ~$1.00-5.00 per 1M tokens

**Documentation:** [https://docs.perplexity.ai](https://docs.perplexity.ai)

---

## 🌟 Optional API Keys (Enhanced Features)

### 3. AWS Bedrock (OPTIONAL - Premium)

**Purpose:** Claude Sonnet 4 for advanced reasoning, tutoring, and career coaching

**Cost:** Pay-as-you-go (premium pricing)

**When to Use:**
- Need highest quality AI responses
- Advanced career coaching
- Complex tutoring scenarios
- Budget allows for premium features

**How to Get:**

1. **Create AWS Account**
   - Go to [https://aws.amazon.com](https://aws.amazon.com)
   - Click "Create an AWS Account"
   - Provide payment information (required)

2. **Enable Bedrock Access**
   - Go to AWS Console
   - Search for "Bedrock"
   - Request access (may take 1-2 business days)

3. **Create IAM User**
   - Go to IAM service
   - Create new user with programmatic access
   - Attach policy: `AmazonBedrockFullAccess`

4. **Generate Access Keys**
   - In IAM user details
   - Security credentials tab
   - Create access key
   - Download credentials CSV

5. **Add to `.env` file:**
   ```env
   AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXX
   AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
   AWS_REGION=us-east-1
   ```

**Pricing:**
- Claude Sonnet 4: ~$3-15 per 1M tokens
- Can get expensive with heavy use

**Alternative:** Use Groq's Llama models instead (free/cheaper)

**Documentation:** [https://docs.aws.amazon.com/bedrock/](https://docs.aws.amazon.com/bedrock/)

---

### 4. Unipile API (OPTIONAL - LinkedIn)

**Purpose:** LinkedIn integration for profile import and post publishing

**Cost:** FREE tier available, then paid plans

**When to Use:**
- Want LinkedIn integration
- Auto-post achievements to LinkedIn
- Import LinkedIn profile data

**How to Get:**

1. Visit [https://unipile.com](https://unipile.com)

2. Sign up for an account
   - Business/Developer plan

3. Access API dashboard

4. Generate API key

5. Add to `.env` file:
   ```env
   UNIPILE_API_KEY=unipile_xxxxxxxxxxxxx
   UNIPILE_BASE_URL=https://api.unipile.com/v1
   ```

**Free Tier:**
- Limited connections
- Good for testing

**Pricing:**
- Starts at ~$29/month
- Per-connection pricing

**Alternative:** Manual LinkedIn posting (copy/paste generated posts)

**Documentation:** [https://docs.unipile.com](https://docs.unipile.com)

---

## 🗄️ Database & Cache

### MongoDB (REQUIRED)

**Two Options:**

#### Option A: Local MongoDB (FREE)
1. Download MongoDB Community: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Install and start service
3. Use in `.env`:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=PBSC-Ignite-db
   ```

#### Option B: MongoDB Atlas (FREE Cloud)
1. Sign up: [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free M0 cluster
3. Get connection string
4. Use in `.env`:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=PBSC-Ignite-db
   ```

**Recommendation:** MongoDB Atlas for ease of use and free tier

---

### Redis (OPTIONAL - Performance)

**Purpose:** Caching for faster responses and reduced API costs

**Cost:** FREE options available

**Options:**

#### Option A: Local Redis (FREE)
- Windows: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
- Linux: `sudo apt-get install redis-server`
- Mac: `brew install redis`

#### Option B: Redis Cloud (FREE Tier)
1. Sign up: [https://redis.com/try-free/](https://redis.com/try-free/)
2. Create free database
3. Get connection URL

**.env Configuration:**
```env
REDIS_URL=redis://localhost:6379/0
# OR for Redis Cloud:
REDIS_URL=redis://username:password@host:port
```

**Note:** App works without Redis, just with reduced caching

---

## 💰 Cost Summary

### Minimal Setup (FREE)
- Groq API: FREE tier
- Perplexity API: $5 trial credit
- MongoDB Atlas: FREE M0 tier
- **Total: ~$0-5 to start**

### Standard Setup
- Groq API: FREE or ~$5/month
- Perplexity API: ~$10-20/month
- MongoDB Atlas: FREE
- Redis Cloud: FREE
- **Total: ~$15-25/month**

### Premium Setup
- All above: ~$25/month
- AWS Bedrock: ~$50-100/month (varies by usage)
- Unipile API: ~$29/month
- **Total: ~$100-150/month**

---

## 📝 .env File Template

Complete `.env` file with all keys:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database (REQUIRED)
MONGO_URI=mongodb://localhost:27017/
DB_NAME=PBSC-Ignite-db

# Redis (OPTIONAL)
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AI APIs (REQUIRED)
GROQ_API_KEY=gsk_your_groq_api_key_here
PERPLEXITY_API_KEY=pplx_your_perplexity_api_key_here

# AWS Bedrock (OPTIONAL)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# LinkedIn Integration (OPTIONAL)
UNIPILE_API_KEY=your_unipile_api_key
UNIPILE_BASE_URL=https://api.unipile.com/v1

# Other APIs (OPTIONAL)
GENMI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## ✅ Verification Checklist

After adding API keys, verify they work:

### 1. Test Groq
```python
python -c "from groq import Groq; import os; from dotenv import load_dotenv; load_dotenv(); client = Groq(api_key=os.getenv('GROQ_API_KEY')); print('✅ Groq OK')"
```

### 2. Test Perplexity
```python
python -c "import requests; import os; from dotenv import load_dotenv; load_dotenv(); r = requests.post('https://api.perplexity.ai/chat/completions', headers={'Authorization': f'Bearer {os.getenv(\"PERPLEXITY_API_KEY\")}'}, json={'model': 'sonar', 'messages': [{'role': 'user', 'content': 'test'}]}); print('✅ Perplexity OK' if r.status_code == 200 else f'❌ Error: {r.status_code}')"
```

### 3. Test MongoDB
```python
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000); client.server_info(); print('✅ MongoDB OK')"
```

---

## 🆘 Troubleshooting

### "Invalid API Key" Error
- Check for extra spaces in .env
- Verify key is correct (copy/paste again)
- Check if key is active in provider dashboard

### "Rate Limit Exceeded"
- Free tier limits reached
- Wait for reset (usually daily)
- Upgrade to paid tier if needed

### "Connection Timeout"
- Check internet connection
- Verify firewall isn't blocking
- Check service status pages

### API Not Working
- Ensure .env file is in project root
- Restart application after adding keys
- Check provider service status

---

## 📚 Additional Resources

### API Documentation
- **Groq:** [https://console.groq.com/docs](https://console.groq.com/docs)
- **Perplexity:** [https://docs.perplexity.ai](https://docs.perplexity.ai)
- **AWS Bedrock:** [https://docs.aws.amazon.com/bedrock/](https://docs.aws.amazon.com/bedrock/)
- **Unipile:** [https://docs.unipile.com](https://docs.unipile.com)

### Community & Support
- Stack Overflow for technical issues
- Provider documentation for API help
- GitHub Issues for project-specific problems

---

## 🎯 Recommendation for Getting Started

**Week 1: Minimal Setup**
1. Get Groq API key (FREE)
2. Get Perplexity trial ($5 credit)
3. Use MongoDB Atlas (FREE)
4. Skip Redis, AWS, Unipile

**Week 2-4: Evaluate Usage**
- Monitor API usage in dashboards
- See if free tiers are sufficient
- Upgrade only if needed

**Production: Scale as Needed**
- Add Redis for performance
- Consider AWS Bedrock for quality
- Add Unipile if LinkedIn is important

---

**Start with the FREE tier, scale as you grow! 🚀**
