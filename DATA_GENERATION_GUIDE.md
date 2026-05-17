# Smart Canteen System - Test Data & Analytics Guide

## 📊 Generated Data Summary

The system now contains **30 days** of realistic synthetic data:

### Database Contents:
- **👥 Users**: 52 total (2 owners + 50 customers)
- **🍽️ Menu Items**: 20 food items across 5 categories
- **📦 Orders**: 4,190 completed orders
- **📋 Order Items**: 8,438 individual items ordered
- **📊 Sales Analytics**: 6,199 records
- **🗑️ Wastage Records**: 620 daily preparation records

---

## 🔑 Login Credentials

### Owner Account:
- **Email**: `owner@canteen.com`
- **Password**: `owner123`

### Customer Accounts:
- **Password** (for all 50 customers): `customer123`
- Emails are randomly generated (check database)

---

## 📈 Key Insights from Generated Data

### Top 5 Selling Items:
1. **Cutlet**: 1,025 units
2. **Samosa**: 1,012 units
3. **Veg Puff**: 992 units
4. **Coffee**: 935 units
5. **Tea**: 920 units

### Peak Selling Hours:
- **10:00 AM**: 1,999 items (Morning Snack Peak)
- **11:00 AM**: 1,971 items (Late Morning)
- **1:00 PM**: 1,398 items (Lunch Peak)

### Items with Highest Waste:
1. **Tea**: 1,209 units wasted
2. **Poori**: 1,147 units wasted (consistently low demand)
3. **Milk**: 1,111 units wasted
4. **Badam Milk**: 1,106 units wasted
5. **Coffee**: 1,099 units wasted

---

## 🤖 AI Assistant Test Queries

The AI Assistant can answer questions like these:

### Sales Analysis:
```
"What food sells the most on Monday?"
"Which item has the highest sales?"
"Show me the top 5 selling items"
"What are the least popular items?"
```

### Time-based Insights:
```
"What item has the highest demand at 10 AM?"
"When is the busiest hour of the day?"
"What sells most during lunch time?"
"Show peak hours for sales"
```

### Predictions & Recommendations:
```
"What should I prepare tomorrow morning?"
"How much Veg Puff should I prepare for Monday?"
"Give me preparation recommendations for breakfast items"
"What items should I stock more of?"
```

### Waste Management:
```
"Which food causes the most waste?"
"What items am I over-preparing?"
"Show me the wastage analysis"
"How can I reduce food waste?"
```

### Day-of-Week Patterns:
```
"What day has the highest sales?"
"Compare Monday vs Saturday sales"
"What items sell better on Fridays?"
```

### Revenue & Profitability:
```
"What's my total revenue this month?"
"Which category generates most revenue?"
"What's the revenue from beverages?"
```

---

## 🎯 Realistic Patterns Implemented

### Time-based Demand:
- **7:30 AM - 9:30 AM**: Breakfast items (Idli, Dosa, Poori, Upma)
- **10:00 AM - 11:30 AM**: Snacks & Beverages (Veg Puff, Samosa, Tea, Coffee)
- **12:30 PM - 2:30 PM**: Lunch items (Veg Biryani, Rice varieties)
- **4:30 PM - 6:30 PM**: Evening snacks (Tea, Coffee, Cutlet)

### Day-of-Week Patterns:
- **Monday**: 30% higher demand (start of week)
- **Tuesday-Thursday**: Normal demand
- **Friday**: 20% higher demand (end of week)
- **Saturday**: 30% lower demand
- **Sunday**: 50% lower demand

### Item-Specific Patterns:
- **Veg Puff**: High demand on Monday mornings
- **Tea/Coffee**: Consistent demand throughout the day
- **Veg Biryani**: Peak demand during lunch (12-2 PM)
- **Poori**: Consistently low demand (high waste)
- **Samosa**: Popular in evening hours

---

## 📱 Testing the Application

### 1. Access the Application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 2. Test Customer Flow:
1. Sign up as a new customer
2. Browse menu items
3. Add items to cart
4. Place an order
5. View order history

