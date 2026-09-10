import React, { useState } from 'react';
import { sendBroadcast } from '../services/api';
import { Megaphone, Send, CheckCircle2, AlertCircle, Sparkles, Users, UserCheck, Globe, FileText, Check } from 'lucide-react';

export default function BroadcastManager() {
  const [target, setTarget] = useState('ALL');
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const templates = [
    {
      title: "Yangi Xizmatlar va Maxsus Takliflar",
      text: "<b>Assalomu alaykum!</b>\n\nPlatformamizda yangi xizmat turlari va qulay takliflar faollashtirildi. O'zingizga kerakli professional mutaxassisni bir necha daqiqada toping."
    },
    {
      title: "Ustalarga Yangi Buyurtmalar Eslatmasi",
      text: "<b>Hurmatli ustalar va mutaxassislar!</b>\n\nHozirda platformada yangi buyurtmalar qabul qilinmoqda. Yangi buyurtmalarni o'z vaqtida qabul qilish uchun iltimos, botda <b>ONLINE</b> rejimini faollashtiring."
    },
    {
      title: "Tizim Yangilanishi va Profil Xabarnomasi",
      text: "<b>Tizim yangilandi!</b>\n\nPlatformamizning qulayliklari kengaytirildi. Shaxsiy profilingizdagi ma'lumotlar va telefon raqamingiz to'g'riligini tekshirib olishingizni so'raymiz."
    }
  ];

  const handleSend = async (e) => {
    e.preventDefault();
    if (!messageText.trim()) {
      alert("Iltimos, e'lon matnini kiriting.");
      return;
    }

    const targetName = target === 'ALL' ? 'barcha foydalanuvchilar' : (target === 'WORKERS' ? 'barcha ustalar' : 'barcha mijozlar');
    if (!window.confirm(`Haqiqatan ham ushbu xabarnomani ${targetName}ga yuborishni tasdiqlaysizmi?`)) {
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await sendBroadcast(target, messageText.trim());
      setResult({
        type: 'success',
        message: res.data.message,
        details: res.data
      });
      setMessageText('');
    } catch (err) {
      const errDetail = err.response?.data?.error || 'Xabarnoma yuborishda xatolik yuz berdi!';
      setResult({
        type: 'error',
        message: errDetail
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      
      {/* Header Info */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ padding: '0.6rem', borderRadius: '10px', background: 'rgba(59, 130, 246, 0.12)', color: '#3b82f6' }}>
            <Megaphone size={22} />
          </div>
          <div>
            <h2 className="card-title" style={{ margin: 0 }}>Ommaviy Xabarnomalar (Broadcast)</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Telegram bot orqali barcha ro'yxatdan o'tgan auditoriyaga yoki maqsadli guruhlarga rasmiy bildirishnoma yuborish
            </p>
          </div>
        </div>

        {/* Result alert */}
        {result && (
          <div style={{
            marginTop: '1.25rem',
            padding: '1rem 1.25rem',
            borderRadius: '8px',
            backgroundColor: result.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
            border: `1px solid ${result.type === 'success' ? '#10b981' : '#ef4444'}`,
            color: result.type === 'success' ? '#10b981' : '#ef4444',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.75rem'
          }}>
            {result.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>{result.message}</div>
              {result.details && (
                <div style={{ fontSize: '0.78rem', marginTop: '0.3rem', color: 'var(--text-secondary)' }}>
                  Jami auditoriya: <strong>{result.details.total_targeted}</strong> ta | 
                  Yetkazildi: <strong style={{ color: '#10b981' }}>{result.details.success_count}</strong> | 
                  Yetmadi: <strong style={{ color: '#ef4444' }}>{result.details.fail_count}</strong>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Main Broadcast Form & Templates */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
        
        {/* Form Panel */}
        <div className="card" style={{ margin: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
            <Send size={18} color="#3b82f6" />
            <h3 className="card-title" style={{ margin: 0 }}>Yangi Xabarnoma Yaratish</h3>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '1.2rem' }}>
            Auditoriya toifasini tanlang va rasmiy xabar matnini kiriting
          </p>

          <form onSubmit={handleSend} style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
            
            {/* Target Audience selection */}
            <div className="form-group">
              <label>Maqsadli Auditoriya:</label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', marginTop: '0.3rem' }}>
                {[
                  { id: 'ALL', label: 'Barcha Foydalanuvchilar', icon: Globe, desc: 'Barcha bot foydalanuvchilari' },
                  { id: 'WORKERS', label: 'Faqat Ustalar', icon: UserCheck, desc: 'Mutaxassislar va ustalar' },
                  { id: 'CLIENTS', label: 'Faqat Mijozlar', icon: Users, desc: 'Buyurtmachilar' }
                ].map(aud => {
                  const Icon = aud.icon;
                  const isSelected = target === aud.id;
                  return (
                    <button
                      key={aud.id}
                      type="button"
                      onClick={() => setTarget(aud.id)}
                      style={{
                        padding: '0.85rem 0.5rem',
                        borderRadius: '8px',
                        border: '1px solid',
                        borderColor: isSelected ? 'var(--primary)' : 'var(--border-color)',
                        background: isSelected ? 'rgba(59, 130, 246, 0.12)' : 'var(--bg-inner)',
                        color: isSelected ? '#3b82f6' : 'var(--text-muted)',
                        cursor: 'pointer',
                        textAlign: 'center',
                        transition: 'all 0.15s',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        gap: '0.3rem'
                      }}
                    >
                      <Icon size={18} />
                      <div style={{ fontWeight: 700, fontSize: '0.84rem' }}>{aud.label}</div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{aud.desc}</div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Message Text */}
            <div className="form-group">
              <label>Xabarnoma Matni (HTML format qo'llab-quvvatlanadi):</label>
              <textarea
                className="form-control"
                rows="7"
                placeholder="Xabarnoma matnini kiriting..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                required
                style={{ fontSize: '0.9rem', lineHeight: '1.5' }}
              ></textarea>
              <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                Formatlash teglari: <code>&lt;b&gt;qalin&lt;/b&gt;</code>, <code>&lt;i&gt;kursiv&lt;/i&gt;</code>, <code>&lt;code&gt;kod&lt;/code&gt;</code>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="btn"
              disabled={loading}
              style={{
                padding: '0.85rem',
                fontSize: '0.92rem',
                fontWeight: 700
              }}
            >
              {loading ? 'Yuborilmoqda...' : 'Xabarnomani Barcha Foydalanuvchilarga Yuborish'}
            </button>
          </form>
        </div>

        {/* Preset Templates */}
        <div className="card" style={{ margin: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
            <FileText size={18} color="#3b82f6" />
            <h3 className="card-title" style={{ margin: 0 }}>Standart Xabarnoma Shablonlari</h3>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '1rem' }}>
            Tezkor foydalanish uchun rasmiy xabarnoma namunalari
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {templates.map((tpl, idx) => (
              <div
                key={idx}
                style={{
                  padding: '1rem',
                  backgroundColor: 'var(--bg-inner)',
                  borderRadius: '8px',
                  border: '1px solid var(--border-color)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.5rem'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-main)' }}>{tpl.title}</span>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    style={{ padding: '0.3rem 0.65rem', fontSize: '0.75rem' }}
                    onClick={() => setMessageText(tpl.text)}
                  >
                    Nusxalash
                  </button>
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', whiteSpace: 'pre-line', lineHeight: '1.4' }}>
                  {tpl.text}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
