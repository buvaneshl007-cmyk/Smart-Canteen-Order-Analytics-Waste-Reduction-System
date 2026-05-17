# 🍽️ Smart Canteen System

A comprehensive full-stack canteen management system with AI-powered analytics, ML demand prediction, and real-time order management.

## 🌟 Features

### For Customers:
- 🔐 User authentication (signup/login)
- 📋 Browse menu items by category
- 🛒 Shopping cart functionality
- 📦 Place and track orders in real-time
- 📜 View complete order history
- ⚡ Live order status updates via WebSocket

### For Owners:
- 📊 **Comprehensive Analytics Dashboard**
  - Sales trends with interactive charts
  - Revenue breakdown by category
  - Top selling items analysis
  - Peak hours and day-of-week patterns
  
- 🤖 **AI Assistant** (Powered by Google Gemini)
  - Natural language query support
  - Data-driven business insights
  - Smart recommendations
  
- 🔮 **ML Demand Prediction**
  - Random Forest algorithm
  - Historical pattern analysis
  - Preparation quantity recommendations
  
- 🗑️ **Food Wastage Tracking**
  - Daily preparation vs sales analysis
  - Identify over-prepared items
  - Cost optimization insights
  
- 📱 **Live Order Management**
  - Real-time WebSocket updates
  - Order status management
  - Menu item control
  
---

## 🛠️ Technology Stack

### Frontend:
- React 18.2.0
- TailwindCSS - Modern styling
- Chart.js - Data visualization
- Axios - HTTP client
- React Router - Navigation  
- Lucide React - Beautiful icons

### Backend:
- FastAPI 0.109.0 - High-performance Python framework
- SQLAlchemy 2.0.25 - Powerful ORM
- PyMySQL - MySQL database driver
- JWT - Secure authentication
- Bcrypt - Password encryption
- Uvicorn - Lightning-fast ASGI server

### Database:
- MySQL 8.0 (Local or AWS RDS)
- Database name: `smart_canteen`

### AI & Machine Learning:
- **Google Gemini API** - AI-powered insights
- **Scikit-learn** - ML demand prediction
- **Pandas/Numpy** - Data processing

---

## 📦 Quick Start

### Prerequisites:
- Python 3.10+
- Node.js 16+
- MySQL 8.0
- Git

### 1. Backend Setup:
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment (edit .env file)
# Local MySQL:
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/smart_canteen
# OR AWS RDS MySQL:
# DATABASE_URL=mysql+pymysql://admin:your_password@your-rds-endpoint.us-east-1.rds.amazonaws.com:3306/smart_canteen
DB_POOL_PRE_PING=True
DB_POOL_RECYCLE=1800
DB_CONNECT_TIMEOUT=10
GEMINI_API_KEY=your-gemini-api-key

# Create database
mysql -u root -p
CREATE DATABASE smart_canteen;
EXIT;

# Generate realistic test data (30 days worth!)
python generate_data.py

# Start backend server
python -m uvicorn app.main:app --reload
```
**Backend runs on:** http://localhost:8000

### 2. Frontend Setup:
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```
**Frontend runs on:** http://localhost:3000

---

## 🔑 Login Credentials

### Owner Account:
- **Email:** `owner@canteen.com`
- **Password:** `owner123`

### Customer Accounts:
- **Password:** `customer123` (for all 50 generated customers)
- Check database or signup as new customer

---

## 📊 Generated Test Data

The system includes **30 days** of realistic operational data:

- ✅ **52 Users** (2 owners + 50 customers)
- ✅ **20 Menu Items** (breakfast, lunch, snacks, beverages)
- ✅ **4,190 Orders** (with realistic time patterns)
- ✅ **8,438 Order Items**
- ✅ **6,199 Sales Analytics Records**
- ✅ **620 Food Preparation/Wastage Records**

### Top Insights:
- **Best Sellers:** Cutlet (1,025), Samosa (1,012), Veg Puff (992)
- **Peak Hours:** 10 AM (1,999 items), 11 AM (1,971), 1 PM (1,398)
- **High Waste Items:** Tea, Poori, Milk, Badam Milk

---

## 🗂️ Project Structure

