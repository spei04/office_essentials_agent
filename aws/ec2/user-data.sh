#!/bin/bash
# EC2 user data script for initializing the application

# Update system
yum update -y

# Install Python 3.11
yum install -y python3.11 python3.11-pip git

# Install PostgreSQL client (if using RDS)
yum install -y postgresql

# Create application directory
mkdir -p /opt/office-essentials-agent
cd /opt/office-essentials-agent

# Clone repository (or copy files)
# git clone <your-repo-url> .

# Install Python dependencies
pip3.11 install -r requirements.txt

# Create systemd service file
cat > /etc/systemd/system/office-agent.service << EOF
[Unit]
Description=Office Essentials Procurement Agent API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/office-essentials-agent
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable office-agent
systemctl start office-agent

