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
  X,
  Crown
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, currentUser, mobileOpen = false, onClose }) {
  const userRole = currentUser?.role || 'CALL_CENTER';
  const isSuperUser = Boolean(currentUser?.is_superuser);
  
  const isTabAllowed = (tabId) => {
    if (!currentUser) return false;
    if (isSuperUser) return true;
    const allowed = currentUser.allowed_tabs || '';
    if (allowed === 'all') return true;
    const list = allowed.split(',').map(s => s.trim()).filter(Boolean);
    if (list.length === 0) {
      if (userRole === 'CALL_CENTER') return ['callcenter', 'orders', 'livemap'].includes(tabId);
      return ['analytics', 'job_posts', 'livemap', 'workers', 'audience'].includes(tabId);
    }
    return list.includes(tabId);
  };

  // Operational Sections
  const allOperationalSections = [
    { id: 'job_posts', label: 'Ish E\'lonlari (Job Posts)', icon: Briefcase },
    { id: 'callcenter', label: 'Call Center & Buyurtmalar', icon: PhoneCall },
    { id: 'orders', label: 'Buyurtmalar Nazorati', icon: ClipboardList },
    { id: 'livemap', label: 'Jonli Xarita & GPS', icon: Map },
  ];

  // Admin Executive & Strategic Sections
  const allAdminSections = [
    { id: 'analytics', label: 'Boshqaruv Analitikasi', icon: BarChart3 },
    { id: 'livemap', label: 'Jonli Xarita & GPS', icon: Map },
    { id: 'job_posts', label: 'Ish E\'lonlari (Job Posts)', icon: Briefcase },
    { id: 'audience', label: 'Foydalanuvchilar Bazasi', icon: Users },
    { id: 'categories', label: 'Xizmat Yo\'nalishlari', icon: FolderTree },
    { id: 'workers', label: 'Usta va Mutaxassislar', icon: HardHat },
    { id: 'broadcast', label: 'Ommaviy Xabarnoma', icon: Megaphone },
    { id: 'feedbacks', label: 'Taklif va Shikoyatlar', icon: Headphones },
    { id: 'bot_control', label: 'Telegram Bot Boshqaruvi', icon: Bot },
    { id: 'settings', label: isSuperUser ? 'Tizim & Xodimlar Sozlamasi' : 'Profil Sozlamalari', icon: Settings },
  ];

  // Filter allowed sections
  const adminSections = allAdminSections.filter(s => isTabAllowed(s.id));
  const operationalSections = allOperationalSections.filter(s => isTabAllowed(s.id));

  // Check if any operational tab is currently active to keep it open
  const isOperationalActive = operationalSections.some(s => s.id === activeTab);
  const [isOperationalOpen, setIsOperationalOpen] = useState(true);

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
              <span className="brand-title">{localStorage.getItem('project_name') || 'IshBazari'}</span>
              <span className="brand-badge" style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
                {isSuperUser ? <><Crown size={10} color="#fbbf24" /> SUPER ADMIN</> : 'ENTERPRISE'}
              </span>
            </div>
          </div>
          {onClose && (
            <button className="sidebar-mobile-close-btn" onClick={onClose} aria-label="Close sidebar">
              <X size={20} />
            </button>
          )}
        </div>

      {/* Admin Executive Sections */}
      {adminSections.length > 0 && (
        <>
          <div className="sidebar-section-header">
            <Layers size={13} />
            <span>{isSuperUser ? 'Boshqaruv & Tahlil' : 'Ruxsat etilgan bo\'limlar'}</span>
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

      {/* Operational Sections */}
      {operationalSections.length > 0 && (
        <div className="sidebar-collapsible-group">
          <button 
            className={`sidebar-section-toggle ${isOperationalActive ? 'has-active-child' : ''}`}
            onClick={() => setIsOperationalOpen(!isOperationalOpen)}
          >
            <div className="toggle-left">
              <Headphones size={15} className="toggle-icon" />
              <span className="toggle-label">{isSuperUser ? 'Operatsion Markaz' : 'Operator Paneli'}</span>
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
      )}

      {/* Logged in User info card in footer */}
      <div style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ padding: '0.65rem 0.75rem', borderRadius: '8px', background: 'var(--bg-inner)', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: isSuperUser ? 'rgba(251, 191, 36, 0.2)' : 'rgba(59, 130, 246, 0.2)', color: isSuperUser ? '#fbbf24' : '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '0.85rem' }}>
            {isSuperUser ? '👑' : (currentUser?.first_name?.[0] || 'A')}
          </div>
          <div style={{ overflow: 'hidden' }}>
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
              {currentUser?.first_name || currentUser?.username}
            </div>
            <div style={{ fontSize: '0.72rem', color: isSuperUser ? '#fbbf24' : 'var(--text-muted)', fontWeight: 600 }}>
              {isSuperUser ? 'Super Admin' : (currentUser?.role === 'CALL_CENTER' ? 'Operator' : 'Menejer / Admin')}
            </div>
          </div>
        </div>
      </div>

      </aside>
    </>
  );
}
