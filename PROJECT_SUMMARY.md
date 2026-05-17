# 🍽️ Smart Canteen System

A comprehensive AI-powered canteen management system built with React, FastAPI, and PostgreSQL. Features include order management, real-time analytics, demand prediction, and an AI assistant to help reduce food wastage.

![Smart Canteen](https://via.placeholder.com/800x400/f59e0b/ffffff?text=Smart+Canteen+System)

## ✨ Features

### For Customers
- 🛒 **Browse Menu** - View available food items with categories and prices
- 🛍️ **Shopping Cart** - Add items, adjust quantities, and place orders
- 📱 **Order Tracking** - Real-time order status updates
- 📜 **Order History** - View past orders and receipts
- ⚡ **Real-time Updates** - Menu changes reflect instantly

### For Owners
- 📊 **Analytics Dashboard** - Comprehensive sales analytics with charts
- 📈 **Daily/Weekly Reports** - Revenue trends and sales patterns
- ⏰ **Peak Hour Analysis** - Identify busy times
- 🎯 **Item Performance** - Track best and worst sellers
- 🤖 **AI Assistant** - Ask questions about your data
- 🔮 **Demand Prediction** - ML-powered forecasting for tomorrow
- 📋 **Menu Management** - Add, edit, delete menu items
- 🔔 **Live Orders** - Real-time order monitoring with status updates
- 🗑️ **Wastage Tracking** - Monitor and reduce food waste

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### Installation

#### Option 1: Automated Setup (Windows)
```bash
# Run the setup script
setup.bat
```

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your database credentials
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
copy .env.example .env
npm start
```

### Default Credentials
- **Owner**: admin@smartcanteen.com / admin123
- **Customer**: Create via signup page

## 📁 Project Structure

```
smart-canteen/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── models/   # Database models
│   │   └── services/ # ML & AI services
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   └── services/
│   └── package.json
├── AWS_DEPLOYMENT.md
├── DEVELOPER_GUIDE.md
└── README.md
```

## 🛠️ Tech Stack

### Frontend
- **React** - UI framework
- **TailwindCSS** - Styling
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation
- **React Hot Toast** - Notifications

### Backend
- **FastAPI** - API framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **JWT** - Authentication
- **bcrypt** - Password hashing
- **scikit-learn** - ML predictions
- **OpenAI** - AI assistant

### Cloud (AWS)
- **RDS** - PostgreSQL database
- **S3** - File storage
- **EC2/Lambda** - Backend hosting
- **CloudFront** - CDN

## 📊 Features Overview

### 1. Analytics Dashboard
- Daily revenue trends (7/14/30 days)
- Sales by day of week
- Hourly sales patterns
- Top selling items
- Item performance metrics

### 2. ML Demand Prediction
- Random Forest algorithm
- Predicts tomorrow's demand
- Considers:
  - Day of week patterns
  - Hour-based trends
  - Historical sales data
  - Seasonal variations

### 3. AI Assistant
- Natural language queries
- Pattern analysis
- Wastage insights
- Actionable recommendations

Example questions:
- "What sells most on Monday?"
- "When does Veg Puff peak?"
- "Which items cause wastage?"
- "What should I prepare tomorrow?"

### 4. Real-Time Features
- WebSocket connections
- Live order updates
- Instant menu changes
- Order status notifications

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:5432/smart_canteen
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 📖 API Documentation

Once running, access interactive API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Deployment

See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for comprehensive AWS deployment guide including:
- RDS setup
- EC2/Lambda configuration
- S3 + CloudFront deployment
- Security groups
- SSL certificates
- Monitoring

## 📸 Screenshots

### Customer View
- **Menu Page**: Browse items with search and category filters
- **Cart**: Review and modify orders before checkout
- **Orders**: Track order status and history

### Owner View
- **Dashboard**: Visual analytics with charts
- **Live Orders**: Real-time order management
- **Menu Management**: CRUD operations for items
- **AI Assistant**: Interactive Q&A interface
- **Analytics**: Detailed reports and predictions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For help and questions:
- Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- Check API docs at `/docs`
- Open an issue

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Payment gateway integration
- [ ] Multi-location support
- [ ] Inventory management
- [ ] Email/SMS notifications
- [ ] Customer ratings & reviews
- [ ] Loyalty program
- [ ] Advanced reporting (PDF export)
- [ ] Recipe management
- [ ] Supplier integration

## 👥 Team

Built with ❤️ for canteen owners who want to reduce waste and increase profits through data-driven decisions.

---

**Made with React, FastAPI, and AI** 🚀