### 3. Test Owner Dashboard:
1. Login with owner credentials
2. View analytics dashboard
3. Check sales charts
4. View live orders
5. Manage menu items
6. Check wastage reports
7. Use AI Assistant

### 4. Test AI Assistant:
1. Login as owner
2. Navigate to "AI Assistant" page
3. Ask questions from the list above
4. Get insights and recommendations

**Note**: AI Assistant requires Gemini API key in `.env`:
```
GEMINI_API_KEY=your-actual-api-key
```
Get free API key from: https://makersuite.google.com/app/apikey

---

## 📊 Analytics Dashboard Features

The owner dashboard should display:

### Sales Overview:
- Total revenue
- Total orders
- Average order value
- Growth trends

### Top Performers:
- Best selling items
- Revenue by category
- Peak hours chart
- Day-of-week comparison

### Wastage Analysis:
- Items with highest waste
- Wastage trends over time
- Preparation efficiency
- Cost of wasted food

### Demand Prediction:
- ML-based predictions for next day
- Recommended preparation quantities
- Seasonal trends
- Pattern recognition

---

## 🧪 Sample API Endpoints to Test

### Authentication:
```bash
# Signup
POST http://localhost:8000/api/auth/signup

# Login
POST http://localhost:8000/api/auth/login
```

### Menu:
```bash
# Get all menu items
GET http://localhost:8000/api/menu/

# Get item by ID
GET http://localhost:8000/api/menu/1
```

### Orders:
```bash
# Place order
POST http://localhost:8000/api/orders/

# Get my orders
GET http://localhost:8000/api/orders/my-orders
```

### Analytics (Owner only):
```bash
# Get sales analytics
GET http://localhost:8000/api/analytics/sales

# Get top items
GET http://localhost:8000/api/analytics/top-items

# Get demand prediction
GET http://localhost:8000/api/analytics/predict-demand
```

### AI Assistant (Owner only):
```bash
# Query AI
POST http://localhost:8000/api/ai/query
Body: {"query": "What sells most on Monday?"}
```

---

## 🔄 Regenerate Data

If you want to regenerate fresh data:

```bash
cd backend
python reset_db.py    # Clear old data
python generate_data.py    # Generate new data
```

---

## 📋 Data Validation Checklist

✅ **Users**: Owner + 50 customers created
✅ **Menu**: 20 items across breakfast, lunch, snacks, beverages
✅ **Orders**: ~4,000+ orders with realistic timestamps
✅ **Time Patterns**: Peak hours at 10 AM, 1 PM, 5 PM
✅ **Day Patterns**: Higher sales on weekdays, lower on weekends
✅ **Analytics**: Sales records with day/hour breakdown
✅ **Wastage**: Daily preparation records with waste tracking
✅ **Variety**: 1-3 items per order, quantities 1-3
✅ **Realism**: Items matched to appropriate time slots

---

## 🎨 Visualization Recommendations

### Charts to Implement:
1. **Line Chart**: Sales trend over 30 days
2. **Bar Chart**: Top 10 selling items
3. **Pie Chart**: Revenue by category
4. **Heatmap**: Sales by day & hour
5. **Doughnut Chart**: Order status distribution
6. **Area Chart**: Wastage trends
7. **Horizontal Bar**: Top wasted items

### Libraries to Use:
- **Frontend**: Chart.js (already included)
- **Backend**: Matplotlib, Plotly (optional)

---

## 🚀 Next Steps

1. ✅ Data generated successfully
2. ⏳ Configure Gemini API key for AI features
3. ⏳ Test analytics dashboard
4. ⏳ Train ML demand prediction model
5. ⏳ Test all AI queries
6. ⏳ Verify charts and visualizations
7. ⏳ Test real-time WebSocket updates

---

## 📞 Support

If you encounter any issues:
1. Check backend logs in terminal
2. Verify database connection
3. Ensure MySQL is running
4. Check .env configuration
5. Review API documentation at `/docs`

---

**Generated on**: ${new Date().toLocaleDateString()}
**Database**: MySQL (smart_canteen)
**Backend**: Running on port 8000
**Frontend**: Running on port 3000
