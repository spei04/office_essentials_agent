#!/bin/bash
# Deployment script for AWS EC2

set -e

echo "Deploying Office Essentials Agent to AWS EC2..."

# Configuration
EC2_INSTANCE="your-ec2-instance-id"
EC2_USER="ec2-user"
DEPLOY_DIR="/opt/office-essentials-agent"

# Copy files to EC2
echo "Copying files to EC2..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
    ./ ${EC2_USER}@${EC2_INSTANCE}:${DEPLOY_DIR}/

# Run setup commands on EC2
echo "Running setup on EC2..."
ssh ${EC2_USER}@${EC2_INSTANCE} << 'EOF'
cd /opt/office-essentials-agent
source venv/bin/activate  # If using virtualenv
pip install -r requirements.txt
python scripts/setup_db.py
sudo systemctl restart office-agent
EOF

echo "Deployment complete!"

