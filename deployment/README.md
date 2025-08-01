# InquiryCircle Deployment Guide

## Development Setup

### Prerequisites
- Python 3.8+
- Git

### Quick Start

1. **Clone and navigate to project**:
   ```bash
   cd InquiryCircle/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Homepage: http://localhost:8000
   - Demo keys: `admin-master-key`, `facilitator-demo`, `participant-demo`

### Data Storage

- **Circles**: Stored in `data/circles.json`
- **Keys**: Stored in `data/keys.json`
- **Logs**: Stored in `logs/inquirycircle.log`
- **Backups**: Created automatically in `data/` directory

## Production Deployment (Ubuntu 22.04)

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Create application user
sudo useradd --system --shell /bin/bash --home /opt/inquirycircle inquirycircle
sudo mkdir -p /opt/inquirycircle
sudo chown inquirycircle:inquirycircle /opt/inquirycircle
```

### 2. Application Deployment

```bash
# Switch to application user
sudo su - inquirycircle

# Clone repository
git clone <your-repo-url> /opt/inquirycircle/app
cd /opt/inquirycircle/app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env for production settings
```

### 3. Configure Environment (.env)

```bash
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
JITSI_DOMAIN=meet.jit.si
JITSI_ROOM_PREFIX=YourPrefix-
LOG_LEVEL=INFO
```

### 4. Set up Gunicorn

```bash
# Create log directories
sudo mkdir -p /var/log/gunicorn
sudo chown inquirycircle:inquirycircle /var/log/gunicorn

# Test Gunicorn
cd /opt/inquirycircle/app/backend
source venv/bin/activate
gunicorn --config ../config/gunicorn.conf.py inquirycircle.wsgi:application
```

### 5. Set up Systemd Service

```bash
# Copy service file
sudo cp /opt/inquirycircle/app/config/inquirycircle.service /etc/systemd/system/

# Edit paths in service file
sudo nano /etc/systemd/system/inquirycircle.service
# Update all /path/to/inquirycircle with /opt/inquirycircle/app

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable inquirycircle
sudo systemctl start inquirycircle
sudo systemctl status inquirycircle
```

### 6. Set up Caddy

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Configure Caddy
sudo cp /opt/inquirycircle/app/config/Caddyfile /etc/caddy/Caddyfile
sudo nano /etc/caddy/Caddyfile
# Update yourdomain.com with your actual domain
# Update static files path

# Create log directory
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy

# Start Caddy
sudo systemctl enable caddy
sudo systemctl start caddy
sudo systemctl status caddy
```

### 7. Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Maintenance

### Backup Data
```bash
# Manual backup
cd /opt/inquirycircle/app/backend
python -c "from circles.storage import storage; storage.backup_data()"
```

### View Logs
```bash
# Application logs
sudo journalctl -u inquirycircle -f

# Caddy logs
sudo journalctl -u caddy -f

# Application file logs
tail -f /opt/inquirycircle/app/backend/logs/inquirycircle.log
```

### Update Application
```bash
sudo su - inquirycircle
cd /opt/inquirycircle/app
git pull
sudo systemctl restart inquirycircle
```

## Troubleshooting

### Common Issues

1. **Service won't start**: Check logs with `sudo journalctl -u inquirycircle`
2. **Permission errors**: Ensure inquirycircle user owns all files
3. **Jitsi not loading**: Check browser console, ensure HTTPS in production
4. **Data not persisting**: Check data directory permissions

### Health Checks

```bash
# Check service status
sudo systemctl status inquirycircle caddy

# Test application
curl http://localhost:8000

# Check data files
ls -la /opt/inquirycircle/app/backend/data/
```
