import React, { useState, useEffect } from 'react';
import { 
  fetchLeads, 
  sendLeadReminder, 
  deleteLead 
} from '../services/api';
import { 
  Target, 
  Users, 
  Search, 
  RefreshCw, 
  Send, 
  Trash2, 
  Eye, 
  CheckCircle2, 
  AlertCircle, 
  MessageSquare, 
  Phone, 
  Clock, 
  Calendar, 
  Briefcase, 
  HardHat, 
  Sparkles, 
  X, 
  Hash, 
  CheckSquare, 
  Square,
  Globe,
  ChevronLeft,
  ChevronRight,
  Shield,
  SendHorizontal
} from 'lucide-react';

const TEMPLATES = {
  welcome: {
    title: "🌟 Xush kelibsiz & Loyihani tushuntirish",
    texts: {
      uz: "Assalomu alaykum, <b>{name}</b>! 🌟\n\nSiz <b>24/7 Xizmat</b> tizimimizga tashrif buyurgan edingiz.\n\nPlatformamiz orqali kun-u tun istalgan sohada usta va mutaxassislarni topishingiz yoki o'zingiz usta sifatida xizmat ko'rsatib, doimiy daromad qilishingiz mumkin!\n\nImkoniyatlardan to'liq foydalanish uchun ro'yxatdan o'tishni yakunlang:\n👉 <b>/start</b> tugmasini bosing!",
      oz: "Ассалому алайкум, <b>{name}</b>! 🌟\n\nСиз <b>24/7 Хизмат</b> тизимимизга ташриф буюрган эдингиз.\n\nПлатформамиз орқали кун-у тун исталган соҳада уста ва мутахассисларни топишингиз ёки ўзингиз уста сифатида хизмат кўрсатиб, доимий даромад қилишингиз мумкин!\n\nИмкониятлардан тўлиқ фойдаланиш учун рўйхатдан ўтишни якунланг:\n👉 <b>/start</b> тугмасини босинг!",
      ru: "Здравствуйте, <b>{name}</b>! 🌟\n\nВы заходили в наш сервис <b>24/7 Xizmat</b>.\n\nЧерез нашу платформу вы можете круглосуточно находить надежных мастеров или сами предлагать свои услуги и зарабатывать!\n\nЧтобы завершить регистрацию и получить полный доступ:\n👉 Нажмите <b>/start</b>!",
      en: "Hello, <b>{name}</b>! 🌟\n\nYou recently visited our <b>24/7 Service</b> platform.\n\nThrough our platform, you can find professionals for any task 24/7 or offer your own services to earn income!\n\nTo complete your registration:\n👉 Press <b>/start</b>!"
    }
  },
  quick_reg: {
    title: "⚡ Tezkor 1 daqiqalik ro'yxatdan o'tish",
    texts: {
      uz: "Hurmatli <b>{name}</b>! ⚡\n\nSiz botimizda ro'yxatdan o'tishni to'liq yakunlamagansiz. Ro'yxatdan o'tish atigi 1 daqiqa vaqt oladi va mutlaqo bepul!\n\nDavom etish uchun quyidagi buyruqni bosing:\n👉 <b>/start</b>",
      oz: "Ҳурматли <b>{name}</b>! ⚡\n\nСиз ботимизда рўйхатдан ўтишни тўлиқ якунламагансиз. Рўйхатдан ўтиш атиги 1 дақиқа вақт олади ва мутлақо бепул!\n\nДавом этиш учун қуйидаги буйруқни босинг:\n👉 <b>/start</b>",
      ru: "Уважаемый(ая) <b>{name}</b>! ⚡\n\nВы еще не завершили регистрацию в боте. Это займет всего 1 минуту и совершенно бесплатно!\n\nЧтобы продолжить, нажмите:\n👉 <b>/start</b>",
      en: "Dear <b>{name}</b>! ⚡\n\nYou haven't completed your registration in our bot yet. It only takes 1 minute and is completely free!\n\nTo continue, press:\n👉 <b>/start</b>"
    }
  },
  worker_call: {
    title: "🛠 Usta va Mutaxassislar uchun taklif",
    texts: {
      uz: "Hurmatli usta / mutaxassis! 🛠\n\n<b>24/7 Xizmat</b> tizimida har kuni yuzlab mijozlar turli yo'nalishlarda usta qidirmoqda. Doimiy mijozlar va yangi buyurtmalarga ega bo'lish uchun profilingizni to'ldiring:\n👉 <b>/start</b>",
      oz: "Ҳурматли уста / мутахассис! 🛠\n\n<b>24/7 Хизмат</b> тизимида ҳар куни юзлаб мижозлар турли йўналишларда уста қидирмоқда. Доимий мижозлар ва янги буюртмаларга эга бўлиш учун профилингизни тўлдиринг:\n👉 <b>/start</b>",
      ru: "Уважаемый мастер / специалист! 🛠\n\nВ сервисе <b>24/7 Xizmat</b> ежедневно клиенты ищут мастеров. Заполните свой профиль, чтобы получать прямые заказы:\n👉 <b>/start</b>",
      en: "Dear specialist / worker! 🛠\n\nClients are looking for professionals daily on <b>24/7 Service</b>. Complete your profile to start receiving direct orders:\n👉 <b>/start</b>"
    }
  },
  custom: {
    title: "✍️ Maxsus xabar yozish",
    texts: {
      uz: "Assalomu alaykum, <b>{name}</b>!\n\n24/7 Xizmat platformamizdan to'liq foydalanish uchun /start tugmasini bosing:\n👉 <b>/start</b>",
      oz: "Ассалому алайкум, <b>{name}</b>!\n\n24/7 Хизмат платформамиздан тўлиқ фойдаланиш учун /start тугмасини босинг:\n👉 <b>/start</b>",
      ru: "Здравствуйте, <b>{name}</b>!\n\nДля доступа к сервису 24/7 Xizmat нажмите /start:\n👉 <b>/start</b>",
      en: "Hello, <b>{name}</b>!\n\nTo access our 24/7 Service platform, please press /start:\n👉 <b>/start</b>"
    }
  }
};