```
Smart canteen/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── auth.py       # Authentication
│   │   │   ├── menu.py       # Menu management
│   │   │   ├── orders.py     # Order processing
│   │   │   ├── analytics.py  # Sales analytics
│   │   │   ├── ai_assistant.py  # AI queries
│   │   │   └── wastage.py    # Wastage tracking
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── ai_service.py    # Gemini AI
│   │   │   └── ml_service.py    # ML predictions
│   │   └── main.py           # FastAPI app
│   ├── .env
│   ├── requirements.txt
│   ├── generate_data.py      # Data generator
│   └── reset_db.py           # DB reset script
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── Menu.js
│   │   │   ├── Cart.js
│   │   │   ├── Orders.js
│   │   │   ├── Dashboard.js        # Owner dashboard
│   │   │   ├── MenuManagement.js   # Manage menu
│   │   │   ├── LiveOrders.js       # Live tracking
│   │   │   ├── Analytics.js        # Charts & insights
│   │   │   ├── AIAssistant.js      # AI chat
│   │   │   └── WastageManagement.js
│   │   ├── components/
│   │   ├── context/
│   │   └── services/
│   └── package.json
│
├── README.md
└── DATA_GENERATION_GUIDE.md  # Testing manual
```

---

## 🤖 AI Assistant Features

Ask questions like:
```
"What food sells the most on Monday?"
"Which item has the highest demand at 10 AM?"
"What should I prepare tomorrow morning?"
"Which food causes the most waste?"
"Show me top 5 selling items"
"When is the busiest hour?"
```

**Setup:** Get free API key from https://makersuite.google.com/app/apikey

---

## 📈 Analytics & Insights

The dashboard provides:
- 📊 Sales trends (line charts)
- 🥇 Top selling items (bar charts)
- 💰 Revenue by category (pie charts)
- 🕐 Peak hours heatmap
- 📅 Day-of-week patterns
- 🗑️ Wastage analysis
- 🔮 Next-day predictions

---

## 📡 API Endpoints

### Authentication:
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Current user

### Menu:
- `GET /api/menu/` - All items
- `POST /api/menu/` - Create (owner)
- `PUT /api/menu/{id}` - Update (owner)
- `DELETE /api/menu/{id}` - Delete (owner)

### Orders:
- `POST /api/orders/` - Place order
- `GET /api/orders/my-orders` - User orders
- `GET /api/orders/all` - All orders (owner)
- `PUT /api/orders/{id}/status` - Update status (owner)

### Analytics (Owner):
- `GET /api/analytics/sales` - Sales data
- `GET /api/analytics/top-items` - Top sellers
- `GET /api/analytics/predict-demand` - ML predictions

### AI Assistant (Owner):
- `POST /api/ai/query` - Ask AI

**Full API docs:** http://localhost:8000/docs

---

## 🧪 Testing

1. **Access Application:** http://localhost:3000
2. **Login as Owner:** owner@canteen.com / owner123
3. **Explore Dashboard:** View charts and analytics
4. **Test AI:** Ask natural language questions
5. **Check Predictions:** View ML recommendations
6. **Manage Orders:** Update statuses in real-time

See `DATA_GENERATION_GUIDE.md` for detailed testing scenarios.

---

## 🔧 Configuration (.env)

```env
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/smart_canteen

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI
GEMINI_API_KEY=your-gemini-api-key

# AWS (Optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=smart-canteen

# App
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

---

## 🐛 Troubleshooting

**Backend won't start?**
- Check MySQL is running: `Get-Service MySQL*`
- Verify .env configuration
- Ensure database exists

**Frontend issues?**
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

**Database errors?**
- Reset: `python reset_db.py`
- Regenerate: `python generate_data.py`

---

## 📝 Future Enhancements

- [ ] QR code table ordering
- [ ] Payment gateway integration  
- [ ] Push notifications
- [ ] Mobile app (React Native)
- [ ] Multi-location support
- [ ] Loyalty rewards program
- [ ] Inventory auto-ordering
- [ ] Supplier management

---

## 📄 License

MIT License

---

## 👨‍💻 Developer

**Buvan**  
Smart Canteen Management System  
March 2026

---

**Built with ❤️ using React, FastAPI, MySQL, and AI**
