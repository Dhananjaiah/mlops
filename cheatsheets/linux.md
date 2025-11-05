# Linux Cheatsheet for MLOps/DevOps Engineers

## System Information & Monitoring

### Basic System Info
```bash
# OS and kernel information
uname -a                    # All system information
cat /etc/os-release         # OS distribution details
hostnamectl                 # System hostname and OS info

# CPU information
lscpu                       # CPU architecture details
cat /proc/cpuinfo          # Detailed CPU info
nproc                      # Number of CPU cores

# Memory information
free -h                    # Memory usage (human-readable)
cat /proc/meminfo         # Detailed memory info
vmstat 1                  # Virtual memory statistics

# Disk information
df -h                     # Disk space usage
lsblk                     # List block devices
fdisk -l                  # Partition table info (requires sudo)
```

### Resource Monitoring
```bash
# Real-time monitoring
top                       # Process activity (classic)
htop                      # Interactive process viewer (better)
glances                   # Modern system monitor

# CPU usage
mpstat 1 10              # CPU stats, 1 sec interval, 10 times
sar -u 1 5               # CPU usage report

# Memory usage
vmstat -s                # Memory statistics
sar -r 1 5               # Memory usage over time

# Disk I/O
iostat -x 1 5           # Extended disk stats
iotop                    # I/O usage by process (requires sudo)

# Network monitoring
iftop                    # Network bandwidth by connection
nethogs                  # Network usage by process
nload                    # Network traffic visualization
```

---

## File Operations & Management

### Basic File Operations
```bash
# Navigation
pwd                      # Print working directory
ls -lah                  # List all files with details
cd /path/to/dir         # Change directory
cd ~                     # Go to home directory
cd -                     # Go to previous directory

# File manipulation
cp source dest           # Copy file
cp -r source/ dest/      # Copy directory recursively
mv source dest           # Move/rename file
rm file.txt              # Remove file
rm -rf directory/        # Remove directory recursively (use carefully!)

# File viewing
cat file.txt             # Display entire file
less file.txt            # Page through file
head -n 20 file.txt      # First 20 lines
tail -n 20 file.txt      # Last 20 lines
tail -f /var/log/app.log # Follow log file in real-time

# File searching
find /path -name "*.log" -type f        # Find files by name
find /path -mtime -7                     # Files modified in last 7 days
find /path -size +100M                   # Files larger than 100MB
grep -r "error" /var/log/                # Search text in files recursively
grep -i "pattern" file.txt               # Case-insensitive search
```

### File Permissions & Ownership
```bash
# View permissions
ls -l file.txt           # Shows permissions (rwxrwxrwx)

# Change permissions
chmod 644 file.txt       # rw-r--r--
chmod 755 script.sh      # rwxr-xr-x
chmod +x script.sh       # Add execute permission
chmod -R 755 directory/  # Recursive permission change

# Change ownership
chown user:group file.txt         # Change owner and group
chown -R user:group directory/    # Recursive ownership change
sudo chown root:root /etc/config  # Change to root (requires sudo)
```

### Archiving & Compression
```bash
# tar (tape archive)
tar -czf archive.tar.gz directory/     # Create compressed archive
tar -xzf archive.tar.gz                # Extract compressed archive
tar -tzf archive.tar.gz                # List contents without extracting
tar -xzf archive.tar.gz -C /dest/      # Extract to specific directory

# zip/unzip
zip -r archive.zip directory/          # Create zip archive
unzip archive.zip                       # Extract zip archive
unzip -l archive.zip                    # List contents

# Other compression
gzip file.txt                           # Compress file (creates file.txt.gz)
gunzip file.txt.gz                      # Decompress file
bzip2 file.txt                          # Better compression (slower)
bunzip2 file.txt.bz2                    # Decompress bzip2
```

---

## Process Management

