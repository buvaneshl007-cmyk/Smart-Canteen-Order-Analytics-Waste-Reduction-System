import google.generativeai as genai
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.models import SalesAnalytics, MenuItem, Order, FoodWastage
from datetime import datetime, timedelta
from typing import Dict, Any
import json


# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None


def get_analytics_context(db: Session) -> Dict[str, Any]:
    """Get comprehensive analytics context for AI"""
    
    # Top selling items
    top_items = db.query(
        MenuItem.item_name,
        func.sum(SalesAnalytics.quantity_sold).label("total_sold"),
        func.sum(SalesAnalytics.revenue).label("total_revenue")
    ).join(
        SalesAnalytics, MenuItem.item_id == SalesAnalytics.item_id
    ).group_by(
        MenuItem.item_name
    ).order_by(
        desc("total_sold")
    ).limit(5).all()
    
    # Sales by day of week
    day_sales = db.query(
        SalesAnalytics.day_of_week,
        func.sum(SalesAnalytics.quantity_sold).label("total_sold")
    ).group_by(
        SalesAnalytics.day_of_week
    ).all()
    
    # Peak hours
    hour_sales = db.query(
        SalesAnalytics.hour,
        func.sum(SalesAnalytics.quantity_sold).label("total_sold")
    ).group_by(
        SalesAnalytics.hour
    ).order_by(
        desc("total_sold")
    ).limit(3).all()
    
    # Recent wastage
    wastage = db.query(
        MenuItem.item_name,
        func.sum(FoodWastage.wasted_quantity).label("total_wasted")
    ).join(
        FoodWastage, MenuItem.item_id == FoodWastage.item_id
    ).group_by(
        MenuItem.item_name
    ).order_by(
        desc("total_wasted")
    ).limit(5).all()

    # Weekly and monthly trend data based on latest available date
    latest_date = db.query(func.max(SalesAnalytics.date)).scalar()
    weekly_sales = []
    week_comparison = {"this_week_qty": 0, "last_week_qty": 0, "growth_pct": 0.0}
    monthly_summary = {
        "total_qty": 0,
        "total_revenue": 0.0,
        "avg_daily_qty": 0.0,
        "best_day": None,
    }

    if latest_date:
        week_start = latest_date - timedelta(days=6)
        month_start = latest_date - timedelta(days=29)
        previous_week_start = latest_date - timedelta(days=13)
        previous_week_end = latest_date - timedelta(days=7)

        weekly_sales = db.query(
            func.date(SalesAnalytics.date).label("sales_date"),
            func.sum(SalesAnalytics.quantity_sold).label("total_sold"),
            func.sum(SalesAnalytics.revenue).label("total_revenue"),
        ).filter(
            SalesAnalytics.date >= week_start
        ).group_by(
            func.date(SalesAnalytics.date)
        ).order_by(
            func.date(SalesAnalytics.date)
        ).all()

        this_week_qty = db.query(
            func.coalesce(func.sum(SalesAnalytics.quantity_sold), 0)
        ).filter(
            SalesAnalytics.date >= week_start
        ).scalar() or 0

        last_week_qty = db.query(
            func.coalesce(func.sum(SalesAnalytics.quantity_sold), 0)
        ).filter(
            SalesAnalytics.date >= previous_week_start,
            SalesAnalytics.date < previous_week_end
        ).scalar() or 0

        growth_pct = 0.0
        if last_week_qty > 0:
            growth_pct = ((this_week_qty - last_week_qty) / last_week_qty) * 100

        week_comparison = {
            "this_week_qty": int(this_week_qty),
            "last_week_qty": int(last_week_qty),
            "growth_pct": float(growth_pct),
        }

        monthly_totals = db.query(
            func.coalesce(func.sum(SalesAnalytics.quantity_sold), 0).label("total_qty"),
            func.coalesce(func.sum(SalesAnalytics.revenue), 0).label("total_revenue"),
            func.count(func.distinct(func.date(SalesAnalytics.date))).label("active_days"),
        ).filter(
            SalesAnalytics.date >= month_start
        ).one()

        monthly_best_day = db.query(
            SalesAnalytics.day_of_week,
            func.sum(SalesAnalytics.quantity_sold).label("total_sold"),
        ).filter(
            SalesAnalytics.date >= month_start
        ).group_by(
            SalesAnalytics.day_of_week
        ).order_by(
            desc("total_sold")
        ).first()

        active_days = int(monthly_totals.active_days or 0)
        total_qty = int(monthly_totals.total_qty or 0)
        avg_daily_qty = (total_qty / active_days) if active_days > 0 else 0.0

        monthly_summary = {
            "total_qty": total_qty,
            "total_revenue": float(monthly_totals.total_revenue or 0),
            "avg_daily_qty": float(avg_daily_qty),
            "best_day": {
                "day": monthly_best_day.day_of_week,
                "quantity": int(monthly_best_day.total_sold),
            } if monthly_best_day else None,
        }
    
    context = {
        "top_selling_items": [
            {
                "name": item.item_name,
                "quantity_sold": int(item.total_sold),
                "revenue": float(item.total_revenue)
            }
            for item in top_items
        ],
        "sales_by_day": [
            {
                "day": day.day_of_week,
                "quantity": int(day.total_sold)
            }
            for day in day_sales
        ],
        "peak_hours": [
            {
                "hour": hour.hour,
                "quantity": int(hour.total_sold)
            }
            for hour in hour_sales
        ],
        "wastage_items": [
            {
                "name": item.item_name,
                "wasted": int(item.total_wasted)
            }
            for item in wastage
        ] if wastage else [],
        "weekly_sales": [
            {
                "date": str(day.sales_date),
                "quantity": int(day.total_sold),
                "revenue": float(day.total_revenue or 0),
            }
            for day in weekly_sales
        ],
        "week_comparison": week_comparison,
        "monthly_summary": monthly_summary,
    }
    
    return context


