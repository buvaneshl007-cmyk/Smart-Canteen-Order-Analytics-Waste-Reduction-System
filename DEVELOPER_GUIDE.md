# Smart Canteen System - Developer Guide

## Quick Start Guide

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd smart-canteen
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your configuration
# At minimum, update:
# - DATABASE_URL
# - SECRET_KEY
```

#### Database Setup

```bash
# If using PostgreSQL locally:
# 1. Install PostgreSQL
# 2. Create database
psql -U postgres
CREATE DATABASE smart_canteen;
\q

# Update DATABASE_URL in .env:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_canteen

# Run migrations (database will be auto-created by app)
```

#### Run Backend

```bash
uvicorn app.main:app --reload

# API will be available at: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

**Default Admin Credentials:**
- Email: `admin@smartcanteen.com`
- Password: `admin123`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start development server
npm start

# App will open at: http://localhost:3000
```

## Project Structure

```
smart-canteen/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── auth.py       # Authentication
│   │   │   ├── menu.py       # Menu management
│   │   │   ├── orders.py     # Order management
│   │   │   ├── analytics.py  # Analytics endpoints
│   │   │   ├── ai_assistant.py # AI queries
│   │   │   └── wastage.py    # Food wastage tracking
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings
│   │   │   ├── database.py   # DB connection
│   │   │   └── security.py   # Auth utilities
│   │   ├── models/           # Database models
│   │   │   ├── models.py     # SQLAlchemy models
│   │   │   └── schemas.py    # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── ml_service.py # ML predictions
│   │   │   └── ai_service.py # AI assistant
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   │   └── Navbar.js
│   │   ├── context/          # React context
│   │   │   ├── AuthContext.js
│   │   │   └── CartContext.js
│   │   ├── pages/            # Page components
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── Menu.js
│   │   │   ├── Cart.js
│   │   │   ├── Orders.js
│   │   │   └── owner/        # Owner pages
│   │   │       ├── Dashboard.js
│   │   │       ├── MenuManagement.js
│   │   │       ├── LiveOrders.js
│   │   │       └── AIAssistant.js
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
└── README.md
```

## Features Implementation

### 1. Authentication

**Endpoints:**
- `POST /auth/signup` - Customer registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

**Security:**
- JWT tokens
- bcrypt password hashing
- Role-based access control (Owner/Customer)

### 2. Menu Management (Owner)

**Endpoints:**
- `GET /menu` - Get all menu items
- `POST /menu` - Create menu item (Owner)
- `PUT /menu/{id}` - Update menu item (Owner)
- `DELETE /menu/{id}` - Delete menu item (Owner)
- `PATCH /menu/{id}/availability` - Toggle availability (Owner)

**Features:**
- Add/Edit/Delete items
- Set prices and categories
- Upload images
- Enable/Disable availability
- Real-time updates to customers

### 3. Order Management

**Endpoints:**
- `POST /orders` - Place order (Customer)
- `GET /orders` - Get user's orders
- `GET /orders/live` - Get pending orders (Owner)
- `PATCH /orders/{id}/status` - Update status (Owner)

**Order Statuses:**
- Pending → Preparing → Ready → Completed

**Features:**
- Shopping cart
- Order placement
- Order history
- Live order tracking
- Status updates

### 4. Analytics Dashboard (Owner)

**Endpoints:**
- `GET /analytics/daily` - Daily sales
- `GET /analytics/weekly` - Sales by day of week
- `GET /analytics/time` - Hourly sales
- `GET /analytics/items` - Item performance

**Visualizations:**
- Daily revenue trend (Line chart)
- Weekly sales comparison (Bar chart)
- Top items distribution (Pie chart)
- Hourly pattern analysis (Line chart)
- Item performance table

**Metrics:**
- Total revenue
- Total orders
- Average order value
- Peak hours
- Top selling items

### 5. Demand Prediction (ML)

**Endpoint:**
- `GET /analytics/predict` - Tomorrow's demand forecast

**Algorithm:**
- Random Forest Regressor
- Features: day of week, hour, historical patterns
- Fallback to averages for new items

**Output:**
- Predicted quantity for each item
- Confidence level

### 6. AI Assistant (Owner)

**Endpoint:**
- `POST /ai/query` - Ask questions

**Capabilities:**
- Natural language Q&A
- Sales pattern analysis
- Wastage insights
- Recommendations

**Example Queries:**
- "What food sells most on Monday?"
- "What time does Veg Puff sell?"
- "Which items cause wastage?"
- "What should I prepare tomorrow?"

### 7. Food Wastage Tracking

**Endpoints:**
- `POST /wastage` - Record wastage (Owner)
- `GET /wastage` - Get wastage history
- `GET /wastage/item/{id}` - Item wastage

**Tracks:**
- Cooked quantity
- Sold quantity
- Wasted quantity
- Historical patterns

## API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users
- user_id, name, email, password, role, created_at

### Menu Items
- item_id, item_name, price, category, description, image_url, available, created_by_owner, created_at

### Orders
- order_id, user_id, order_time, total_price, status

### Order Items
- order_item_id, order_id, item_id, quantity, price_at_order

### Sales Analytics
- id, item_id, date, day_of_week, hour, quantity_sold, revenue

### Food Wastage
- wastage_id, item_id, date, cooked_quantity, sold_quantity, wasted_quantity

## Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## Common Issues & Solutions

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
# Format: postgresql://username:password@host:port/database
```

### CORS Errors
```bash
# Update CORS_ORIGINS in backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Module Not Found
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Port Already in Use
```bash
# Backend (change port)
uvicorn app.main:app --port 8001

# Frontend (change port)
PORT=3001 npm start
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/smart_canteen
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=canteen-bucket
OPENAI_API_KEY=your-openai-key
DEBUG=True
CORS_ORIGINS=http://localhost:3000
DEFAULT_ADMIN_EMAIL=admin@smartcanteen.com
DEFAULT_ADMIN_PASSWORD=admin123
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
```

## Production Deployment

See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for detailed AWS deployment guide.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: <your-repo-url>/issues
- Email: support@smartcanteen.com

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Payment integration
- [ ] Multi-location support
- [ ] Inventory management
- [ ] Supplier integration
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Advanced reporting
- [ ] Customer feedback system
- [ ] Loyalty program
