import React, { useState } from 'react';
import { dispatchOrder } from '../services/api';
import { UserCheck, X, CheckCircle2 } from 'lucide-react';

export default function ManualDispatchModal({ order, workers, onClose, onDispatched }) {
  const [selectedWorkerId, setSelectedWorkerId] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDispatch = async () => {
    if (!selectedWorkerId) return;
    setLoading(true);
    try {
      await dispatchOrder(order.id, selectedWorkerId);
      onDispatched();
      onClose();
    } catch (err) {
      alert('Buyurtmani biriktirishda xatolik yuz berdi!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <UserCheck size={20} color="#3b82f6" />
            <h3 className="card-title" style={{ margin: 0 }}>Buyurtma #{order.id} ni Ustaga Biriktirish</h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={18} />
          </button>
        </div>

        <p style={{ color: 'var(--text-muted)', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
          Mijoz: <strong style={{ color: 'var(--text-main)' }}>{order.customer_name}</strong> | Xizmat: <span style={{ color: '#38bdf8' }}>{order.service_type}</span>
        </p>

        <div className="form-group" style={{ marginBottom: '1.5rem' }}>
          <label>Mas'ul Mutaxassisni Tanlang:</label>
          <select
            className="form-select"
            value={selectedWorkerId}
            onChange={(e) => setSelectedWorkerId(e.target.value)}
          >
            <option value="">-- Mutaxassis ustani tanlang --</option>
            {workers.map((w) => (
              <option key={w.id} value={w.id}>
                {w.first_name} {w.last_name} ({w.specialty || 'Umumiy'}) — [{w.is_online ? 'Online' : 'Offline'}] {w.is_busy ? '(Band)' : '(Bo\'sh)'}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Bekor qilish
          </button>
          <button type="button" className="btn" onClick={handleDispatch} disabled={!selectedWorkerId || loading}>
            {loading ? 'Biriktirilmoqda...' : 'Ustaga Biriktirish'}
          </button>
        </div>
      </div>
    </div>
  );
}