### Process Monitoring
```bash
# List processes
ps aux                   # All processes with details
ps aux | grep python     # Filter processes
pgrep -a python          # Find python processes

# Process tree
pstree                   # Visual process tree
pstree -p                # Include PIDs

# Real-time monitoring
top                      # Interactive process monitor
htop                     # Better interactive monitor
top -u username          # Monitor specific user's processes
```

### Process Control
```bash
# Start/stop processes
command &                # Run in background
nohup command &          # Run immune to hangups
disown                   # Detach process from shell

# Job control
jobs                     # List background jobs
fg %1                    # Bring job to foreground
bg %1                    # Resume job in background
Ctrl+Z                   # Suspend current process
Ctrl+C                   # Terminate current process

# Kill processes
kill PID                 # Terminate process
kill -9 PID              # Force kill
killall process_name     # Kill by name
pkill -f pattern         # Kill by pattern
```

### Service Management (systemd)
```bash
# Service control
sudo systemctl start nginx              # Start service
sudo systemctl stop nginx               # Stop service
sudo systemctl restart nginx            # Restart service
sudo systemctl reload nginx             # Reload configuration
sudo systemctl enable nginx             # Enable on boot
sudo systemctl disable nginx            # Disable on boot

# Service status
systemctl status nginx                  # Check service status
systemctl list-units --type=service     # List all services
systemctl is-active nginx               # Check if active
systemctl is-enabled nginx              # Check if enabled

# Logs
journalctl -u nginx                     # View service logs
journalctl -u nginx -f                  # Follow service logs
journalctl -u nginx --since "1 hour ago" # Recent logs
journalctl -xe                          # Recent errors
```

---

## Networking

### Network Configuration
```bash
# Network interfaces
ip addr show             # Show IP addresses
ip link show             # Show network interfaces
ifconfig                 # Legacy interface info

# Routing
ip route show            # Show routing table
route -n                 # Legacy routing table
traceroute google.com    # Trace route to host

# DNS
nslookup google.com      # DNS lookup
dig google.com           # Detailed DNS query
host google.com          # Simple DNS lookup
cat /etc/resolv.conf     # DNS server configuration
```

### Network Testing & Troubleshooting
```bash
# Connectivity testing
ping google.com          # Test connectivity
ping -c 5 8.8.8.8        # Send 5 packets
ping6 google.com         # IPv6 ping

# Port testing
telnet host 80           # Test TCP port
nc -zv host 80           # Check if port is open
nmap -p 80,443 host      # Scan specific ports
nmap -p- host            # Scan all ports (slow)

# Bandwidth testing
wget http://speedtest.tele2.net/1GB.zip -O /dev/null  # Download speed
curl -o /dev/null http://speedtest.tele2.net/10MB.zip # Download with curl
```

### Network Connections
```bash
# Active connections
netstat -tuln            # List listening ports
netstat -tulnp           # Include process names
ss -tuln                 # Modern netstat replacement
ss -tulnp                # Include process info
lsof -i :8080            # Show process using port 8080

# Connection statistics
netstat -s               # Network statistics
ss -s                    # Socket statistics
```

### Firewall (UFW/iptables)
```bash
# UFW (Uncomplicated Firewall)
sudo ufw status          # Check firewall status
sudo ufw enable          # Enable firewall
sudo ufw allow 22        # Allow SSH
sudo ufw allow 80/tcp    # Allow HTTP
sudo ufw allow from 192.168.1.0/24  # Allow from subnet
sudo ufw delete allow 80 # Remove rule
sudo ufw reset           # Reset to defaults

# iptables (advanced)
sudo iptables -L -n      # List rules
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT  # Allow port
sudo iptables-save > /etc/iptables/rules.v4         # Save rules
```

---

## User & Permission Management

### User Management
```bash
# User information
whoami                   # Current username
id                       # User ID and groups
w                        # Who is logged in
last                     # Login history
finger username          # User details (if available)

# User operations (require sudo)
sudo useradd -m -s /bin/bash newuser    # Create user
sudo passwd newuser                      # Set password
sudo usermod -aG sudo newuser           # Add to sudo group
sudo userdel -r username                # Delete user and home
```

