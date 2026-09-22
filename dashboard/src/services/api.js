import axios from 'axios';

const getBaseUrl = () => {
  if (typeof window !== 'undefined' && window.location) {
    if (window.location.port === '8000' || window.location.port === '' || window.location.port === '80' || window.location.port === '443') {
      return `${window.location.origin}/api`;
    }
    return `${window.location.protocol}//${window.location.hostname}:8000/api`;
  }
  return 'http://127.0.0.1:8000/api';
};

const api = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginUser = (username, password) => api.post('/accounts/login/', { username, password });
export const changeAdminCredentials = (data) => api.post('/accounts/change-credentials/', data);
export const downloadDatabaseBackupUrl = () => `${getBaseUrl()}/accounts/download-backup/`;

// Categories & Positions
export const fetchCategories = () => api.get('/categories/');
export const createCategory = (catData) => api.post('/categories/', catData);
export const updateCategory = (id, catData) => api.put(`/categories/${id}/`, catData);
export const deleteCategory = (id) => api.delete(`/categories/${id}/`);

export const fetchPositions = (params = {}) => api.get('/categories/positions/', { params });
export const createPosition = (posData) => api.post('/categories/positions/', posData);
export const updatePosition = (id, posData) => api.put(`/categories/positions/${id}/`, posData);
export const deletePosition = (id) => api.delete(`/categories/positions/${id}/`);

// Orders & Dispatch
export const fetchOrders = () => api.get('/orders/');
export const fetchOrderStats = () => api.get('/orders/stats/');
export const createOrder = (orderData) => api.post('/orders/', orderData);
export const dispatchOrder = (orderId, workerId) => api.post(`/orders/${orderId}/dispatch/`, { worker_id: workerId });
export const updateOrderStatus = (orderId, status) => api.post(`/orders/${orderId}/status/`, { status });

// Job Posts (E'lonlar va Ishlar)
export const fetchJobPosts = (params = {}) => api.get('/orders/job-posts/', { params });
export const createJobPost = (data) => api.post('/orders/job-posts/', data);
export const updateJobPost = (id, data) => api.patch(`/orders/job-posts/${id}/`, data);
export const deleteJobPost = (id) => api.delete(`/orders/job-posts/${id}/`);
export const offerJobToWorker = (jobId, workerId) => api.post(`/orders/job-posts/${jobId}/offer/`, { worker_id: workerId });


// Accounts & Workers
export const fetchWorkers = (params = {}) => api.get('/accounts/workers/', { params });
export const fetchWorkerDetail = (id) => api.get(`/accounts/workers/${id}/`);
export const updateWorker = (id, data) => api.patch(`/accounts/workers/${id}/`, data);
export const registerWorker = (workerData) => api.post('/accounts/register-worker/', workerData);
export const fetchUsers = (params = {}) => api.get('/accounts/users/', { params });
export const createUser = (userData) => api.post('/accounts/users/', userData);
export const updateUser = (id, userData) => api.patch(`/accounts/users/${id}/`, userData);
export const deleteUser = (id) => api.delete(`/accounts/users/${id}/`);
export const updateUserCredits = (userId, data) => api.post(`/accounts/users/${userId}/credits/`, data);
export const requestProfileUpdate = (userId, data) => api.post(`/accounts/users/${userId}/request-profile-update/`, data);

// Feedbacks & Support
export const fetchFeedbacks = (params = {}) => api.get('/accounts/feedbacks/', { params });
export const updateFeedback = (id, data) => api.patch(`/accounts/feedbacks/${id}/`, data);
export const deleteFeedback = (id) => api.delete(`/accounts/feedbacks/${id}/`);

// GPS & Live Locations
export const fetchLiveLocations = () => api.get('/locations/live-workers/');

// Bot Control & Notifications
export const fetchBotStatus = () => api.get('/bot/status/');
export const startBot = () => api.post('/bot/start/');
export const stopBot = () => api.post('/bot/stop/');
export const restartBot = () => api.post('/bot/restart/');
export const updateBotToken = (token) => api.post('/bot/token/', { token });
export const updateBotTokens = (tokensData) => api.post('/bot/token/', tokensData);
export const updateBotSettings = (settingsData) => api.post('/bot/settings/', settingsData);
export const sendBotMessage = (chatId, text, botType = 'CLIENT') => api.post('/bot/send-message/', { chat_id: chatId, text, bot_type: botType });
export const sendBroadcast = (target, text) => api.post('/bot/broadcast/', { target, text });

export default api;



