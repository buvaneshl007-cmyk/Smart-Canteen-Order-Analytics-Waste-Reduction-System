# AWS RDS MySQL Setup Guide

Use this guide to move from local MySQL to Amazon RDS MySQL.

## 1. Create RDS MySQL Instance

1. Open AWS Console -> RDS -> Create database.
2. Choose:
- Engine: MySQL
- Version: MySQL 8.0.x
- Template: Free tier (or Production)
3. Set:
- DB instance identifier: smart-canteen-db
- Master username: admin
- Master password: strong password
- DB class: db.t3.micro (free tier) or higher
- Storage: 20 GB gp3 (or gp2)
4. Connectivity:
- Public access: Yes (for testing)
- Security group: allow inbound TCP 3306 from your IP
5. Additional configuration:
- Initial database name: smart_canteen

Wait until status is Available.

## 2. Update Backend Environment

Edit backend/.env and set:

DATABASE_URL=mysql+pymysql://admin:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:3306/smart_canteen
DB_POOL_PRE_PING=True
DB_POOL_RECYCLE=1800
DB_CONNECT_TIMEOUT=10

Optional SSL verification:

DB_SSL_CA=/absolute/path/to/global-bundle.pem

If you do not verify CA yet, keep DB_SSL_CA empty.

## 3. Restart Backend

From backend folder:

python -m uvicorn app.main:app --reload

## 4. Verify Connection

1. Open http://localhost:8000/docs
2. Login and call analytics endpoints.
3. If needed, run generate_data.py to create test data in RDS.

## 5. AWS CLI Alternative

Create RDS MySQL with CLI:

aws rds create-db-instance \
  --db-instance-identifier smart-canteen-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0.39 \
  --master-username admin \
  --master-user-password YourStrongPassword123 \
  --allocated-storage 20 \
  --db-name smart_canteen \
  --publicly-accessible \
  --backup-retention-period 7 \
  --region us-east-1

Allow MySQL port in SG:

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 3306 \
  --cidr YOUR_PUBLIC_IP/32

## Troubleshooting

### Cannot connect
- Confirm RDS status is Available.
- Confirm SG inbound allows TCP 3306 from your IP.
- Confirm DATABASE_URL username/password/endpoint are correct.
- Confirm database name smart_canteen exists.

### Connection drops/timeouts
- Keep DB_POOL_PRE_PING=True.
- Increase DB_CONNECT_TIMEOUT (for unstable networks).
- Ensure RDS is in same region as app host when deployed.

### SSL issues
- Set DB_SSL_CA only if you have the CA bundle path.
- Leave DB_SSL_CA empty for initial connectivity test.

## Notes

- This project uses PyMySQL driver, so use mysql+pymysql URL format.
- You are still using MySQL, but now hosted on AWS (cloud-managed).