### Group Management
```bash
# Group operations
groups                   # Show current user's groups
groups username          # Show user's groups
sudo groupadd devops     # Create group
sudo usermod -aG devops user  # Add user to group
sudo gpasswd -d user group    # Remove user from group
```

---

## Disk & Storage Management

### Disk Usage
```bash
# Disk space
df -h                    # File system disk space
df -i                    # Inode usage
du -sh /path/to/dir      # Directory size
du -h --max-depth=1 /var # Size of subdirectories
ncdu /path               # Interactive disk usage (install first)

# Find large files
find / -type f -size +100M 2>/dev/null  # Files over 100MB
du -ah /var | sort -rh | head -20       # 20 largest files/dirs
```

### Disk Partitioning & Mounting
```bash
# List disks and partitions
lsblk                    # Block devices tree
fdisk -l                 # Partition tables (requires sudo)
blkid                    # Block device IDs

# Mounting
mount                    # Show mounted filesystems
sudo mount /dev/sdb1 /mnt/data  # Mount partition
sudo umount /mnt/data    # Unmount
cat /etc/fstab           # Auto-mount configuration
```

---

## Package Management

### APT (Debian/Ubuntu)
```bash
# Update package lists
sudo apt update          # Update package index
sudo apt upgrade         # Upgrade packages
sudo apt full-upgrade    # Upgrade with dependency changes

# Install/remove packages
sudo apt install package-name     # Install package
sudo apt install -y nginx         # Install without prompt
sudo apt remove package-name      # Remove package
sudo apt purge package-name       # Remove with config files
sudo apt autoremove              # Remove unused dependencies

# Search packages
apt search keyword       # Search for packages
apt show package-name    # Show package details
apt list --installed     # List installed packages
```

### YUM/DNF (RHEL/CentOS/Fedora)
```bash
# Update system
sudo yum update          # Update packages (CentOS 7)
sudo dnf update          # Update packages (CentOS 8+, Fedora)

# Install/remove
sudo yum install package-name     # Install package
sudo dnf install package-name     # Install package
sudo yum remove package-name      # Remove package
sudo yum autoremove              # Remove unused dependencies

# Search packages
yum search keyword       # Search packages
dnf search keyword       # Search packages
yum info package-name    # Package information
```

---

## Security & Permissions

### SSH Configuration
```bash
# SSH connection
ssh user@host            # Connect to remote host
ssh -i key.pem user@host # Connect with key
ssh -p 2222 user@host    # Non-standard port

# SSH key management
ssh-keygen -t rsa -b 4096 -C "email@example.com"  # Generate SSH key
ssh-copy-id user@host                             # Copy key to server
chmod 600 ~/.ssh/id_rsa                           # Secure private key
chmod 644 ~/.ssh/id_rsa.pub                       # Public key permissions

# SSH config (~/.ssh/config)
# Host myserver
#     HostName 192.168.1.100
#     User ubuntu
#     Port 22
#     IdentityFile ~/.ssh/mykey.pem
```

### SSL/TLS Certificates
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Check certificate
openssl x509 -in cert.pem -text -noout          # View certificate
openssl x509 -in cert.pem -dates -noout         # Check expiration
openssl s_client -connect google.com:443        # Test SSL connection

# Let's Encrypt (Certbot)
sudo certbot --nginx -d example.com             # Get certificate for nginx
sudo certbot renew                              # Renew certificates
sudo certbot certificates                       # List certificates
```

### Security Scanning
```bash
# Port scanning
nmap -sV localhost       # Scan open ports with service detection
nmap -A target.com       # Aggressive scan (OS, version, scripts)

# File integrity
md5sum file.txt          # MD5 checksum
sha256sum file.txt       # SHA-256 checksum
md5sum -c checksums.txt  # Verify checksums

