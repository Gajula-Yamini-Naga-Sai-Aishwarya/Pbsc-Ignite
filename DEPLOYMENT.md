# 🚢 Deployment Guide - PBSC-Ignite

Production deployment guide for PBSC-Ignite Platform.

## 📋 Pre-Deployment Checklist

- [ ] All API keys obtained and tested
- [ ] Production database set up (MongoDB Atlas recommended)
- [ ] Redis instance configured (Redis Cloud recommended)
- [ ] Secret key generated
- [ ] Domain name configured (if applicable)
- [ ] SSL certificate obtained
- [ ] Backup strategy planned

## 🌐 Deployment Options

### Option 1: Cloud Platform (Recommended)

#### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set MONGO_URI=your-mongodb-atlas-uri
   heroku config:set GROQ_API_KEY=your-groq-key
   heroku config:set PERPLEXITY_API_KEY=your-perplexity-key
   # Add other API keys as needed
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Initialize Database**
   ```bash
   heroku run python init_db.py init
   ```

#### Deploy to Railway

1. **Connect Repository**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo

2. **Add Environment Variables**
   - In Railway dashboard, add all variables from .env

3. **Deploy**
   - Railway auto-deploys on push to main branch

4. **Initialize Database**
   - Use Railway CLI or web terminal

#### Deploy to Render

1. **Create Web Service**
   - Go to [render.com](https://render.com)
   - New Web Service from GitHub

2. **Configure**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`

3. **Environment Variables**
   - Add all .env variables in dashboard

### Option 2: VPS (DigitalOcean, AWS EC2, etc.)

#### Ubuntu Server Setup

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python & Dependencies**
   ```bash
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

3. **Install MongoDB**
   ```bash
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   sudo apt update
   sudo apt install mongodb-org -y
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

4. **Clone Repository**
   ```bash
   cd /var/www
   git clone https://github.com/yourusername/PBSC-Ignite.git
   cd PBSC-Ignite
   ```

5. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your production values
   ```

7. **Initialize Database**
   ```bash
   python init_db.py init
   ```

8. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/pbsc-ignite.service
   ```

   Add:
   ```ini
   [Unit]
   Description=PBSC-Ignite Platform
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/PBSC-Ignite
   Environment="PATH=/var/www/PBSC-Ignite/venv/bin"
   ExecStart=/var/www/PBSC-Ignite/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

9. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/pbsc-ignite
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }

       location /static {
           alias /var/www/PBSC-Ignite/app/Static;
       }
   }
   ```

10. **Enable and Start Services**
    ```bash
    sudo ln -s /etc/nginx/sites-available/pbsc-ignite /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo systemctl enable pbsc-ignite
    sudo systemctl start pbsc-ignite
    ```

11. **Setup SSL with Let's Encrypt**
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d your-domain.com
    ```

## 🔒 Production Security

### 1. Generate Strong Secret Key
```python
import secrets
print(secrets.token_hex(32))
```
Use this in .env as SECRET_KEY

### 2. Secure Database
- Use MongoDB Atlas with IP whitelist
- Enable authentication
- Use strong passwords
- Regular backups

### 3. Environment Variables
```env
# Production .env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-generated-secret-key

# Use production databases
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname
REDIS_URL=redis://user:password@host:port

# API Keys
GROQ_API_KEY=your-key
PERPLEXITY_API_KEY=your-key
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-key
```

### 4. Firewall Configuration
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📊 Monitoring & Logging

### 1. Application Logging
Add to run.py:
```python
import logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

### 2. Monitor Service
```bash
# Check service status
sudo systemctl status pbsc-ignite

# View logs
sudo journalctl -u pbsc-ignite -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. MongoDB Monitoring
```bash
mongosh --eval "db.serverStatus()"
```

## 🔄 Updates & Maintenance

### Deploy Updates
```bash
cd /var/www/PBSC-Ignite
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pbsc-ignite
```

### Database Backup
```bash
# Backup
mongodump --uri="your-mongo-uri" --out=/backup/$(date +%Y%m%d)

# Restore
mongorestore --uri="your-mongo-uri" /backup/20240115
```

### Auto-Backup Script
```bash
#!/bin/bash
# /usr/local/bin/backup-pbsc.sh
BACKUP_DIR="/backups/pbsc-ignite"
DATE=$(date +%Y%m%d_%H%M%S)

# MongoDB backup
mongodump --uri="$MONGO_URI" --out="$BACKUP_DIR/db_$DATE"

# Keep only last 7 days
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} \;
```

Add to crontab:
```bash
0 2 * * * /usr/local/bin/backup-pbsc.sh
```

## ⚡ Performance Optimization

### 1. Use Gunicorn
```bash
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 "app:create_app()"
```

### 2. Enable Gzip in Nginx
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### 3. Redis Caching
Ensure Redis is configured and running for optimal performance.

### 4. Database Indexing
Already handled by init_db.py, but verify:
```python
python init_db.py check
```

## 🌍 Environment-Specific Configuration

### Development
```env
FLASK_ENV=development
FLASK_DEBUG=True
MONGO_URI=mongodb://localhost:27017/
```

### Staging
```env
FLASK_ENV=staging
FLASK_DEBUG=False
MONGO_URI=mongodb://staging-db-url
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
MONGO_URI=mongodb+srv://production-db-url
```

## 📞 Support & Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check logs
sudo journalctl -u pbsc-ignite -n 50

# Check if port is in use
sudo lsof -i :5000
```

**Database connection error:**
```bash
# Test MongoDB
mongosh "your-connection-string"

# Check firewall
sudo ufw status
```

**Nginx 502 error:**
```bash
# Check if app is running
sudo systemctl status pbsc-ignite

# Restart services
sudo systemctl restart pbsc-ignite nginx
```

## ✅ Post-Deployment Verification

1. **Access website** - https://your-domain.com
2. **Create test account**
3. **Generate roadmap**
4. **Test AI features**
5. **Check logs for errors**
6. **Verify SSL certificate**
7. **Test all routes**

---

**Your PBSC-Ignite platform is now live! 🎉**
