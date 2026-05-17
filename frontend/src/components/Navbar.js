import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { ShoppingCart, User, LogOut, LayoutDashboard, ChefHat, MessageSquare } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isOwner } = useAuth();
  const { getTotalItems } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <ChefHat className="h-8 w-8 text-primary-500" />
            <span className="text-2xl font-bold text-primary-600">Smart Canteen</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            {user ? (
              <>
                {isOwner() ? (
                  <>
                    <Link
                      to="/owner/dashboard"
                      className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      <LayoutDashboard className="h-5 w-5" />
                      <span>Dashboard</span>
                    </Link>
                    <Link
                      to="/owner/menu"
                      className="text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      Menu
                    </Link>
                    <Link
                      to="/owner/orders"
                      className="text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      Orders
                    </Link>
                    <Link
                      to="/owner/analytics"
                      className="text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      Analytics
                    </Link>
                    <Link
                      to="/owner/ai"
                      className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      <MessageSquare className="h-5 w-5" />
                      <span>AI Assistant</span>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to="/menu"
                      className="text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      Menu
                    </Link>
                    <Link
                      to="/orders"
                      className="text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      My Orders
                    </Link>
                    <Link
                      to="/cart"
                      className="relative flex items-center space-x-1 text-gray-700 hover:text-primary-600 font-medium transition"
                    >
                      <ShoppingCart className="h-5 w-5" />
                      <span>Cart</span>
                      {getTotalItems() > 0 && (
                        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                          {getTotalItems()}
                        </span>
                      )}
                    </Link>
                  </>
                )}
                
                <div className="flex items-center space-x-4 ml-4 pl-4 border-l border-gray-300">
                  <div className="flex items-center space-x-2">
                    <User className="h-5 w-5 text-gray-600" />
                    <span className="text-gray-700 font-medium">{user.name}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 text-red-600 hover:text-red-700 font-medium transition"
                  >
                    <LogOut className="h-5 w-5" />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-primary-600 font-medium transition"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="btn-primary"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