# Security updates
sudo apt list --upgradable           # List upgradable packages
sudo apt upgrade -s                   # Simulate upgrade
sudo unattended-upgrades --dry-run   # Test auto-updates
```

---

## Environment Variables

### Managing Environment Variables
```bash
# View variables
env                      # List all environment variables
printenv                 # Alternative to env
echo $PATH               # Print specific variable
echo $HOME               # User home directory

# Set variables
export VAR="value"       # Set for current session
export PATH="$PATH:/new/path"  # Append to PATH

# Permanent variables
# Add to ~/.bashrc or ~/.profile:
# export MY_VAR="value"

# Load variables
source ~/.bashrc         # Reload bash config
. ~/.profile             # Alternative syntax
```

---

## Text Processing & Manipulation

### Text Viewing & Editing
```bash
# Viewing
cat file.txt             # Display file
less file.txt            # Paginated viewing
head -n 10 file.txt      # First 10 lines
tail -n 10 file.txt      # Last 10 lines
tail -f /var/log/syslog  # Follow file changes

# Editing
nano file.txt            # Simple text editor
vim file.txt             # Advanced text editor
vi file.txt              # Classic editor
```

### Text Processing
```bash
# Search and filter
grep "pattern" file.txt              # Search for pattern
grep -i "pattern" file.txt           # Case-insensitive
grep -r "pattern" /path/             # Recursive search
grep -v "pattern" file.txt           # Invert match (exclude)
grep -E "regex" file.txt             # Extended regex

# Text manipulation
cut -d',' -f1,3 file.csv            # Extract columns (CSV)
awk '{print $1, $3}' file.txt       # Print columns 1 and 3
sed 's/old/new/g' file.txt          # Replace text
sed -i 's/old/new/g' file.txt       # Replace in-place
sort file.txt                        # Sort lines
sort -u file.txt                     # Sort and remove duplicates
uniq file.txt                        # Remove consecutive duplicates
wc -l file.txt                       # Count lines
wc -w file.txt                       # Count words

# Advanced text processing
tr '[:lower:]' '[:upper:]' < file.txt   # Convert to uppercase
paste file1.txt file2.txt               # Merge files side by side
join file1.txt file2.txt                # Join on common field
diff file1.txt file2.txt                # Show differences
comm file1.txt file2.txt                # Compare sorted files
```

---

## Scripting & Automation

### Bash Scripting Basics
```bash
#!/bin/bash
# Example deployment script

# Variables
APP_NAME="myapp"
DEPLOY_DIR="/opt/$APP_NAME"
LOG_FILE="/var/log/${APP_NAME}_deploy.log"

# Functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
set -e  # Exit on error
set -u  # Error on undefined variable

# Main script
log "Starting deployment of $APP_NAME"

if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir -p "$DEPLOY_DIR"
    log "Created directory: $DEPLOY_DIR"
fi

# Backup
if [ -d "$DEPLOY_DIR/current" ]; then
    tar -czf "${DEPLOY_DIR}/backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$DEPLOY_DIR/current"
    log "Backup created"
fi

log "Deployment completed successfully"
```

### Cron Jobs (Scheduled Tasks)
```bash
# Edit crontab
crontab -e               # Edit current user's crontab
sudo crontab -e          # Edit root's crontab
crontab -l               # List cron jobs
crontab -r               # Remove all cron jobs

# Crontab format: minute hour day month weekday command
# Examples:
# 0 2 * * * /path/to/backup.sh              # Daily at 2 AM
# */5 * * * * /path/to/check.sh             # Every 5 minutes
# 0 0 * * 0 /path/to/weekly.sh              # Weekly on Sunday
# 0 9 1 * * /path/to/monthly.sh             # Monthly on 1st at 9 AM
# 0 6 * * 1-5 /path/to/weekday.sh           # Weekdays at 6 AM
```

---

## Performance Analysis

### CPU Profiling
```bash
# CPU usage
top -b -n 1              # CPU snapshot
mpstat -P ALL 1 5        # Per-CPU statistics
pidstat -u 1 5           # Per-process CPU usage

