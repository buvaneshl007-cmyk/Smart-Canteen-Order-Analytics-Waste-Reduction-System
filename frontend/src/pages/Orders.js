import React, { useState, useEffect } from 'react';
import { orderService } from '../services/api';
import toast from 'react-hot-toast';
import { Clock, CheckCircle, Package } from 'lucide-react';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await orderService.getOrders();
      setOrders(response.data);
    } catch (error) {
      toast.error('Failed to fetch orders');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock },
      preparing: { color: 'bg-blue-100 text-blue-800', icon: Package },
      ready: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
      completed: { color: 'bg-gray-100 text-gray-800', icon: CheckCircle },
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-sm font-semibold ${config.color}`}>
        <Icon className="h-4 w-4" />
        <span className="capitalize">{status}</span>
      </span>
    );
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
      <h1 className="text-3xl font-bold text-gray-900 mb-8">My Orders</h1>

      {orders.length === 0 ? (
        <div className="text-center py-12">
          <Package className="h-24 w-24 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 text-lg">No orders yet</p>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map(order => (
            <div key={order.order_id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Order #{order.order_id}</h3>
                  <p className="text-sm text-gray-600">
                    {new Date(order.order_time).toLocaleString()}
                  </p>
                </div>
                {getStatusBadge(order.status)}
              </div>

              <div className="border-t pt-4">
                <h4 className="font-semibold mb-3">Items:</h4>
                <div className="space-y-2">
                  {order.order_items.map(item => (
                    <div key={item.order_item_id} className="flex justify-between items-center">
                      <div className="flex items-center space-x-3">
                        <span className="text-gray-700">
                          {item.menu_item.item_name}
                        </span>
                        <span className="text-sm text-gray-500">x {item.quantity}</span>
                      </div>
                      <span className="font-semibold">₹{(item.price_at_order * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="border-t mt-4 pt-4 flex justify-between items-center">
                <span className="font-bold text-lg">Total</span>
                <span className="text-2xl font-bold text-primary-600">₹{order.total_price.toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;
