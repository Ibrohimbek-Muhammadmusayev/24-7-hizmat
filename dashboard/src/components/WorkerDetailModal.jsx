import React, { useState, useEffect } from 'react';
import { 
  X, 
  HardHat, 
  MapPin, 
  Phone, 
  Calendar, 
  Briefcase, 
  Star, 
  CheckCircle2, 
  Clock, 
  Image as ImageIcon, 
  MessageSquare,
  Shield,
  UserCheck,
  UserX,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { updateWorker } from '../services/api';

export default function WorkerDetailModal({ worker: initialWorker, onClose, onUpdated }) {
  const [worker, setWorker] = useState(initialWorker);
  const [activeSubTab, setActiveSubTab] = useState('info');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    setWorker(initialWorker);
  }, [initialWorker]);

  if (!worker) return null;

  const handleToggleOnline = async () => {
    try {
      setUpdating(true);
      const newStatus = !worker.is_online;
      const res = await updateWorker(worker.id, { is_online: newStatus });
      setWorker(prev => ({ ...prev, is_online: newStatus, ...(res.data || {}) }));
      if (onUpdated) onUpdated();
    } catch (err) {
      console.error(err);
      alert("Statusni o'zgartirishda xatolik yuz berdi");
    } finally {
      setUpdating(false);
    }
  };

  const handleToggleBusy = async () => {
    try {
      setUpdating(true);
      const newStatus = !worker.is_busy;
      const res = await updateWorker(worker.id, { is_busy: newStatus });
      setWorker(prev => ({ ...prev, is_busy: newStatus, ...(res.data || {}) }));
      if (onUpdated) onUpdated();
    } catch (err) {
      console.error(err);
      alert("Bandlik holatini o'zgartirishda xatolik yuz berdi");
    } finally {
      setUpdating(false);
    }
  };

  const initials = (worker.first_name ? worker.first_name[0] : (worker.username ? worker.username[0] : 'W')).toUpperCase();

  const getWorkScheduleText = (val) => {
    if (val === '24_7') return '🔥 24/7 (Istalgan vaqt / Shoshilinch)';
    if (val === 'day_shift') return '☀️ 09:00 - 18:00 (Kunduzgi)';
    return '⏱️ Erkin grafik';
  };

  const getEmploymentTypeText = (val) => {
    if (val === 'daily') return '⚡ Bir martalik / Kunbay';
    if (val === 'permanent') return '💼 Doimiy ish';
    return '🌟 Ikkalasi ham (Kunbay & Doimiy)';
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(5px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 9999,
      padding: '1rem'
    }}>
      <div className="card" style={{ maxWidth: '850px', width: '100%', maxHeight: '90vh', display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
        
        {/* Modal Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: 'var(--bg-inner)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #10b981, #06b6d4)',
              color: '#fff',
              fontWeight: 800,
              fontSize: '1.1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {initials}
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h3 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--text-main)', fontWeight: 800 }}>
                  {worker.first_name || worker.username} {worker.last_name || ''}
                </h3>
                <span className={`badge ${worker.is_registered ? 'badge-finished' : 'badge-offline'}`}>
                  {worker.is_registered ? '✓ Tasdiqlangan' : 'Tugallanmagan'}
                </span>
              </div>
              <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
                ID: #{worker.id} • Tel: <b>{worker.phone_number || 'Kiritilmagan'}</b> • Til: <b>{(worker.language || 'uz').toUpperCase()}</b>
              </p>
            </div>
          </div>

          <button 
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '0.4rem' }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Sub-tab navigation */}
        <div style={{ display: 'flex', borderBottom: '1px solid var(--border-color)', padding: '0.5rem 1.5rem', gap: '0.75rem', backgroundColor: 'var(--bg-card)' }}>
          <button
            onClick={() => setActiveSubTab('info')}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: 'none',
              background: activeSubTab === 'info' ? 'var(--primary)' : 'transparent',
              color: activeSubTab === 'info' ? '#fff' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: '0.85rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
          >
            <HardHat size={15} />
            Asosiy Ma'lumotlar
          </button>

          <button
            onClick={() => setActiveSubTab('portfolio')}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: 'none',
              background: activeSubTab === 'portfolio' ? 'var(--primary)' : 'transparent',
              color: activeSubTab === 'portfolio' ? '#fff' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: '0.85rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
          >
            <ImageIcon size={15} />
            Ish Namunalar (Portfolio) ({worker.portfolio_items?.length || 0})
          </button>

          <button
            onClick={() => setActiveSubTab('reviews')}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: 'none',
              background: activeSubTab === 'reviews' ? 'var(--primary)' : 'transparent',
              color: activeSubTab === 'reviews' ? '#fff' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: '0.85rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
          >
            <MessageSquare size={15} />
            Mijoz Sharhlari ({worker.received_reviews?.length || 0})
          </button>
        </div>

        {/* Modal Body Content */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', flex: 1 }}>
          
          {/* TAB 1: ASOSIY MA'LUMOTLAR */}
          {activeSubTab === 'info' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              
              {/* Quick Status Control Bar */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '0.85rem 1.25rem',
                backgroundColor: 'var(--bg-inner)',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                flexWrap: 'wrap',
                gap: '0.75rem'
              }}>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Tarmoqda:</span>
                    <span className={`badge ${worker.is_online ? 'badge-online' : 'badge-offline'}`}>
                      {worker.is_online ? 'Online' : 'Offline'}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Bandlik:</span>
                    <span className={`badge ${worker.is_busy ? 'badge-busy' : 'badge-online'}`}>
                      {worker.is_busy ? 'Band (Ishda)' : "Bo'sh"}
                    </span>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button 
                    className="btn btn-secondary" 
                    onClick={handleToggleOnline} 
                    disabled={updating}
                    style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                  >
                    {worker.is_online ? <UserX size={14} color="#ef4444" /> : <UserCheck size={14} color="#10b981" />}
                    {worker.is_online ? 'Offline Qilish' : 'Online Qilish'}
                  </button>
                  <button 
                    className="btn btn-secondary" 
                    onClick={handleToggleBusy} 
                    disabled={updating}
                    style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }}
                  >
                    {worker.is_busy ? "Bo'shatish" : 'Band Qilish'}
                  </button>
                </div>
              </div>

              {/* Grid of Attributes */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Jinsi va Yoshi</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', marginTop: '0.25rem' }}>
                    {worker.gender === 'female' ? '👩 Ayol' : '👨 Erkak'}, {worker.age ? `${worker.age} yosh` : "Ko'rsatilmagan"}
                  </div>
                </div>

                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Reyting & Bajarilgan Ishlar</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fbbf24', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <Star size={16} fill="#fbbf24" />
                    <span>{worker.rating || 5.0}</span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 500 }}>
                      ({worker.completed_jobs_count || 0} ta ish)
                    </span>
                  </div>
                </div>

                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Ish Rejimi</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)', marginTop: '0.25rem' }}>
                    {getWorkScheduleText(worker.work_schedule)}
                  </div>
                </div>

                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Bandlik Turi</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)', marginTop: '0.25rem' }}>
                    {getEmploymentTypeText(worker.employment_type)}
                  </div>
                </div>
              </div>

              {/* Manzil va Joylashuv */}
              <div style={{ padding: '1rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#38bdf8', fontWeight: 700, fontSize: '0.88rem', marginBottom: '0.5rem' }}>
                  <MapPin size={16} />
                  Hudud va Manzil Ma'lumotlari
                </div>
                <p style={{ margin: 0, fontSize: '0.88rem', color: 'var(--text-main)' }}>
                  <b>Viloyat / Shahar:</b> {worker.region_name || 'Kiritilmagan'} <br />
                  <b>Tuman / Hudud:</b> {worker.district || 'Kiritilmagan'} <br />
                  <b>Aniq Manzil / Mo'ljal:</b> {worker.street_address || worker.address_title || 'Mavjud emas'}
                </p>
                {worker.latitude && worker.longitude && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    GPS: <code>{worker.latitude.toFixed(5)}, {worker.longitude.toFixed(5)}</code>
                  </div>
                )}
              </div>

              {/* Mutaxassisliklar va Tanlangan Lavozimlar */}
              <div style={{ padding: '1rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#10b981', fontWeight: 700, fontSize: '0.88rem', marginBottom: '0.65rem' }}>
                  <Briefcase size={16} />
                  Tanlangan Soha va Lavozimlar ({worker.selected_positions_details?.length || 0} ta)
                </div>

                {worker.category_details && (
                  <div style={{ marginBottom: '0.6rem', fontSize: '0.85rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Asosiy Soha: </span>
                    <span className="badge badge-dispatched">{worker.category_details.icon} {worker.category_details.name_uz}</span>
                  </div>
                )}

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.45rem' }}>
                  {worker.selected_positions_details && worker.selected_positions_details.length > 0 ? (
                    worker.selected_positions_details.map((pos) => (
                      <span key={pos.id} style={{
                        padding: '0.35rem 0.7rem',
                        backgroundColor: 'var(--bg-card)',
                        border: '1px solid var(--border-color)',
                        borderRadius: '6px',
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        color: 'var(--text-main)'
                      }}>
                        🔨 {pos.name_uz}
                      </span>
                    ))
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                      {worker.specialty || 'Mutaxassislik kiritilmagan'}
                    </span>
                  )}
                </div>
              </div>

            </div>
          )}

          {/* TAB 2: PORTFOLIO / ISH NAMUNALARI */}
          {activeSubTab === 'portfolio' && (
            <div>
              {(!worker.portfolio_items || worker.portfolio_items.length === 0) ? (
                <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
                  <ImageIcon size={40} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
                  <p style={{ margin: 0 }}>Ushbu usta hozircha portfolio rasmlarini yuklamagan.</p>
                </div>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
                  {worker.portfolio_items.map((item) => (
                    <div 
                      key={item.id} 
                      style={{
                        borderRadius: '8px',
                        overflow: 'hidden',
                        backgroundColor: 'var(--bg-inner)',
                        border: '1px solid var(--border-color)',
                        display: 'flex',
                        flexDirection: 'column'
                      }}
                    >
                      <div style={{
                        height: '140px',
                        backgroundColor: '#1e293b',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--text-muted)',
                        position: 'relative'
                      }}>
                        <ImageIcon size={32} />
                        <span style={{ position: 'absolute', bottom: '6px', right: '6px', fontSize: '0.7rem', background: 'rgba(0,0,0,0.6)', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
                          Telegram Rasm
                        </span>
                      </div>
                      <div style={{ padding: '0.75rem' }}>
                        <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
                          {item.caption || 'Izohsiz namuna'}
                        </div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          Yuklangan: {new Date(item.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: SHARHLAR VA BAHOLAR */}
          {activeSubTab === 'reviews' && (
            <div>
              {(!worker.received_reviews || worker.received_reviews.length === 0) ? (
                <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
                  <MessageSquare size={40} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
                  <p style={{ margin: 0 }}>Hozircha mijozlar tomonidan sharh qoldirilmagan.</p>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {worker.received_reviews.map((rev) => (
                    <div 
                      key={rev.id}
                      style={{
                        padding: '1rem',
                        backgroundColor: 'var(--bg-inner)',
                        borderRadius: '8px',
                        border: '1px solid var(--border-color)'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                        <strong style={{ color: 'var(--text-main)', fontSize: '0.9rem' }}>{rev.client_name || 'Anonim mijoz'}</strong>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#fbbf24', fontWeight: 700, fontSize: '0.85rem' }}>
                          <Star size={13} fill="#fbbf24" />
                          <span>{rev.rating}/5</span>
                        </div>
                      </div>
                      <p style={{ margin: 0, fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                        "{rev.comment}"
                      </p>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
                        {new Date(rev.created_at).toLocaleString()} {rev.client_phone ? `• Tel: ${rev.client_phone}` : ''}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

        </div>

        {/* Modal Footer */}
        <div style={{
          padding: '1rem 1.5rem',
          borderTop: '1px solid var(--border-color)',
          display: 'flex',
          justifyContent: 'flex-end',
          backgroundColor: 'var(--bg-inner)'
        }}>
          <button className="btn btn-secondary" onClick={onClose}>
            Yopish
          </button>
        </div>

      </div>
    </div>
  );
}
