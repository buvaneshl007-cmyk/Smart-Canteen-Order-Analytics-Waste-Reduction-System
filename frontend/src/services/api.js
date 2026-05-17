import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API Services
export const authService = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

export const menuService = {
  getMenu: () => api.get('/menu'),
  getMenuItem: (id) => api.get(`/menu/${id}`),
  createMenuItem: (data) => api.post('/menu', data),
  updateMenuItem: (id, data) => api.put(`/menu/${id}`, data),
  deleteMenuItem: (id) => api.delete(`/menu/${id}`),
  toggleAvailability: (id, available) => api.patch(`/menu/${id}/availability`, null, {
    params: { available }
  }),
};

export const orderService = {
  createOrder: (data) => api.post('/orders', data),
  getOrders: () => api.get('/orders'),
  getLiveOrders: () => api.get('/orders/live'),
  getOrder: (id) => api.get(`/orders/${id}`),
  updateOrderStatus: (id, status) => api.patch(`/orders/${id}/status`, { status }),
};

export const analyticsService = {
  getDailySales: (days = 7) => api.get('/analytics/daily', { params: { days } }),
  getWeeklySales: () => api.get('/analytics/weekly'),
  getHourlySales: () => api.get('/analytics/time'),
  getItemAnalytics: () => api.get('/analytics/items'),
  getPredictions: () => api.get('/analytics/predict'),
};

export const aiService = {
  query: (queryText) => api.post('/ai/query', { query: queryText }),
};

export const wastageService = {
  recordWastage: (data) => api.post('/wastage', data),
  getWastageRecords: () => api.get('/wastage'),
  getItemWastage: (itemId) => api.get(`/wastage/item/${itemId}`),
};

export default api;