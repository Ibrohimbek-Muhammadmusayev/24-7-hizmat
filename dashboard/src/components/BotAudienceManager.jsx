import React, { useState, useEffect } from 'react';
import { 
  fetchUsers, 
  createUser, 
  updateUser, 
  deleteUser, 
  updateUserCredits, 
  requestProfileUpdate,
  fetchCategories, 
  fetchPositions 
} from '../services/api';
import { 
  Users, 
  Search, 
  RefreshCw, 
  RotateCcw,
  Shield, 
  Star, 
  Hash, 
  CheckCircle2, 
  Briefcase, 
  HardHat, 
  Sparkles, 
  Coins, 
  PlusCircle, 
  Edit3, 
  Trash2,
  Eye,
  X,
  Save,
  AlertCircle,
  Phone,
  Calendar,
  MapPin,
  Clock,
  UserPlus,
  UserCheck,
  UserX,
  Globe,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

export default function BotAudienceManager() {
  const [users, setUsers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('ALL'); // 'ALL' | 'WORKER' | 'CLIENT'
  const [botFilter, setBotFilter] = useState('ALL'); // 'ALL' | 'CLIENT_BOT' | 'WORKER_BOT' | 'BOTH'
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;
  
  // Modals state
  const [viewingUser, setViewingUser] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [creditUser, setCreditUser] = useState(null);
  const [deleteConfirmUser, setDeleteConfirmUser] = useState(null);
  const [requestUpdateUser, setRequestUpdateUser] = useState(null);
  const [updateReasonInput, setUpdateReasonInput] = useState('');

  // Credit Edit Modal State
  const [creditsInput, setCreditsInput] = useState(3);
  const [modalSaving, setModalSaving] = useState(false);
  const [modalFeedback, setModalFeedback] = useState(null);

  // Form State (for Create & Edit)
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    phone_number: '+99890',
    role: 'CLIENT',
    language: 'uz',
    telegram_id: '',
    gender: '',
    age: '',
    region_name: '',
    district: '',
    street_address: '',
    specialty: '',
    category: '',
    position: '',
    employment_type: 'daily',
    work_schedule: '24_7',
    job_credits: 3,
    is_online: true,
    is_registered: true
  });

  const loadInitialData = async () => {
    try {
      const [catsRes, posRes] = await Promise.all([
        fetchCategories(),
        fetchPositions()
      ]);
      setCategories(catsRes.data || []);
      setPositions(posRes.data || []);
    } catch (e) {
      console.error('Error fetching categories/positions:', e);
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    try {
      const params = {};
      if (roleFilter !== 'ALL') {
        params.role = roleFilter;
      }
      if (botFilter === 'CLIENT_BOT') {
        params.bot_filter = 'CLIENT';
      } else if (botFilter === 'WORKER_BOT') {
        params.bot_filter = 'WORKER';
      } else if (botFilter === 'BOTH') {
        params.bot_filter = 'BOTH';
      }

      if (searchTerm.trim()) {
        params.search = searchTerm.trim();
      }
      const res = await fetchUsers(params);
      setUsers(res.data || []);
    } catch (err) {
      console.error('Error fetching users:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    setCurrentPage(1);
    loadUsers();
  }, [roleFilter, botFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadUsers();
  };

  // Open Create Modal
  const handleOpenAddModal = () => {
    setFormData({
      username: `user_${Date.now()}`,
      first_name: '',
      last_name: '',
      phone_number: '+99890',
      role: 'CLIENT',
      language: 'uz',
      telegram_id: '',
      gender: '',
      age: '',
      region_name: '',
      district: '',
      street_address: '',
      specialty: '',
      category: '',
      position: '',
      employment_type: 'daily',
      work_schedule: '24_7',
      job_credits: 3,
      is_online: true,
      is_registered: true
    });
    setModalFeedback(null);
    setIsAddModalOpen(true);
  };

  // Open Edit Modal
  const handleOpenEditModal = (u) => {
    setEditingUser(u);
    setFormData({
      username: u.username || '',
      first_name: u.first_name || '',
      last_name: u.last_name || '',
      phone_number: u.phone_number || '',
      role: u.role || 'CLIENT',
      language: u.language || 'uz',
      telegram_id: u.telegram_id || '',
      gender: u.gender || '',
      age: u.age || '',
      region_name: u.region_name || '',
      district: u.district || '',
      street_address: u.street_address || '',
      specialty: u.specialty || '',
      category: u.category || '',
      position: u.position || '',
      employment_type: u.employment_type || 'daily',
      work_schedule: u.work_schedule || '24_7',
      job_credits: u.job_credits ?? 3,
      is_online: u.is_online ?? true,
      is_registered: u.is_registered ?? true
    });
    setModalFeedback(null);
  };

  // Save (Create or Update)
  const handleSaveUserForm = async (e) => {
    e.preventDefault();
    setModalSaving(true);
    setModalFeedback(null);

    try {
      const payload = { ...formData };
      if (!payload.telegram_id) delete payload.telegram_id;
      if (!payload.category) delete payload.category;
      if (!payload.position) delete payload.position;
      if (!payload.age) delete payload.age;

      if (editingUser) {
        await updateUser(editingUser.id, payload);
        setModalFeedback({ type: 'success', message: 'Foydalanuvchi ma\'lumotlari muvaffaqiyatli yangilandi!' });
      } else {
        await createUser(payload);
        setModalFeedback({ type: 'success', message: 'Yangi foydalanuvchi muvaffaqiyatli yaratildi!' });
      }

      await loadUsers();
      setTimeout(() => {
        setIsAddModalOpen(false);
        setEditingUser(null);
      }, 1000);
    } catch (err) {
      console.error(err);
      const msg = err.response?.data?.error || JSON.stringify(err.response?.data) || 'Saqlashda xatolik yuz berdi!';
      setModalFeedback({ type: 'error', message: msg });
    } finally {
      setModalSaving(false);
    }
  };

  // Delete User
  const handleDeleteUser = async () => {
    if (!deleteConfirmUser) return;
    setModalSaving(true);
    try {
      await deleteUser(deleteConfirmUser.id);
      setUsers(prev => prev.filter(u => u.id !== deleteConfirmUser.id));
      setDeleteConfirmUser(null);
    } catch (err) {
      alert("Foydalanuvchini o'chirishda xatolik yuz berdi!");
    } finally {
      setModalSaving(false);
    }
  };

  // Credits Modal
  const handleOpenCreditModal = (user) => {
    setCreditUser(user);
    setCreditsInput(user.job_credits ?? 3);
    setModalFeedback(null);
  };

  const handleSaveCredits = async (e) => {
    e.preventDefault();
    if (!creditUser) return;
    setModalSaving(true);
    try {
      await updateUserCredits(creditUser.id, { job_credits: creditsInput });
      setModalFeedback({ type: 'success', message: 'Kreditlar muvaffaqiyatli saqlandi!' });
      setUsers(prev => prev.map(u => u.id === creditUser.id ? { ...u, job_credits: creditsInput } : u));
      
      setTimeout(() => {
        setCreditUser(null);
      }, 1000);
    } catch (err) {
      const msg = err.response?.data?.error || 'Kreditlarni saqlashda xatolik!';
      setModalFeedback({ type: 'error', message: msg });
    } finally {
      setModalSaving(false);
    }
  };

  const [selectedUpdateFields, setSelectedUpdateFields] = useState(['name', 'phone', 'location', 'positions', 'gender_age', 'work_schedule']);

  // Request Profile Update Modal
  const handleOpenRequestUpdateModal = (user) => {
    setRequestUpdateUser(user);
    setSelectedUpdateFields(['name', 'phone', 'location', 'positions', 'gender_age', 'work_schedule']);
    setUpdateReasonInput("Profil ma'lumotlaringizda noaniqliklar aniqlandi. Iltimos, ma'lumotlaringizni to'liq va to'g'ri qaytadan kiriting.");
    setModalFeedback(null);
  };

  const toggleUpdateField = (fieldKey) => {
    setSelectedUpdateFields(prev => {
      if (prev.includes(fieldKey)) {
        return prev.filter(k => k !== fieldKey);
      } else {
        return [...prev, fieldKey];
      }
    });
  };

  const handleSaveRequestUpdate = async (e) => {
    e.preventDefault();
    if (!requestUpdateUser) return;
    if (selectedUpdateFields.length === 0) {
      setModalFeedback({ type: 'error', message: "Iltimos, kamida bitta to'ldirilishi kerak bo'lgan maydonni tanlang!" });
      return;
    }
    setModalSaving(true);
    try {
      await requestProfileUpdate(requestUpdateUser.id, { 
        reason: updateReasonInput,
        fields: selectedUpdateFields
      });
      setModalFeedback({ type: 'success', message: "Foydalanuvchiga tanlangan maydonlarni qayta to'ldirish so'rovi va Telegram xabarnomasi yuborildi!" });
      setUsers(prev => prev.map(u => u.id === requestUpdateUser.id ? { 
        ...u, 
        needs_profile_update: true, 
        profile_update_reason: updateReasonInput,
        profile_update_fields: selectedUpdateFields.join(',')
      } : u));
      
      setTimeout(() => {
        setRequestUpdateUser(null);
      }, 1500);
    } catch (err) {
      const msg = err.response?.data?.error || "So'rov yuborishda xatolik yuz berdi!";
      setModalFeedback({ type: 'error', message: msg });
    } finally {
      setModalSaving(false);
    }
  };

  const workerCount = users.filter(u => u.role === 'WORKER').length;
  const clientCount = users.filter(u => u.role === 'CLIENT').length;
  const registeredCount = users.filter(u => u.is_registered).length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Header card with summary stats */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Users size={20} color="#3b82f6" />
              Foydalanuvchilar Boshqaruvi & CRM ({users.length} ta)
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Barcha ro'yxatdan o'tgan ustalar, ish beruvchilar, ularning profillari, kreditlari va faollik holati
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
            <button className="btn btn-secondary" onClick={loadUsers} disabled={loading}>
              <RefreshCw size={14} className={loading ? 'spin' : ''} />
              <span>Yangilash</span>
            </button>
            <button className="btn" onClick={handleOpenAddModal} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
              <UserPlus size={15} />
              <span>Yangi Foydalanuvchi</span>
            </button>
          </div>
        </div>

        {/* Audience summary counters */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '1rem',
          padding: '1rem',
          backgroundColor: 'var(--bg-inner)',
          borderRadius: '10px',
          border: '1px solid var(--border-color)',
          marginBottom: '1rem'
        }}>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Jami Foydalanuvchilar</div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', marginTop: '0.15rem' }}>{users.length}</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>👷 Ustalar / Mutaxassislar</div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981', marginTop: '0.15rem' }}>{workerCount}</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>👔 Ish Beruvchilar / Mijozlar</div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#3b82f6', marginTop: '0.15rem' }}>{clientCount}</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>✅ To'liq Ro'yxatdan O'tgan</div>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#8b5cf6', marginTop: '0.15rem' }}>{registeredCount}</div>
          </div>
        </div>

        {/* Filter and Search Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          
          {/* Role Filter Tabs */}
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {[
              { id: 'ALL', label: 'Barchasi', icon: Users },
              { id: 'WORKER', label: '👷 Ustalar', icon: HardHat },
              { id: 'CLIENT', label: '👔 Ish Beruvchilar', icon: Briefcase },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setRoleFilter(tab.id)}
                style={{
                  padding: '0.45rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid',
                  borderColor: roleFilter === tab.id ? 'var(--primary)' : 'var(--border-color)',
                  background: roleFilter === tab.id ? 'var(--primary)' : 'var(--bg-inner)',
                  color: roleFilter === tab.id ? '#fff' : 'var(--text-muted)',
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
          <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', flex: 1, maxWidth: '360px' }}>
            <input
              type="text"
              className="form-control"
              placeholder="Ism, telefon, mutaxassislik, TG ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ fontSize: '0.85rem' }}
            />
            <button type="submit" className="btn" style={{ padding: '0.5rem 0.9rem' }}>
              <Search size={15} />
            </button>
          </form>
        </div>
      </div>

      {/* Users Table */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Foydalanuvchi</th>
                <th>Rol & Soha</th>
                <th>Telefon & Manzil</th>
                <th>Telegram & Til</th>
                <th>Bot Ishtiroki</th>
                <th>💳 Kreditlar</th>
                <th style={{ textAlign: 'center' }}>Amallar</th>
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
                          <div className="skeleton skeleton-title" style={{ width: '100px', height: '14px' }} />
                          <div className="skeleton skeleton-text" style={{ width: '60px', height: '10px' }} />
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="skeleton skeleton-text" style={{ width: '90px', height: '14px', marginBottom: '4px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '60px', height: '10px' }} />
                    </td>
                    <td>
                      <div className="skeleton skeleton-text" style={{ width: '100px', height: '14px', marginBottom: '4px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '70px', height: '10px' }} />
                    </td>
                    <td>
                      <div className="skeleton skeleton-text" style={{ width: '75px', height: '14px' }} />
                    </td>
                    <td>
                      <div className="skeleton" style={{ width: '80px', height: '22px', borderRadius: '12px' }} />
                    </td>
                    <td>
                      <div className="skeleton" style={{ width: '50px', height: '20px', borderRadius: '6px' }} />
                    </td>
                    <td style={{ textAlign: 'center' }}>
                      <div style={{ display: 'inline-flex', gap: '4px' }}>
                        <div className="skeleton" style={{ width: '26px', height: '26px', borderRadius: '6px' }} />
                        <div className="skeleton" style={{ width: '26px', height: '26px', borderRadius: '6px' }} />
                        <div className="skeleton" style={{ width: '26px', height: '26px', borderRadius: '6px' }} />
                      </div>
                    </td>
                  </tr>
                ))
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan="8" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                    Foydalanuvchilar topilmadi.
                  </td>
                </tr>
              ) : (
                users.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((u) => {
                  const initials = (u.first_name ? u.first_name[0] : (u.username ? u.username[0] : 'U')).toUpperCase();

                  // Bot Participation Badge
                  let botBadge = null;
                  if (u.started_client_bot && u.started_worker_bot) {
                    botBadge = (
                      <span className="badge" style={{ background: 'rgba(139, 92, 246, 0.18)', color: '#c084fc', border: '1px solid rgba(139, 92, 246, 0.35)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <Sparkles size={11} /> Ikkala Bot
                      </span>
                    );
                  } else if (u.started_client_bot) {
                    botBadge = (
                      <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', border: '1px solid rgba(59, 130, 246, 0.3)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <Briefcase size={11} /> Ish Beruvchi
                      </span>
                    );
                  } else if (u.started_worker_bot) {
                    botBadge = (
                      <span className="badge badge-online" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                        <HardHat size={11} /> Usta Boti
                      </span>
                    );
                  } else {
                    botBadge = <span className="badge badge-offline">Veb Ilova</span>;
                  }

                  return (
                    <tr key={u.id}>
                      <td style={{ color: 'var(--text-muted)', fontWeight: 600, fontSize: '0.8rem' }}>#{u.id}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                          <div style={{
                            width: '34px',
                            height: '34px',
                            borderRadius: '50%',
                            background: u.role === 'WORKER' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #3b82f6, #2563eb)',
                            color: '#fff',
                            fontWeight: 700,
                            fontSize: '0.82rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 2px 6px rgba(0,0,0,0.15)'
                          }}>
                            {initials}
                          </div>
                          <div>
                            <div style={{ fontWeight: 600, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                              <span>{u.first_name || u.username} {u.last_name || ''}</span>
                              {u.is_registered && <CheckCircle2 size={13} color="#10b981" title="To'liq ro'yxatdan o'tgan" />}
                            </div>
                            <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                              @{u.username}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.15rem' }}>
                          <span style={{ 
                            fontWeight: 600, 
                            fontSize: '0.82rem', 
                            color: u.role === 'WORKER' ? '#10b981' : '#3b82f6' 
                          }}>
                            {u.role === 'WORKER' ? '👷 Usta / Mutaxassis' : '👔 Ish Beruvchi'}
                          </span>
                          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                            {u.specialty || u.position_details?.name || 'Kiritilmagan'}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.15rem' }}>
                          <span style={{ fontWeight: 500, fontFamily: 'monospace', fontSize: '0.84rem' }}>
                            {u.phone_number || '—'}
                          </span>
                          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                            <MapPin size={11} /> {u.region_name || u.district || 'Manzil yo\'q'}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                          {u.telegram_id ? (
                            <span style={{ 
                              display: 'inline-flex', 
                              alignItems: 'center', 
                              gap: '0.25rem', 
                              fontFamily: 'monospace', 
                              background: 'var(--bg-inner)', 
                              padding: '0.15rem 0.45rem', 
                              borderRadius: '4px',
                              border: '1px solid var(--border-color)',
                              fontSize: '0.76rem',
                              color: 'var(--text-secondary)'
                            }}>
                              <Hash size={11} color="#06b6d4" />
                              {u.telegram_id}
                            </span>
                          ) : (
                            <span style={{ color: 'var(--text-muted)', fontSize: '0.76rem' }}>—</span>
                          )}
                          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                            🌐 {u.language || 'UZ'}
                          </span>
                        </div>
                      </td>
                      <td>{botBadge}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          <span style={{
                            fontWeight: 700,
                            color: (u.job_credits ?? 0) > 0 ? '#10b981' : '#ef4444',
                            fontSize: '0.88rem',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.25rem',
                            background: 'var(--bg-inner)',
                            padding: '0.2rem 0.55rem',
                            borderRadius: '6px',
                            border: '1px solid var(--border-color)'
                          }}>
                            <Coins size={13} color="#f59e0b" />
                            {u.job_credits ?? 0} ta
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem' }}>
                          <button
                            className="btn btn-secondary"
                            onClick={() => setViewingUser(u)}
                            title="Batafsil ko'rish"
                            style={{ padding: '0.35rem 0.5rem', fontSize: '0.76rem' }}
                          >
                            <Eye size={13} color="#06b6d4" />
                          </button>

                          <button
                            className="btn btn-secondary"
                            onClick={() => handleOpenEditModal(u)}
                            title="Tahrirlash"
                            style={{ padding: '0.35rem 0.5rem', fontSize: '0.76rem' }}
                          >
                            <Edit3 size={13} color="#3b82f6" />
                          </button>

                          {/* Super Admin uchun boshqa amallar (kredit, qayta to'ldirish, o'chirish) yopiq */}
                          {u.is_superuser ? (
                            <span 
                              title="Super Admin hisobi daxlsiz (Faqat tahrirlash mumkin)" 
                              style={{ 
                                padding: '0.35rem 0.6rem', 
                                fontSize: '0.74rem', 
                                color: '#fbbf24', 
                                background: 'rgba(251, 191, 36, 0.12)', 
                                border: '1px solid rgba(251, 191, 36, 0.3)', 
                                borderRadius: '6px',
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '0.25rem',
                                fontWeight: 700
                              }}
                            >
                              👑 Super Admin
                            </span>
                          ) : (
                            <>
                              <button
                                className="btn btn-secondary"
                                onClick={() => handleOpenCreditModal(u)}
                                title="Kredit tahrirlash"
                                style={{ padding: '0.35rem 0.5rem', fontSize: '0.76rem' }}
                              >
                                <Coins size={13} color="#f59e0b" />
                              </button>
                              <button
                                className="btn btn-secondary"
                                onClick={() => handleOpenRequestUpdateModal(u)}
                                title="Ma'lumotlarni qayta to'ldirishga yuborish"
                                style={{ 
                                  padding: '0.35rem 0.5rem', 
                                  fontSize: '0.76rem', 
                                  color: u.needs_profile_update ? '#ef4444' : '#f59e0b',
                                  borderColor: u.needs_profile_update ? 'rgba(239, 68, 68, 0.4)' : 'rgba(245, 158, 11, 0.4)'
                                }}
                              >
                                <RotateCcw size={13} />
                              </button>
                              {!(u.is_staff || u.role === 'ADMIN') ? (
                                <button
                                  className="btn btn-secondary"
                                  onClick={() => setDeleteConfirmUser(u)}
                                  title="O'chirish"
                                  style={{ padding: '0.35rem 0.5rem', fontSize: '0.76rem', color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.25)' }}
                                >
                                  <Trash2 size={13} />
                                </button>
                              ) : (
                                <span 
                                  title="Admin hisobi (O'chirish mumkin emas)" 
                                  style={{ 
                                    padding: '0.35rem 0.5rem', 
                                    fontSize: '0.76rem', 
                                    color: '#10b981', 
                                    background: 'rgba(16, 185, 129, 0.1)', 
                                    border: '1px solid rgba(16, 185, 129, 0.25)', 
                                    borderRadius: '6px',
                                    display: 'inline-flex',
                                    alignItems: 'center'
                                  }}
                                >
                                  <Shield size={13} />
                                </span>
                              )}
                            </>
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
        {users.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, users.length)}</b> / Jami: <b>{users.length}</b> ta
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
              {Array.from({ length: Math.ceil(users.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(users.length / pageSize) || Math.abs(p - currentPage) <= 1)
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
                disabled={currentPage === Math.ceil(users.length / pageSize)}
                onClick={() => setCurrentPage(prev => Math.min(Math.ceil(users.length / pageSize), prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* --- MODAL 1: VIEW DETAILS MODAL --- */}
      {viewingUser && (
        <div className="modal-backdrop" onClick={() => setViewingUser(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '540px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Users size={20} color="#3b82f6" />
                <h3 className="card-title" style={{ margin: 0 }}>Foydalanuvchi Profili</h3>
              </div>
              <button onClick={() => setViewingUser(null)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', backgroundColor: 'var(--bg-inner)', borderRadius: '10px', marginBottom: '1.25rem' }}>
              <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '50%',
                background: viewingUser.role === 'WORKER' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #3b82f6, #2563eb)',
                color: '#fff',
                fontWeight: 800,
                fontSize: '1.2rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {(viewingUser.first_name ? viewingUser.first_name[0] : (viewingUser.username ? viewingUser.username[0] : 'U')).toUpperCase()}
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--text-main)' }}>
                  {viewingUser.first_name || viewingUser.username} {viewingUser.last_name || ''}
                </h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  ID: #{viewingUser.id} • @{viewingUser.username}
                </div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.85rem' }}>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Rol:</span>
                <div style={{ fontWeight: 600, color: viewingUser.role === 'WORKER' ? '#10b981' : '#3b82f6', marginTop: '0.2rem' }}>
                  {viewingUser.role === 'WORKER' ? '👷 Usta / Mutaxassis' : '👔 Ish Beruvchi'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Telefon:</span>
                <div style={{ fontWeight: 600, fontFamily: 'monospace', marginTop: '0.2rem' }}>
                  {viewingUser.phone_number || 'Kiritilmagan'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Telegram ID:</span>
                <div style={{ fontWeight: 600, fontFamily: 'monospace', marginTop: '0.2rem' }}>
                  {viewingUser.telegram_id ? `#${viewingUser.telegram_id}` : 'Mavjud emas'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Kreditlar Balansi:</span>
                <div style={{ fontWeight: 700, color: '#f59e0b', marginTop: '0.2rem' }}>
                  {viewingUser.job_credits ?? 0} ta
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Manzil:</span>
                <div style={{ fontWeight: 600, marginTop: '0.2rem' }}>
                  {viewingUser.region_name || viewingUser.district || 'Kiritilmagan'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Mutaxassislik:</span>
                <div style={{ fontWeight: 600, marginTop: '0.2rem' }}>
                  {viewingUser.specialty || viewingUser.position_details?.name || 'Mavjud emas'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Ro'yxatdan o'tgan sana:</span>
                <div style={{ fontWeight: 500, fontSize: '0.8rem', marginTop: '0.2rem' }}>
                  {viewingUser.date_joined ? new Date(viewingUser.date_joined).toLocaleString() : '—'}
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Faollik (Online):</span>
                <div style={{ marginTop: '0.2rem' }}>
                  <span className={`badge ${viewingUser.is_online ? 'badge-online' : 'badge-offline'}`}>
                    {viewingUser.is_online ? 'Online' : 'Offline'}
                  </span>
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Bandlik Holati:</span>
                <div style={{ marginTop: '0.2rem' }}>
                  <span className={`badge ${viewingUser.is_busy ? 'badge-busy' : 'badge-finished'}`}>
                    {viewingUser.is_busy ? '🔴 Band (Ishda)' : "🟢 Bo'sh"}
                  </span>
                </div>
              </div>
              <div className="card" style={{ padding: '0.75rem', marginBottom: 0 }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.74rem' }}>Til:</span>
                <div style={{ fontWeight: 600, textTransform: 'uppercase', marginTop: '0.2rem' }}>
                  {viewingUser.language || 'UZ'}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
              <button className="btn btn-secondary" onClick={() => setViewingUser(null)}>
                Yopish
              </button>
              <button className="btn" onClick={() => { const u = viewingUser; setViewingUser(null); handleOpenEditModal(u); }}>
                <Edit3 size={14} /> Tahrirlash
              </button>
            </div>
          </div>
        </div>
      )}

      {/* --- MODAL 2: CREATE / EDIT USER MODAL --- */}
      {(isAddModalOpen || editingUser) && (
        <div className="modal-backdrop" onClick={() => { setIsAddModalOpen(false); setEditingUser(null); }}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '620px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <UserPlus size={20} color="#3b82f6" />
                <h3 className="card-title" style={{ margin: 0 }}>
                  {editingUser ? "Foydalanuvchi Ma'lumotlarini Tahrirlash" : "Yangi Foydalanuvchi Yaratish"}
                </h3>
              </div>
              <button onClick={() => { setIsAddModalOpen(false); setEditingUser(null); }} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            {modalFeedback && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                backgroundColor: modalFeedback.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
                color: modalFeedback.type === 'success' ? '#10b981' : '#ef4444',
                border: `1px solid ${modalFeedback.type === 'success' ? '#10b981' : '#ef4444'}`
              }}>
                {modalFeedback.message}
              </div>
            )}

            <form onSubmit={handleSaveUserForm}>
              <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
                
                <div className="form-group">
                  <label>Ismi *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    placeholder="Masalan: Ali"
                  />
                </div>

                <div className="form-group">
                  <label>Familiyasi</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    placeholder="Masalan: Valiyev"
                  />
                </div>

                <div className="form-group">
                  <label>Telefon Raqam *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                    placeholder="+998901234567"
                  />
                </div>

                <div className="form-group">
                  <label>Rol *</label>
                  <select
                    className="form-control"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    <option value="CLIENT">👔 Ish Beruvchi / Mijoz</option>
                    <option value="WORKER">👷 Usta / Mutaxassis</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Telegram ID (ixtiyoriy)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.telegram_id}
                    onChange={(e) => setFormData({ ...formData, telegram_id: e.target.value })}
                    placeholder="Masalan: 123456789"
                  />
                </div>

                <div className="form-group">
                  <label>Til</label>
                  <select
                    className="form-control"
                    value={formData.language}
                    onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                  >
                    <option value="uz">Lotincha (O'zbek)</option>
                    <option value="oz">Kirillcha (Ўзбек)</option>
                    <option value="ru">Русский</option>
                    <option value="en">English</option>
                  </select>
                </div>

                {formData.role === 'WORKER' && (
                  <>
                    <div className="form-group">
                      <label>Mutaxassislik / Kasbi</label>
                      <input
                        type="text"
                        className="form-control"
                        value={formData.specialty}
                        onChange={(e) => setFormData({ ...formData, specialty: e.target.value })}
                        placeholder="Masalan: Santexnik, Elektrik..."
                      />
                    </div>

                    <div className="form-group">
                      <label>Ish Grafiki</label>
                      <select
                        className="form-control"
                        value={formData.work_schedule}
                        onChange={(e) => setFormData({ ...formData, work_schedule: e.target.value })}
                      >
                        <option value="24_7">🔥 24/7 Shoshilinch</option>
                        <option value="day_shift">☀️ Kunduzgi (09:00 - 18:00)</option>
                        <option value="flexible">⏱️ Erkin grafik</option>
                      </select>
                    </div>
                  </>
                )}

                <div className="form-group">
                  <label>Tuman / Hudud</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.district}
                    onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                    placeholder="Masalan: Chilonzor, Yunusobod..."
                  />
                </div>

                <div className="form-group">
                  <label>Kreditlar Soni</label>
                  <input
                    type="number"
                    min="0"
                    className="form-control"
                    value={formData.job_credits}
                    onChange={(e) => setFormData({ ...formData, job_credits: parseInt(e.target.value) || 0 })}
                  />
                </div>

              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => { setIsAddModalOpen(false); setEditingUser(null); }}
                  disabled={modalSaving}
                >
                  Bekor Qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={modalSaving}
                  style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
                >
                  <Save size={15} />
                  {modalSaving ? 'Saqlanmoqda...' : 'Saqlash'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --- MODAL 3: CREDIT EDIT MODAL --- */}
      {creditUser && (
        <div className="modal-backdrop" onClick={() => setCreditUser(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '440px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem' }}>
                <Coins size={18} color="#f59e0b" />
                Kredit Balansini O'zgartirish
              </h3>
              <button 
                onClick={() => setCreditUser(null)}
                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
              >
                <X size={18} />
              </button>
            </div>

            <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', marginBottom: '1.25rem' }}>
              Foydalanuvchi: <b>{creditUser.first_name || creditUser.username}</b> (ID: #{creditUser.id})
            </p>

            {modalFeedback && (
              <div style={{
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                backgroundColor: modalFeedback.type === 'success' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
                color: modalFeedback.type === 'success' ? '#10b981' : '#ef4444',
                border: `1px solid ${modalFeedback.type === 'success' ? '#10b981' : '#ef4444'}`
              }}>
                {modalFeedback.message}
              </div>
            )}

            <form onSubmit={handleSaveCredits}>
              
              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label style={{ fontWeight: 600 }}>Kreditlar Soni (Jami Balans):</label>
                <input
                  type="number"
                  min="0"
                  max="1000"
                  className="form-control"
                  value={creditsInput}
                  onChange={(e) => setCreditsInput(parseInt(e.target.value) || 0)}
                  style={{ fontSize: '1.2rem', fontWeight: 700, textAlign: 'center', marginTop: '0.4rem' }}
                />
              </div>

              {/* Quick Add Buttons */}
              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                  Tezkor Qo'shish:
                </div>
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  {[1, 3, 5, 10, 20].map(val => (
                    <button
                      key={val}
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => setCreditsInput(prev => prev + val)}
                      style={{ flex: 1, padding: '0.4rem 0', fontSize: '0.8rem', fontWeight: 600 }}
                    >
                      +{val}
                    </button>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setCreditUser(null)}
                  disabled={modalSaving}
                >
                  Bekor Qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={modalSaving}
                  style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
                >
                  <Save size={15} />
                  {modalSaving ? 'Saqlanmoqda...' : 'Kreditni Saqlash'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

      {/* --- MODAL 4: DELETE CONFIRMATION MODAL --- */}
      {deleteConfirmUser && (
        <div className="modal-backdrop" onClick={() => setDeleteConfirmUser(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '420px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: '#ef4444' }}>
              <AlertCircle size={22} />
              <h3 className="card-title" style={{ margin: 0, color: '#ef4444' }}>Foydalanuvchini O'chirish</h3>
            </div>
            
            <p style={{ fontSize: '0.88rem', color: 'var(--text-main)', marginBottom: '1.25rem' }}>
              Haqiqatan ham <b>{deleteConfirmUser.first_name || deleteConfirmUser.username}</b> (ID: #{deleteConfirmUser.id}) foydalanuvchisini bazadan butunlay o'chirmoqchimisiz?
            </p>

            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
              <button
                className="btn btn-secondary"
                onClick={() => setDeleteConfirmUser(null)}
                disabled={modalSaving}
              >
                Bekor Qilish
              </button>
              <button
                className="btn"
                onClick={handleDeleteUser}
                disabled={modalSaving}
                style={{ backgroundColor: '#ef4444', borderColor: '#ef4444', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
              >
                <Trash2 size={15} />
                {modalSaving ? 'O\'chirilmoqda...' : 'Ha, O\'chirilsin'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* --- MODAL 5: REQUEST PROFILE UPDATE MODAL --- */}
      {requestUpdateUser && (
        <div className="modal-backdrop" onClick={() => setRequestUpdateUser(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()} style={{ maxWidth: '480px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b' }}>
                <RotateCcw size={20} />
                <h3 className="card-title" style={{ margin: 0 }}>Profilni Qayta To'ldirish So'rovi</h3>
              </div>
              <button className="btn btn-secondary" onClick={() => setRequestUpdateUser(null)} style={{ padding: '0.2rem 0.4rem' }}>
                <X size={16} />
              </button>
            </div>

            <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
              Foydalanuvchi: <b>{requestUpdateUser.first_name || requestUpdateUser.username}</b> (ID: #{requestUpdateUser.id})
              <br />
              Ushbu amal bajarilganda foydalanuvchiga Telegram orqali bildirishnoma yuboriladi va botga kirganida ma'lumotlarini (ism, telefon, mutaxassislik, joylashuv) qaytadan to'ldirish so'raladi.
            </p>

            {modalFeedback && (
              <div style={{
                padding: '0.6rem 0.8rem',
                borderRadius: '6px',
                fontSize: '0.84rem',
                marginBottom: '1rem',
                backgroundColor: modalFeedback.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                color: modalFeedback.type === 'success' ? '#10b981' : '#ef4444',
                border: `1px solid ${modalFeedback.type === 'success' ? '#10b981' : '#ef4444'}`
              }}>
                {modalFeedback.message}
              </div>
            )}

            <form onSubmit={handleSaveRequestUpdate}>
              <div className="form-group" style={{ marginBottom: '1rem' }}>
                <label style={{ fontWeight: 600, display: 'block', marginBottom: '0.4rem' }}>
                  Qaysi ma'lumotlar qayta to'ldirilishi kerak?
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.5rem', background: 'var(--bg-secondary)', padding: '0.75rem', borderRadius: '6px' }}>
                  {[
                    { key: 'name', label: "👤 Ism va Familiya" },
                    { key: 'phone', label: "📞 Telefon raqam" },
                    { key: 'location', label: "📍 Joylashuv / Manzil" },
                    { key: 'positions', label: "🛠 Soha / Mutaxassislik" },
                    { key: 'gender_age', label: "⚧ Yoshi va Jinsi" },
                    { key: 'work_schedule', label: "⏱ Ish rejimi / Bandlik" },
                  ].map(f => (
                    <label key={f.key} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', cursor: 'pointer', margin: 0 }}>
                      <input
                        type="checkbox"
                        checked={selectedUpdateFields.includes(f.key)}
                        onChange={() => toggleUpdateField(f.key)}
                        style={{ cursor: 'pointer' }}
                      />
                      <span>{f.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="form-group" style={{ marginBottom: '1.25rem' }}>
                <label style={{ fontWeight: 600 }}>Qayta to'ldirish sababi / Foydalanuvchiga xabar:</label>
                <textarea
                  className="form-control"
                  rows={3}
                  value={updateReasonInput}
                  onChange={(e) => setUpdateReasonInput(e.target.value)}
                  placeholder="Sabab yoki ko'rsatmani yozing..."
                  style={{ marginTop: '0.4rem', fontSize: '0.86rem', resize: 'vertical' }}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setRequestUpdateUser(null)}
                  disabled={modalSaving}
                >
                  Bekor Qilish
                </button>
                <button
                  type="submit"
                  className="btn"
                  disabled={modalSaving}
                  style={{ backgroundColor: '#f59e0b', borderColor: '#f59e0b', color: '#000', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem' }}
                >
                  <RotateCcw size={15} />
                  {modalSaving ? 'Yuborilmoqda...' : 'Qayta to\'ldirishga yuborish'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