# CPU load
uptime                   # System load averages
cat /proc/loadavg        # Load average values
w                        # Load and users
```

### Memory Profiling
```bash
# Memory usage
free -h                  # Memory overview
vmstat 1 5               # Virtual memory stats
pidstat -r 1 5           # Per-process memory

# Memory details
cat /proc/meminfo        # Detailed memory info
smem -p                  # Memory by process (install smem)
ps aux --sort=-rss | head -10  # Top memory consumers
```

### Disk I/O Profiling
```bash
# I/O statistics
iostat -x 1 5           # Extended I/O stats
iotop -o                # Only show processes doing I/O
pidstat -d 1 5          # Per-process disk I/O

# File I/O
lsof | wc -l            # Count open files
lsof -u username        # Files opened by user
lsof -p PID             # Files opened by process
```

---

## Real-World DevOps Tasks

### Task 1: Deploy Application (20 minutes)

**Scenario**: Deploy a Python Flask API to production server

```bash
#!/bin/bash
# deploy_api.sh - Deploy Flask API

set -e
APP_NAME="flask-api"
APP_DIR="/opt/$APP_NAME"
REPO_URL="https://github.com/user/flask-api.git"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"

echo "=== Starting deployment of $APP_NAME ==="

# 1. Install dependencies (first time only)
if ! command -v python3 &> /dev/null; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv nginx
fi

# 2. Create application directory
sudo mkdir -p "$APP_DIR"
cd "$APP_DIR"

# 3. Clone or pull latest code
if [ -d ".git" ]; then
    echo "Pulling latest changes..."
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" .
fi

# 4. Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create systemd service file
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Flask API Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
EOF

# 6. Set permissions
sudo chown -R www-data:www-data "$APP_DIR"

# 7. Start service
sudo systemctl daemon-reload
sudo systemctl enable "$APP_NAME"
sudo systemctl restart "$APP_NAME"

# 8. Configure nginx reverse proxy
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 9. Verify deployment
sleep 2
if systemctl is-active --quiet "$APP_NAME"; then
    echo "✓ Deployment successful!"
    echo "✓ Service is running"
    curl -f http://localhost:5000/health || echo "⚠ Health check failed"
else
    echo "✗ Deployment failed"
    sudo journalctl -u "$APP_NAME" -n 50
    exit 1
fi

echo "=== Deployment completed ==="
```

**Verification Steps**:
```bash
# Check service status
sudo systemctl status flask-api

# View logs
sudo journalctl -u flask-api -f

# Test API
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/data

# Monitor performance
htop  # Check CPU/memory usage
```

**Expected Time**: 15-20 minutes

---

### Task 2: Setup Log Rotation (10 minutes)

**Scenario**: Configure log rotation for application logs

```bash
#!/bin/bash
# setup_logrotate.sh

APP_NAME="flask-api"
LOG_DIR="/var/log/$APP_NAME"
CONFIG_FILE="/etc/logrotate.d/$APP_NAME"

# Create log directory
sudo mkdir -p "$LOG_DIR"
sudo chown www-data:www-data "$LOG_DIR"

