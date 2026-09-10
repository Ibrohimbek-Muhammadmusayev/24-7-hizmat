import React, { useState, useEffect } from 'react';
import { fetchFeedbacks, updateFeedback, sendBotMessage } from '../services/api';
import { 
  MessageSquare, 
  CheckCircle2, 
  Clock, 
  Send, 
  RefreshCw, 
  User, 
  Phone, 
  Calendar,
  Search,
  Filter,
  AlertCircle,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

export default function FeedbackManager() {
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterReviewed, setFilterReviewed] = useState('ALL'); // 'ALL' | 'UNREVIEWED' | 'REVIEWED'
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;
  const [replyingItem, setReplyingItem] = useState(null);
  const [replyText, setReplyText] = useState('');
  const [sendingReply, setSendingReply] = useState(false);

  const loadFeedbacks = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filterReviewed === 'UNREVIEWED') params.is_reviewed = 'false';
      if (filterReviewed === 'REVIEWED') params.is_reviewed = 'true';
      const res = await fetchFeedbacks(params);
      setFeedbacks(res.data || []);
    } catch (err) {
      console.error('Error fetching feedbacks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeedbacks();
  }, [filterReviewed]);

  const handleToggleReviewed = async (item) => {
    try {
      await updateFeedback(item.id, { is_reviewed: !item.is_reviewed });
      setFeedbacks(prev => prev.map(f => f.id === item.id ? { ...f, is_reviewed: !f.is_reviewed } : f));
    } catch (err) {
      alert("Holatni yangilashda xatolik yuz berdi");
    }
  };

  const handleSendReply = async (e) => {
    e.preventDefault();
    if (!replyingItem || !replyText.trim()) return;

    if (!replyingItem.user_telegram_id) {
      alert("Ushbu foydalanuvchining Telegram ID si mavjud emas");
      return;
    }

    setSendingReply(true);
    try {
      const escapeHtml = (text) => {
        return (text || '')
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
      };

      const userOrigText = escapeHtml(replyingItem.message);
      const adminReplyText = escapeHtml(replyText.trim());

      const formattedMessage = 
        `📩 <b>ADMINISTRATOR JAVOBI</b>\n\n` +
        `💬 <b>Sizning murojaatingiz:</b>\n` +
        `<i>«${userOrigText}»</i>\n\n` +
        `✍️ <b>Javob:</b>\n` +
        `${adminReplyText}\n\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `💡 <i>Agar savollaringiz bo'lsa, botimiz orqali yana murojaat qilishingiz mumkin.</i>`;

      const botType = (replyingItem.user_role === 'CLIENT' || replyingItem.user_role === 'client') ? 'CLIENT' : 'WORKER';

      await sendBotMessage(replyingItem.user_telegram_id, formattedMessage, botType);
      await updateFeedback(replyingItem.id, { is_reviewed: true });
      setFeedbacks(prev => prev.map(f => f.id === replyingItem.id ? { ...f, is_reviewed: true } : f));
      setReplyingItem(null);
      setReplyText('');
      alert("Javob foydalanuvchiga Telegram orqali muvaffaqiyatli yuborildi!");
    } catch (err) {
      alert("Javob yuborishda xatolik yuz berdi. Bot sozlamalarini tekshiring.");
    } finally {
      setSendingReply(false);
    }
  };

  const unreviewedCount = feedbacks.filter(f => !f.is_reviewed).length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Header Card */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <MessageSquare size={20} color="#3b82f6" />
              Taklif va Shikoyatlar Markazi ({feedbacks.length} ta)
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Foydalanuvchilar va ustalarning Telegram bot orqali yuborgan murojaatlari, taklif va shikoyatlari
            </p>
          </div>

          <button className="btn btn-secondary" onClick={loadFeedbacks} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'spin' : ''} />
            Yangilash
          </button>
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
          {[
            { id: 'ALL', label: `Barchasi (${feedbacks.length})` },
            { id: 'UNREVIEWED', label: `⚠️ Ko'rib chiqilmagan (${unreviewedCount})` },
            { id: 'REVIEWED', label: `✓ Ko'rib chiqilgan` },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setFilterReviewed(tab.id)}
              style={{
                padding: '0.45rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid',
                borderColor: filterReviewed === tab.id ? 'var(--primary)' : 'var(--border-color)',
                background: filterReviewed === tab.id ? 'var(--primary)' : 'var(--bg-inner)',
                color: filterReviewed === tab.id ? '#fff' : 'var(--text-muted)',
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
      </div>

      {/* Feedbacks List */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Foydalanuvchi</th>
                <th>Murojaat Matni</th>
                <th>Sana</th>
                <th>Holat</th>
                <th>Amallar</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 6 }).map((_, idx) => (
                  <tr key={idx}>
                    <td><div className="skeleton" style={{ width: '25px', height: '14px' }} /></td>
                    <td>
                      <div className="skeleton skeleton-title" style={{ width: '110px', height: '14px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '70px', height: '10px' }} />
                    </td>
                    <td>
                      <div className="skeleton skeleton-text" style={{ width: '90%', height: '14px', marginBottom: '4px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '60%', height: '12px' }} />
                    </td>
                    <td><div className="skeleton skeleton-text" style={{ width: '80px', height: '14px' }} /></td>
                    <td><div className="skeleton" style={{ width: '75px', height: '22px', borderRadius: '12px' }} /></td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '4px' }}>
                        <div className="skeleton" style={{ width: '32px', height: '26px', borderRadius: '6px' }} />
                        <div className="skeleton" style={{ width: '32px', height: '26px', borderRadius: '6px' }} />
                      </div>
                    </td>
                  </tr>
                ))
              ) : feedbacks.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    Hech qanday taklif yoki shikoyat topilmadi.
                  </td>
                </tr>
              ) : (
                feedbacks.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((item) => (
                  <tr key={item.id}>
                    <td style={{ color: 'var(--text-muted)', fontWeight: 600, fontSize: '0.8rem' }}>#{item.id}</td>
                    <td>
                      <div>
                        <div style={{ fontWeight: 600, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                          <User size={13} color="#3b82f6" />
                          {item.user_name || 'Noma\'lum'}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace', marginTop: '0.15rem' }}>
                          {item.user_phone || 'Tel kiritilmagan'} {item.user_telegram_id ? `(TG: ${item.user_telegram_id})` : ''}
                        </div>
                      </div>
                    </td>
                    <td style={{ maxWidth: '380px' }}>
                      <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: 1.45, whiteSpace: 'pre-wrap' }}>
                        {item.message}
                      </p>
                    </td>
                    <td>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {new Date(item.created_at).toLocaleString()}
                      </span>
                    </td>
                    <td>
                      <button
                        onClick={() => handleToggleReviewed(item)}
                        className={`badge ${item.is_reviewed ? 'badge-finished' : 'badge-busy'}`}
                        style={{ cursor: 'pointer', border: 'none', padding: '0.35rem 0.65rem' }}
                        title="Statusni o'zgartirish uchun bosing"
                      >
                        {item.is_reviewed ? '✓ Ko\'rib chiqilgan' : '⚠️ Yangi murojaat'}
                      </button>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        {item.user_telegram_id && (
                          <button
                            className="btn btn-secondary"
                            onClick={() => {
                              setReplyingItem(item);
                              setReplyText('');
                            }}
                            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                          >
                            <Send size={12} color="#10b981" />
                            <span>Javob berish</span>
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        {feedbacks.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, feedbacks.length)}</b> / Jami: <b>{feedbacks.length}</b> ta
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              >
                <ChevronLeft size={14} /> Oldingi
              </button>
              
              {Array.from({ length: Math.ceil(feedbacks.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(feedbacks.length / pageSize) || Math.abs(p - currentPage) <= 1)
                .map((p, idx, arr) => (
                  <React.Fragment key={p}>
                    {idx > 0 && arr[idx - 1] !== p - 1 && <span style={{ color: 'var(--text-muted)', padding: '0 4px' }}>...</span>}
                    <button
                      className={`btn ${currentPage === p ? '' : 'btn-secondary'}`}
                      style={{
                        padding: '0.35rem 0.65rem',
                        fontSize: '0.78rem',
                        background: currentPage === p ? 'var(--primary)' : 'transparent',
                        borderColor: currentPage === p ? 'var(--primary)' : 'var(--border-color)',
                        color: currentPage === p ? '#fff' : 'var(--text-main)',
                        minWidth: '32px'
                      }}
                      onClick={() => setCurrentPage(p)}
                    >
                      {p}
                    </button>
                  </React.Fragment>
                ))}

              <button
                className="btn btn-secondary"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}
                disabled={currentPage === Math.ceil(feedbacks.length / pageSize)}
                onClick={() => setCurrentPage(prev => Math.min(Math.ceil(feedbacks.length / pageSize), prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Reply Modal */}
      {replyingItem && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 9999,
          padding: '1rem'
        }}>
          <div className="card" style={{ maxWidth: '500px', width: '100%' }}>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', color: 'var(--text-main)' }}>
              Foydalanuvchiga Telegram orqali javob yozish
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '1rem' }}>
              Qabul qiluvchi: <b>{replyingItem.user_name}</b> (TG ID: {replyingItem.user_telegram_id})
            </p>

            <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-inner)', borderRadius: '6px', border: '1px solid var(--border-color)', marginBottom: '1rem', fontSize: '0.82rem' }}>
              <div style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Murojaat:</div>
              "{replyingItem.message}"
            </div>

            <form onSubmit={handleSendReply}>
              <div className="form-group" style={{ marginBottom: '1rem' }}>
                <label style={{ fontWeight: 600, fontSize: '0.85rem' }}>Javob matni:</label>
                <textarea
                  className="form-control"
                  rows="4"
                  required
                  placeholder="Murojaatingiz uchun rahmat! Taklifingiz ko'rib chiqildi..."
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  style={{ fontSize: '0.85rem', marginTop: '0.4rem' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setReplyingItem(null)}
                  disabled={sendingReply}
                >
                  Bekor qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={sendingReply}
                  style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
                >
                  <Send size={14} />
                  {sendingReply ? 'Yuborilmoqda...' : 'Telegramga Yuborish'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
