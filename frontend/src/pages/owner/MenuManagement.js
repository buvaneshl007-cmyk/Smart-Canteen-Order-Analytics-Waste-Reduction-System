import React, { useState, useEffect } from 'react';
import { menuService } from '../../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, ToggleLeft, ToggleRight } from 'lucide-react';

const OwnerMenu = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({
    item_name: '',
    price: '',
    category: '',
    description: '',
    image_url: '',
    available: true,
  });

  useEffect(() => {
    fetchMenu();
  }, []);

  const fetchMenu = async () => {
    try {
      const response = await menuService.getMenu();
      setMenuItems(response.data);
    } catch (error) {
      toast.error('Failed to fetch menu');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingItem) {
        await menuService.updateMenuItem(editingItem.item_id, formData);
        toast.success('Item updated successfully');
      } else {
        await menuService.createMenuItem(formData);
        toast.success('Item created successfully');
      }
      
      fetchMenu();
      closeModal();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Operation failed');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await menuService.deleteMenuItem(id);
        toast.success('Item deleted');
        fetchMenu();
      } catch (error) {
        toast.error('Failed to delete item');
      }
    }
  };

  const handleToggleAvailability = async (item) => {
    try {
      await menuService.toggleAvailability(item.item_id, !item.available);
      toast.success(`Item ${!item.available ? 'enabled' : 'disabled'}`);
      fetchMenu();
    } catch (error) {
      toast.error('Failed to update availability');
    }
  };

  const openModal = (item = null) => {
    if (item) {
      setEditingItem(item);
      setFormData(item);
    } else {
      setEditingItem(null);
      setFormData({
        item_name: '',
        price: '',
        category: '',
        description: '',
        image_url: '',
        available: true,
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingItem(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Menu Management</h1>
        <button
          onClick={() => openModal()}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Add Item</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {menuItems.map(item => (
          <div key={item.item_id} className="card">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-bold text-gray-900">{item.item_name}</h3>
                <span className="inline-block mt-1 px-2 py-1 text-xs font-semibold bg-primary-100 text-primary-700 rounded">
                  {item.category}
                </span>
              </div>
              <button
                onClick={() => handleToggleAvailability(item)}
                className="text-gray-600 hover:text-gray-900"
              >
                {item.available ? (
                  <ToggleRight className="h-6 w-6 text-green-500" />
                ) : (
                  <ToggleLeft className="h-6 w-6 text-gray-400" />
                )}
              </button>
            </div>

            <p className="text-sm text-gray-600 mb-3">{item.description || 'No description'}</p>
            
            <div className="flex items-center justify-between mb-4">
              <span className="text-2xl font-bold text-primary-600">₹{item.price}</span>
              <span className={`text-sm font-semibold ${item.available ? 'text-green-600' : 'text-red-600'}`}>
                {item.available ? 'Available' : 'Unavailable'}
              </span>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={() => openModal(item)}
                className="flex-1 btn-secondary flex items-center justify-center space-x-1"
              >
                <Edit2 className="h-4 w-4" />
                <span>Edit</span>
              </button>
              <button
                onClick={() => handleDelete(item.item_id)}
                className="flex-1 btn-danger flex items-center justify-center space-x-1"
              >
                <Trash2 className="h-4 w-4" />
                <span>Delete</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">
              {editingItem ? 'Edit Item' : 'Add New Item'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Item Name</label>
                <input
                  type="text"
                  value={formData.item_name}
                  onChange={(e) => setFormData({...formData, item_name: e.target.value})}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Price (₹)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({...formData, price: e.target.value})}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <input
                  type="text"
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="input-field"
                  rows="3"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
                <input
                  type="text"
                  value={formData.image_url}
                  onChange={(e) => setFormData({...formData, image_url: e.target.value})}
                  className="input-field"
                  placeholder="https://example.com/image.jpg"
                />
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.available}
                  onChange={(e) => setFormData({...formData, available: e.target.checked})}
                  className="h-4 w-4 text-primary-600 rounded"
                />
                <label className="ml-2 text-sm font-medium text-gray-700">Available</label>
              </div>

              <div className="flex space-x-3 pt-4">
                <button type="submit" className="flex-1 btn-primary">
                  {editingItem ? 'Update' : 'Create'}
                </button>
                <button type="button" onClick={closeModal} className="flex-1 btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default OwnerMenu;