# Create logrotate configuration
sudo tee "$CONFIG_FILE" > /dev/null <<EOF
$LOG_DIR/*.log {
    daily                    # Rotate daily
    missingok               # Don't error if log is missing
    rotate 14               # Keep 14 days of logs
    compress                # Compress rotated logs
    delaycompress           # Delay compression for 1 rotation
    notifempty              # Don't rotate empty logs
    create 0640 www-data www-data  # Permissions for new logs
    sharedscripts           # Run scripts once for all logs
    postrotate
        systemctl reload $APP_NAME > /dev/null 2>&1 || true
    endscript
}
EOF

# Test logrotate configuration
sudo logrotate -d "$CONFIG_FILE"

echo "✓ Log rotation configured for $APP_NAME"
echo "  - Logs directory: $LOG_DIR"
echo "  - Retention: 14 days"
echo "  - Compression: enabled"
```

**Verification**:
```bash
# Test rotation manually
sudo logrotate -f /etc/logrotate.d/flask-api

# Check rotated logs
ls -lh /var/log/flask-api/
```

**Expected Time**: 10 minutes

---

### Task 3: Database Backup Script (15 minutes)

**Scenario**: Automated PostgreSQL database backup with retention

```bash
#!/bin/bash
# backup_database.sh

set -e

# Configuration
DB_NAME="production_db"
DB_USER="postgres"
BACKUP_DIR="/backups/postgresql"
RETENTION_DAYS=7
S3_BUCKET="s3://my-backups/postgresql"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

echo "=== Starting database backup ==="
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"

# Create compressed backup
pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

# Verify backup was created
if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✓ Backup created successfully (Size: $SIZE)"
else
    echo "✗ Backup failed"
    exit 1
fi

# Upload to S3 (optional)
if command -v aws &> /dev/null; then
    echo "Uploading to S3..."
    aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/"
    echo "✓ Uploaded to S3"
fi

# Remove old backups (older than RETENTION_DAYS)
echo "Cleaning up old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +$RETENTION_DAYS -delete
echo "✓ Old backups removed"

# List recent backups
echo ""
echo "Recent backups:"
ls -lh "$BACKUP_DIR" | tail -5

echo "=== Backup completed ==="
```

**Setup as cron job**:
```bash
# Add to crontab (runs daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * /path/to/backup_database.sh >> /var/log/backup.log 2>&1
```

**Restore from backup**:
```bash
# List available backups
ls -lh /backups/postgresql/

# Restore specific backup
gunzip -c /backups/postgresql/production_db_20250105_020000.sql.gz | psql -U postgres production_db

# Restore from S3
aws s3 cp s3://my-backups/postgresql/production_db_20250105_020000.sql.gz - | gunzip | psql -U postgres production_db
```

**Expected Time**: 15 minutes

---

### Task 4: SSL Certificate Setup (20 minutes)

**Scenario**: Setup Let's Encrypt SSL certificate for domain

```bash
#!/bin/bash
# setup_ssl.sh

set -e

DOMAIN="api.example.com"
EMAIL="admin@example.com"

echo "=== Setting up SSL certificate for $DOMAIN ==="

# 1. Install Certbot
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

# 2. Get certificate
echo "Obtaining SSL certificate..."
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

# 3. Test automatic renewal
echo "Testing certificate renewal..."
sudo certbot renew --dry-run

# 4. Setup auto-renewal cron job
if ! crontab -l 2>/dev/null | grep -q certbot; then
    (crontab -l 2>/dev/null; echo "0 0,12 * * * certbot renew --quiet") | crontab -
    echo "✓ Auto-renewal configured"
fi

# 5. Verify SSL configuration
echo "Verifying SSL setup..."
curl -I https://$DOMAIN

echo "=== SSL setup completed ==="
echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
echo "Renewal: Automatic (twice daily)"
```

**Verification**:
```bash
# Check certificate details
sudo certbot certificates

# Test SSL grade
curl https://api.ssllabs.com/api/v3/analyze?host=api.example.com

# Manual renewal
sudo certbot renew --force-renewal
```

**Expected Time**: 20 minutes

---

### Task 5: System Monitoring Setup (25 minutes)

**Scenario**: Deploy monitoring stack with node_exporter and Prometheus

```bash
#!/bin/bash
# setup_monitoring.sh

set -e

PROMETHEUS_VERSION="2.45.0"
NODE_EXPORTER_VERSION="1.6.1"
INSTALL_DIR="/opt/monitoring"

echo "=== Setting up system monitoring ==="

# 1. Create monitoring user
sudo useradd --no-create-home --shell /bin/false prometheus || true
sudo useradd --no-create-home --shell /bin/false node_exporter || true

# 2. Install node_exporter
echo "Installing node_exporter..."
wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
tar xzf node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
sudo cp node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter /usr/local/bin/
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
rm -rf node_exporter-*

# 3. Create node_exporter service
sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# 4. Start node_exporter
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter

# 5. Verify node_exporter
if curl -s http://localhost:9100/metrics > /dev/null; then
    echo "✓ node_exporter is running"
else
    echo "✗ node_exporter failed to start"
    exit 1
fi

echo "=== Monitoring setup completed ==="
echo "Node exporter metrics: http://localhost:9100/metrics"
echo ""
echo "To visualize metrics, install Prometheus:"
echo "1. Download Prometheus from https://prometheus.io/download/"
echo "2. Configure prometheus.yml to scrape localhost:9100"
echo "3. Start Prometheus and access UI at http://localhost:9090"
```

**Prometheus Configuration** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
        labels:
          instance: 'production-server'
```

**Verification**:
```bash
# Check node_exporter status
sudo systemctl status node_exporter

# View metrics
curl http://localhost:9100/metrics | grep node_cpu

# Monitor CPU usage
curl -s http://localhost:9100/metrics | grep node_cpu_seconds_total
```

**Expected Time**: 25 minutes

---

### Task 6: Security Hardening (30 minutes)

**Scenario**: Implement basic security hardening for production server

```bash
#!/bin/bash
# security_hardening.sh

set -e

echo "=== Starting security hardening ==="

# 1. Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# 2. Configure firewall (UFW)
echo "Configuring firewall..."
sudo ufw --force enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw status

# 3. Disable root SSH login
echo "Hardening SSH configuration..."
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*X11Forwarding.*/X11Forwarding no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# 4. Install fail2ban
echo "Installing fail2ban..."
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 5. Configure fail2ban
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 22
logpath = /var/log/auth.log
EOF

