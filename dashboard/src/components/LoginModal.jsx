import React, { useState } from 'react';
import { loginUser } from '../services/api';
import { Lock, ShieldCheck, User, KeyRound, AlertCircle } from 'lucide-react';

export default function LoginModal({ onLoginSuccess, sessionMessage }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await loginUser(username, password);
      const { access, user } = res.data;
      localStorage.setItem('token', access);
      localStorage.setItem('user', JSON.stringify(user));
      onLoginSuccess(user);
    } catch (err) {
      setError("Login yoki parol noto'g'ri kiritildi!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-card" style={{ maxWidth: '400px', padding: '2.25rem 2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{
            width: '52px',
            height: '52px',
            borderRadius: '14px',
            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2))',
            border: '1px solid rgba(59, 130, 246, 0.35)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1.1rem auto',
            boxShadow: '0 4px 15px rgba(59, 130, 246, 0.15)'
          }}>
            <ShieldCheck size={28} color="#3b82f6" />
          </div>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
            {localStorage.getItem('project_name') || 'IshBazari'} Boshqaruv Tizimi
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', marginTop: '0.35rem' }}>
            Tizimga kirish uchun login va parolingizni kiriting
          </p>
        </div>

        {sessionMessage && !error && (
          <div style={{ 
            padding: '0.75rem', 
            borderRadius: '8px', 
            backgroundColor: 'rgba(245, 158, 11, 0.15)', 
            color: '#f59e0b', 
            fontSize: '0.84rem', 
            marginBottom: '1.25rem',
            border: '1px solid rgba(245, 158, 11, 0.35)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            lineHeight: 1.4
          }}>
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{sessionMessage}</span>
          </div>
        )}

        {error && (
          <div style={{ 
            padding: '0.75rem', 
            borderRadius: '8px', 
            backgroundColor: 'rgba(239, 68, 68, 0.12)', 
            color: '#ef4444', 
            fontSize: '0.84rem', 
            marginBottom: '1.25rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            border: '1px solid rgba(239, 68, 68, 0.25)'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '1.2rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              <User size={14} color="var(--primary)" /> Login (Foydalanuvchi nomi)
            </label>
            <input
              type="text"
              required
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Loginni kiriting"
              autoFocus
            />
          </div>

          <div className="form-group" style={{ marginBottom: '1.75rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              <KeyRound size={14} color="var(--primary)" /> Maxfiy Parol
            </label>
            <input
              type="password"
              required
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Parolni kiriting"
            />
          </div>

          <button type="submit" className="btn" style={{ width: '100%', padding: '0.85rem', fontWeight: 700, fontSize: '0.95rem' }} disabled={loading}>
            {loading ? 'Tekshirilmoqda...' : 'Tizimga Kirish'}
          </button>
        </form>
      </div>
    </div>
  );
}
