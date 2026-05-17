import React, { useState, useEffect } from 'react';
import { orderService } from '../../services/api';
import toast from 'react-hot-toast';
import { Clock, Package, CheckCircle, AlertCircle } from 'lucide-react';

const LiveOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
    // Refresh orders every 10 seconds
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await orderService.getLiveOrders();
      setOrders(response.data);
    } catch (error) {
      toast.error('Failed to fetch orders');
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (orderId, status) => {
    try {
      await orderService.updateOrderStatus(orderId, status);
      toast.success('Order status updated');
      fetchOrders();
    } catch (error) {
      toast.error('Failed to update status');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-500',
      preparing: 'bg-blue-500',
      ready: 'bg-green-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Live Orders</h1>
        <div className="flex items-center space-x-2 text-gray-600">
          <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm">Auto-refresh every 10s</span>
        </div>
      </div>

      {orders.length === 0 ? (
        <div className="text-center py-12 card">
          <CheckCircle className="h-24 w-24 text-green-500 mx-auto mb-4" />
          <p className="text-gray-500 text-lg">No pending orders</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {orders.map(order => (
            <div key={order.order_id} className="card border-l-4" style={{ borderLeftColor: getStatusColor(order.status) }}>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">Order #{order.order_id}</h3>
                  <p className="text-sm text-gray-600">{order.user.name}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(order.order_time).toLocaleTimeString()}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${getStatusColor(order.status)}`}>
                  {order.status}
                </span>
              </div>

              <div className="border-t pt-4 mb-4">
                <h4 className="font-semibold mb-2 text-gray-700">Items:</h4>
                <div className="space-y-2">
                  {order.order_items.map(item => (
                    <div key={item.order_item_id} className="flex justify-between text-sm">
                      <span className="text-gray-700">
                        {item.quantity}x {item.menu_item.item_name}
                      </span>
                      <span className="font-semibold">₹{(item.price_at_order * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="border-t pt-3 mb-4">
                <div className="flex justify-between items-center">
                  <span className="font-bold">Total</span>
                  <span className="text-xl font-bold text-primary-600">₹{order.total_price.toFixed(2)}</span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                {order.status === 'pending' && (
                  <button
                    onClick={() => updateStatus(order.order_id, 'preparing')}
                    className="col-span-3 btn-primary flex items-center justify-center space-x-1 text-sm"
                  >
                    <Package className="h-4 w-4" />
                    <span>Start Preparing</span>
                  </button>
                )}
                
                {order.status === 'preparing' && (
                  <>
                    <button
                      onClick={() => updateStatus(order.order_id, 'ready')}
                      className="col-span-3 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center space-x-1 text-sm"
                    >
                      <CheckCircle className="h-4 w-4" />
                      <span>Mark Ready</span>
                    </button>
                  </>
                )}
                
                {order.status === 'ready' && (
                  <button
                    onClick={() => updateStatus(order.order_id, 'completed')}
                    className="col-span-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center space-x-1 text-sm"
                  >
                    <CheckCircle className="h-4 w-4" />
                    <span>Complete</span>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LiveOrders;