def query_ai_assistant(query: str, db: Session) -> str:
    """Process natural language query using AI"""
    
    # If Gemini is not configured, use local analysis
    if not model:
        return analyze_query_locally(query, db)
    
    # Get analytics context
    context = get_analytics_context(db)
    
    # Create system prompt with context
    system_prompt = f"""You are a Smart Canteen analytics assistant. Help the canteen owner make data-driven decisions.

Current Analytics Data:

**Top Selling Items:**
{json.dumps(context['top_selling_items'], indent=2)}

**Sales by Day of Week:**
{json.dumps(context['sales_by_day'], indent=2)}

**Peak Selling Hours:**
{json.dumps(context['peak_hours'], indent=2)}

**Food Wastage:**
{json.dumps(context['wastage_items'], indent=2)}

Provide clear, actionable insights based on this data. Be specific with numbers and recommendations. Use emojis to make responses engaging.
"""
    
    try:
        # Combine system prompt and user query for Gemini
        full_prompt = f"{system_prompt}\n\nUser Question: {query}"
        
        response = model.generate_content(full_prompt)
        
        return response.text
    
    except Exception as e:
        # Fallback to local analysis on error
        print(f"Gemini AI error: {str(e)}, using local analysis")
        return analyze_query_locally(query, db)


def analyze_query_locally(query: str, db: Session) -> str:
    """Fallback local analysis when AI is not available"""
    query_lower = query.lower()
    context = get_analytics_context(db)
    
    # Peak Hour/Time Analysis
    if any(word in query_lower for word in ["peak hour", "busiest time", "peak time", "hourly"]):
        peak_hours = context['peak_hours']
        if peak_hours:
            peak = peak_hours[0]
            hours_list = ", ".join([f"{h['hour']}:00 ({h['quantity']} items)" for h in peak_hours])
            return f"📊 **Peak Hours Analysis:**\n\nBusiest time: {peak['hour']}:00 with {peak['quantity']} items sold\n\nAll peak hours:\n{hours_list}\n\n💡 Tip: Ensure maximum staff and inventory during these times!"

    # Weekly Analysis
    if any(word in query_lower for word in ["week", "weekly", "this week", "last week", "week over week"]):
        weekly_data = context.get('weekly_sales', [])
        comparison = context.get('week_comparison', {})

        if weekly_data:
            weekly_lines = "\n".join([
                f"- {entry['date']}: {entry['quantity']} items (₹{entry['revenue']:.2f})"
                for entry in weekly_data
            ])
            growth = comparison.get('growth_pct', 0.0)
            growth_text = "up" if growth >= 0 else "down"
            return (
                "📆 **Weekly Sales Analysis:**\n\n"
                f"This week: {comparison.get('this_week_qty', 0)} items\n"
                f"Last week: {comparison.get('last_week_qty', 0)} items\n"
                f"Week-over-week: {abs(growth):.1f}% {growth_text}\n\n"
                f"Daily breakdown:\n{weekly_lines}\n\n"
                "💡 Plan staffing based on high-volume days this week."
            )

    # Monthly Analysis
    if any(word in query_lower for word in ["month", "monthly", "this month", "monthly summary"]):
        monthly = context.get('monthly_summary', {})
        best_day = monthly.get('best_day')
        best_day_text = (
            f"{best_day['day']} ({best_day['quantity']} items)"
            if best_day else "No day-level data"
        )
        return (
            "🗓️ **Monthly Performance Summary:**\n\n"
            f"Total quantity sold: {monthly.get('total_qty', 0)} items\n"
            f"Total revenue: ₹{monthly.get('total_revenue', 0.0):.2f}\n"
            f"Average daily sales: {monthly.get('avg_daily_qty', 0.0):.1f} items\n"
            f"Best performing day: {best_day_text}\n\n"
            "💡 Use this monthly trend for procurement and budgeting."
        )
    
    # Peak Day Analysis
    if any(word in query_lower for word in ["peak day", "busiest day", "best day", "day has highest", "weekday"]):
        day_data = context['sales_by_day']
        if day_data:
            sorted_days = sorted(day_data, key=lambda x: x['quantity'], reverse=True)
            best_day = sorted_days[0]
            worst_day = sorted_days[-1]
            days_list = "\n".join([f"- {d['day']}: {d['quantity']} items" for d in sorted_days])
            return f"📅 **Day-wise Sales Analysis:**\n\nBest Day: {best_day['day']} ({best_day['quantity']} items)\nSlowest Day: {worst_day['day']} ({worst_day['quantity']} items)\n\nAll days:\n{days_list}\n\n💡 Tip: Stock more inventory for {best_day['day']}!"
    
    # Specific day queries (Monday, Tuesday, etc.)
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in days_of_week:
        if day in query_lower:
            day_data = context['sales_by_day']
            day_info = next((d for d in day_data if d['day'].lower() == day), None)
            if day_info:
                return f"📊 **{day_info['day']} Sales:**\n\n{day_info['quantity']} items sold\n\n💡 This is a {'high' if day_info['quantity'] > 800 else 'moderate' if day_info['quantity'] > 500 else 'low'} sales day. Plan inventory accordingly!"
    
    # Top Items / Best Sellers
    if any(word in query_lower for word in ["top", "best", "most popular", "highest selling", "top 5", "best selling"]):
        top_items = context['top_selling_items']
        if top_items:
            items_list = "\n".join([f"{i+1}. {item['name']}: {item['quantity_sold']} units (₹{item['revenue']:.2f})" for i, item in enumerate(top_items)])
            return f"🏆 **Top Selling Items:**\n\n{items_list}\n\n💡 Tip: These are your money makers - always keep them in stock!"
    
    # Revenue Analysis
    if any(word in query_lower for word in ["revenue", "money", "earning", "income"]):
        top_items = context['top_selling_items']
        if top_items:
            total_rev = sum(item['revenue'] for item in top_items)
            best_rev = top_items[0]
            return f"💰 **Revenue Analysis:**\n\nTop Revenue Item: {best_rev['name']} (₹{best_rev['revenue']:.2f})\n\nTotal from top items: ₹{total_rev:.2f}\n\n💡 Focus on promoting high-revenue items!"
    
    # Wastage Analysis
    if any(word in query_lower for word in ["waste", "wastage", "over-preparing", "throwing"]):
        wastage = context['wastage_items']
        if wastage and wastage[0]['wasted'] > 0:
            waste_list = "\n".join([f"- {item['name']}: {item['wasted']} units wasted" for item in wastage])
            worst = wastage[0]
            return f"🗑️ **Wastage Analysis:**\n\n{waste_list}\n\n⚠️ Highest waste: {worst['name']} ({worst['wasted']} units)\n\n💡 Reduce preparation of these items to minimize waste!"
        else:
            return "✅ Great! No significant wastage recorded. Keep up the good inventory management!"
    
    # Low Demand Items
    if any(word in query_lower for word in ["low demand", "least popular", "slow moving", "lowest"]):
        top_items = context['top_selling_items']
        if len(top_items) > 3:
            low_items = top_items[-3:]
            items_list = "\n".join([f"- {item['name']}: {item['quantity_sold']} units" for item in reversed(low_items)])
            return f"📉 **Low Demand Items:**\n\n{items_list}\n\n💡 Consider promotions or removing these items from the menu."
    
    # Predictions / Tomorrow
    if any(word in query_lower for word in ["tomorrow", "predict", "forecast", "should i prepare"]):
        top_items = context['top_selling_items'][:5]
        items_str = "\n".join([f"- {item['name']}: ~{max(10, item['quantity_sold'] // 7)} units" for item in top_items])
        return f"🔮 **Preparation Recommendations:**\n\n{items_str}\n\n💡 These are estimates based on weekly averages. Adjust for special events!"
    
    # Breakfast, Lunch, Snacks queries
    if "breakfast" in query_lower:
        return f"🌅 **Breakfast Recommendations:**\n\nPeak Time: 7:30 AM - 9:30 AM\nTop Items: Idli, Masala Dosa, Poori\n\n💡 Prepare breakfast items in advance for morning rush!"
    
    if "lunch" in query_lower:
        return f"🍛 **Lunch Recommendations:**\n\nPeak Time: 12:30 PM - 2:30 PM\nTop Items: Veg Biryani, Rice varieties\n\n💡 Ensure maximum stock during lunch hours!"
    
    if "snack" in query_lower or "evening" in query_lower:
        return f"☕ **Snacks Recommendations:**\n\nPeak Time: 4:30 PM - 6:30 PM\nTop Items: Tea, Coffee, Veg Puff, Samosa\n\n💡 Stock up evening snacks for tea time rush!"
    
    # General Summary (default)
    summary = f"""📊 **Smart Canteen Analytics Summary:**

🏆 **Top Sellers:**
{chr(10).join([f"{i+1}. {item['name']}: {item['quantity_sold']} units (₹{item['revenue']:.2f})" for i, item in enumerate(context['top_selling_items'][:3])])}

⏰ **Peak Hours:**
{chr(10).join([f"• {h['hour']}:00 - {h['quantity']} items" for h in context['peak_hours']])}

📅 **Best Days:**
{chr(10).join([f"• {d['day']}: {d['quantity']} items" for d in sorted(context['sales_by_day'], key=lambda x: x['quantity'], reverse=True)[:3]])}

💡 **Ask me specific questions like:**
- "What is the peak hour?"
- "Which day has highest sales?"
- "Show me top 5 items"
- "What items cause wastage?"
- "What should I prepare tomorrow?"
- "Give me this week summary"
- "Show me monthly performance"
"""
    return summary