export default function LeadsManager({ currentUser }) {
  const isSuper = Boolean(currentUser?.is_superuser);
  const [leads, setLeads] = useState([]);
  const [stats, setStats] = useState({
    total_leads: 0,
    client_leads: 0,
    worker_leads: 0,
    with_phone: 0,
    without_phone: 0,
    filtered_count: 0
  });
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [botFilter, setBotFilter] = useState('ALL'); // 'ALL' | 'CLIENT' | 'WORKER' | 'BOTH'
  const [langFilter, setLangFilter] = useState('ALL'); // 'ALL' | 'uz' | 'oz' | 'ru' | 'en'
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 12;

  // Selected leads for bulk action
  const [selectedLeadIds, setSelectedLeadIds] = useState([]);

  // Modals state
  const [viewingLead, setViewingLead] = useState(null);
  const [reminderModalOpen, setReminderModalOpen] = useState(false);
  const [reminderTarget, setReminderTarget] = useState('SELECTED'); // 'SINGLE' | 'SELECTED' | 'ALL_FILTERED'
  const [singleLeadTarget, setSingleLeadTarget] = useState(null);
  
  // Reminder form state
  const [selectedTemplate, setSelectedTemplate] = useState('welcome');
  const [customText, setCustomText] = useState('');
  const [previewLang, setPreviewLang] = useState('uz');
  const [sending, setSending] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const loadLeadsData = async () => {
    setLoading(true);
    try {
      const params = {};
      if (botFilter !== 'ALL') params.bot_filter = botFilter;
      if (langFilter !== 'ALL') params.language = langFilter;
      if (searchTerm.trim()) params.search = searchTerm.trim();

      const res = await fetchLeads(params);
      setLeads(res.data.results || []);
      if (res.data.stats) {
        setStats(res.data.stats);
      }
    } catch (err) {
      console.error("Lidlarni yuklashda xatolik:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
    loadLeadsData();
  }, [botFilter, langFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadLeadsData();
  };

  // Checkbox handlers
  const handleSelectAllOnPage = () => {
    const pageLeads = leads.slice((currentPage - 1) * pageSize, currentPage * pageSize);
    const pageIds = pageLeads.map(l => l.id);
    const allSelected = pageIds.every(id => selectedLeadIds.includes(id));

    if (allSelected) {
      setSelectedLeadIds(prev => prev.filter(id => !pageIds.includes(id)));
    } else {
      setSelectedLeadIds(prev => Array.from(new Set([...prev, ...pageIds])));
    }
  };

  const handleToggleLead = (id) => {
    setSelectedLeadIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  // Open Reminder Modal for Single Lead
  const openSingleReminderModal = (lead) => {
    setSingleLeadTarget(lead);
    setReminderTarget('SINGLE');
    setSelectedTemplate('welcome');
    setCustomText('');
    setPreviewLang(lead.language || 'uz');
    setFeedback(null);
    setReminderModalOpen(true);
  };

  // Open Reminder Modal for Bulk Selected Leads
  const openBulkReminderModal = () => {
    if (selectedLeadIds.length === 0) {
      alert("Iltimos, kamida bitta lidni belgilang!");
      return;
    }
    setSingleLeadTarget(null);
    setReminderTarget('SELECTED');
    setSelectedTemplate('welcome');
    setCustomText('');
    setPreviewLang('uz');
    setFeedback(null);
    setReminderModalOpen(true);
  };

  // Send Reminder Handler
  const handleSendReminder = async (e) => {
    e.preventDefault();
    setSending(true);
    setFeedback(null);

    try {
      let payload = {
        template_type: selectedTemplate,
        custom_text: selectedTemplate === 'custom' ? customText : undefined
      };

      if (reminderTarget === 'SINGLE' && singleLeadTarget) {
        payload.user_id = singleLeadTarget.id;
      } else {
        payload.user_ids = selectedLeadIds;
      }

      const res = await sendLeadReminder(payload);
      setFeedback({
        type: 'success',
        message: res.data.message || "Xabarnomalar muvaffaqiyatli yuborildi!"
      });

      setTimeout(() => {
        setReminderModalOpen(false);
        setSelectedLeadIds([]);
      }, 1500);
    } catch (err) {
      const msg = err.response?.data?.error || "Xabar yuborishda xatolik yuz berdi!";
      setFeedback({ type: 'error', message: msg });
    } finally {
      setSending(false);
    }
  };

  // Delete Lead Handler
  const handleDeleteLead = async (lead) => {
    if (!window.confirm(`Haqiqatan ham #${lead.id} (@${lead.username || lead.telegram_id}) lidini o'chirmoqchimisiz?`)) {
      return;
    }

    try {
      await deleteLead(lead.id);
      setLeads(prev => prev.filter(l => l.id !== lead.id));
      setSelectedLeadIds(prev => prev.filter(id => id !== lead.id));
    } catch (err) {
      alert("O'chirishda xatolik: " + (err.response?.data?.error || err.message));
    }
  };

  // Preview Message computation
  const getPreviewMessage = () => {
    const sampleName = singleLeadTarget ? (singleLeadTarget.full_name || "Foydalanuvchi") : "Foydalanuvchi";
    if (selectedTemplate === 'custom') {
      return (customText || TEMPLATES.custom.texts[previewLang] || '').replace('{name}', sampleName);
    }
    const tmplObj = TEMPLATES[selectedTemplate] || TEMPLATES.welcome;
    const text = tmplObj.texts[previewLang] || tmplObj.texts.uz;
    return text.replace('{name}', sampleName);
  };

  const pageLeads = leads.slice((currentPage - 1) * pageSize, currentPage * pageSize);
  const totalPages = Math.ceil(leads.length / pageSize) || 1;

  return (
    <div className="space-y-6" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Top Banner */}
      <div className="card" style={{ 
        background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(245, 158, 11, 0.08))',
        borderColor: 'rgba(239, 68, 68, 0.25)',
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
            background: 'linear-gradient(135deg, #ef4444, #f59e0b)', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 4px 14px rgba(239, 68, 68, 0.3)'
          }}>
            <Target size={26} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.01em' }}>
              Lidlar & Potensial Mijozlar Boshqaruvi
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem', marginTop: '0.2rem' }}>
              Botga <strong>/start</strong> bosgan, ammo ro'yxatdan o'tishni to'liq yakunlamagan foydalanuvchilar tahlili va ularni qayta jalb qilish
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-secondary" onClick={loadLeadsData} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'spin' : ''} />
            <span>Yangilash</span>
          </button>
          
          <button 
            className="btn" 
            onClick={openBulkReminderModal}
            disabled={selectedLeadIds.length === 0}
            style={{ 
              display: 'inline-flex', 
              alignItems: 'center', 
              gap: '0.4rem', 
              fontWeight: 700,
              backgroundColor: selectedLeadIds.length > 0 ? '#ef4444' : undefined,
              borderColor: selectedLeadIds.length > 0 ? '#ef4444' : undefined
            }}
          >
            <Send size={15} />
            <span>Tanlanganlarga Xabar Yuborish ({selectedLeadIds.length})</span>
          </button>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem'
      }}>
        <div className="card" style={{ padding: '1.2rem', marginBottom: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.76rem', textTransform: 'uppercase', fontWeight: 600 }}>
              🎯 Jami Chala Lidlar
            </div>
            <Target size={18} color="#ef4444" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ef4444', marginTop: '0.35rem' }}>
            {stats.total_leads}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Botga kirib to'xtaganlar
          </div>
        </div>

        <div className="card" style={{ padding: '1.2rem', marginBottom: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.76rem', textTransform: 'uppercase', fontWeight: 600 }}>
              👔 Mijoz Boti Lidlar
            </div>
            <Briefcase size={18} color="#3b82f6" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#3b82f6', marginTop: '0.35rem' }}>
            {stats.client_leads}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Ish beruvchi botida qolganlar
          </div>
        </div>

        <div className="card" style={{ padding: '1.2rem', marginBottom: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.76rem', textTransform: 'uppercase', fontWeight: 600 }}>
              👷 Usta Boti Lidlar
            </div>
            <HardHat size={18} color="#10b981" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#10b981', marginTop: '0.35rem' }}>
            {stats.worker_leads}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Usta botida qolganlar
          </div>
        </div>

        <div className="card" style={{ padding: '1.2rem', marginBottom: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.76rem', textTransform: 'uppercase', fontWeight: 600 }}>
              📱 Telefon Raqamli
            </div>
            <Phone size={18} color="#8b5cf6" />
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#8b5cf6', marginTop: '0.35rem' }}>
            {stats.with_phone}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Kontaktini kiritganlar
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ padding: '1.25rem', marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          
          {/* Bot Type Filters */}
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {[
              { id: 'ALL', label: 'Barchasi', icon: Target },
              { id: 'CLIENT', label: '👔 Mijoz Boti', icon: Briefcase },
              { id: 'WORKER', label: '👷 Usta Boti', icon: HardHat },
              { id: 'BOTH', label: '✨ Ikkala Bot', icon: Sparkles },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setBotFilter(tab.id)}
                style={{
                  padding: '0.45rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid',
                  borderColor: botFilter === tab.id ? 'var(--primary)' : 'var(--border-color)',
                  background: botFilter === tab.id ? 'var(--primary)' : 'var(--bg-inner)',
                  color: botFilter === tab.id ? '#fff' : 'var(--text-muted)',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.15s'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Search form */}
          <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', flex: 1, maxWidth: '380px' }}>
            <input
              type="text"
              className="form-control"
              placeholder="Ism, @username, TG ID, telefon..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ fontSize: '0.85rem', padding: '0.5rem 0.85rem' }}
            />
            <button type="submit" className="btn btn-secondary" style={{ padding: '0.5rem 0.85rem' }}>
              <Search size={14} />
            </button>
          </form>

        </div>
      </div>

      {/* Main Leads Table */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div style={{ overflowX: 'auto' }}>
          <table className="table" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)', textAlign: 'left' }}>
                <th style={{ padding: '0.85rem 1rem', width: '40px' }}>
                  <input
                    type="checkbox"
                    checked={pageLeads.length > 0 && pageLeads.every(l => selectedLeadIds.includes(l.id))}
                    onChange={handleSelectAllOnPage}
                    style={{ cursor: 'pointer' }}
                  />
                </th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>FOYDALANUVCHI</th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>BOT TURI</th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>TELEFON</th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>YETISHMAYOTGAN BOSQICHLAR</th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>BOSHLAGAN VAQTI</th>
                <th style={{ padding: '0.85rem 1rem', fontSize: '0.82rem', color: 'var(--text-muted)', textAlign: 'right' }}>AMALLAR</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    <RefreshCw size={22} className="spin" style={{ margin: '0 auto 0.5rem auto' }} />
                    <div>Lidlar yuklanmoqda...</div>
                  </td>
                </tr>
              ) : leads.length === 0 ? (
                <tr>
                  <td colSpan="7" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    <Target size={32} color="var(--text-muted)" style={{ margin: '0 auto 0.5rem auto', opacity: 0.5 }} />
                    <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-main)' }}>Chala qolgan lidlar topilmadi</div>
                    <div style={{ fontSize: '0.8rem', marginTop: '0.2rem' }}>Barcha foydalanuvchilar to'liq ro'yxatdan o'tgan yoki filter parametrlariga mos foydalanuvchi yo'q.</div>
                  </td>
                </tr>
              ) : (
                pageLeads.map((lead) => {
                  const isChecked = selectedLeadIds.includes(lead.id);
                  const initials = (lead.first_name ? lead.first_name[0] : (lead.username ? lead.username[0] : 'U')).toUpperCase();

                  let botBadge = null;
                  if (lead.started_client_bot && lead.started_worker_bot) {
                    botBadge = (
                      <span className="badge" style={{ background: 'rgba(139, 92, 246, 0.18)', color: '#c084fc', border: '1px solid rgba(139, 92, 246, 0.35)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <Sparkles size={11} /> Ikkala Bot
                      </span>
                    );
                  } else if (lead.started_client_bot || lead.role === 'CLIENT') {
                    botBadge = (
                      <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', border: '1px solid rgba(59, 130, 246, 0.3)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <Briefcase size={11} /> Mijoz Boti
                      </span>
                    );
                  } else {
                    botBadge = (
                      <span className="badge badge-online" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <HardHat size={11} /> Usta Boti
                      </span>
                    );
                  }

                  return (
                    <tr key={lead.id} style={{ borderBottom: '1px solid var(--border-color)', backgroundColor: isChecked ? 'rgba(59, 130, 246, 0.05)' : 'transparent' }}>
                      <td style={{ padding: '0.85rem 1rem' }}>
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => handleToggleLead(lead.id)}
                          style={{ cursor: 'pointer' }}
                        />
                      </td>
                      <td style={{ padding: '0.85rem 1rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                          <div style={{
                            width: '36px',
                            height: '36px',
                            borderRadius: '50%',
                            background: 'linear-gradient(135deg, #ef4444, #f59e0b)',
                            color: '#fff',
                            fontWeight: 700,
                            fontSize: '0.85rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 2px 6px rgba(0,0,0,0.15)'
                          }}>
                            {initials}
                          </div>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-main)', fontSize: '0.88rem' }}>
                              {lead.full_name}
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                              <span>@{lead.username || 'username_yoq'}</span>
                              <span>•</span>
                              <span style={{ fontFamily: 'monospace' }}>TG: #{lead.telegram_id}</span>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td style={{ padding: '0.85rem 1rem' }}>
                        {botBadge}
                      </td>
                      <td style={{ padding: '0.85rem 1rem' }}>
                        {lead.phone_number ? (
                          <span style={{ fontWeight: 600, fontFamily: 'monospace', fontSize: '0.84rem', color: 'var(--text-main)' }}>
                            {lead.phone_number}
                          </span>
                        ) : (
                          <span style={{ color: '#ef4444', fontSize: '0.78rem', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                            <AlertCircle size={12} /> Kiritilmagan
                          </span>
                        )}
                      </td>
                      <td style={{ padding: '0.85rem 1rem' }}>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                          {lead.missing_fields && lead.missing_fields.length > 0 ? (
                            lead.missing_fields.map((field, fIdx) => (
                              <span 
                                key={fIdx}
                                style={{
                                  padding: '0.15rem 0.45rem',
                                  borderRadius: '4px',
                                  fontSize: '0.72rem',
                                  fontWeight: 600,
                                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                  color: '#ef4444',
                                  border: '1px solid rgba(239, 68, 68, 0.25)'
                                }}
                              >
                                {field}
                              </span>
                            ))
                          ) : (
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Yakuniy bosqich</span>
                          )}
                        </div>
                      </td>
                      <td style={{ padding: '0.85rem 1rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                          <Clock size={12} />
                          {lead.date_joined ? new Date(lead.date_joined).toLocaleString() : '—'}
                        </div>
                      </td>
                      <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '0.4rem' }}>
                          <button
                            className="btn"
                            onClick={() => openSingleReminderModal(lead)}
                            title="Xabarnoma yuborish (/start taklifi)"
                            style={{
                              padding: '0.4rem 0.65rem',
                              fontSize: '0.78rem',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.3rem',
                              backgroundColor: '#ef4444',
                              borderColor: '#ef4444'
                            }}
                          >
                            <Send size={13} /> Xabar
                          </button>
                          <button
                            className="btn btn-secondary"
                            onClick={() => setViewingLead(lead)}
                            title="Batafsil ko'rish"
                            style={{ padding: '0.4rem 0.65rem', fontSize: '0.78rem' }}
                          >
                            <Eye size={13} color="#06b6d4" />
                          </button>
                          {isSuper && (
                            <button
                              className="btn btn-secondary"
                              onClick={() => handleDeleteLead(lead)}
                              title="O'chirish"
                              style={{ padding: '0.4rem 0.65rem', fontSize: '0.78rem', color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }}
                            >
                              <Trash2 size={13} />
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

        {/* Pagination Footer */}
        {leads.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Jami: <strong>{leads.length}</strong> ta liddan <strong>{(currentPage - 1) * pageSize + 1}</strong> - <strong>{Math.min(currentPage * pageSize, leads.length)}</strong> ko'rsatilmoqda
            </div>
            <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              >
                <ChevronLeft size={14} /> Oldingi
              </button>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, padding: '0 0.5rem' }}>
                {currentPage} / {totalPages}
              </span>
              <button
                className="btn btn-secondary"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* --- MODAL 1: SEND REMINDER MODAL --- */}
      {reminderModalOpen && (
        <div className="modal-backdrop" onClick={() => setReminderModalOpen(false)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '640px', maxHeight: '90vh', overflowY: 'auto' }}>
            
            {/* Modal Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <SendHorizontal size={20} color="#ef4444" />
                <h3 className="card-title" style={{ margin: 0 }}>
                  {reminderTarget === 'SINGLE' && singleLeadTarget 
                    ? `Lidga Xabar Yuborish: ${singleLeadTarget.full_name}`
                    : `Tanlangan ${selectedLeadIds.length} ta Lidga Xabar Yuborish`
                  }
                </h3>
              </div>
              <button onClick={() => setReminderModalOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            {feedback && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                backgroundColor: feedback.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
                color: feedback.type === 'success' ? '#10b981' : '#ef4444',
                border: `1px solid ${feedback.type === 'success' ? '#10b981' : '#ef4444'}`
              }}>
                {feedback.message}
              </div>
            )}

            <form onSubmit={handleSendReminder} style={{ display: 'flex', flexDirection: 'column', gap: '1.15rem' }}>
              
              {/* Target Info */}
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(239, 68, 68, 0.08)',
                border: '1px solid rgba(239, 68, 68, 0.2)',
                fontSize: '0.82rem',
                color: 'var(--text-main)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <Target size={16} color="#ef4444" style={{ flexShrink: 0 }} />
                <span>
                  Qabul qiluvchilar: <strong>{reminderTarget === 'SINGLE' ? '1 ta foydalanuvchi' : `${selectedLeadIds.length} ta belgilangan lidlar`}</strong> (Telegram bot orqali to'g'ridan-to'g'ri yetkaziladi).
                </span>
              </div>

              {/* Template Selector */}
              <div className="form-group">
                <label style={{ fontSize: '0.86rem', fontWeight: 700, marginBottom: '0.4rem', display: 'block' }}>
                  Xabarnoma Shablonini Tanlang:
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '0.5rem' }}>
                  {Object.entries(TEMPLATES).map(([key, tmpl]) => {
                    const isSelected = selectedTemplate === key;
                    return (
                      <div
                        key={key}
                        onClick={() => setSelectedTemplate(key)}
                        style={{
                          padding: '0.65rem 0.85rem',
                          borderRadius: '8px',
                          cursor: 'pointer',
                          backgroundColor: isSelected ? 'rgba(239, 68, 68, 0.12)' : 'var(--bg-inner)',
                          border: `1px solid ${isSelected ? '#ef4444' : 'var(--border-color)'}`,
                          transition: 'all 0.15s ease'
                        }}
                      >
                        <div style={{ fontWeight: 700, fontSize: '0.84rem', color: isSelected ? '#ef4444' : 'var(--text-main)' }}>
                          {tmpl.title}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Custom Text Area if Custom is selected */}
              {selectedTemplate === 'custom' && (
                <div className="form-group">
                  <label style={{ fontSize: '0.86rem', fontWeight: 600, marginBottom: '0.4rem', display: 'block' }}>
                    Maxsus Xabar Matni (HTML formatida):
                  </label>
                  <textarea
                    className="form-control"
                    rows={4}
                    required
                    value={customText}
                    onChange={(e) => setCustomText(e.target.value)}
                    placeholder="Xabar matnini kiriting. Ism qo'yish uchun {name} dan foydalaning..."
                    style={{ fontSize: '0.85rem', lineHeight: '1.4' }}
                  />
                  <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'block' }}>
                    Eslatma: Xabarda foydalanuvchi ismini chiqarish uchun <code>{'{name}'}</code> belgisidan foydalaning.
                  </span>
                </div>
              )}

              {/* Live Preview Box */}
              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '0.85rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label style={{ fontSize: '0.84rem', fontWeight: 700, color: 'var(--text-main)' }}>
                    Telegram Xabar Ko'rinishi (Preview):
                  </label>
                  <div style={{ display: 'flex', gap: '0.3rem' }}>
                    {['uz', 'oz', 'ru', 'en'].map(l => (
                      <button
                        key={l}
                        type="button"
                        onClick={() => setPreviewLang(l)}
                        style={{
                          padding: '0.2rem 0.5rem',
                          borderRadius: '4px',
                          border: '1px solid',
                          borderColor: previewLang === l ? '#ef4444' : 'var(--border-color)',
                          backgroundColor: previewLang === l ? '#ef4444' : 'var(--bg-inner)',
                          color: previewLang === l ? '#fff' : 'var(--text-muted)',
                          fontSize: '0.72rem',
                          fontWeight: 700,
                          cursor: 'pointer'
                        }}
                      >
                        {l.toUpperCase()}
                      </button>
                    ))}
                  </div>
                </div>

                <div style={{
                  padding: '1rem',
                  borderRadius: '10px',
                  backgroundColor: '#17212b',
                  color: '#fff',
                  fontSize: '0.86rem',
                  lineHeight: '1.5',
                  border: '1px solid rgba(255,255,255,0.1)',
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'system-ui, -apple-system, sans-serif'
                }}>
                  <div dangerouslySetInnerHTML={{ __html: getPreviewMessage() }} />
                </div>
              </div>

              {/* Modal Actions */}
              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setReminderModalOpen(false)}
                  disabled={sending}
                >
                  Bekor Qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={sending}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.4rem',
                    fontWeight: 700,
                    backgroundColor: '#ef4444',
                    borderColor: '#ef4444'
                  }}
                >
                  <Send size={15} />
                  {sending ? 'Yuborilmoqda...' : 'Xabarni Yuborish'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

      {/* --- MODAL 2: VIEW LEAD DETAILS MODAL --- */}
      {viewingLead && (
        <div className="modal-backdrop" onClick={() => setViewingLead(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '520px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Target size={20} color="#ef4444" />
                <h3 className="card-title" style={{ margin: 0 }}>Lid Ma'lumotlari</h3>
              </div>
              <button onClick={() => setViewingLead(null)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            {/* Avatar & Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', backgroundColor: 'var(--bg-inner)', borderRadius: '10px', marginBottom: '1.25rem' }}>
              <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #ef4444, #f59e0b)',
                color: '#fff',
                fontWeight: 800,
                fontSize: '1.2rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {(viewingLead.first_name ? viewingLead.first_name[0] : (viewingLead.username ? viewingLead.username[0] : 'U')).toUpperCase()}
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--text-main)' }}>
                  {viewingLead.full_name}
                </h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  ID: #{viewingLead.id} • @{viewingLead.username || 'username_yoq'}
                </div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.85rem' }}>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Telegram ID:</span>
                <div style={{ fontWeight: 600, fontFamily: 'monospace', marginTop: '0.2rem' }}>
                  #{viewingLead.telegram_id}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Telefon:</span>
                <div style={{ fontWeight: 600, fontFamily: 'monospace', marginTop: '0.2rem', color: viewingLead.phone_number ? 'var(--text-main)' : '#ef4444' }}>
                  {viewingLead.phone_number || 'Kiritilmagan'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Bot Turi:</span>
                <div style={{ fontWeight: 600, color: 'var(--primary)', marginTop: '0.2rem' }}>
                  {viewingLead.bot_type_display}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Tanlangan Til:</span>
                <div style={{ fontWeight: 600, textTransform: 'uppercase', marginTop: '0.2rem' }}>
                  {viewingLead.language || 'UZ'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0, gridColumn: 'span 2' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Yetishmayotgan Ma'lumotlar:</span>
                <div style={{ fontWeight: 600, color: '#ef4444', marginTop: '0.3rem', display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                  {viewingLead.missing_fields && viewingLead.missing_fields.length > 0 ? (
                    viewingLead.missing_fields.map((f, idx) => (
                      <span key={idx} className="badge badge-danger">
                        {f}
                      </span>
                    ))
                  ) : (
                    <span className="badge badge-warning">Yakuniy tasdiq</span>
                  )}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0, gridColumn: 'span 2' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Botga kirgan sana:</span>
                <div style={{ fontWeight: 500, fontSize: '0.82rem', marginTop: '0.2rem' }}>
                  {viewingLead.date_joined ? new Date(viewingLead.date_joined).toLocaleString() : '—'}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
              <button className="btn btn-secondary" onClick={() => setViewingLead(null)}>
                Yopish
              </button>
              <button
                className="btn"
                onClick={() => {
                  const lead = viewingLead;
                  setViewingLead(null);
                  openSingleReminderModal(lead);
                }}
                style={{ backgroundColor: '#ef4444', borderColor: '#ef4444' }}
              >
                <Send size={14} /> Xabar Yuborish
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
