import React, { useState, useEffect } from 'react';
import { 
  KeyRound, 
  User, 
  ShieldCheck, 
  CheckCircle2, 
  AlertCircle, 
  Lock, 
  Save,
  Eye,
  EyeOff,
  Settings,
  HelpCircle,
  Database,
  Download,
  Users,
  UserPlus,
  Edit2,
  Trash2,
  CheckSquare,
  Square,
  Clock,
  ShieldAlert,
  X
} from 'lucide-react';
import { changeAdminCredentials, fetchUsers, createUser, updateUser, deleteUser } from '../services/api';

const AVAILABLE_TABS = [
  { id: 'analytics', label: 'Boshqaruv Analitikasi', icon: '📊' },
  { id: 'job_posts', label: 'Ish E\'lonlari & Vakansiyalar', icon: '💼' },
  { id: 'audience', label: 'Foydalanuvchilar Bazasi', icon: '👥' },
  { id: 'leads', label: 'Lidlar & Potensial Mijozlar', icon: '🎯' },
  { id: 'broadcast', label: 'Ommaviy Xabarnoma', icon: '📢' },
  { id: 'bot_control', label: 'Telegram Bot Boshqaruvi', icon: '🤖' },
  { id: 'categories', label: 'Kasblar & Kategoriyalar', icon: '🗂️' },
  { id: 'workers', label: 'Usta va Mutaxassislar', icon: '🛠️' },
  { id: 'feedbacks', label: 'Taklif va Shikoyatlar', icon: '💬' },
  { id: 'callcenter', label: 'Call Center & Buyurtmalar', icon: '🎧' },
  { id: 'livemap', label: 'Jonli Xarita & GPS', icon: '📍' },
  { id: 'settings', label: 'Tizim Sozlamalari', icon: '⚙️' },
];

