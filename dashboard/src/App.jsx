import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ExecutiveAnalytics from './components/ExecutiveAnalytics';
import JobPostsManager from './components/JobPostsManager';
import BotAudienceManager from './components/BotAudienceManager';
import BroadcastManager from './components/BroadcastManager';
import BotControlPanel from './components/BotControlPanel';
import CategoriesManager from './components/CategoriesManager';
import AllWorkers from './components/AllWorkers';
import FeedbackManager from './components/FeedbackManager';
import PaymentOrderStatus from './components/PaymentOrderStatus';
import LiveMap from './components/LiveMap';
import ManualDispatchModal from './components/ManualDispatchModal';
import AddWorkerModal from './components/AddWorkerModal';
import CreateOrderModal from './components/CreateOrderModal';
import LoginModal from './components/LoginModal';
import SettingsManager from './components/SettingsManager';
import LeadsManager from './components/LeadsManager';
import { Sun, Moon, RotateCw, LogOut, ShieldCheck, Headphones, User, Menu, Crown } from 'lucide-react';

import { fetchOrders, fetchWorkers, fetchLiveLocations, fetchOrderStats, fetchCategories, fetchJobPosts, fetchUsers } from './services/api';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState(localStorage.getItem('activeTab') || 'analytics');
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [orders, setOrders] = useState([]);
  const [jobPosts, setJobPosts] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [locations, setLocations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [stats, setStats] = useState({});
  const [refreshing, setRefreshing] = useState(false);
  
  const [dispatchModalOrder, setDispatchModalOrder] = useState(null);
  const [isAddWorkerModalOpen, setIsAddWorkerModalOpen] = useState(false);
  const [isCreateOrderModalOpen, setIsCreateOrderModalOpen] = useState(false);

  // Apply Theme
  useEffect(() => {
    if (theme === 'light') {
      document.body.classList.add('light-theme');
      document.body.classList.remove('dark-theme');
    } else {
      document.body.classList.remove('light-theme');
      document.body.classList.add('dark-theme');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const isTabAllowed = (tabId) => {
    if (!currentUser) return false;
    if (currentUser.is_superuser) return true;
    const allowedStr = currentUser.allowed_tabs || '';
    if (allowedStr === 'all') return true;
    const list = allowedStr.split(',').map(s => s.trim()).filter(Boolean);
    if (list.length === 0) {
      if (currentUser.role === 'CALL_CENTER') return ['callcenter', 'orders', 'livemap'].includes(tabId);
      return ['analytics', 'job_posts', 'livemap', 'workers', 'audience'].includes(tabId);
    }
    return list.includes(tabId);
  };

  const handleTabChange = (tab) => {
    if (isTabAllowed(tab)) {
      setActiveTab(tab);
      localStorage.setItem('activeTab', tab);
    }
  };

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const savedTab = localStorage.getItem('activeTab');
    if (savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        setCurrentUser(parsed);
        if (savedTab) {
          setActiveTab(savedTab);
        } else if (parsed.role === 'CALL_CENTER') {
          setActiveTab('callcenter');
          localStorage.setItem('activeTab', 'callcenter');
        } else {
          setActiveTab('analytics');
          localStorage.setItem('activeTab', 'analytics');
        }
      } catch (e) {
        localStorage.removeItem('user');
      }
    }
  }, []);

  // Check tab permission on user load or tab change
  useEffect(() => {
    if (currentUser && !isTabAllowed(activeTab)) {
      const fallbackTabs = ['analytics', 'job_posts', 'livemap', 'callcenter', 'audience', 'workers', 'settings'];
      const firstAllowed = fallbackTabs.find(t => isTabAllowed(t)) || 'job_posts';
      setActiveTab(firstAllowed);
      localStorage.setItem('activeTab', firstAllowed);
    }
  }, [currentUser, activeTab]);

  // 10-Minute session auto logout for sub-admins & operators
  useEffect(() => {
    if (currentUser && !currentUser.is_superuser) {
      const tenMinutesMs = 10 * 60 * 1000;
      const timer = setTimeout(() => {
        handleLogoutWithMessage("Xavfsizlik yuzasidan xodim sessiyasi (10 daqiqa) tugadi. Iltimos, qaytadan tizimga kiring!");
      }, tenMinutesMs);
      return () => clearTimeout(timer);
    }
  }, [currentUser]);

  const loadData = async () => {
    try {
      setRefreshing(true);
      const [ordersRes, workersRes, locationsRes, statsRes, catRes, jobPostsRes, usersRes] = await Promise.all([
        fetchOrders().catch(() => ({ data: [] })),
        fetchWorkers().catch(() => ({ data: [] })),
        fetchLiveLocations().catch(() => ({ data: [] })),
        fetchOrderStats().catch(() => ({ data: {} })),
        fetchCategories().catch(() => ({ data: [] })),
        fetchJobPosts().catch(() => ({ data: [] })),
        fetchUsers().catch(() => ({ data: [] })),
      ]);
      setOrders(ordersRes.data || []);
      setWorkers(workersRes.data || []);
      setLocations(locationsRes.data || []);
      setStats(statsRes.data || {});
      setCategories(catRes.data || []);
      setJobPosts(jobPostsRes.data || []);
      setAllUsers(usersRes.data || []);
    } catch (err) {
      console.error('Data load error:', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (currentUser) {
      loadData();
      const interval = setInterval(loadData, 5000);
      return () => clearInterval(interval);
    }
  }, [currentUser]);

  const [sessionExpiredMessage, setSessionExpiredMessage] = useState(null);

  useEffect(() => {
    const handleExpired = (e) => {
      const msg = e?.detail?.message || "Sessiyangiz (token) muddati tugadi. Iltimos, qaytadan tizimga kiring!";
      handleLogoutWithMessage(msg);
    };

    window.addEventListener('auth:token_expired', handleExpired);
    return () => window.removeEventListener('auth:token_expired', handleExpired);
  }, []);

  const handleLogoutWithMessage = (msg) => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('activeTab');
    setSessionExpiredMessage(msg);
    setCurrentUser(null);
  };

  const handleLogout = () => {
    handleLogoutWithMessage(null);
  };

  if (!currentUser) {
    return (
      <LoginModal 
        sessionMessage={sessionExpiredMessage}
        onLoginSuccess={(user) => { 
          setSessionExpiredMessage(null);
          setCurrentUser(user); 
          const defaultTab = user.role === 'CALL_CENTER' ? 'callcenter' : 'analytics';
          const initialTab = localStorage.getItem('activeTab') || defaultTab;
          setActiveTab(initialTab);
          localStorage.setItem('activeTab', initialTab);
          loadData(); 
        }} 
      />
    );
  }

  const userRole = currentUser.role || 'CALL_CENTER';
  const isSuperUser = Boolean(currentUser.is_superuser);

  const tabTitles = {
    analytics: 'Boshqaruv Analitikasi & Moliyaviy KPI',
    job_posts: 'Ish E\'lonlari & Vakansiyalar Boshqaruvi',
    audience: 'Telegram Bot Foydalanuvchilar Bazasi',
    leads: 'Lidlar & Potensial Mijozlar Boshqaruvi',
    broadcast: 'Ommaviy Xabarnomalar (Broadcast)',
    bot_control: 'Telegram Bot Monitoring & Servis Boshqaruvi',
    categories: 'Xizmat Yo\'nalishlari & Kategoriyalar',
    workers: 'Usta va Mutaxassislar Boshqaruvi',
    feedbacks: 'Taklif va Shikoyatlar Markazi',
    callcenter: 'Call Center & Tezkor Buyurtmalar',
    orders: 'Buyurtmalar & Dispatch Markazi',
    livemap: 'Jonli Xarita & GPS Monitoring',
    settings: isSuperUser ? 'Tizim & Xodimlar Sozlamasi' : 'Profil Sozlamalari',
  };

  return (
    <div className="dashboard-layout">
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={handleTabChange} 
        currentUser={currentUser}
        mobileOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />
      
      <main className="main-content">
        <header className="header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            {/* Mobile Hamburger Toggle */}
            <button 
              className="mobile-menu-toggle-btn"
              onClick={() => setMobileMenuOpen(true)}
              aria-label="Open menu"
            >
              <Menu size={22} />
            </button>
            
            <div>
              <h1 className="header-page-title">
                {tabTitles[activeTab] || 'Boshqaruv Paneli'}
              </h1>
              <p className="header-subtitle">
                Xush kelibsiz, <strong>{currentUser.first_name || currentUser.username}</strong> ({isSuperUser ? 'Super Administrator' : (userRole === 'ADMIN' ? 'Menejer / Admin' : 'Call Center Operatori')})
              </p>
            </div>
          </div>

          <div className="header-actions">
            {/* Theme Toggle Button */}
            <button 
              className="theme-toggle-btn"
              onClick={toggleTheme}
              title="Mavzuni almashtirish (Dark/Light)"
            >
              {theme === 'dark' ? (
                <>
                  <Sun size={15} color="#fbbf24" />
                  <span className="btn-text-hide-mobile">Kun (Light)</span>
                </>
              ) : (
                <>
                  <Moon size={15} color="#3b82f6" />
                  <span className="btn-text-hide-mobile">Tun (Dark)</span>
                </>
              )}
            </button>

            <span className={`badge header-role-badge ${isSuperUser ? 'badge-in-progress' : (userRole === 'ADMIN' ? 'badge-finished' : 'badge-dispatched')}`} style={{ padding: '0.4rem 0.85rem', fontSize: '0.8rem', gap: '0.4rem' }}>
              {isSuperUser ? <Crown size={14} color="#fbbf24" /> : (userRole === 'ADMIN' ? <ShieldCheck size={14} /> : <Headphones size={14} />)}
              <span>{isSuperUser ? 'Super Admin' : (userRole === 'ADMIN' ? 'Administrator' : 'Operator')}</span>
            </span>

            <button className="btn btn-secondary" onClick={loadData} title="Ma'lumotlarni yangilash">
              <RotateCw size={14} className={refreshing ? 'spin' : ''} />
              <span className="btn-text-hide-mobile">Yangilash</span>
            </button>

            <button 
              className="btn btn-secondary" 
              style={{ backgroundColor: 'rgba(239, 68, 68, 0.12)', color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }} 
              onClick={handleLogout}
              title="Tizimdan chiqish"
            >
              <LogOut size={14} />
              <span className="btn-text-hide-mobile">Chiqish</span>
            </button>
          </div>
        </header>

        {/* 1. Admin & Operatsion Bo'limlar */}
        {activeTab === 'analytics' && isTabAllowed('analytics') && (
          <ExecutiveAnalytics stats={stats} loading={refreshing && !stats.total_orders} />
        )}

        {activeTab === 'job_posts' && isTabAllowed('job_posts') && (
          <JobPostsManager categories={categories} onRefresh={loadData} />
        )}

        {activeTab === 'audience' && isTabAllowed('audience') && (
          <BotAudienceManager currentUser={currentUser} />
        )}

        {activeTab === 'leads' && isTabAllowed('leads') && (
          <LeadsManager currentUser={currentUser} />
        )}

        {activeTab === 'broadcast' && isTabAllowed('broadcast') && (
          <BroadcastManager />
        )}

        {activeTab === 'bot_control' && isTabAllowed('bot_control') && (
          <BotControlPanel />
        )}

        {activeTab === 'categories' && isTabAllowed('categories') && (
          <CategoriesManager categories={categories} onRefresh={loadData} loading={refreshing && categories.length === 0} />
        )}

        {activeTab === 'workers' && isTabAllowed('workers') && (
          <AllWorkers workers={workers} onOpenAddWorkerModal={() => setIsAddWorkerModalOpen(true)} onRefresh={loadData} loading={refreshing && workers.length === 0} />
        )}

        {activeTab === 'feedbacks' && isTabAllowed('feedbacks') && (
          <FeedbackManager />
        )}

        {/* 2. Call Center & Operativ Bo'limlar */}
        {activeTab === 'callcenter' && isTabAllowed('callcenter') && (
          <PaymentOrderStatus 
            orders={orders} 
            loading={refreshing && orders.length === 0}
            onOpenDispatchModal={setDispatchModalOrder} 
            onOrderUpdated={loadData} 
            onOpenCreateOrderModal={() => setIsCreateOrderModalOpen(true)}
          />
        )}

        {activeTab === 'orders' && isTabAllowed('orders') && (
          <PaymentOrderStatus 
            orders={orders} 
            loading={refreshing && orders.length === 0}
            onOpenDispatchModal={setDispatchModalOrder} 
            onOrderUpdated={loadData} 
            onOpenCreateOrderModal={null}
          />
        )}

        {activeTab === 'livemap' && isTabAllowed('livemap') && (
          <LiveMap 
            workers={workers} 
            locations={locations} 
            orders={orders} 
            jobPosts={jobPosts}
            allUsers={allUsers}
            categories={categories}
          />
        )}

        {activeTab === 'settings' && isTabAllowed('settings') && (
          <SettingsManager 
            currentUser={currentUser} 
            allUsers={allUsers}
            onRefresh={loadData}
            onUserUpdated={(updated) => {
              setCurrentUser(updated);
              localStorage.setItem('user', JSON.stringify(updated));
            }} 
          />
        )}

        {/* Modal: Only opened when triggered in Call Center */}
        {isCreateOrderModalOpen && (
          <CreateOrderModal
            isOpen={isCreateOrderModalOpen}
            onClose={() => setIsCreateOrderModalOpen(false)}
            categories={categories}
            onOrderCreated={loadData}
          />
        )}

        {dispatchModalOrder && (
          <ManualDispatchModal
            order={dispatchModalOrder}
            workers={workers}
            onClose={() => setDispatchModalOrder(null)}
            onDispatched={loadData}
          />
        )}

        {isAddWorkerModalOpen && (
          <AddWorkerModal
            onClose={() => setIsAddWorkerModalOpen(false)}
            onWorkerAdded={loadData}
          />
        )}
      </main>
    </div>
  );
}
