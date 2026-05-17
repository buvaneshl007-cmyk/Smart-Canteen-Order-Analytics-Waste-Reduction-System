# MySQL Local Setup Guide

## Quick Setup (5 minutes)

### Step 1: Install MySQL

**Download MySQL**:
- Go to: https://dev.mysql.com/downloads/installer/
- Download: **MySQL Installer for Windows**
- Choose: **mysql-installer-community** (larger file, recommended)

**Install**:
1. Run the installer
2. Choose setup type: **Developer Default** or **Server only**
3. Click **Next** through requirements
4. Configure MySQL Server:
   - Config Type: **Development Computer**
   - Port: **3306** (default)
   - Authentication: **Use Strong Password Encryption**
   - Root Password: Leave **EMPTY** or set a password
   - Click **Next** and **Execute**

### Step 2: Create Database

**Option A: Using MySQL Workbench** (Installed with MySQL):
1. Open **MySQL Workbench**
2. Connect to Local instance (root user)
3. Click **"Create new schema"** button
4. Schema name: `smart_canteen`
5. Click **Apply**

**Option B: Using Command Line**:
```bash
# Open Command Prompt or PowerShell
mysql -u root -p

# In MySQL prompt:
CREATE DATABASE smart_canteen;
EXIT;
```

**Option C: Using Quick Command**:
```bash
mysql -u root -e "CREATE DATABASE smart_canteen;"
```

### Step 3: Update Configuration

**Your .env is already configured!**

If root has a password, update `backend\.env`:
```env
# If root has NO password (default):
DATABASE_URL=mysql+pymysql://root:@localhost:3306/smart_canteen

# If root has a password:
DATABASE_URL=mysql+pymysql://root:YourPassword@localhost:3306/smart_canteen
```

### Step 4: Install MySQL Driver

```bash
cd "c:\Users\buvan\OneDrive\Documents\Smart canteen\backend"
pip install pymysql cryptography
```

### Step 5: Restart Backend

```bash
# Stop current backend (Ctrl+C)
# Then start:
python -m uvicorn app.main:app --reload
```

## ✅ Quick Verification

Test if MySQL is running:
```bash
# Check MySQL service
Get-Service MySQL* | Select-Object Name, Status

# Or try to connect
mysql -u root -p
```

## 🎯 Complete Setup Commands

```bash
# 1. Install MySQL driver
cd "c:\Users\buvan\OneDrive\Documents\Smart canteen\backend"
pip install pymysql cryptography

# 2. Create database (if MySQL installed)
mysql -u root -e "CREATE DATABASE smart_canteen;"

# 3. Restart backend
python -m uvicorn app.main:app --reload
```

## Common MySQL Configurations

### If you have a MySQL password:
```env
DATABASE_URL=mysql+pymysql://root:YourPassword@localhost:3306/smart_canteen
```

### Different username:
```env
DATABASE_URL=mysql+pymysql://myuser:mypass@localhost:3306/smart_canteen
```

### Different port:
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3307/smart_canteen
```

## Troubleshooting

### MySQL not installed?
1. Download from: https://dev.mysql.com/downloads/installer/
2. Or use XAMPP: https://www.apachefriends.org/
3. Or use WAMP: https://www.wampserver.com/

### Can't connect?
```bash
# Check if MySQL is running
Get-Service MySQL*

# Start MySQL service
net start MySQL80  # or MySQL57, MySQL
```

### Access denied?
- Reset root password in MySQL Workbench
- Or use different user credentials

### Port already in use?
- Change MySQL port in configuration
- Update .env with new port

## Alternative: Use XAMPP/WAMP

If you prefer XAMPP or WAMP:

**XAMPP**:
1. Download: https://www.apachefriends.org/
2. Install and start MySQL from control panel
3. Open phpMyAdmin
4. Create database: `smart_canteen`
5. Default credentials: root / (no password)

**Connection**:
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/smart_canteen
```

## 💰 Cost

**FREE** - Runs on your local machine!

## 🚀 You're Ready!

Once MySQL is installed and database created:
1. Backend will auto-create tables
2. Admin user will be created automatically
3. Login: admin@smartcanteen.com / admin123
4. Start adding menu items!
