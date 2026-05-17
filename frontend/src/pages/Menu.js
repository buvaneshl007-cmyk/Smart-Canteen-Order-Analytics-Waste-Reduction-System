import React, { useState, useEffect } from 'react';
import { menuService } from '../services/api';
import { useCart } from '../context/CartContext';
import toast from 'react-hot-toast';
import { Plus, Search, ShoppingCart } from 'lucide-react';

const Menu = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const { addToCart } = useCart();

  useEffect(() => {
    fetchMenu();
  }, []);

  const fetchMenu = async () => {
    try {
      const response = await menuService.getMenu();
      setMenuItems(response.data);
    } catch (error) {
      toast.error('Failed to fetch menu');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (item) => {
    addToCart(item);
    toast.success(`${item.item_name} added to cart!`);
  };

  const categories = ['All', ...new Set(menuItems.map(item => item.category))];

  const filteredItems = menuItems.filter(item => {
    const matchesSearch = item.item_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
    return matchesSearch && matchesCategory && item.available;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Our Menu</h1>
        <p className="text-gray-600">Fresh and delicious food items</p>
      </div>

      {/* Search and Filter */}
      <div className="mb-8 flex flex-col md:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search menu items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field pl-10"
          />
        </div>
        
        <div className="flex gap-2 overflow-x-auto">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition ${
                selectedCategory === category
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Menu Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredItems.map(item => (
          <div key={item.item_id} className="card group hover:scale-105 transition-transform">
            <div className="aspect-w-16 aspect-h-12 mb-4 bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg overflow-hidden">
              {item.image_url ? (
                <img
                  src={item.image_url}
                  alt={item.item_name}
                  className="w-full h-48 object-cover"
                />
              ) : (
                <div className="w-full h-48 flex items-center justify-center">
                  <ShoppingCart className="h-16 w-16 text-primary-400" />
                </div>
              )}
            </div>
            
            <div className="mb-3">
              <h3 className="text-lg font-bold text-gray-900">{item.item_name}</h3>
              <span className="inline-block mt-1 px-2 py-1 text-xs font-semibold bg-primary-100 text-primary-700 rounded">
                {item.category}
              </span>
            </div>
            
            {item.description && (
              <p className="text-sm text-gray-600 mb-3">{item.description}</p>
            )}
            
            <div className="flex items-center justify-between mt-auto">
              <span className="text-2xl font-bold text-primary-600">₹{item.price}</span>
              <button
                onClick={() => handleAddToCart(item)}
                className="btn-primary flex items-center space-x-1"
              >
                <Plus className="h-4 w-4" />
                <span>Add</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No items found</p>
        </div>
      )}
    </div>
  );
};

export default Menu;