sudo systemctl restart fail2ban

# 6. Enable automatic security updates
echo "Configuring automatic security updates..."
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 7. Set file permissions
echo "Setting secure file permissions..."
sudo chmod 600 /etc/ssh/sshd_config
sudo chmod 644 /etc/passwd
sudo chmod 644 /etc/group
sudo chmod 600 /etc/shadow
sudo chmod 600 /etc/gshadow

# 8. Disable unused services
echo "Disabling unused services..."
for service in bluetooth cups avahi-daemon; do
    if systemctl is-active --quiet $service; then
        sudo systemctl stop $service
        sudo systemctl disable $service
        echo "✓ Disabled $service"
    fi
done

# 9. Install security scanning tools
echo "Installing security tools..."
sudo apt install -y lynis rkhunter

# 10. Run security audit
echo "Running security audit..."
sudo lynis audit system --quick

echo "=== Security hardening completed ==="
echo ""
echo "Next steps:"
echo "1. Review SSH keys: ls -la ~/.ssh/"
echo "2. Check fail2ban status: sudo fail2ban-client status sshd"
echo "3. Review firewall rules: sudo ufw status verbose"
echo "4. Run full audit: sudo lynis audit system"
```

**Verification**:
```bash
# Check firewall status
sudo ufw status verbose

# Check fail2ban status
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Check SSH configuration
sudo sshd -T | grep -i "permitrootlogin\|passwordauthentication"

# Check for security updates
sudo apt list --upgradable | grep -i security

