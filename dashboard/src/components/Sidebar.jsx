import React, { useState } from 'react';
import { 
  BarChart3, 
  Users, 
  Megaphone, 
  Bot, 
  FolderTree, 
  HardHat, 
  PhoneCall, 
  ClipboardList, 
  Compass, 
  Map,
  ShieldCheck,
  Layers,
  Headphones,
  Briefcase,
  ChevronDown,
  ChevronRight,
  Settings,
  X
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, userRole, mobileOpen = false, onClose }) {
  // Call Center & Operational Sections
  const operationalSections = [
    { id: 'job_posts', label: 'Ish E\'lonlari (Job Posts)', icon: Briefcase },
    { id: 'callcenter', label: 'Call Center & Buyurtmalar', icon: PhoneCall },
    { id: 'orders', label: 'Buyurtmalar Nazorati', icon: ClipboardList },
    { id: 'livemap', label: 'Jonli Xarita & GPS', icon: Map },
    { id: 'settings', label: 'Sozlamalar & Profil', icon: Settings },
  ];

  // Check if any operational tab is currently active to keep it open
  const isOperationalActive = operationalSections.some(s => s.id === activeTab);
  const [isOperationalOpen, setIsOperationalOpen] = useState(true);

  // 1. Admin Executive & Strategic Sections
  const adminSections = [
    { id: 'analytics', label: 'Boshqaruv Analitikasi', icon: BarChart3 },
    { id: 'livemap', label: 'Jonli Xarita & Joylashuvlar', icon: Map },
    { id: 'job_posts', label: 'Ish E\'lonlari (Job Posts)', icon: Briefcase },
    { id: 'audience', label: 'Foydalanuvchilar', icon: Users },
    { id: 'categories', label: 'Xizmat Yo\'nalishlari', icon: FolderTree },
    { id: 'workers', label: 'Usta va Mutaxassislar', icon: HardHat },
    { id: 'broadcast', label: 'Ommaviy Xabarnoma', icon: Megaphone },
    { id: 'feedbacks', label: 'Taklif va Shikoyatlar', icon: Headphones },
    { id: 'bot_control', label: 'Telegram Bot Boshqaruvi', icon: Bot },
    { id: 'settings', label: 'Tizim Sozlamalari', icon: Settings },
  ];

  const handleNavClick = (id) => {
    setActiveTab(id);
    if (onClose) onClose();
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div className="sidebar-mobile-backdrop" onClick={onClose} />
      )}

      <aside className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`}>
        {/* Brand Logo */}
        <div className="logo" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div className="logo-icon-box">
              <ShieldCheck size={20} color="#3b82f6" />
            </div>
            <div className="logo-text-group">
              <span className="brand-title">24/7-ishlar</span>
              <span className="brand-badge">ENTERPRISE</span>
            </div>
          </div>
          {onClose && (
            <button className="sidebar-mobile-close-btn" onClick={onClose} aria-label="Close sidebar">
              <X size={20} />
            </button>
          )}
        </div>

      {/* Admin Executive Sections */}
      {userRole === 'ADMIN' && (
        <>
          <div className="sidebar-section-header">
            <Layers size={13} />
            <span>Boshqaruv & Tahlil</span>
          </div>
          <nav className="nav-links">
            {adminSections.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  className={`nav-btn ${isActive ? 'active' : ''}`}
                  onClick={() => handleNavClick(item.id)}
                >
                  <Icon size={17} className="nav-icon" />
                  <span className="nav-label">{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="sidebar-divider" />
        </>
      )}

      {/* Operational Sections - Collapsible Dropdown */}
      <div className="sidebar-collapsible-group">
        <button 
          className={`sidebar-section-toggle ${isOperationalActive ? 'has-active-child' : ''}`}
          onClick={() => setIsOperationalOpen(!isOperationalOpen)}
        >
          <div className="toggle-left">
            <Headphones size={15} className="toggle-icon" />
            <span className="toggle-label">{userRole === 'ADMIN' ? 'Operatsion Markaz' : 'Operator Paneli'}</span>
          </div>
          {isOperationalOpen ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
        </button>

        {isOperationalOpen && (
          <nav className="nav-links sub-nav-links">
            {operationalSections.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  className={`nav-btn sub-nav-btn ${isActive ? 'active' : ''}`}
                  onClick={() => handleNavClick(item.id)}
                >
                  <Icon size={16} className="nav-icon" />
                  <span className="nav-label">{item.label}</span>
                </button>
              );
            })}
          </nav>
        )}
      </div>

      {/* Footer Info */}
      <div className="sidebar-footer">
        <div className="system-status-indicator">
          <span className="status-dot-pulse"></span>
          <span>Tizim barqaror ishlamoqda</span>
        </div>
        <div className="system-version">v2.4.0 • Secure SaaS</div>
      </div>
    </aside>
    </>
  );
}
