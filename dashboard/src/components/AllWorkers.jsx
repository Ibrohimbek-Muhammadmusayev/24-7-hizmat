import React, { useState } from 'react';
import { 
  HardHat, 
  UserPlus, 
  Star, 
  Phone, 
  CheckCircle2, 
  Clock, 
  ShieldCheck, 
  MapPin, 
  Eye, 
  Search,
  Filter,
  Briefcase,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import WorkerDetailModal from './WorkerDetailModal';

export default function AllWorkers({ workers, onOpenAddWorkerModal, onRefresh, loading = false }) {
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL'); // 'ALL' | 'ONLINE' | 'BUSY' | 'REGISTERED'
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const filteredWorkers = workers.filter(w => {
    const term = searchTerm.toLowerCase();
    const nameMatch = (w.first_name || '').toLowerCase().includes(term) ||
                      (w.last_name || '').toLowerCase().includes(term) ||
                      (w.username || '').toLowerCase().includes(term) ||
                      (w.phone_number || '').includes(term) ||
                      (w.specialty || '').toLowerCase().includes(term) ||
                      (w.district || '').toLowerCase().includes(term);

    if (!nameMatch) return false;

    if (statusFilter === 'ONLINE') return w.is_online;
    if (statusFilter === 'BUSY') return w.is_busy;
    if (statusFilter === 'REGISTERED') return w.is_registered;

    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Header & Filter Card */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <HardHat size={20} color="#3b82f6" />
              Usta va Mutaxassislar Boshqaruvi ({workers.length} nafar)
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Platformada ro'yxatdan o'tgan ustalar, ularning mutaxassisliklari, portfolio, reyting va kontaktlari
            </p>
          </div>
          <button className="btn" onClick={onOpenAddWorkerModal}>
            <UserPlus size={16} />
            Yangi Usta Qo'shish
          </button>
        </div>

        {/* Filter and Search Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {[
              { id: 'ALL', label: `Barchasi (${workers.length})` },
              { id: 'ONLINE', label: `🟢 Online (${workers.filter(w => w.is_online).length})` },
              { id: 'BUSY', label: `🔴 Band (${workers.filter(w => w.is_busy).length})` },
              { id: 'REGISTERED', label: `✓ Tasdiqlangan (${workers.filter(w => w.is_registered).length})` },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setStatusFilter(tab.id)}
                style={{
                  padding: '0.45rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid',
                  borderColor: statusFilter === tab.id ? 'var(--primary)' : 'var(--border-color)',
                  background: statusFilter === tab.id ? 'var(--primary)' : 'var(--bg-inner)',
                  color: statusFilter === tab.id ? '#fff' : 'var(--text-muted)',
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

          <div style={{ display: 'flex', gap: '0.5rem', flex: 1, maxWidth: '340px' }}>
            <input
              type="text"
              className="form-control"
              placeholder="Ism, telefon, tuman yoki kasb..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ fontSize: '0.85rem' }}
            />
          </div>
        </div>
      </div>

      {/* Workers Table */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Mutaxassis</th>
                <th>Hudud / Manzil</th>
                <th>Soha & Lavozimlar</th>
                <th>Reyting & Tajriba</th>
                <th>Ish Rejimi</th>
                <th>Bandlik</th>
                <th>Faollik</th>
                <th>Amallar</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 7 }).map((_, idx) => (
                  <tr key={idx}>
                    <td><div className="skeleton" style={{ width: '25px', height: '14px' }} /></td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                        <div className="skeleton skeleton-avatar" />
                        <div style={{ flex: 1 }}>
                          <div className="skeleton skeleton-title" style={{ width: '120px', height: '14px' }} />
                          <div className="skeleton skeleton-text" style={{ width: '70px', height: '10px' }} />
                        </div>
                      </div>
                    </td>
                    <td><div className="skeleton skeleton-text" style={{ width: '90px', height: '14px' }} /></td>
                    <td><div className="skeleton skeleton-text" style={{ width: '100px', height: '14px' }} /></td>
                    <td><div className="skeleton skeleton-text" style={{ width: '80px', height: '14px' }} /></td>
                    <td><div className="skeleton skeleton-text" style={{ width: '85px', height: '14px' }} /></td>
                    <td><div className="skeleton" style={{ width: '65px', height: '20px', borderRadius: '10px' }} /></td>
                    <td><div className="skeleton" style={{ width: '60px', height: '20px', borderRadius: '10px' }} /></td>
                    <td style={{ textAlign: 'center' }}><div className="skeleton" style={{ width: '32px', height: '26px', borderRadius: '6px' }} /></td>
                  </tr>
                ))
              ) : filteredWorkers.length === 0 ? (
                <tr>
                  <td colSpan="9" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    Mos keluvchi ustalar topilmadi.
                  </td>
                </tr>
              ) : (
                filteredWorkers.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((w) => {
                  const initials = (w.first_name ? w.first_name[0] : (w.username ? w.username[0] : 'W')).toUpperCase();
                  const positionsCount = w.selected_positions_details?.length || (w.selected_positions ? w.selected_positions.length : 0);

                  return (
                    <tr key={w.id} style={{ cursor: 'pointer' }} onClick={() => setSelectedWorker(w)}>
                      <td style={{ color: 'var(--text-muted)', fontWeight: 600, fontSize: '0.8rem' }}>#{w.id}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                          <div style={{
                            width: '34px',
                            height: '34px',
                            borderRadius: '50%',
                            background: 'linear-gradient(135deg, #10b981, #06b6d4)',
                            color: '#fff',
                            fontWeight: 700,
                            fontSize: '0.85rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}>
                            {initials}
                          </div>
                          <div>
                            <strong style={{ color: 'var(--text-main)', fontSize: '0.9rem' }}>
                              {w.first_name || w.username} {w.last_name || ''}
                            </strong>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                              {w.phone_number || 'Tel kiritilmagan'}
                            </div>
                          </div>
                        </div>
                      </td>

                      <td>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-main)', fontWeight: 600 }}>
                          {w.region_name || (w.region && w.region.name) || 'Toshkent'}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {w.district || 'Tuman ko\'rsatilmagan'} {w.street_address ? `• ${w.street_address}` : ''}
                        </div>
                      </td>

                      <td>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-main)', fontWeight: 600 }}>
                          {w.category_details ? w.category_details.name_uz : (w.specialty || 'Mutaxassis')}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {positionsCount > 0 ? (
                            <span style={{ color: '#38bdf8' }}>{positionsCount} ta lavozim tanlangan</span>
                          ) : (
                            <span>{w.position_details ? w.position_details.name_uz : 'Umumiy'}</span>
                          )}
                        </div>
                      </td>

                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#fbbf24', fontWeight: 700, fontSize: '0.88rem' }}>
                          <Star size={13} fill="#fbbf24" />
                          <span>{w.rating || 5.0}</span>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 400 }}>
                            ({w.completed_jobs_count || 0} ish)
                          </span>
                        </div>
                      </td>

                      <td>
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                          {w.work_schedule === '24_7' ? '🔥 24/7' : (w.work_schedule === 'day_shift' ? '☀️ Kunduzgi' : '⏱️ Erkin')}
                        </span>
                      </td>

                      <td>
                        <span className={`badge ${w.is_busy ? 'badge-busy' : 'badge-finished'}`}>
                          {w.is_busy ? '🔴 Band' : "🟢 Bo'sh"}
                        </span>
                      </td>

                      <td>
                        <span className={`badge ${w.is_online ? 'badge-online' : 'badge-offline'}`}>
                          {w.is_online ? 'Online' : 'Offline'}
                        </span>
                      </td>

                      <td>
                        <button
                          className="btn btn-secondary"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedWorker(w);
                          }}
                          style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                        >
                          <Eye size={13} color="#3b82f6" />
                          <span>Profil</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        {filteredWorkers.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, filteredWorkers.length)}</b> / Jami: <b>{filteredWorkers.length}</b> nafar
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
              
              {Array.from({ length: Math.ceil(filteredWorkers.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(filteredWorkers.length / pageSize) || Math.abs(p - currentPage) <= 1)
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
                disabled={currentPage === Math.ceil(filteredWorkers.length / pageSize)}
                onClick={() => setCurrentPage(prev => Math.min(Math.ceil(filteredWorkers.length / pageSize), prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Full Worker Detail Modal */}
      {selectedWorker && (
        <WorkerDetailModal
          worker={selectedWorker}
          onClose={() => setSelectedWorker(null)}
          onUpdated={() => {
            if (onRefresh) onRefresh();
            setSelectedWorker(null);
          }}
        />
      )}

    </div>
  );
}

