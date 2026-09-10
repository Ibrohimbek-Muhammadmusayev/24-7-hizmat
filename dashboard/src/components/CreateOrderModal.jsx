import React, { useState, useEffect } from 'react';
import { createOrder } from '../services/api';
import { PlusCircle, X, Check, MapPin, DollarSign, Phone, User, Tag, FileText, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function CreateOrderModal({ isOpen, onClose, categories = [], onOrderCreated }) {
  const defaultCategory = categories.length > 0 ? categories[0] : null;

  const [formData, setFormData] = useState({
    title: '',
    customer_name: '',
    customer_phone: '+998 ',
    address: '',
    category: defaultCategory ? defaultCategory.id : '',
    service_type: defaultCategory ? defaultCategory.name : 'Santexnika',
    work_format: 'OFFLINE',
    description: '',
    price: 100000,
    latitude: 41.311081,
    longitude: 69.240562,
    source: 'CALL_CENTER',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (categories.length > 0 && !formData.category) {
      setFormData(prev => ({
        ...prev,
        category: categories[0].id,
        service_type: categories[0].name,
        title: `${categories[0].name} xizmati`
      }));
    }
  }, [categories]);

  if (!isOpen) return null;

  const districtPresets = [
    'Chilonzor', 'Yunusobod', 'M.Ulug\'bek', 'Yakkasaroy', 
    'Shayxontohur', 'Olmazor', 'Sergeli', 'Mirobod', 'Yashnobod'
  ];

  const pricePresets = [50000, 100000, 150000, 200000, 300000, 500000];

  const handleSelectCategory = (cat) => {
    setFormData(prev => ({
      ...prev,
      category: cat.id,
      service_type: cat.name,
      title: `${cat.name} xizmati`
    }));
  };

  const handleSelectDistrict = (district) => {
    const prefix = `Toshkent sh., ${district} tumani, `;
    setFormData(prev => ({
      ...prev,
      address: prev.address ? `${prefix}${prev.address.replace(/^Toshkent sh.,.*?tumani,\s*/, '')}` : prefix
    }));
  };

  const handleSelectPrice = (p) => {
    setFormData(prev => ({ ...prev, price: p }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.customer_name.trim()) {
      setError("Iltimos, mijoz ismini kiriting!");
      return;
    }
    if (!formData.customer_phone.trim() || formData.customer_phone.length < 9) {
      setError("Iltimos, mijoz telefon raqamini to'g'ri kiriting!");
      return;
    }
    if (!formData.address.trim()) {
      setError("Iltimos, manzilni to'liq kiriting!");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        title: formData.title || `${formData.service_type} xizmati`,
        price: parseFloat(formData.price) || 50000
      };

      const res = await createOrder(payload);
      if (onOrderCreated) {
        onOrderCreated(res.data);
      }
      onClose();
    } catch (err) {
      const msg = err.response?.data?.error || "Buyurtmani kiritishda xatolik yuz berdi!";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div 
        className="modal-card" 
        style={{ maxWidth: '650px', maxHeight: '90vh', overflowY: 'auto' }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{ padding: '0.5rem', borderRadius: '8px', background: 'rgba(59, 130, 246, 0.12)', color: '#3b82f6' }}>
              <PlusCircle size={22} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 800, margin: 0, color: 'var(--text-main)' }}>
                Tezkor Buyurtma Qabul Qilish (Call Center)
              </h2>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', margin: 0 }}>
                Mijoz ma'lumotlarini qulay va standart formatda kiritish
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '0.3rem' }}
          >
            <X size={20} />
          </button>
        </div>

        {error && (
          <div style={{
            padding: '0.75rem 1rem',
            backgroundColor: 'rgba(239, 68, 68, 0.12)',
            border: '1px solid #ef4444',
            borderRadius: '8px',
            color: '#ef4444',
            fontSize: '0.84rem',
            marginBottom: '1rem',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
          
          {/* 1. Xizmat Kategoriyasi (Tezkor Chiplar) */}
          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Tag size={14} color="#3b82f6" /> Xizmat Kategoriyasini Tanlang:
            </label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.2rem' }}>
              {categories.map((c) => {
                const isSelected = formData.category.toString() === c.id.toString();
                return (
                  <button
                    key={c.id}
                    type="button"
                    onClick={() => handleSelectCategory(c)}
                    style={{
                      padding: '0.45rem 0.8rem',
                      borderRadius: '8px',
                      border: '1px solid',
                      borderColor: isSelected ? 'var(--primary)' : 'var(--border-color)',
                      backgroundColor: isSelected ? 'rgba(59, 130, 246, 0.15)' : 'var(--bg-inner)',
                      color: isSelected ? '#3b82f6' : 'var(--text-secondary)',
                      fontSize: '0.84rem',
                      fontWeight: isSelected ? 700 : 500,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                      transition: 'all 0.15s'
                    }}
                  >
                    <span>{c.name}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 1.5 Xizmat Formati (Offline / Online) */}
          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <MapPin size={14} color="#8b5cf6" /> Xizmat Formati:
            </label>
            <div style={{ display: 'flex', gap: '0.6rem', marginTop: '0.2rem' }}>
              {[
                { id: 'OFFLINE', label: '📍 Joyiga borish (Offline)', desc: 'Usta mijoz manziliga boradi' },
                { id: 'ONLINE', label: '💻 Masofaviy (Online)', desc: 'Onlayn maslahat yoki masofaviy ish' }
              ].map((fmt) => {
                const isSelected = formData.work_format === fmt.id;
                return (
                  <button
                    key={fmt.id}
                    type="button"
                    onClick={() => setFormData({ 
                      ...formData, 
                      work_format: fmt.id,
                      address: fmt.id === 'ONLINE' ? '💻 Masofaviy / Onlayn' : (formData.address === '💻 Masofaviy / Onlayn' ? '' : formData.address)
                    })}
                    style={{
                      flex: 1,
                      padding: '0.6rem 0.85rem',
                      borderRadius: '8px',
                      border: '1px solid',
                      borderColor: isSelected ? 'var(--primary)' : 'var(--border-color)',
                      backgroundColor: isSelected ? 'rgba(59, 130, 246, 0.15)' : 'var(--bg-inner)',
                      color: isSelected ? '#3b82f6' : 'var(--text-secondary)',
                      fontSize: '0.84rem',
                      fontWeight: isSelected ? 700 : 500,
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.15s'
                    }}
                  >
                    <div>{fmt.label}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>{fmt.desc}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 2. Mijoz Ismi & Telefon Raqami (Grid) */}
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <User size={14} color="#10b981" /> Mijoz Ismi / F.I.Sh *:
              </label>
              <input
                type="text"
                required
                className="form-control"
                placeholder="Masalan: Sardor Rahimov"
                value={formData.customer_name}
                onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                autoFocus
              />
            </div>

            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <Phone size={14} color="#10b981" /> Telefon Raqam *:
              </label>
              <input
                type="text"
                required
                className="form-control"
                placeholder="+998 90 123 45 67"
                value={formData.customer_phone}
                onChange={(e) => setFormData({ ...formData, customer_phone: e.target.value })}
              />
            </div>
          </div>

          {/* 3. Ish Sarlavhasi */}
          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <FileText size={14} color="#3b82f6" /> Ish Nomi / Tavsifi:
            </label>
            <input
              type="text"
              className="form-control"
              placeholder="Masalan: Oshxona jo'mragini almashtirish"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          {/* 4. Manzil & Tuman Presets */}
          <div className="form-group">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <MapPin size={14} color="#ef4444" /> Manzil (Tuman, ko'cha, uy) *:
              </label>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Tezkor tuman tanlang:</span>
            </div>
            
            {/* Tuman chiplari */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', margin: '0.2rem 0 0.4rem 0' }}>
              {districtPresets.map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => handleSelectDistrict(d)}
                  style={{
                    padding: '0.25rem 0.55rem',
                    borderRadius: '6px',
                    border: '1px solid var(--border-color)',
                    background: 'var(--bg-inner)',
                    color: 'var(--text-muted)',
                    fontSize: '0.74rem',
                    cursor: 'pointer'
                  }}
                >
                  +{d}
                </button>
              ))}
            </div>

            <input
              type="text"
              required
              className="form-control"
              placeholder="Masalan: Toshkent sh., Chilonzor 9-mavze, 25-uy, 44-xonadon"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
            />
          </div>

          {/* 5. Narx & Narx Presets */}
          <div className="form-group">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <DollarSign size={14} color="#10b981" /> Kelishilgan / Taklif Narxi (SUM) *:
              </label>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Tezkor qiymatlar:</span>
            </div>

            {/* Narx chiplari */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', margin: '0.2rem 0 0.4rem 0' }}>
              {pricePresets.map((p) => {
                const isSelected = formData.price === p;
                return (
                  <button
                    key={p}
                    type="button"
                    onClick={() => handleSelectPrice(p)}
                    style={{
                      padding: '0.25rem 0.55rem',
                      borderRadius: '6px',
                      border: '1px solid',
                      borderColor: isSelected ? '#10b981' : 'var(--border-color)',
                      background: isSelected ? 'rgba(16, 185, 129, 0.15)' : 'var(--bg-inner)',
                      color: isSelected ? '#10b981' : 'var(--text-muted)',
                      fontSize: '0.75rem',
                      fontWeight: isSelected ? 700 : 500,
                      cursor: 'pointer'
                    }}
                  >
                    {p.toLocaleString()} SUM
                  </button>
                );
              })}
            </div>

            <input
              type="number"
              className="form-control"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: e.target.value })}
            />
          </div>

          {/* 6. Izoh (Optional) */}
          <div className="form-group">
            <label>Qo'shimcha Izoh yoki Talablar:</label>
            <textarea
              rows="2"
              className="form-control"
              placeholder="Mijozning maxsus istaklari yoki mutaxassis uchun qo'shimcha ko'rsatma..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
            <button
              type="submit"
              className="btn"
              disabled={loading}
              style={{ flex: 1, padding: '0.8rem', fontSize: '0.92rem', fontWeight: 700 }}
            >
              {loading ? 'Saqlanmoqda...' : 'Buyurtmani Qabul Qilish & Saqlash'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              style={{ padding: '0.8rem 1.25rem' }}
            >
              Bekor Qilish
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}
