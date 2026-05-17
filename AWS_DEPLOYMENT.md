# AWS Deployment Guide for Smart Canteen System

## Architecture Overview

```
Internet
    ↓
CloudFront (CDN)
    ↓
S3 Bucket (React Frontend)
    ↓
ALB/API Gateway
    ↓
EC2/Lambda (FastAPI Backend)
    ↓
RDS PostgreSQL (Database)
    ↓
S3 Bucket (File Storage)
```

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Domain name (optional)

## Setup Instructions

### 1. Database Setup (RDS PostgreSQL)

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier smart-canteen-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password YourPassword123 \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxx \
    --db-name smart_canteen \
    --backup-retention-period 7 \
    --publicly-accessible

# Get endpoint
aws rds describe-db-instances \
    --db-instance-identifier smart-canteen-db \
    --query 'DBInstances[0].Endpoint.Address'
```

Update `.env`:
```
DATABASE_URL=postgresql://admin:YourPassword123@your-rds-endpoint:5432/smart_canteen
```

### 2. Backend Deployment (EC2)

#### Option A: EC2 Instance

```bash
# Launch EC2 instance (Amazon Linux 2)
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxx

# SSH into instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git nginx -y

# Clone and setup
git clone <your-repo-url>
cd smart-canteen/backend

# Install Python packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/smart-canteen.service
```

Create service file:
```ini
[Unit]
Description=Smart Canteen FastAPI
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/smart-canteen/backend
Environment="PATH=/home/ec2-user/smart-canteen/backend/venv/bin"
ExecStart=/home/ec2-user/smart-canteen/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable smart-canteen
sudo systemctl start smart-canteen

# Configure Nginx
sudo nano /etc/nginx/conf.d/smart-canteen.conf
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo systemctl restart nginx
```

#### Option B: AWS Lambda + API Gateway

Create `zappa_settings.json`:
```json
{
    "production": {
        "app_function": "app.main.app",
        "aws_region": "us-east-1",
        "profile_name": "default",
        "project_name": "smart-canteen",
        "runtime": "python3.9",
        "s3_bucket": "smart-canteen-lambda-deployments"
    }
}
```

```bash
pip install zappa
zappa deploy production
```

### 3. Frontend Deployment (S3 + CloudFront)

```bash
cd frontend

# Build React app
npm install
npm run build

# Create S3 bucket
aws s3 mb s3://smart-canteen-frontend

# Configure bucket for static hosting
aws s3 website s3://smart-canteen-frontend \
    --index-document index.html \
    --error-document index.html

# Upload build files
aws s3 sync build/ s3://smart-canteen-frontend --acl public-read

# Create CloudFront distribution
aws cloudfront create-distribution \
    --origin-domain-name smart-canteen-frontend.s3.amazonaws.com \
    --default-root-object index.html
```

CloudFront configuration (JSON):
```json
{
    "DistributionConfig": {
        "CallerReference": "smart-canteen-1",
        "Aliases": {
            "Quantity": 1,
            "Items": ["canteen.yourdomain.com"]
        },
        "DefaultRootObject": "index.html",
        "Origins": {
            "Quantity": 1,
            "Items": [{
                "Id": "S3-smart-canteen",
                "DomainName": "smart-canteen-frontend.s3.amazonaws.com",
                "S3OriginConfig": {
                    "OriginAccessIdentity": ""
                }
            }]
        },
        "DefaultCacheBehavior": {
            "TargetOriginId": "S3-smart-canteen",
            "ViewerProtocolPolicy": "redirect-to-https",
            "AllowedMethods": {
                "Quantity": 2,
                "Items": ["GET", "HEAD"]
            }
        },
        "Enabled": true
    }
}
```

### 4. S3 Bucket for File Storage

```bash
# Create bucket for food images
aws s3 mb s3://smart-canteen-images

# Configure CORS
aws s3api put-bucket-cors \
    --bucket smart-canteen-images \
    --cors-configuration file://cors.json
```

`cors.json`:
```json
{
    "CORSRules": [{
        "AllowedOrigins": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST"],
        "AllowedHeaders": ["*"]
    }]
}
```

### 5. Environment Variables

Backend `.env`:
```bash
DATABASE_URL=postgresql://admin:password@your-rds-endpoint:5432/smart_canteen
SECRET_KEY=your-super-secret-key-generate-this
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=smart-canteen-images
OPENAI_API_KEY=your-openai-key
CORS_ORIGINS=https://your-cloudfront-domain.cloudfront.net
```

Frontend `.env`:
```bash
REACT_APP_API_URL=https://your-api-domain.com
```

### 6. Security Groups

```bash
# Backend security group
aws ec2 create-security-group \
    --group-name smart-canteen-backend \
    --description "Backend API security group"

# Allow HTTP
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Allow HTTPS
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxx \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Database security group
aws ec2 create-security-group \
    --group-name smart-canteen-db \
    --description "Database security group"

# Allow PostgreSQL from backend
aws ec2 authorize-security-group-ingress \
    --group-id sg-db-xxxxxxxx \
    --protocol tcp \
    --port 5432 \
    --source-group sg-backend-xxxxxxxx
```

## SSL Certificate (Optional)

```bash
# Request certificate
aws acm request-certificate \
    --domain-name canteen.yourdomain.com \
    --validation-method DNS

# Validate via DNS
# Add CNAME record to your DNS provider

# Wait for validation
aws acm describe-certificate --certificate-arn arn:aws:acm:...
```

## Monitoring & Logging

### CloudWatch

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/smart-canteen

# Set retention
aws logs put-retention-policy \
    --log-group-name /aws/smart-canteen \
    --retention-in-days 30
```

### Alarms

```bash
# CPU Utilization alarm
aws cloudwatch put-metric-alarm \
    --alarm-name smart-canteen-high-cpu \
    --alarm-description "Alert when CPU > 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold
```

## Backup Strategy

### Database Backups

```bash
# Configure automated backups
aws rds modify-db-instance \
    --db-instance-identifier smart-canteen-db \
    --backup-retention-period 7 \
    --preferred-backup-window "03:00-04:00"
```

### S3 Versioning

```bash
aws s3api put-bucket-versioning \
    --bucket smart-canteen-images \
    --versioning-configuration Status=Enabled
```

## Cost Optimization

1. **Use Free Tier**: t2.micro EC2, RDS db.t3.micro
2. **S3 Lifecycle Policies**: Archive old images to Glacier
3. **CloudFront Caching**: Reduce origin requests
4. **Reserved Instances**: For production workloads

## Deployment Checklist

- [ ] RDS PostgreSQL instance created
- [ ] Backend deployed and running
- [ ] Database migrations completed
- [ ] Frontend built and deployed to S3
- [ ] CloudFront distribution configured
- [ ] SSL certificate issued and attached
- [ ] Environment variables configured
- [ ] Security groups configured
- [ ] Monitoring and alarms set up
- [ ] Backup strategy implemented
- [ ] Domain DNS configured

## Useful Commands

```bash
# Check backend health
curl https://your-api-domain.com/health

# View logs
aws logs tail /aws/smart-canteen --follow

# Redeploy frontend
cd frontend && npm run build && aws s3 sync build/ s3://smart-canteen-frontend

# Restart backend
sudo systemctl restart smart-canteen

# Database migrations
cd backend && alembic upgrade head
```
