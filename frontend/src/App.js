import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';

import Navbar from './components/Navbar';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Menu from './pages/Menu';
import Cart from './pages/Cart';
import Orders from './pages/Orders';

import OwnerDashboard from './pages/owner/Dashboard';
import OwnerMenu from './pages/owner/MenuManagement';
import LiveOrders from './pages/owner/LiveOrders';
import AIAssistant from './pages/owner/AIAssistant';

// Protected Route Component
const ProtectedRoute = ({ children, ownerOnly = false }) => {
  const { user, loading, isOwner } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (ownerOnly && !isOwner()) {
    return <Navigate to="/menu" />;
  }

  return children;
};

// Home Page
const Home = () => {
  const { user, isOwner } = useAuth();

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (isOwner()) {
    return <Navigate to="/owner/dashboard" />;
  }

  return <Navigate to="/menu" />;
};

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Navbar />
            <Toaster position="top-right" />
            
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              
              {/* Customer Routes */}
              <Route
                path="/menu"
                element={
                  <ProtectedRoute>
                    <Menu />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/cart"
                element={
                  <ProtectedRoute>
                    <Cart />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/orders"
                element={
                  <ProtectedRoute>
                    <Orders />
                  </ProtectedRoute>
                }
              />
              
              {/* Owner Routes */}
              <Route
                path="/owner/dashboard"
                element={
                  <ProtectedRoute ownerOnly>
                    <OwnerDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/owner/menu"
                element={
                  <ProtectedRoute ownerOnly>
                    <OwnerMenu />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/owner/orders"
                element={
                  <ProtectedRoute ownerOnly>
                    <LiveOrders />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/owner/analytics"
                element={
                  <ProtectedRoute ownerOnly>
                    <OwnerDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/owner/ai"
                element={
                  <ProtectedRoute ownerOnly>
                    <AIAssistant />
                  </ProtectedRoute>
                }
              />
              
              {/* 404 */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