# Run security scan
sudo lynis audit system
sudo rkhunter --check
```

**Expected Time**: 30 minutes

---

## Quick Reference Tables

### File Permissions
| Permission | Numeric | Symbolic | Meaning |
|------------|---------|----------|---------|
| Read | 4 | r | View file contents |
| Write | 2 | w | Modify file |
| Execute | 1 | x | Run as program |
| Read + Write | 6 | rw- | View and modify |
| Read + Execute | 5 | r-x | View and run |
| All | 7 | rwx | Full permissions |

### Common Ports
| Service | Port | Protocol | Description |
|---------|------|----------|-------------|
| SSH | 22 | TCP | Secure Shell |
| HTTP | 80 | TCP | Web traffic |
| HTTPS | 443 | TCP | Secure web |
| MySQL | 3306 | TCP | Database |
| PostgreSQL | 5432 | TCP | Database |
| MongoDB | 27017 | TCP | Database |
| Redis | 6379 | TCP | Cache |
| Elasticsearch | 9200 | TCP | Search engine |
| Prometheus | 9090 | TCP | Monitoring |
| Grafana | 3000 | TCP | Visualization |

### System Load Interpretation
| Load Average | Status | Action |
|--------------|--------|--------|
| < 0.7 × cores | Good | Normal operation |
| 0.7-1.0 × cores | Busy | Monitor closely |
| 1.0-5.0 × cores | High | Investigate |
| > 5.0 × cores | Critical | Urgent action needed |

### Process Priority (nice values)
| Nice Value | Priority | Use Case |
|------------|----------|----------|
| -20 | Highest | Critical system processes |
| -10 to -1 | High | Important services |
| 0 | Normal | Default priority |
| 1 to 10 | Low | Background tasks |
| 11 to 19 | Lowest | Non-critical batch jobs |

---

## Troubleshooting Guide

### High CPU Usage
```bash
# Identify top CPU consumers
top -b -n 1 | head -20
ps aux --sort=-pcpu | head -10

# Check CPU by core
mpstat -P ALL 1 5

# Profile specific process
pidstat -p PID 1 10
```

### High Memory Usage
```bash
# Identify memory hogs
ps aux --sort=-rss | head -10
smem -p

# Check for memory leaks
watch -n 1 'free -h'

# Clear cache (if needed)
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### Disk Space Issues
```bash
# Find large files
du -ah / 2>/dev/null | sort -rh | head -20
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Check inode usage
df -i

# Clean package cache
sudo apt clean
sudo apt autoremove
```

### Network Issues
```bash
# Test connectivity
ping -c 5 8.8.8.8
ping -c 5 google.com

# Check routing
traceroute google.com
ip route show

# Check DNS
nslookup google.com
dig google.com

# Check listening ports
sudo ss -tulpn
sudo netstat -tulpn
```

### Service Not Starting
```bash
# Check service status
sudo systemctl status service-name

# View recent logs
sudo journalctl -u service-name -n 50

# Check for errors
sudo journalctl -xe

# Verify configuration
sudo service-name -t  # For nginx, apache, etc.
```

---

## Best Practices

### 1. **Security**
- ✅ Keep system updated: `sudo apt update && sudo apt upgrade`
- ✅ Use SSH keys instead of passwords
- ✅ Configure firewall (UFW/iptables)
- ✅ Regular security audits with Lynis
- ✅ Enable fail2ban for SSH protection
- ✅ Disable root SSH login

### 2. **Monitoring**
- ✅ Monitor disk space: `df -h` and set up alerts
- ✅ Monitor system load: `uptime` and `top`
- ✅ Review logs regularly: `journalctl -f`
- ✅ Setup log rotation
- ✅ Use monitoring tools (Prometheus, Grafana)

### 3. **Backups**
- ✅ Automate daily backups
- ✅ Test restore procedures regularly
- ✅ Store backups off-site (S3, cloud storage)
- ✅ Implement retention policies
- ✅ Encrypt sensitive backups

### 4. **Performance**
- ✅ Disable unnecessary services
- ✅ Optimize application configurations
- ✅ Use caching (Redis, Memcached)
- ✅ Monitor resource usage trends
- ✅ Regular performance profiling

### 5. **Documentation**
- ✅ Document all configurations
- ✅ Maintain runbooks for common tasks
- ✅ Keep inventory of servers and services
- ✅ Document incident responses
- ✅ Create standard operating procedures (SOPs)

---

## Resources

- [Linux Documentation Project](https://www.tldp.org/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Red Hat Enterprise Linux Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/)
- [Arch Linux Wiki](https://wiki.archlinux.org/) (Excellent for all distros)
- [Linux Journey](https://linuxjourney.com/)
- [ExplainShell](https://explainshell.com/) - Explain shell commands
- [Awesome Sysadmin](https://github.com/awesome-foss/awesome-sysadmin)
