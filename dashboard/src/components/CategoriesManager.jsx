import React, { useState } from 'react';
import { 
  createCategory, 
  updateCategory, 
  deleteCategory,
  createPosition,
  updatePosition,
  deletePosition
} from '../services/api';
import { 
  FolderTree, 
  Plus, 
  Trash2, 
  Power, 
  ChevronRight, 
  ChevronDown, 
  Tag, 
  Briefcase, 
  Edit3, 
  PlusCircle, 
  Check, 
  X,
  Layers
} from 'lucide-react';

export default function CategoriesManager({ categories, onRefresh, loading = false }) {
  const [expandedCategories, setExpandedCategories] = useState({});
  
  // Category Modal / Form State
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [catFormData, setCatFormData] = useState({
    name_uz: '',
    name_oz: '',
    name_ru: '',
    name_en: '',
    icon: '🛠️',
    order: 0,
    is_active: true
  });

  // Position Modal / Form State
  const [isPositionModalOpen, setIsPositionModalOpen] = useState(false);
  const [targetCategoryId, setTargetCategoryId] = useState(null);
  const [editingPosition, setEditingPosition] = useState(null);
  const [posFormData, setPosFormData] = useState({
    category: null,
    name_uz: '',
    name_oz: '',
    name_ru: '',
    name_en: '',
    order: 0,
    is_active: true
  });

  const [saving, setSaving] = useState(false);

  const toggleExpand = (catId) => {
    setExpandedCategories(prev => ({ ...prev, [catId]: !prev[catId] }));
  };

  // --- Category Handlers ---
  const handleOpenCategoryModal = (category = null) => {
    if (category) {
      setEditingCategory(category);
      setCatFormData({
        name_uz: category.name_uz || '',
        name_oz: category.name_oz || '',
        name_ru: category.name_ru || '',
        name_en: category.name_en || '',
        icon: category.icon || '🛠️',
        order: category.order || 0,
        is_active: category.is_active ?? true
      });
    } else {
      setEditingCategory(null);
      setCatFormData({
        name_uz: '',
        name_oz: '',
        name_ru: '',
        name_en: '',
        icon: '🛠️',
        order: categories.length + 1,
        is_active: true
      });
    }
    setIsCategoryModalOpen(true);
  };

  const handleSaveCategory = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, catFormData);
      } else {
        await createCategory(catFormData);
      }
      setIsCategoryModalOpen(false);
      onRefresh();
    } catch (err) {
      alert("Kategoriyani saqlashda xatolik yuz berdi!");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteCategory = async (id) => {
    if (!window.confirm("Ushbu soha va uning barcha ichki lavozimlarini o'chirishga ishonchingiz komilmi?")) return;
    try {
      await deleteCategory(id);
      onRefresh();
    } catch (err) {
      alert("O'chirishda xatolik yuz berdi!");
    }
  };

  // --- Position Handlers ---
  const handleOpenPositionModal = (categoryId, position = null) => {
    setTargetCategoryId(categoryId);
    if (position) {
      setEditingPosition(position);
      setPosFormData({
        category: categoryId,
        name_uz: position.name_uz || '',
        name_oz: position.name_oz || '',
        name_ru: position.name_ru || '',
        name_en: position.name_en || '',
        order: position.order || 0,
        is_active: position.is_active ?? true
      });
    } else {
      setEditingPosition(null);
      setPosFormData({
        category: categoryId,
        name_uz: '',
        name_oz: '',
        name_ru: '',
        name_en: '',
        order: 0,
        is_active: true
      });
    }
    setIsPositionModalOpen(true);
  };

  const handleSavePosition = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (editingPosition) {
        await updatePosition(editingPosition.id, { ...posFormData, category: targetCategoryId });
      } else {
        await createPosition({ ...posFormData, category: targetCategoryId });
      }
      setIsPositionModalOpen(false);
      onRefresh();
    } catch (err) {
      alert("Lavozimni saqlashda xatolik yuz berdi!");
    } finally {
      setSaving(false);
    }
  };

  const handleDeletePosition = async (id) => {
    if (!window.confirm("Ushbu lavozimni o'chirishga ishonchingiz komilmi?")) return;
    try {
      await deletePosition(id);
      onRefresh();
    } catch (err) {
      alert("Lavozimni o'chirishda xatolik yuz berdi!");
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Header Card */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FolderTree size={20} color="#3b82f6" />
              Sohalar & Mutaxassislik Lavozimlari Boshqaruvi
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Telegram bot va platformadagi asosiy sohalar hamda ularning ichki lavozimlarini (10 tagacha tanlash) boshqarish
            </p>
          </div>

          <button className="btn" onClick={() => handleOpenCategoryModal(null)}>
            <Plus size={16} />
            Yangi Soha Qo'shish
          </button>
        </div>
      </div>

      {/* Categories & Positions Accordion List */}
      <div className="card" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {loading ? (
          Array.from({ length: 5 }).map((_, idx) => (
            <div key={idx} style={{ border: '1px solid var(--border-color)', borderRadius: '8px', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div className="skeleton" style={{ width: '28px', height: '28px', borderRadius: '6px' }} />
                <div>
                  <div className="skeleton skeleton-title" style={{ width: '130px', height: '16px' }} />
                  <div className="skeleton skeleton-text" style={{ width: '80px', height: '11px' }} />
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <div className="skeleton" style={{ width: '60px', height: '24px', borderRadius: '12px' }} />
                <div className="skeleton" style={{ width: '28px', height: '28px', borderRadius: '6px' }} />
              </div>
            </div>
          ))
        ) : categories.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
            Hozircha xizmat sohalari kiritilmagan.
          </div>
        ) : (
          categories.map((cat) => {
            const isExpanded = !!expandedCategories[cat.id];
            const positions = cat.positions || [];

            return (
              <div 
                key={cat.id}
                style={{
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  backgroundColor: 'var(--bg-inner)',
                  transition: 'all 0.2s'
                }}
              >
                {/* Category Header Row */}
                <div style={{
                  padding: '0.85rem 1.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  backgroundColor: 'var(--bg-card)',
                  cursor: 'pointer',
                  userSelect: 'none'
                }}
                onClick={() => toggleExpand(cat.id)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{ color: 'var(--text-muted)' }}>
                      {isExpanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                    </div>
                    <span style={{ fontSize: '1.25rem' }}>{cat.icon || '🛠️'}</span>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span>{cat.name_uz}</span>
                        {cat.name_ru && <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 400 }}>({cat.name_ru})</span>}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.1rem' }}>
                        Tartib: #{cat.order} • Lavozimlar: <b>{positions.length} ta</b>
                      </div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }} onClick={(e) => e.stopPropagation()}>
                    <span className={`badge ${cat.is_active ? 'badge-online' : 'badge-offline'}`}>
                      {cat.is_active ? 'Faol' : 'Nofaol'}
                    </span>

                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleOpenPositionModal(cat.id, null)}
                      style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                      title="Ushbu sohaga lavozim qo'shish"
                    >
                      <PlusCircle size={13} color="#10b981" />
                      <span>Lavozim Qo'shish</span>
                    </button>

                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleOpenCategoryModal(cat)}
                      style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}
                      title="Sohani tahrirlash"
                    >
                      <Edit3 size={13} color="#3b82f6" />
                    </button>

                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleDeleteCategory(cat.id)}
                      style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem', color: '#ef4444' }}
                      title="Sohani o'chirish"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                </div>

                {/* Sub-Positions List */}
                {isExpanded && (
                  <div style={{ padding: '0.85rem 1.25rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
                    {positions.length === 0 ? (
                      <div style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                        Ushbu soha ostida lavozimlar mavjud emas. Yuqoridagi "Lavozim Qo'shish" tugmasini bosing.
                      </div>
                    ) : (
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.75rem' }}>
                        {positions.map((pos) => (
                          <div 
                            key={pos.id}
                            style={{
                              padding: '0.65rem 0.85rem',
                              backgroundColor: 'var(--bg-card)',
                              border: '1px solid var(--border-color)',
                              borderRadius: '6px',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between'
                            }}
                          >
                            <div>
                              <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-main)' }}>
                                🔨 {pos.name_uz}
                              </div>
                              {pos.name_ru && (
                                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.1rem' }}>
                                  RU: {pos.name_ru}
                                </div>
                              )}
                            </div>

                            <div style={{ display: 'flex', gap: '0.3rem' }}>
                              <button 
                                className="btn btn-secondary"
                                onClick={() => handleOpenPositionModal(cat.id, pos)}
                                style={{ padding: '0.25rem 0.45rem', fontSize: '0.7rem' }}
                                title="Tahrirlash"
                              >
                                <Edit3 size={11} color="#3b82f6" />
                              </button>
                              <button 
                                className="btn btn-secondary"
                                onClick={() => handleDeletePosition(pos.id)}
                                style={{ padding: '0.25rem 0.45rem', fontSize: '0.7rem', color: '#ef4444' }}
                                title="O'chirish"
                              >
                                <Trash2 size={11} />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

              </div>
            );
          })
        )}
      </div>

      {/* MODAL 1: Category Modal (Add / Edit) */}
      {isCategoryModalOpen && (
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
          <div className="card" style={{ maxWidth: '540px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-main)' }}>
                {editingCategory ? 'Sohani Tahrirlash' : 'Yangi Soha Qo\'shish'}
              </h3>
              <button onClick={() => setIsCategoryModalOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSaveCategory}>
              <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <div className="form-group">
                  <label>Nomi (O'zbek Lotin) *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={catFormData.name_uz}
                    onChange={(e) => setCatFormData({ ...catFormData, name_uz: e.target.value })}
                    placeholder="Qurilish va Ta'mirlash"
                  />
                </div>
                <div className="form-group">
                  <label>Номи (Ўзбек Кирилл)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={catFormData.name_oz}
                    onChange={(e) => setCatFormData({ ...catFormData, name_oz: e.target.value })}
                    placeholder="Қурилиш ва Таъмирлаш"
                  />
                </div>
                <div className="form-group">
                  <label>Название (Русский)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={catFormData.name_ru}
                    onChange={(e) => setCatFormData({ ...catFormData, name_ru: e.target.value })}
                    placeholder="Строительство и Ремонт"
                  />
                </div>
                <div className="form-group">
                  <label>Name (English)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={catFormData.name_en}
                    onChange={(e) => setCatFormData({ ...catFormData, name_en: e.target.value })}
                    placeholder="Construction & Repair"
                  />
                </div>
              </div>

              <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.25rem' }}>
                <div className="form-group">
                  <label>Emoji Ikonka</label>
                  <input
                    type="text"
                    className="form-control"
                    value={catFormData.icon}
                    onChange={(e) => setCatFormData({ ...catFormData, icon: e.target.value })}
                    placeholder="🛠️"
                  />
                </div>
                <div className="form-group">
                  <label>Tartib Raqami</label>
                  <input
                    type="number"
                    className="form-control"
                    value={catFormData.order}
                    onChange={(e) => setCatFormData({ ...catFormData, order: parseInt(e.target.value) || 0 })}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setIsCategoryModalOpen(false)}>
                  Bekor qilish
                </button>
                <button type="submit" className="btn" disabled={loading}>
                  {loading ? 'Saqlanmoqda...' : 'Saqlash'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 2: Position Modal (Add / Edit) */}
      {isPositionModalOpen && (
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
          <div className="card" style={{ maxWidth: '540px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-main)' }}>
                {editingPosition ? 'Lavozimni Tahrirlash' : 'Yangi Lavozim / Mutaxassislik Qo\'shish'}
              </h3>
              <button onClick={() => setIsPositionModalOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSavePosition}>
              <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <div className="form-group">
                  <label>Lavozim Nomi (Lotin) *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={posFormData.name_uz}
                    onChange={(e) => setPosFormData({ ...posFormData, name_uz: e.target.value })}
                    placeholder="Devor urish (G'isht teruvchi)"
                  />
                </div>
                <div className="form-group">
                  <label>Лавозим номи (Кирилл)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={posFormData.name_oz}
                    onChange={(e) => setPosFormData({ ...posFormData, name_oz: e.target.value })}
                    placeholder="Девор уриш"
                  />
                </div>
                <div className="form-group">
                  <label>Название (Русский)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={posFormData.name_ru}
                    onChange={(e) => setPosFormData({ ...posFormData, name_ru: e.target.value })}
                    placeholder="Каменщик / Кладка стен"
                  />
                </div>
                <div className="form-group">
                  <label>Name (English)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={posFormData.name_en}
                    onChange={(e) => setPosFormData({ ...posFormData, name_en: e.target.value })}
                    placeholder="Bricklayer / Wall builder"
                  />
                </div>
              </div>

              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label>Tartib Raqami</label>
                <input
                  type="number"
                  className="form-control"
                  value={posFormData.order}
                  onChange={(e) => setPosFormData({ ...posFormData, order: parseInt(e.target.value) || 0 })}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setIsPositionModalOpen(false)}>
                  Bekor qilish
                </button>
                <button type="submit" className="btn" disabled={loading}>
                  {loading ? 'Saqlanmoqda...' : 'Lavozimni Saqlash'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

