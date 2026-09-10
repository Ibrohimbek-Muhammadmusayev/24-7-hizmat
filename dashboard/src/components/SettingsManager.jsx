import React, { useState } from 'react';
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
  HelpCircle
} from 'lucide-react';
import { changeAdminCredentials } from '../services/api';

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
              Admin panelga kirish paroli, logini va boshqaruv xavfsizligini moslashtirish
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
                  {currentUser?.role === 'ADMIN' ? 'Bosh Administrator (Superuser)' : 'Operator'}
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

          <div className="card" style={{ padding: '1.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
              <HelpCircle size={18} color="var(--primary)" />
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)' }}>
                Xavfsizlik Tavsiyasi
              </h4>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: '1.5' }}>
              Parolni yangilaganingizdan so'ng xavfsizlik maqsadida yangi login va parolingizni eslab qoling. Yangilanish bilan joriy sessiyangiz yangi token bilan uzluksiz davom etadi.
            </p>
          </div>
        </div>

      </div>

    </div>
  );
}