export default function SettingsManager({ currentUser, onUserUpdated }) {
  // Login & Password State
  const [newUsername, setNewUsername] = useState(currentUser?.username || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  // Sub-Admins / Staff State
  const [staffUsers, setStaffUsers] = useState([]);
  const [loadingStaff, setLoadingStaff] = useState(false);
  const [staffModalOpen, setStaffModalOpen] = useState(false);
  const [editingStaff, setEditingStaff] = useState(null);
  
  // Staff Form State
  const [staffForm, setStaffForm] = useState({
    username: '',
    password: '',
    first_name: '',
    phone_number: '',
    role: 'ADMIN',
    allowed_tabs: ['analytics', 'job_posts', 'audience']
  });
  const [staffSaving, setStaffSaving] = useState(false);
  const [staffError, setStaffError] = useState(null);
  const [staffSuccess, setStaffSuccess] = useState(null);

  useEffect(() => {
    if (currentUser?.is_superuser) {
      loadStaffUsers();
    }
  }, [currentUser]);

  const loadStaffUsers = async () => {
    setLoadingStaff(true);
    try {
      const res = await fetchUsers({ limit: 100 });
      const users = res.data?.results || res.data || [];
      // Filter staff / dashboard users
      const staff = users.filter(u => u.is_staff || u.role === 'ADMIN' || u.role === 'CALL_CENTER' || u.is_superuser);
      setStaffUsers(staff);
    } catch (err) {
      console.error("Xodimlarni yuklashda xatolik:", err);
    } finally {
      setLoadingStaff(false);
    }
  };

  const handleSaveCredentials = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    if (newPassword && newPassword !== confirmPassword) {
      setErrorMsg("Yangi parollar bir-biriga mos kelmadi!");
      setSaving(false);
      return;
    }

    if (newPassword && newPassword.length < 4) {
      setErrorMsg("Parol kamida 4 ta belgidan iborat bo'lishi kerak!");
      setSaving(false);
      return;
    }

    try {
      const payload = {
        user_id: currentUser?.id,
        current_username: currentUser?.username,
        new_username: newUsername.trim(),
        current_password: currentPassword || undefined,
        new_password: newPassword || undefined,
        confirm_password: confirmPassword || undefined
      };

      const res = await changeAdminCredentials(payload);
      setSuccessMsg(res.data.message || "Login va parol muvaffaqiyatli yangilandi!");
      
      if (res.data.user) {
        localStorage.setItem('user', JSON.stringify(res.data.user));
        if (res.data.access) {
          localStorage.setItem('token', res.data.access);
        }
        if (onUserUpdated) {
          onUserUpdated(res.data.user);
        }
      }

      // Reset sensitive password fields
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      const msg = err.response?.data?.error || "Ma'lumotlarni o'zgartirishda xatolik yuz berdi!";
      setErrorMsg(msg);
    } finally {
      setSaving(false);
    }
  };

  const openAddStaffModal = () => {
    setEditingStaff(null);
    setStaffForm({
      username: '',
      password: '',
      first_name: '',
      phone_number: '',
      role: 'ADMIN',
      allowed_tabs: ['analytics', 'job_posts', 'audience']
    });
    setStaffError(null);
    setStaffSuccess(null);
    setStaffModalOpen(true);
  };

  const openEditStaffModal = (user) => {
    setEditingStaff(user);
    let tabs = [];
    if (!user.allowed_tabs || user.allowed_tabs === 'all') {
      tabs = AVAILABLE_TABS.map(t => t.id);
    } else {
      tabs = user.allowed_tabs.split(',').map(s => s.trim()).filter(Boolean);
    }

    setStaffForm({
      username: user.username || '',
      password: '',
      first_name: user.first_name || '',
      phone_number: user.phone_number || '',
      role: user.role || 'ADMIN',
      allowed_tabs: tabs
    });
    setStaffError(null);
    setStaffSuccess(null);
    setStaffModalOpen(true);
  };

  const toggleTabPermission = (tabId) => {
    setStaffForm(prev => {
      const exists = prev.allowed_tabs.includes(tabId);
      if (exists) {
        return { ...prev, allowed_tabs: prev.allowed_tabs.filter(t => t !== tabId) };
      } else {
        return { ...prev, allowed_tabs: [...prev.allowed_tabs, tabId] };
      }
    });
  };

  const handleSelectAllTabs = () => {
    if (staffForm.allowed_tabs.length === AVAILABLE_TABS.length) {
      setStaffForm(prev => ({ ...prev, allowed_tabs: [] }));
    } else {
      setStaffForm(prev => ({ ...prev, allowed_tabs: AVAILABLE_TABS.map(t => t.id) }));
    }
  };

  const handleSaveStaff = async (e) => {
    e.preventDefault();
    setStaffSaving(true);
    setStaffError(null);
    setStaffSuccess(null);

    if (!staffForm.username.trim()) {
      setStaffError("Login (foydalanuvchi nomi) kiritilishi shart!");
      setStaffSaving(false);
      return;
    }

    if (!editingStaff && (!staffForm.password || staffForm.password.length < 4)) {
      setStaffError("Yangi xodim uchun kamida 4 belgidan iborat parol kiriting!");
      setStaffSaving(false);
      return;
    }

    const allowedTabsStr = staffForm.allowed_tabs.length === AVAILABLE_TABS.length ? 'all' : staffForm.allowed_tabs.join(',');

    try {
      const payload = {
        username: staffForm.username.trim(),
        first_name: staffForm.first_name.trim(),
        phone_number: staffForm.phone_number.trim(),
        role: staffForm.role,
        is_staff: true,
        allowed_tabs: allowedTabsStr
      };

      if (staffForm.password && staffForm.password.trim()) {
        payload.password = staffForm.password.trim();
      }

      if (editingStaff) {
        await updateUser(editingStaff.id, payload);
        setStaffSuccess("Xodim ma'lumotlari muvaffaqiyatli saqlandi!");
      } else {
        await createUser(payload);
        setStaffSuccess("Yangi xodim muvaffaqiyatli qo'shildi!");
      }

      await loadStaffUsers();
      setTimeout(() => {
        setStaffModalOpen(false);
      }, 1000);
    } catch (err) {
      const data = err.response?.data;
      let msg = "Xodimni saqlashda xatolik yuz berdi!";
      if (typeof data === 'object' && data !== null) {
        msg = Object.entries(data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
      }
      setStaffError(msg);
    } finally {
      setStaffSaving(false);
    }
  };

  const handleDeleteStaff = async (user) => {
    if (user.is_superuser || user.id === currentUser?.id) {
      alert("Bosh Administrator (Superuser) hisobini o'chirish taqiqlangan!");
      return;
    }
    if (!window.confirm(`Haqiqatan ham "${user.username}" xodimini o'chirmoqchimisiz?`)) {
      return;
    }

    try {
      await deleteUser(user.id);
      loadStaffUsers();
    } catch (err) {
      alert("Xodimni o'chirishda xatolik: " + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="space-y-6" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      
      {/* Top Banner */}
      <div className="card" style={{ 
        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.08))',
        borderColor: 'rgba(59, 130, 246, 0.25)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        padding: '1.5rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ 
            width: '48px', 
            height: '48px', 
            borderRadius: '12px', 
            background: 'var(--primary)', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 4px 14px rgba(59, 130, 246, 0.4)'
          }}>
            <Settings size={26} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.01em' }}>
              Tizim va Xavfsizlik Sozlamalari
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem', marginTop: '0.2rem' }}>
              Admin panelga kirish paroli, sub-adminlar va boshqaruv xavfsizligini moslashtirish
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="badge badge-finished" style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem', gap: '0.4rem' }}>
            <ShieldCheck size={15} /> Xavfsiz Shifrlangan Tizim
          </span>
        </div>
      </div>

      {/* Main Settings Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem' }}>
        
        {/* Card 1: Admin Login & Password Change */}
        <div className="card" style={{ padding: '1.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1.25rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)' }}>
            <KeyRound size={20} color="var(--primary)" />
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)' }}>
              Kirish Ma'lumotlarini O'zgartirish
            </h3>
          </div>

          {/* Success Alert */}
          {successMsg && (
            <div style={{ 
              padding: '0.85rem 1rem', 
              borderRadius: '10px', 
              backgroundColor: 'rgba(16, 185, 129, 0.12)', 
              color: '#10b981', 
              fontSize: '0.88rem', 
              marginBottom: '1.25rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}>
              <CheckCircle2 size={18} />
              <span>{successMsg}</span>
            </div>
          )}

          {/* Error Alert */}
          {errorMsg && (
            <div style={{ 
              padding: '0.85rem 1rem', 
              borderRadius: '10px', 
              backgroundColor: 'rgba(239, 68, 68, 0.12)', 
              color: '#ef4444', 
              fontSize: '0.88rem', 
              marginBottom: '1.25rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              border: '1px solid rgba(239, 68, 68, 0.3)'
            }}>
              <AlertCircle size={18} />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSaveCredentials} style={{ display: 'flex', flexDirection: 'column', gap: '1.15rem' }}>
            
            {/* Username Field */}
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                <User size={14} color="var(--primary)" /> Login (Foydalanuvchi nomi)
              </label>
              <input
                type="text"
                required
                className="form-control"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="Yangi login kiriting"
              />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
                Joriy faol login: <strong>{currentUser?.username}</strong>
              </span>
            </div>

            {/* Current Password Field */}
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                <Lock size={14} color="var(--text-muted)" /> Joriy (Eski) Parol
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showCurrentPassword ? "text" : "password"}
                  className="form-control"
                  style={{ paddingRight: '2.5rem' }}
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Agar parolni o'zgartirmoqchi bo'lsangiz kiriting"
                />
                <button
                  type="button"
                  onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                  style={{
                    position: 'absolute',
                    right: '10px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: 'var(--text-muted)',
                    cursor: 'pointer'
                  }}
                >
                  {showCurrentPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* New Password Field */}
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                <KeyRound size={14} color="var(--primary)" /> Yangi Parol
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showNewPassword ? "text" : "password"}
                  className="form-control"
                  style={{ paddingRight: '2.5rem' }}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Yangi kuchli parol kiriting"
                />
                <button
                  type="button"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  style={{
                    position: 'absolute',
                    right: '10px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: 'var(--text-muted)',
                    cursor: 'pointer'
                  }}
                >
                  {showNewPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Confirm Password Field */}
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                <CheckCircle2 size={14} color="var(--primary)" /> Yangi Parolni Tasdiqlang
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  className="form-control"
                  style={{ paddingRight: '2.5rem' }}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Yangi parolni qayta tering"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  style={{
                    position: 'absolute',
                    right: '10px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: 'var(--text-muted)',
                    cursor: 'pointer'
                  }}
                >
                  {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button 
              type="submit" 
              className="btn" 
              style={{ width: '100%', padding: '0.85rem', fontWeight: 700, marginTop: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }} 
              disabled={saving}
            >
              <Save size={16} />
              {saving ? "Saqlanmoqda..." : "O'zgarishlarni Saqlash"}
            </button>
          </form>
        </div>

        {/* Card 2: Account Overview & Platform Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card" style={{ padding: '1.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1.25rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)' }}>
              <ShieldCheck size={20} color="var(--primary)" />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)' }}>
                Akkaunt Ma'lumotlari
              </h3>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', borderRadius: '8px', background: 'var(--bg-inner)' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Foydalanuvchi Roli:</span>
                <span style={{ fontWeight: 700, color: 'var(--primary)', fontSize: '0.85rem' }}>
                  {currentUser?.is_superuser ? 'Bosh Administrator (Superuser)' : 'Operator / Sub-Admin'}
                </span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', borderRadius: '8px', background: 'var(--bg-inner)' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Sessiya Muddati:</span>
                <span style={{ fontWeight: 600, color: currentUser?.is_superuser ? 'var(--text-main)' : 'var(--warning)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <Clock size={14} /> {currentUser?.is_superuser ? 'Cheksiz (Superuser)' : '10 daqiqa (Avto-chiqish)'}
                </span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', borderRadius: '8px', background: 'var(--bg-inner)' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Avtorizatsiya Turi:</span>
                <span style={{ fontWeight: 600, color: 'var(--text-main)', fontSize: '0.85rem' }}>
                  JWT Bearer Token
                </span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', borderRadius: '8px', background: 'var(--bg-inner)' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Tizim Serveri:</span>
                <span style={{ fontWeight: 600, color: 'var(--success)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <span className="status-dot-pulse" style={{ width: '8px', height: '8px' }}></span> Online (Port 8000)
                </span>
              </div>
            </div>
          </div>

          {/* Card: Ma'lumotlar bazasi zaxira nusxasini yuklab olish */}
          <div className="card" style={{ 
            padding: '1.75rem', 
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(59, 130, 246, 0.06))',
            borderColor: 'rgba(16, 185, 129, 0.25)' 
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
              <Database size={20} color="var(--success)" />
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)' }}>
                Ma'lumotlar Bazasi Zaxirasi (Backup)
              </h4>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: '1.5', marginBottom: '1.25rem' }}>
              Barcha foydalanuvchilar, buyurtmalar, ustalar va tizim ma'lumotlarining to'liq va yangi nusxasini kompyuteringizga yuklab oling.
            </p>

            <a
              href="/api/accounts/download-backup/"
              download
              className="btn"
              style={{
                width: '100%',
                padding: '0.85rem',
                backgroundColor: 'var(--success)',
                borderColor: 'var(--success)',
                color: '#fff',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                textDecoration: 'none',
                boxShadow: '0 4px 14px rgba(16, 185, 129, 0.3)'
              }}
            >
              <Download size={18} />
              Bazani Yuklab Olish (.sqlite3)
            </a>
          </div>
        </div>

      </div>

      {/* Card 3: Sub-Admin and Staff Management (Super Admin Exclusive) */}
      {currentUser?.is_superuser && (
        <div className="card" style={{ padding: '1.75rem', marginTop: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Users size={22} color="var(--primary)" />
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-main)' }}>
                  Admin Panel Xodimlari & Sub-Adminlar
                </h3>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>
                  Qo'shimcha xodimlar yaratish va ularga faqat ruxsat etilgan bo'limlarni biriktirish
                </p>
              </div>
            </div>

            <button
              onClick={openAddStaffModal}
              className="btn"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.65rem 1.1rem',
                fontSize: '0.88rem',
                fontWeight: 600,
                borderRadius: '8px'
              }}
            >
              <UserPlus size={16} /> + Yangi Xodim Qo'shish
            </button>
          </div>

          {/* Security Banner regarding 10 minute token */}
          <div style={{
            padding: '0.85rem 1.1rem',
            borderRadius: '10px',
            backgroundColor: 'rgba(59, 130, 246, 0.08)',
            border: '1px solid rgba(59, 130, 246, 0.2)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            marginBottom: '1.25rem'
          }}>
            <Clock size={20} color="var(--primary)" style={{ flexShrink: 0 }} />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: '1.4' }}>
              <strong>Xavfsizlik qoidasi:</strong> Sub-admin xodimlar faqat o'zlariga ruxsat berilgan bo'limlarni ko'ra oladilar va ularning sessiyasi har <strong>10 daqiqada</strong> avtomatik yakunlanadi (qayta kirish talab etiladi).
            </span>
          </div>

          {/* Staff Table */}
          <div style={{ overflowX: 'auto' }}>
            <table className="table" style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left' }}>
                  <th style={{ padding: '0.75rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>FOYDALANUVCHI</th>
                  <th style={{ padding: '0.75rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>ROL</th>
                  <th style={{ padding: '0.75rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>RUXSAT ETILGAN BO'LIMLAR</th>
                  <th style={{ padding: '0.75rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>SESSIYA</th>
                  <th style={{ padding: '0.75rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)', textAlign: 'right' }}>AMALLAR</th>
                </tr>
              </thead>
              <tbody>
                {loadingStaff ? (
                  <tr>
                    <td colSpan={5} style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                      Yuklanmoqda...
                    </td>
                  </tr>
                ) : staffUsers.length === 0 ? (
                  <tr>
                    <td colSpan={5} style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                      Xodimlar topilmadi
                    </td>
                  </tr>
                ) : (
                  staffUsers.map((u) => {
                    const isSuper = Boolean(u.is_superuser);
                    const isAll = !u.allowed_tabs || u.allowed_tabs === 'all' || isSuper;
                    const tabsCount = isAll ? AVAILABLE_TABS.length : u.allowed_tabs.split(',').filter(Boolean).length;

                    return (
                      <tr key={u.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                            <div style={{
                              width: '34px',
                              height: '34px',
                              borderRadius: '8px',
                              backgroundColor: isSuper ? 'rgba(239, 68, 68, 0.15)' : 'rgba(59, 130, 246, 0.15)',
                              color: isSuper ? '#ef4444' : 'var(--primary)',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontWeight: 700,
                              fontSize: '0.85rem'
                            }}>
                              {(u.first_name || u.username || 'U')[0].toUpperCase()}
                            </div>
                            <div>
                              <div style={{ fontWeight: 600, color: 'var(--text-main)', fontSize: '0.9rem' }}>
                                {u.first_name || u.username} {isSuper && <span style={{ fontSize: '0.72rem', color: '#ef4444', fontWeight: 700 }}>(Super Admin)</span>}
                              </div>
                              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                                @{u.username} {u.phone_number ? `• ${u.phone_number}` : ''}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          <span className={`badge ${isSuper ? 'badge-danger' : 'badge-primary'}`} style={{ fontSize: '0.78rem' }}>
                            {isSuper ? 'Super Admin' : u.role === 'ADMIN' ? 'Admin / Operator' : u.role}
                          </span>
                        </td>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          {isAll ? (
                            <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                              <CheckCircle2 size={14} /> Barcha bo'limlar ({AVAILABLE_TABS.length} ta)
                            </span>
                          ) : (
                            <span style={{ fontSize: '0.82rem', color: 'var(--text-main)' }}>
                              <strong>{tabsCount} ta</strong> bo'lim ruxsat etilgan
                            </span>
                          )}
                        </td>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          <span style={{ fontSize: '0.82rem', color: isSuper ? 'var(--text-muted)' : 'var(--warning)', fontWeight: 600 }}>
                            {isSuper ? 'Cheksiz' : '10 daqiqa'}
                          </span>
                        </td>
                        <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '0.4rem' }}>
                            <button
                              onClick={() => openEditStaffModal(u)}
                              className="btn btn-secondary"
                              style={{ padding: '0.4rem 0.65rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                              title="Tahrirlash"
                            >
                              <Edit2 size={13} /> Tahrirlash
                            </button>
                            {!isSuper && u.id !== currentUser?.id && (
                              <button
                                onClick={() => handleDeleteStaff(u)}
                                className="btn"
                                style={{
                                  padding: '0.4rem 0.65rem',
                                  fontSize: '0.8rem',
                                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                  color: '#ef4444',
                                  borderColor: 'rgba(239, 68, 68, 0.3)',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '0.3rem'
                                }}
                                title="O'chirish"
                              >
                                <Trash2 size={13} /> O'chirish
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Sub-Admin Create/Edit Modal */}
      {staffModalOpen && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.65)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '1rem'
        }}>
          <div className="card" style={{
            maxWidth: '650px',
            width: '100%',
            maxHeight: '90vh',
            overflowY: 'auto',
            padding: '1.75rem',
            position: 'relative'
          }}>
            {/* Modal Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Users size={20} color="var(--primary)" />
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>
                  {editingStaff ? `Xodimni Tahrirlash: @${editingStaff.username}` : "Yangi Xodim Qo'shish"}
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setStaffModalOpen(false)}
                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Error / Success messages in modal */}
            {staffError && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(239, 68, 68, 0.12)',
                color: '#ef4444',
                fontSize: '0.85rem',
                marginBottom: '1rem',
                border: '1px solid rgba(239, 68, 68, 0.3)'
              }}>
                {staffError}
              </div>
            )}
            {staffSuccess && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(16, 185, 129, 0.12)',
                color: '#10b981',
                fontSize: '0.85rem',
                marginBottom: '1rem',
                border: '1px solid rgba(16, 185, 129, 0.3)'
              }}>
                {staffSuccess}
              </div>
            )}

            <form onSubmit={handleSaveStaff} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
                <div className="form-group">
                  <label style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem', display: 'block' }}>
                    Ism / Familiya
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    value={staffForm.first_name}
                    onChange={(e) => setStaffForm({ ...staffForm, first_name: e.target.value })}
                    placeholder="Masalan: Sardor Aliyev"
                  />
                </div>

                <div className="form-group">
                  <label style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem', display: 'block' }}>
                    Login (Foydalanuvchi nomi) *
                  </label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={staffForm.username}
                    onChange={(e) => setStaffForm({ ...staffForm, username: e.target.value })}
                    placeholder="Masalan: sardor_admin"
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
                <div className="form-group">
                  <label style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem', display: 'block' }}>
                    {editingStaff ? "Yangi Parol (O'zgartirmaslik uchun bo'sh qoldiring)" : "Parol *"}
                  </label>
                  <input
                    type="text"
                    required={!editingStaff}
                    className="form-control"
                    value={staffForm.password}
                    onChange={(e) => setStaffForm({ ...staffForm, password: e.target.value })}
                    placeholder="Kamida 4 ta belgi"
                  />
                </div>

                <div className="form-group">
                  <label style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem', display: 'block' }}>
                    Telefon raqami
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    value={staffForm.phone_number}
                    onChange={(e) => setStaffForm({ ...staffForm, phone_number: e.target.value })}
                    placeholder="+998901234567"
                  />
                </div>
              </div>

              {/* Ruxsat etilgan bo'limlar (Permissions) */}
              <div style={{ marginTop: '0.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <label style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)' }}>
                    Ruxsat etilgan bo'limlar (Tab Permissions)
                  </label>
                  <button
                    type="button"
                    onClick={handleSelectAllTabs}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'var(--primary)',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    {staffForm.allowed_tabs.length === AVAILABLE_TABS.length ? "Barchasini bekor qilish" : "Barchasini belgilash"}
                  </button>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                  gap: '0.6rem',
                  maxHeight: '220px',
                  overflowY: 'auto',
                  padding: '0.5rem',
                  borderRadius: '8px',
                  backgroundColor: 'var(--bg-inner)'
                }}>
                  {AVAILABLE_TABS.map(tab => {
                    const isChecked = staffForm.allowed_tabs.includes(tab.id);
                    return (
                      <div
                        key={tab.id}
                        onClick={() => toggleTabPermission(tab.id)}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.5rem',
                          padding: '0.5rem 0.75rem',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          backgroundColor: isChecked ? 'rgba(59, 130, 246, 0.12)' : 'transparent',
                          border: `1px solid ${isChecked ? 'rgba(59, 130, 246, 0.3)' : 'var(--border-color)'}`,
                          transition: 'all 0.15s ease'
                        }}
                      >
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {}} // Handled by div onClick
                          style={{ cursor: 'pointer' }}
                        />
                        <span style={{ fontSize: '0.88rem' }}>{tab.icon}</span>
                        <span style={{ fontSize: '0.84rem', fontWeight: isChecked ? 600 : 400, color: isChecked ? 'var(--primary)' : 'var(--text-main)' }}>
                          {tab.label}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Modal Actions */}
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
                <button
                  type="button"
                  onClick={() => setStaffModalOpen(false)}
                  className="btn btn-secondary"
                  style={{ padding: '0.65rem 1.25rem', fontSize: '0.88rem' }}
                >
                  Bekor qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={staffSaving}
                  style={{ padding: '0.65rem 1.5rem', fontSize: '0.88rem', fontWeight: 700 }}
                >
                  {staffSaving ? "Saqlanmoqda..." : editingStaff ? "O'zgarishlarni Saqlash" : "Xodimni Yaratish"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

