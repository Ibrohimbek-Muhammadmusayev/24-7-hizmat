import React, { useState } from 'react';
import { registerWorker } from '../services/api';
import { UserPlus, X, AlertCircle } from 'lucide-react';

export default function AddWorkerModal({ onClose, onWorkerAdded }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    phone_number: '+99890',
    specialty: 'Santexnik',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await registerWorker(formData);
      onWorkerAdded();
      onClose();
    } catch (err) {
      setError("Mutaxassisni ro'yxatdan o'tkazishda xatolik! Username yoki telefon avval ro'yxatdan o'tgan bo'lishi mumkin.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <UserPlus size={20} color="#3b82f6" />
            <h3 className="card-title" style={{ margin: 0 }}>Yangi Usta (Mutaxassis) Qo'shish</h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={18} />
          </button>
        </div>
        
        {error && (
          <div style={{ 
            padding: '0.75rem', 
            borderRadius: '8px', 
            backgroundColor: 'rgba(239, 68, 68, 0.12)', 
            color: '#ef4444', 
            fontSize: '0.84rem', 
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem'
          }}>
            <AlertCircle size={15} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
            <div className="form-group">
              <label>Ismi *</label>
              <input
                type="text"
                required
                className="form-control"
                value={formData.first_name}
                onChange={(e) => setFormData({...formData, first_name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Familiyasi *</label>
              <input
                type="text"
                required
                className="form-control"
                value={formData.last_name}
                onChange={(e) => setFormData({...formData, last_name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Tizim Login (Username) *</label>
              <input
                type="text"
                required
                className="form-control"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                placeholder="masalan: usta_sardor"
              />
            </div>
            <div className="form-group">
              <label>Parol *</label>
              <input
                type="password"
                required
                className="form-control"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Telefon Raqami *</label>
              <input
                type="text"
                required
                className="form-control"
                value={formData.phone_number}
                onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Mutaxassislik Yo'nalishi *</label>
              <select
                className="form-select"
                value={formData.specialty}
                onChange={(e) => setFormData({...formData, specialty: e.target.value})}
              >
                <option value="Santexnik">Santexnika xizmati</option>
                <option value="Elektrik">Elektr montaj xizmati</option>
                <option value="Usta">Maishiy ta'mirlash</option>
                <option value="Tozalash">Tozalash (Cleaning)</option>
                <option value="Mebel">Mebel yig'ish va ta'mirlash</option>
                <option value="Avto">Avto usta / Diagnostika</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Bekor qilish
            </button>
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Saqlanmoqda...' : 'Ustani Saqlash'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
