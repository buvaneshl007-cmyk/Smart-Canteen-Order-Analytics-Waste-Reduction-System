from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db, get_db
from app.core.security import get_password_hash
from app.models.models import User, UserRole
from app.api import auth, menu, orders, analytics, ai_assistant, wastage
from contextlib import asynccontextmanager
from typing import List
import json


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing database...")
    init_db()
    
    # Create default admin user if not exists
    db = next(get_db())
    admin = db.query(User).filter(User.role == UserRole.OWNER).first()
    if not admin:
        print("Creating default admin user...")
        admin = User(
            name="Admin",
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            role=UserRole.OWNER
        )
        db.add(admin)
        db.commit()
        print(f"Admin created: {settings.DEFAULT_ADMIN_EMAIL} / {settings.DEFAULT_ADMIN_PASSWORD}")
    
    db.close()
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Smart Canteen API",
    description="AI-powered canteen management system with analytics and demand prediction",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(analytics.router)
app.include_router(ai_assistant.router)
app.include_router(wastage.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Smart Canteen API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now - can be extended for real-time order updates
            await manager.broadcast({
                "type": "update",
                "data": data
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Broadcast helper function
async def broadcast_menu_update():
    await manager.broadcast({
        "type": "menu_update",
        "message": "Menu has been updated"
    })


async def broadcast_new_order(order_id: int):
    await manager.broadcast({
        "type": "new_order",
        "order_id": order_id
    })
