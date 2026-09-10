import React, { useState } from 'react';
import { updateOrderStatus } from '../services/api';
import { ClipboardList, Plus, Search, UserCheck, XCircle, MapPin, CheckCircle2, Clock, Zap, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';

export default function PaymentOrderStatus({ orders, onOpenDispatchModal, onOrderUpdated, onOpenCreateOrderModal, loading = false }) {
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm(`Buyurtma #${orderId} ni bekor qilishga ishonchingiz komilmi?`)) return;
    try {
      await updateOrderStatus(orderId, 'CANCELLED');
      if (onOrderUpdated) onOrderUpdated();
    } catch (err) {
      alert('Buyurtmani bekor qilishda xatolik yuz berdi!');
    }
  };

  const filteredOrders = orders.filter(o => {
    const matchesFilter = filter === 'ALL' || o.status === filter;
    const matchesSearch = 
      o.customer_name.toLowerCase().includes(search.toLowerCase()) ||
      o.customer_phone.includes(search) ||
      o.id.toString().includes(search);
    return matchesFilter && matchesSearch;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case 'PENDING': 
        return <span className="badge badge-pending">Kutilmoqda</span>;
      case 'DISPATCHED': 
        return <span className="badge badge-dispatched">Biriktirildi</span>;
      case 'STARTED': 
        return <span className="badge badge-busy">Bajarilmoqda</span>;
      case 'FINISHED': 
        return <span className="badge badge-finished">Yakunlandi</span>;
      case 'CANCELLED': 
        return <span className="badge badge-offline">Bekor qilindi</span>;
      default: 
        return <span className="badge badge-offline">{status}</span>;
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <ClipboardList size={20} color="#3b82f6" />
            Buyurtmalar & Operatsion Dispatch Markazi
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
            Platformadagi barcha xizmat buyurtmalari, ularning ijrochilari va to'lov nazorati
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
          {onOpenCreateOrderModal && (
            <button 
              className="btn" 
              onClick={onOpenCreateOrderModal}
              style={{ backgroundColor: '#10b981', fontWeight: 700 }}
            >
              <Plus size={16} />
              Yangi Buyurtma Kiritish
            </button>
          )}

          <div style={{ position: 'relative' }}>
            <input
              type="text"
              className="form-control"
              style={{ width: '200px', fontSize: '0.85rem', paddingLeft: '2rem' }}
              placeholder="Qidirish (Ism, Tel, ID)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <Search size={14} style={{ position: 'absolute', left: '0.65rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          </div>

          <div style={{ display: 'flex', gap: '0.25rem', background: 'var(--bg-inner)', padding: '0.2rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            {[
              { id: 'ALL', label: 'Barchasi' },
              { id: 'PENDING', label: 'Kutilmoqda' },
              { id: 'DISPATCHED', label: 'Biriktirildi' },
              { id: 'STARTED', label: 'Jarayonda' },
              { id: 'FINISHED', label: 'Yakunlandi' },
              { id: 'CANCELLED', label: 'Bekor' }
            ].map(f => (
              <button
                key={f.id}
                onClick={() => setFilter(f.id)}
                className={`btn ${filter === f.id ? '' : 'btn-secondary'}`}
                style={{ 
                  fontSize: '0.75rem', 
                  padding: '0.35rem 0.65rem',
                  borderRadius: '6px',
                  border: 'none',
                  background: filter === f.id ? 'var(--primary)' : 'transparent',
                  color: filter === f.id ? '#fff' : 'var(--text-muted)'
                }}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Format</th>
              <th>Mijoz F.I.Sh</th>
              <th>Telefon Raqami</th>
              <th>Xizmat Turi</th>
              <th>Manzil</th>
              <th>Narx (SUM)</th>
              <th>To'lov</th>
              <th>Holat</th>
              <th>Biriktirilgan Usta</th>
              <th>Amallar</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array.from({ length: 6 }).map((_, idx) => (
                <tr key={idx}>
                  <td><div className="skeleton" style={{ width: '30px', height: '14px' }} /></td>
                  <td><div className="skeleton" style={{ width: '65px', height: '20px', borderRadius: '10px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '110px', height: '14px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '90px', height: '14px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '80px', height: '14px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '120px', height: '14px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '85px', height: '14px' }} /></td>
                  <td><div className="skeleton" style={{ width: '60px', height: '20px', borderRadius: '10px' }} /></td>
                  <td><div className="skeleton" style={{ width: '75px', height: '20px', borderRadius: '10px' }} /></td>
                  <td><div className="skeleton skeleton-text" style={{ width: '90px', height: '14px' }} /></td>
                  <td><div className="skeleton" style={{ width: '70px', height: '26px', borderRadius: '6px' }} /></td>
                </tr>
              ))
            ) : filteredOrders.length === 0 ? (
              <tr>
                <td colSpan="11" style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
                  Buyurtmalar topilmadi.
                </td>
              </tr>
            ) : (
              filteredOrders.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((o) => (
                <tr key={o.id}>
                  <td style={{ color: 'var(--text-muted)', fontWeight: 700, fontSize: '0.82rem', fontFamily: 'monospace' }}>#{o.id}</td>
                  <td>
                    <span className="badge" style={{
                      backgroundColor: o.work_format === 'ONLINE' ? 'rgba(139, 92, 246, 0.15)' : 'rgba(59, 130, 246, 0.15)',
                      color: o.work_format === 'ONLINE' ? '#8b5cf6' : '#3b82f6',
                      fontSize: '0.72rem',
                      fontWeight: 600
                    }}>
                      {o.work_format === 'ONLINE' ? '💻 Online' : '📍 Offline'}
                    </span>
                  </td>
                  <td><strong style={{ color: 'var(--text-main)' }}>{o.customer_name}</strong></td>
                  <td>
                    <span style={{ fontFamily: 'monospace', fontSize: '0.84rem' }}>{o.customer_phone}</span>
                  </td>
                  <td>
                    <span style={{ color: '#38bdf8', fontWeight: 500 }}>{o.service_type}</span>
                  </td>
                  <td style={{ maxWidth: '180px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: 'var(--text-secondary)' }}>
                    {o.address}
                  </td>
                  <td>
                    <strong style={{ color: '#10b981' }}>{Number(o.price).toLocaleString()} SUM</strong>
                  </td>
                  <td>
                    <span className={`badge ${o.is_paid ? 'badge-finished' : 'badge-pending'}`}>
                      {o.is_paid ? 'To\'landi' : 'Kutilmoqda'}
                    </span>
                  </td>
                  <td>{getStatusBadge(o.status)}</td>
                  <td>
                    {o.assigned_worker_detail ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                        <UserCheck size={14} color="#10b981" />
                        <span style={{ fontWeight: 600 }}>{o.assigned_worker_detail.first_name} {o.assigned_worker_detail.last_name}</span>
                      </div>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Biriktirilmagan</span>
                    )}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      {o.status === 'PENDING' && (
                        <button
                          className="btn"
                          style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
                          onClick={() => onOpenDispatchModal(o)}
                        >
                          <ArrowRight size={13} />
                          Dispatch
                        </button>
                      )}
                      {o.status !== 'FINISHED' && o.status !== 'CANCELLED' && (
                        <button
                          className="btn btn-secondary"
                          style={{ 
                            fontSize: '0.75rem', 
                            padding: '0.35rem 0.65rem', 
                            backgroundColor: 'rgba(239, 68, 68, 0.15)', 
                            color: '#ef4444', 
                            borderColor: 'rgba(239, 68, 68, 0.3)' 
                          }}
                          onClick={() => handleCancelOrder(o.id)}
                        >
                          Bekor qilish
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>

        {/* Pagination Controls */}
        {filteredOrders.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, filteredOrders.length)}</b> / Jami: <b>{filteredOrders.length}</b> ta
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
              
              {Array.from({ length: Math.ceil(filteredOrders.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(filteredOrders.length / pageSize) || Math.abs(p - currentPage) <= 1)
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
                disabled={currentPage === Math.ceil(filteredOrders.length / pageSize)}
                onClick={() => setCurrentPage(prev => Math.min(Math.ceil(filteredOrders.length / pageSize), prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
