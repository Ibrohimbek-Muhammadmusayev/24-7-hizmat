import React, { useState, useEffect, useRef } from 'react';
import { 
  fetchBotStatus, 
  startBot, 
  stopBot, 
  restartBot, 
  updateBotTokens,
  updateBotSettings,
  sendBotMessage 
} from '../services/api';
import { 
  Bot, 
  Play, 
  Square, 
  RotateCw, 
  Eye, 
  EyeOff, 
  Send, 
  CheckCircle2, 
  AlertCircle, 
  X, 
  Save, 
  PhoneCall, 
  FileText, 
  MessageSquare, 
  ExternalLink,
  Settings,
  Sparkles,
  ShieldCheck,
  Globe,
  Layers,
  Phone,
  HardHat,
  Briefcase
} from 'lucide-react';

export default function BotControlPanel() {
  const [activeTab, setActiveTab] = useState('token'); // 'token' | 'cms' | 'test'
  const initialLoadedRef = useRef(false);
  
  const [botStatus, setBotStatus] = useState({
    token: '',
    worker_bot_token: '',
    client_bot_token: '',
    is_running: false,
    pid: null,
    project_name: 'IshBazari',
    welcome_text: '',
    about_text: '',
    call_center_phone: '',
    help_text: '',
    worker_bot_username: '',
    worker_bot_name: '',
    worker_token_valid: false,
    client_bot_username: '',
    client_bot_name: '',
    client_token_valid: false,
    bot_username: '',
    bot_name: '',
    token_valid: false
  });

  const [workerTokenInput, setWorkerTokenInput] = useState('');
  const [clientTokenInput, setClientTokenInput] = useState('');
  const [showWorkerToken, setShowWorkerToken] = useState(false);
  const [showClientToken, setShowClientToken] = useState(false);

  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState('');
  const [notification, setNotification] = useState(null);

  const [cmsData, setCmsData] = useState({
    project_name: 'IshBazari',
    welcome_text: '',
    about_text: '',
    call_center_phone: '+998 (71) 200-00-00',
    help_text: '',
    client_bot_url: '',
    worker_bot_url: '',
    app_url: '',
    app_url_enabled: false
  });

  const [msgChatId, setMsgChatId] = useState('');
  const [msgText, setMsgText] = useState('');
  const [msgBotType, setMsgBotType] = useState('WORKER'); // 'WORKER' | 'CLIENT'
  const [sendingMsg, setSendingMsg] = useState(false);

  const showFeedback = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 5000);
  };

  const loadStatus = async (isManual = false) => {
    try {
      if (isManual) setLoading(true);
      const res = await fetchBotStatus();
      if (res && res.data) {
        setBotStatus(res.data);
        if (res.data.project_name) {
          localStorage.setItem('project_name', res.data.project_name);
        }
        
        // Only update form inputs on first initial load or explicit manual refresh / save
        if (!initialLoadedRef.current || isManual) {
          const wTok = res.data.worker_bot_token || res.data.token || '';
          const cTok = res.data.client_bot_token || '';
          
          if (wTok) setWorkerTokenInput(wTok);
          if (cTok) setClientTokenInput(cTok);

          setCmsData({
            project_name: res.data.project_name || 'IshBazari',
            welcome_text: res.data.welcome_text || '',
            about_text: res.data.about_text || '',
            call_center_phone: res.data.call_center_phone || '+998 (71) 200-00-00',
            help_text: res.data.help_text || '',
            client_bot_url: res.data.client_bot_url || '',
            worker_bot_url: res.data.worker_bot_url || '',
            app_url: res.data.app_url || '',
            app_url_enabled: Boolean(res.data.app_url_enabled)
          });

          initialLoadedRef.current = true;
        }
      }
    } catch (err) {
      console.error("Bot holatini yuklashda xatolik:", err);
      if (isManual) {
        showFeedback('error', 'Bot holatini serverdan yuklab bo\'lmadi.');
      }
    } finally {
      if (isManual) setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus(false);
    const interval = setInterval(() => loadStatus(false), 8000);
    return () => clearInterval(interval);
  }, []);

  const handleStartBot = async () => {
    try {
      setActionLoading('start');
      const res = await startBot();
      showFeedback('success', res.data.message || 'Telegram botlar muvaffaqiyatli ishga tushirildi!');
      loadStatus();
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Botlarni ishga tushirishda xatolik yuz berdi.');
    } finally {
      setActionLoading('');
    }
  };

  const handleStopBot = async () => {
    try {
      setActionLoading('stop');
      const res = await stopBot();
      showFeedback('success', res.data.message || 'Telegram botlar to\'xtatildi.');
      loadStatus();
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Botlarni to\'xtatishda xatolik yuz berdi.');
    } finally {
      setActionLoading('');
    }
  };

  const handleRestartBot = async () => {
    try {
      setActionLoading('restart');
      const res = await restartBot();
      showFeedback('success', res.data.message || 'Telegram botlar qayta ishga tushirildi!');
      loadStatus();
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Botlarni qayta yuklashda xatolik yuz berdi.');
    } finally {
      setActionLoading('');
    }
  };

  const handleSaveTokens = async (e) => {
    e.preventDefault();
    if (!workerTokenInput.trim() && !clientTokenInput.trim()) {
      showFeedback('error', 'Iltimos, kamida bitta bot tokenini kiriting.');
      return;
    }

    try {
      setActionLoading('save_token');
      const res = await updateBotTokens({ 
        worker_bot_token: workerTokenInput.trim(),
        client_bot_token: clientTokenInput.trim()
      });
      showFeedback('success', res.data.message || 'Bot tokenlari muvaffaqiyatli saqlandi!');
      loadStatus();
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Tokenlarni saqlashda xatolik yuz berdi.');
    } finally {
      setActionLoading('');
    }
  };

  const handleSaveCMS = async (e) => {
    e.preventDefault();
    try {
      setActionLoading('save_cms');
      const res = await updateBotSettings(cmsData);
      showFeedback('success', res.data.message || 'Bot matnlari va sozlamalari saqlandi!');
      loadStatus();
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Sozlamalarni saqlashda xatolik yuz berdi.');
    } finally {
      setActionLoading('');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!msgChatId.trim() || !msgText.trim()) {
      showFeedback('error', 'Telegram ID va xabar matnini to\'ldiring.');
      return;
    }

    try {
      setSendingMsg(true);
      await sendBotMessage(msgChatId.trim(), msgText.trim(), msgBotType);
      showFeedback('success', `Xabar (ID: ${msgChatId}) ga ${msgBotType === 'WORKER' ? 'Usta boti' : 'Ish joylash boti'} orqali yuborildi!`);
      setMsgText('');
    } catch (err) {
      showFeedback('error', err.response?.data?.error || 'Xabar yuborishda xatolik yuz berdi.');
    } finally {
      setSendingMsg(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Toast Notification */}
      {notification && (
        <div style={{
          padding: '0.85rem 1.15rem',
          borderRadius: '10px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          backgroundColor: notification.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
          border: `1px solid ${notification.type === 'success' ? '#10b981' : '#ef4444'}`,
          color: notification.type === 'success' ? '#10b981' : '#ef4444',
          fontSize: '0.9rem',
          fontWeight: 600
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            {notification.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
            <span>{notification.message}</span>
          </div>
          <button 
            onClick={() => setNotification(null)}
            style={{ background: 'transparent', border: 'none', color: 'inherit', cursor: 'pointer' }}
          >
            <X size={16} />
          </button>
        </div>
      )}

      {/* Main Banner Card */}
      <div className="card" style={{ marginBottom: 0, padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.25rem' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2))',
              border: '1px solid rgba(59, 130, 246, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#3b82f6'
            }}>
              <Bot size={28} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <h2 className="card-title" style={{ margin: 0, fontSize: '1.3rem' }}>
                  Telegram Bot Boshqaruv Markazi (Dual Bot)
                </h2>
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  padding: '0.2rem 0.55rem',
                  borderRadius: '6px',
                  backgroundColor: 'rgba(139, 92, 246, 0.15)',
                  color: '#8b5cf6',
                  border: '1px solid rgba(139, 92, 246, 0.3)'
                }}>
                  DUAL ENTERPRISE
                </span>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                Ikkala botni (Usta va Ish beruvchi botlari) yagona markazdan boshqarish, monitoring qilish va sozlash
              </p>
            </div>
          </div>

          {/* Action Control Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
            <button
              onClick={handleStartBot}
              disabled={actionLoading !== '' || botStatus.is_running}
              className="btn"
              style={{
                backgroundColor: botStatus.is_running ? 'var(--bg-inner)' : '#10b981',
                borderColor: botStatus.is_running ? 'var(--border-color)' : '#10b981',
                color: botStatus.is_running ? 'var(--text-muted)' : '#fff',
                cursor: botStatus.is_running ? 'not-allowed' : 'pointer'
              }}
            >
              <Play size={16} />
              {actionLoading === 'start' ? 'Ishga tushmoqda...' : 'Botlarni Ishga Tushirish'}
            </button>

            <button
              onClick={handleStopBot}
              disabled={actionLoading !== '' || !botStatus.is_running}
              className="btn"
              style={{
                backgroundColor: !botStatus.is_running ? 'var(--bg-inner)' : '#ef4444',
                borderColor: !botStatus.is_running ? 'var(--border-color)' : '#ef4444',
                color: !botStatus.is_running ? 'var(--text-muted)' : '#fff',
                cursor: !botStatus.is_running ? 'not-allowed' : 'pointer'
              }}
            >
              <Square size={16} />
              {actionLoading === 'stop' ? 'To\'xtatilmoqda...' : 'To\'xtatish'}
            </button>

            <button
              onClick={handleRestartBot}
              disabled={actionLoading !== ''}
              className="btn btn-secondary"
              title="Qayta yuklash"
            >
              <RotateCw size={16} className={actionLoading === 'restart' ? 'spin' : ''} />
              Qayta Yuklash
            </button>
          </div>

        </div>

        {/* Live Status Indicators Grid (Dual Bot Cards) */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '1rem',
          marginTop: '1.25rem',
          paddingTop: '1.25rem',
          borderTop: '1px solid var(--border-color)'
        }}>
          
          {/* Service status */}
          <div style={{
            padding: '1rem',
            borderRadius: '10px',
            backgroundColor: 'var(--bg-inner)',
            border: '1px solid var(--border-color)'
          }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
              Servis & Polling Holati
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.35rem' }}>
              <span style={{
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                backgroundColor: botStatus.is_running ? '#10b981' : '#ef4444',
                boxShadow: botStatus.is_running ? '0 0 8px #10b981' : 'none'
              }} />
              <strong style={{ fontSize: '1rem', color: 'var(--text-main)' }}>
                {botStatus.is_running ? 'FAOL (Ishlamoqda)' : 'TO\'XTATILGAN'}
              </strong>
            </div>
            {botStatus.pid && (
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem', display: 'block' }}>
                PID: <code>{botStatus.pid}</code>
              </span>
            )}
          </div>

          {/* 1-Bot: Worker Bot */}
          <div style={{
            padding: '1rem',
            borderRadius: '10px',
            backgroundColor: 'var(--bg-inner)',
            border: '1px solid var(--border-color)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <HardHat size={14} color="#10b981" />
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
                  1. {botStatus.project_name || 'IshBazari'} (Usta Boti)
                </span>
              </div>
              <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', marginTop: '0.35rem' }}>
                {botStatus.worker_bot_username ? `@${botStatus.worker_bot_username}` : (botStatus.bot_username ? `@${botStatus.bot_username}` : 'Ulanmagan')}
              </div>
              <div style={{ fontSize: '0.74rem', color: botStatus.worker_token_valid ? '#10b981' : '#f59e0b', marginTop: '0.2rem' }}>
                {botStatus.worker_token_valid ? '✓ Token faol' : 'Token kiritilmagan'}
              </div>
            </div>
            {botStatus.worker_bot_username && (
              <a
                href={`https://t.me/${botStatus.worker_bot_username}`}
                target="_blank"
                rel="noreferrer"
                style={{
                  padding: '0.45rem',
                  borderRadius: '8px',
                  backgroundColor: 'rgba(16, 185, 129, 0.12)',
                  color: '#10b981',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <ExternalLink size={16} />
              </a>
            )}
          </div>

          {/* 2-Bot: Client Bot */}
          <div style={{
            padding: '1rem',
            borderRadius: '10px',
            backgroundColor: 'var(--bg-inner)',
            border: '1px solid var(--border-color)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Briefcase size={14} color="#3b82f6" />
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
                  2. Ish Joylash (Client Boti)
                </span>
              </div>
              <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', marginTop: '0.35rem' }}>
                {botStatus.client_bot_username ? `@${botStatus.client_bot_username}` : 'Ulanmagan'}
              </div>
              <div style={{ fontSize: '0.74rem', color: botStatus.client_token_valid ? '#10b981' : '#f59e0b', marginTop: '0.2rem' }}>
                {botStatus.client_token_valid ? '✓ Token faol' : 'Token kiritilmagan'}
              </div>
            </div>
            {botStatus.client_bot_username && (
              <a
                href={`https://t.me/${botStatus.client_bot_username}`}
                target="_blank"
                rel="noreferrer"
                style={{
                  padding: '0.45rem',
                  borderRadius: '8px',
                  backgroundColor: 'rgba(59, 130, 246, 0.12)',
                  color: '#3b82f6',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <ExternalLink size={16} />
              </a>
            )}
          </div>

        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
        {[
          { id: 'token', label: '🔑 Bot Tokenlari & Ulanish', icon: Settings },
          { id: 'cms', label: '📝 Bot Matnlari & Call Center (CMS)', icon: FileText },
          { id: 'test', label: '✉️ Xabar Sinash (Test Message)', icon: MessageSquare }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className="btn"
              style={{
                backgroundColor: isActive ? 'var(--primary)' : 'var(--bg-card)',
                borderColor: isActive ? 'var(--primary)' : 'var(--border-color)',
                color: isActive ? '#fff' : 'var(--text-secondary)',
                padding: '0.55rem 1.1rem',
                fontSize: '0.86rem'
              }}
            >
              <Icon size={16} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* TAB 1: TOKEN & CONNECTION */}
      {activeTab === 'token' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.25rem' }}>
          
          {/* Dual Bot Tokens Form */}
          <div className="card" style={{ marginBottom: 0 }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Bot size={18} color="#3b82f6" />
              Bot Tokenlarini Sozlash (Dual Bot)
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.3rem' }}>
              Ikkala bot uchun alohida yoki yagona token kiriting. Tokenlar saqlangach tizim avtomatik qayta ulanadi:
            </p>

            <form onSubmit={handleSaveTokens} style={{ marginTop: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              
              {/* 1. Worker Bot Token */}
              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 600 }}>
                  <HardHat size={15} color="#10b981" />
                  1. Usta & Ish Qidiruvchi Boti Tokeni ({botStatus.project_name || 'IshBazari'})
                </label>
                <div style={{ position: 'relative', marginTop: '0.3rem' }}>
                  <input
                    type={showWorkerToken ? 'text' : 'password'}
                    value={workerTokenInput}
                    onChange={(e) => setWorkerTokenInput(e.target.value)}
                    placeholder="Masalan: 8926495899:AAFNhhgjj..."
                    className="form-input"
                    style={{ paddingRight: '2.5rem', fontFamily: 'monospace' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowWorkerToken(!showWorkerToken)}
                    style={{
                      position: 'absolute',
                      right: '0.75rem',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      background: 'transparent',
                      border: 'none',
                      color: 'var(--text-muted)',
                      cursor: 'pointer'
                    }}
                  >
                    {showWorkerToken ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {botStatus.worker_bot_username && (
                  <span style={{ fontSize: '0.75rem', color: '#10b981', marginTop: '0.25rem', display: 'block' }}>
                    Ulangan bot: @{botStatus.worker_bot_username} ({botStatus.worker_bot_name})
                  </span>
                )}
              </div>

              {/* 2. Client Bot Token */}
              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 600 }}>
                  <Briefcase size={15} color="#3b82f6" />
                  2. Ish Beruvchi / E'lon Joylash Boti Tokeni (Client Bot)
                </label>
                <div style={{ position: 'relative', marginTop: '0.3rem' }}>
                  <input
                    type={showClientToken ? 'text' : 'password'}
                    value={clientTokenInput}
                    onChange={(e) => setClientTokenInput(e.target.value)}
                    placeholder="Masalan: 7890123456:AAGH..."
                    className="form-input"
                    style={{ paddingRight: '2.5rem', fontFamily: 'monospace' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowClientToken(!showClientToken)}
                    style={{
                      position: 'absolute',
                      right: '0.75rem',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      background: 'transparent',
                      border: 'none',
                      color: 'var(--text-muted)',
                      cursor: 'pointer'
                    }}
                  >
                    {showClientToken ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {botStatus.client_bot_username && (
                  <span style={{ fontSize: '0.75rem', color: '#3b82f6', marginTop: '0.25rem', display: 'block' }}>
                    Ulangan bot: @{botStatus.client_bot_username} ({botStatus.client_bot_name})
                  </span>
                )}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  * Tokenlar kiritilgach ikkala bot mustaqil ishlaydi va o'zaro integratsiyada ishlaydi.
                </span>
                <button
                  type="submit"
                  disabled={actionLoading === 'save_token'}
                  className="btn"
                >
                  <Save size={15} />
                  {actionLoading === 'save_token' ? 'Tekshirilmoqda...' : 'Tokenlarni Saqlash'}
                </button>
              </div>
            </form>
          </div>

          {/* Dual Bot Info Card */}
          <div className="card" style={{ marginBottom: 0, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Sparkles size={16} color="#f59e0b" />
                Ikkita Bot Arxitekturasi
              </h4>
              <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.84rem' }}>
                <li style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#10b981', fontWeight: 'bold' }}>1.</span>
                  <div>
                    <strong style={{ color: '#10b981' }}>{botStatus.project_name || 'IshBazari'} (Usta boti):</strong>
                    <div>Ustalarni ro'yxatga olish, portfolio, bandlik holati (Online/Band) va yangi e'lonlar haqida tezkor push-xabarlar qabul qilish.</div>
                  </div>
                </li>
                <li style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#3b82f6', fontWeight: 'bold' }}>2.</span>
                  <div>
                    <strong style={{ color: '#3b82f6' }}>Ish Joylash (Client boti):</strong>
                    <div>Ish beruvchilar va mijozlar uchun kunbay/doimiy e'lon berish, mutaxassis tanlash, GPS lokatsiya, otkliklar va arizalarni ko'rish.</div>
                  </div>
                </li>
                <li style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#8b5cf6', fontWeight: 'bold' }}>⚡</span>
                  <div>
                    <strong style={{ color: '#8b5cf6' }}>Smart Distribution Engine:</strong>
                    <div>Ish beruvchi e'lon joylaganda, tizim shu hududdagi barcha tegishli ustalarga Usta boti orqali avtomatik push xabar yuboradi.</div>
                  </div>
                </li>
              </ul>
            </div>

            <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)', display: 'flex', gap: '0.5rem' }}>
              {botStatus.worker_bot_username && (
                <a
                  href={`https://t.me/${botStatus.worker_bot_username}`}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-secondary"
                  style={{ flex: 1, color: '#10b981', justifyContent: 'center', fontSize: '0.8rem' }}
                >
                  <HardHat size={14} />
                  Usta Boti
                </a>
              )}
              {botStatus.client_bot_username && (
                <a
                  href={`https://t.me/${botStatus.client_bot_username}`}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-secondary"
                  style={{ flex: 1, color: '#3b82f6', justifyContent: 'center', fontSize: '0.8rem' }}
                >
                  <Briefcase size={14} />
                  Ish Joylash Boti
                </a>
              )}
            </div>
          </div>

        </div>
      )}

      {/* TAB 2: CMS & TEXT SETTINGS */}
      {activeTab === 'cms' && (
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileText size={18} color="#8b5cf6" />
            Bot Matnlari va Call Center Sozlamalari
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.3rem' }}>
            Botdagi ma'lumotlar, Call Center telefoni va yordam matnlarini to'g'ridan-to'g'ri boshqaring:
          </p>

          <form onSubmit={handleSaveCMS} style={{ marginTop: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 700 }}>
                <Sparkles size={15} color="#f59e0b" />
                🏢 Loyiha & Brend Nomi (Platform Brand Name)
              </label>
              <input
                type="text"
                value={cmsData.project_name}
                onChange={(e) => setCmsData({ ...cmsData, project_name: e.target.value })}
                placeholder="IshBazari"
                className="form-input"
                style={{ fontWeight: 600, fontSize: '0.95rem' }}
              />
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
                💡 Bu nom butun tizim bo'ylab (Usta boti, Ish beruvchi boti, asosiy menyu, xabarnomalar va qo'llanmalarda) avtomatik aks etadi.
              </span>
            </div>

            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Phone size={14} color="#3b82f6" />
                Call Center Telefon Raqami
              </label>
              <input
                type="text"
                value={cmsData.call_center_phone}
                onChange={(e) => setCmsData({ ...cmsData, call_center_phone: e.target.value })}
                placeholder="+998 (71) 200-00-00"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Bot Haqida Matni (About Text)</label>
              <textarea
                rows={3}
                value={cmsData.about_text}
                onChange={(e) => setCmsData({ ...cmsData, about_text: e.target.value })}
                className="form-textarea"
                placeholder="Full-Xizmat — usta va mijozlarni bog'lovchi xizmat platformasi..."
              />
            </div>

            <div className="form-group">
              <label>Yordam va Qo'llanma Matni (Help Text)</label>
              <textarea
                rows={3}
                value={cmsData.help_text}
                onChange={(e) => setCmsData({ ...cmsData, help_text: e.target.value })}
                className="form-textarea"
                placeholder="Botdan foydalanish yo'riqnomasi..."
              />
            </div>

            {/* Botlararo O'tish Havolalari (Cross-Bot Redirection URLs) */}
            <div style={{
              marginTop: '0.5rem',
              padding: '1.2rem',
              borderRadius: '10px',
              backgroundColor: 'var(--bg-hover)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}>
              <div>
                <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                  <Bot size={16} color="#10b981" />
                  🔗 Botlararo O'tish Havolalari (O'zaro bog'lanish)
                </h4>
                <p style={{ margin: '0.2rem 0 0 0', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Usta botidagi "Ish beruvchi botiga o'tish" tugmasi havolasini boshqaring. Agar bo'sh qoldirilsa, tizim avtomatik tarzda kiritilgan bot tokeni orqali to'g'ri havolani shakllantiradi.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label style={{ fontSize: '0.82rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <Briefcase size={14} color="#3b82f6" />
                    Ish Beruvchi (Client) Boti Havolasi
                  </label>
                  <input
                    type="url"
                    value={cmsData.client_bot_url}
                    onChange={(e) => setCmsData({ ...cmsData, client_bot_url: e.target.value })}
                    placeholder={botStatus.client_bot_username ? `https://t.me/${botStatus.client_bot_username}?start=ref_worker_bot (Avto)` : "https://t.me/ishjoyla_bot?start=ref_worker_bot"}
                    className="form-input"
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem', display: 'block' }}>
                    {botStatus.client_bot_username ? `Avtomatik havola: https://t.me/${botStatus.client_bot_username}?start=ref_worker_bot` : "Standart: Ish joylash botiga yo'naltiradi"}
                  </span>
                </div>

                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label style={{ fontSize: '0.82rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <HardHat size={14} color="#10b981" />
                    Ish Qidiruvchi (Usta) Boti Havolasi
                  </label>
                  <input
                    type="url"
                    value={cmsData.worker_bot_url}
                    onChange={(e) => setCmsData({ ...cmsData, worker_bot_url: e.target.value })}
                    placeholder={botStatus.worker_bot_username ? `https://t.me/${botStatus.worker_bot_username}?start=ref_client_bot (Avto)` : "https://t.me/ish_24_7_bot?start=ref_client_bot"}
                    className="form-input"
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem', display: 'block' }}>
                    {botStatus.worker_bot_username ? `Avtomatik havola: https://t.me/${botStatus.worker_bot_username}?start=ref_client_bot` : "Standart: Usta botiga yo'naltiradi"}
                  </span>
                </div>
              </div>
            </div>

            {/* Ilovaga kirish (Web App URL) Boshqaruvi */}
            <div style={{
              marginTop: '0.5rem',
              padding: '1.2rem',
              borderRadius: '10px',
              backgroundColor: 'var(--bg-hover)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.85rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div>
                  <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                    <Globe size={16} color="#3b82f6" />
                    📱 "Ilovaga kirish" Tugmasi va Havolasi
                  </h4>
                  <p style={{ margin: '0.2rem 0 0 0', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Botning Asosiy Menyusida tashqi web ilovaga (yoki veb-saytga) o'tuvchi tugmani yoqing yoki o'chiring.
                  </p>
                </div>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontWeight: 600, fontSize: '0.85rem', color: cmsData.app_url_enabled ? '#10b981' : 'var(--text-muted)' }}>
                  <input
                    type="checkbox"
                    checked={cmsData.app_url_enabled}
                    onChange={(e) => setCmsData({ ...cmsData, app_url_enabled: e.target.checked })}
                    style={{ width: '18px', height: '18px', cursor: 'pointer' }}
                  />
                  {cmsData.app_url_enabled ? "Tugma Faol (Yoqilgan)" : "O'chirilgan (Ko'rinmaydi)"}
                </label>
              </div>

              {cmsData.app_url_enabled && (
                <div className="form-group" style={{ marginTop: '0.3rem', marginBottom: 0 }}>
                  <label style={{ fontSize: '0.82rem' }}>Ilova / Sayt Havolasi (URL)</label>
                  <input
                    type="url"
                    value={cmsData.app_url}
                    onChange={(e) => setCmsData({ ...cmsData, app_url: e.target.value })}
                    placeholder="https://app.fullxizmat.uz yoki https://t.me/..."
                    className="form-input"
                  />
                </div>
              )}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
              <button
                type="submit"
                disabled={actionLoading === 'save_cms'}
                className="btn"
              >
                <Save size={16} />
                {actionLoading === 'save_cms' ? 'Saqlanmoqda...' : 'Matnlarni Saqlash'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* TAB 3: DIRECT MESSAGE TEST */}
      {activeTab === 'test' && (
        <div className="card" style={{ marginBottom: 0, maxWidth: '640px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Send size={18} color="#10b981" />
            To'g'ridan-to'g'ri Xabar Sinash (Test Message)
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.3rem' }}>
            Qaysi bot orqali xabar yuborishni tanlang va foydalanuvchiga Telegram ID orqali sinov xabari yuboring:
          </p>

          <form onSubmit={handleSendMessage} style={{ marginTop: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            
            <div className="form-group">
              <label>Qaysi Bot Orqali Yuborilsin?</label>
              <select
                className="form-input"
                value={msgBotType}
                onChange={(e) => setMsgBotType(e.target.value)}
              >
                <option value="WORKER">👷 1. Usta Boti ({botStatus.project_name || 'IshBazari'})</option>
                <option value="CLIENT">👔 2. Ish Joylash Boti (Client Bot)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Foydalanuvchi Telegram ID</label>
              <input
                type="number"
                value={msgChatId}
                onChange={(e) => setMsgChatId(e.target.value)}
                placeholder="Masalan: 123456789"
                className="form-input"
                style={{ fontFamily: 'monospace' }}
              />
            </div>

            <div className="form-group">
              <label>Xabar Matni</label>
              <textarea
                rows={4}
                value={msgText}
                onChange={(e) => setMsgText(e.target.value)}
                placeholder="Salom, bu Full-Xizmat botidan sinov xabari..."
                className="form-textarea"
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
              <button
                type="submit"
                disabled={sendingMsg}
                className="btn"
                style={{ backgroundColor: '#10b981', borderColor: '#10b981' }}
              >
                <Send size={16} />
                {sendingMsg ? 'Yuborilmoqda...' : 'Xabarni Yuborish'}
              </button>
            </div>
          </form>
        </div>
      )}

    </div>
  );
}
