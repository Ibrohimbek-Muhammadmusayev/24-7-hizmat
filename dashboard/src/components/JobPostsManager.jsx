import React, { useState, useEffect } from 'react';
import { 
  Briefcase, 
  Search, 
  Filter, 
  Plus, 
  Trash2, 
  Edit3, 
  Eye, 
  Send, 
  Users, 
  Clock, 
  MapPin, 
  DollarSign, 
  CheckCircle, 
  XCircle, 
  PauseCircle, 
  PlayCircle,
  Phone,
  MessageSquare,
  AlertCircle,
  X,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { fetchJobPosts, createJobPost, updateJobPost, deleteJobPost, offerJobToWorker, fetchWorkers } from '../services/api';

export default function JobPostsManager({ categories, onRefresh }) {
  const [jobPosts, setJobPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [empTypeFilter, setEmpTypeFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  // Modals
  const [selectedJob, setSelectedJob] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isOfferModalOpen, setIsOfferModalOpen] = useState(false);

  // Offer Modal State
  const [availableWorkers, setAvailableWorkers] = useState([]);
  const [selectedWorkerId, setSelectedWorkerId] = useState('');
  const [offerLoading, setOfferLoading] = useState(false);
  const [offerSuccessMsg, setOfferSuccessMsg] = useState('');

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    position: '',
    custom_position_name: '',
    employment_type: 'daily',
    workers_count: '1 nafar',
    gender_requirement: 'any',
    start_time_type: 'urgent',
    custom_start_date: '',
    is_price_negotiable: true,
    price_amount: '',
    region: '',
    district: '',
    address: '',
    description: '',
    contact_name: '',
    contact_phone: '',
    status: 'active'
  });

  const loadJobPosts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (empTypeFilter) params.employment_type = empTypeFilter;

      const res = await fetchJobPosts(params);
      setJobPosts(res.data || []);
    } catch (err) {
      console.error("Error loading job posts:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobPosts();
  }, [search, statusFilter, categoryFilter, empTypeFilter]);

  const loadWorkersForOffer = async () => {
    try {
      const res = await fetchWorkers({ is_online: true });
      setAvailableWorkers(res.data || []);
    } catch (err) {
      console.error("Error loading workers:", err);
    }
  };

  const handleOpenOfferModal = (job) => {
    setSelectedJob(job);
    setSelectedWorkerId('');
    setOfferSuccessMsg('');
    setIsOfferModalOpen(true);
    loadWorkersForOffer();
  };

  const handleSendOffer = async () => {
    if (!selectedJob || !selectedWorkerId) return;
    try {
      setOfferLoading(true);
      await offerJobToWorker(selectedJob.id, selectedWorkerId);
      setOfferSuccessMsg("✅ Ish taklifi usta Telegram botiga muvaffaqiyatli yuborildi!");
      setTimeout(() => {
        setIsOfferModalOpen(false);
        setOfferSuccessMsg('');
      }, 2000);
    } catch (err) {
      alert("Taklif yuborishda xatolik yuz berdi!");
    } finally {
      setOfferLoading(false);
    }
  };

  const handleStatusChange = async (jobId, newStatus) => {
    try {
      await updateJobPost(jobId, { status: newStatus });
      loadJobPosts();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert("Statusni o'zgartirishda xatolik!");
    }
  };

  const handleDelete = async (jobId) => {
    if (!window.confirm("Haqiqatdan ham ushbu e'lonni o'chirmoqchimisiz?")) return;
    try {
      await deleteJobPost(jobId);
      loadJobPosts();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert("O'chirishda xatolik!");
    }
  };

  const handleOpenEdit = (job) => {
    setSelectedJob(job);
    setFormData({
      category: job.category || '',
      position: job.position || '',
      custom_position_name: job.custom_position_name || '',
      employment_type: job.employment_type || 'daily',
      workers_count: job.workers_count || '1 nafar',
      gender_requirement: job.gender_requirement || 'any',
      start_time_type: job.start_time_type || 'urgent',
      custom_start_date: job.custom_start_date || '',
      is_price_negotiable: job.is_price_negotiable,
      price_amount: job.price_amount || '',
      region: job.region || '',
      district: job.district || '',
      address: job.address || '',
      description: job.description || '',
      contact_name: job.contact_name || '',
      contact_phone: job.contact_phone || '',
      status: job.status || 'active'
    });
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    try {
      await updateJobPost(selectedJob.id, formData);
      setIsEditModalOpen(false);
      loadJobPosts();
      if (onRefresh) onRefresh();
    } catch (err) {
      alert("Saqlashda xatolik yuz berdi!");
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return <span className="badge badge-started" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}><PlayCircle size={12} /> Faol / Ochiq</span>;
      case 'paused':
        return <span className="badge badge-dispatched" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}><PauseCircle size={12} /> To'xtatilgan</span>;
      case 'completed':
        return <span className="badge badge-finished" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}><CheckCircle size={12} /> Ishchi topildi</span>;
      case 'cancelled':
        return <span className="badge badge-cancelled" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}><XCircle size={12} /> Bekor qilingan</span>;
      default:
        return <span className="badge badge-pending">{status}</span>;
    }
  };

  return (
    <div className="section-container" style={{ padding: '1.25rem' }}>
      {/* Header & Filter Toolbar */}
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: '16px',
        padding: '1.2rem',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--card-shadow)',
        marginBottom: '1.25rem'
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, margin: 0, display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-main)' }}>
              <Briefcase size={22} color="var(--primary)" /> Ish E'lonlari Boshqaruvi
            </h2>
            <p style={{ margin: '4px 0 0 0', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Barcha joylangan vakansiyalar, buyurtmalar va kelib tushgan takliflarni real-vaqtda boshqarish
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.6rem' }}>
            <button 
              className="btn btn-secondary" 
              onClick={loadJobPosts}
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', padding: '0.5rem 0.9rem', borderRadius: '10px' }}
            >
              <Clock size={15} /> Yangilash
            </button>
          </div>
        </div>

        {/* Filters Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '0.75rem',
          alignItems: 'center'
        }}>
          {/* Search Box */}
          <div style={{ position: 'relative', gridColumn: 'span 1' }}>
            <Search size={15} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              type="text"
              className="input-field"
              placeholder="Qidiruv (nomi, tel, manzil)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: '36px', height: '40px', borderRadius: '10px', fontSize: '0.85rem', width: '100%' }}
            />
          </div>

          {/* Status Filter */}
          <select
            className="input-field"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ height: '40px', borderRadius: '10px', fontSize: '0.85rem', width: '100%' }}
          >
            <option value="">🔘 Barcha Holatlar</option>
            <option value="active">🟢 Faol / Qidirilmoqda</option>
            <option value="paused">⏸ Vaqtincha to'xtatilgan</option>
            <option value="completed">✅ Ishchi topildi / Yopilgan</option>
            <option value="cancelled">❌ Bekor qilingan</option>
          </select>

          {/* Employment Type Filter */}
          <select
            className="input-field"
            value={empTypeFilter}
            onChange={(e) => setEmpTypeFilter(e.target.value)}
            style={{ height: '40px', borderRadius: '10px', fontSize: '0.85rem', width: '100%' }}
          >
            <option value="">⚡️ Barcha Bandlik turlari</option>
            <option value="daily">⚡️ Kunbay / Bir martalik</option>
            <option value="permanent">💼 Doimiy ish (oylik)</option>
          </select>

          {/* Category Filter */}
          <select
            className="input-field"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            style={{ height: '40px', borderRadius: '10px', fontSize: '0.85rem', width: '100%' }}
          >
            <option value="">📁 Barcha Sohalar</option>
            {categories && categories.map(c => (
              <option key={c.id} value={c.id}>{c.name_uz || c.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Stats Quick Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '0.9rem', marginBottom: '1.25rem' }}>
        <div style={{
          background: 'var(--bg-card)',
          padding: '1.1rem',
          borderRadius: '14px',
          border: '1px solid var(--border-color)',
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(59, 130, 246, 0.12)', color: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Briefcase size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Jami E'lonlar</div>
            <div style={{ fontSize: '1.35rem', fontWeight: 800, color: 'var(--text-main)', marginTop: '2px' }}>{jobPosts.length} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-muted)' }}>ta</span></div>
          </div>
        </div>

        <div style={{
          background: 'var(--bg-card)',
          padding: '1.1rem',
          borderRadius: '14px',
          border: '1px solid var(--border-color)',
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(16, 185, 129, 0.12)', color: '#10b981', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <PlayCircle size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Faol E'lonlar</div>
            <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#10b981', marginTop: '2px' }}>
              {jobPosts.filter(j => j.status === 'active').length} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-muted)' }}>ta</span>
            </div>
          </div>
        </div>

        <div style={{
          background: 'var(--bg-card)',
          padding: '1.1rem',
          borderRadius: '14px',
          border: '1px solid var(--border-color)',
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(245, 158, 11, 0.12)', color: '#f59e0b', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Users size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Otkliklar</div>
            <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#f59e0b', marginTop: '2px' }}>
              {jobPosts.reduce((acc, j) => acc + (j.applications_count || (j.applications ? j.applications.length : 0)), 0)} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-muted)' }}>ta</span>
            </div>
          </div>
        </div>

        <div style={{
          background: 'var(--bg-card)',
          padding: '1.1rem',
          borderRadius: '14px',
          border: '1px solid var(--border-color)',
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(139, 92, 246, 0.12)', color: '#8b5cf6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CheckCircle size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Bajarilgan / Yopilgan</div>
            <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#8b5cf6', marginTop: '2px' }}>
              {jobPosts.filter(j => j.status === 'completed').length} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-muted)' }}>ta</span>
            </div>
          </div>
        </div>
      </div>

      {/* Job Posts Table Container */}
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: '16px',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--card-shadow)',
        overflow: 'hidden'
      }}>
        <div style={{ overflowX: 'auto', width: '100%' }}>
          <table className="custom-table" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: '850px' }}>
            <thead>
              <tr style={{ background: 'var(--bg-inner)', borderBottom: '1px solid var(--border-color)' }}>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)' }}>#ID & Lavozim</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)' }}>Ish Beruvchi</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)' }}>Manzil & Vaqt</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)' }}>To'lov & Talab</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)', textAlign: 'center' }}>Otkliklar</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)', textAlign: 'center' }}>Holat</th>
                <th style={{ padding: '0.9rem 1.1rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.5px', color: 'var(--text-muted)', textAlign: 'right' }}>Amallar</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 5 }).map((_, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: '1rem 1.1rem' }}>
                      <div className="skeleton skeleton-title" style={{ width: '70%', height: '16px', borderRadius: '4px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '45%', height: '12px', marginTop: '6px', borderRadius: '4px' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem' }}>
                      <div className="skeleton skeleton-text" style={{ width: '80%', height: '14px', borderRadius: '4px' }} />
                      <div className="skeleton skeleton-text" style={{ width: '60%', height: '12px', marginTop: '4px', borderRadius: '4px' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem' }}>
                      <div className="skeleton skeleton-text" style={{ width: '90%', height: '14px', borderRadius: '4px' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem' }}>
                      <div className="skeleton skeleton-text" style={{ width: '75%', height: '14px', borderRadius: '4px' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem', textAlign: 'center' }}>
                      <div className="skeleton" style={{ width: '45px', height: '22px', borderRadius: '12px', margin: '0 auto' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem', textAlign: 'center' }}>
                      <div className="skeleton" style={{ width: '75px', height: '24px', borderRadius: '12px', margin: '0 auto' }} />
                    </td>
                    <td style={{ padding: '1rem 1.1rem', textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '6px' }}>
                        <div className="skeleton" style={{ width: '32px', height: '32px', borderRadius: '8px' }} />
                        <div className="skeleton" style={{ width: '32px', height: '32px', borderRadius: '8px' }} />
                      </div>
                    </td>
                  </tr>
                ))
              ) : jobPosts.length === 0 ? (
                <tr>
                  <td colSpan="7" style={{ textAlign: 'center', padding: '3rem 1.5rem', color: 'var(--text-muted)' }}>
                    <Briefcase size={36} style={{ opacity: 0.3, marginBottom: '0.5rem' }} />
                    <div style={{ fontSize: '0.95rem', fontWeight: 600 }}>Hech qanday e'lon topilmadi</div>
                    <div style={{ fontSize: '0.8rem', marginTop: '4px' }}>Qidiruv yoki filtrlarni o'zgartirib ko'ring</div>
                  </td>
                </tr>
              ) : (
                jobPosts.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((job) => {
                  const posName = job.position_detail ? job.position_detail.name_uz : (job.custom_position_name || 'Ish');
                  const catName = job.category_detail ? job.category_detail.name_uz : 'Boshqa';
                  const priceDisp = job.price_amount ? job.price_amount : 'Kelishilgan';

                  return (
                    <tr 
                      key={job.id} 
                      style={{ 
                        borderBottom: '1px solid var(--border-color)',
                        transition: 'background-color 0.15s ease'
                      }}
                      className="table-row-hover"
                    >
                      <td style={{ padding: '0.95rem 1.1rem' }}>
                        <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ color: 'var(--primary)', opacity: 0.8 }}>#{job.id}</span> {posName}
                        </div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '3px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span>{catName}</span>
                          <span>•</span>
                          <span style={{ 
                            background: job.employment_type === 'daily' ? 'rgba(59, 130, 246, 0.1)' : 'rgba(139, 92, 246, 0.1)',
                            color: job.employment_type === 'daily' ? 'var(--primary)' : '#8b5cf6',
                            padding: '1px 6px',
                            borderRadius: '4px',
                            fontWeight: 600
                          }}>
                            {job.employment_type === 'daily' ? '⚡️ Kunbay' : '💼 Doimiy'}
                          </span>
                        </div>
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem' }}>
                        <div style={{ fontWeight: 600, fontSize: '0.88rem', color: 'var(--text-main)' }}>
                          {job.contact_name || (job.employer_detail && job.employer_detail.first_name) || 'Ish beruvchi'}
                        </div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '3px' }}>
                          <Phone size={12} color="var(--primary)" /> {job.contact_phone || (job.employer_detail && job.employer_detail.phone_number) || '—'}
                        </div>
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem' }}>
                        <div style={{ fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-main)' }}>
                          <MapPin size={13} color="#f59e0b" />
                          <span>{job.region_detail ? job.region_detail.name_uz : ''} {job.district || ''}</span>
                        </div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '3px' }}>
                          <Clock size={12} />
                          <span>{job.start_time_type === 'urgent' ? '🔥 Shoshilinch' : (job.start_time_type === 'tomorrow' ? 'Ertaga' : job.custom_start_date || 'Kelishilgan')}</span>
                        </div>
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem' }}>
                        <div style={{ fontWeight: 700, color: '#10b981', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <DollarSign size={13} /> {priceDisp}
                        </div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '3px' }}>
                          👥 {job.workers_count || '1 nafar'} ({job.gender_requirement === 'male' ? 'Erkak' : (job.gender_requirement === 'female' ? 'Ayol' : 'Farqi yo\'q')})
                        </div>
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem', textAlign: 'center' }}>
                        <span 
                          className={`badge ${job.applications && job.applications.length > 0 ? 'badge-started' : 'badge-pending'}`}
                          style={{ 
                            cursor: 'pointer', 
                            padding: '0.35rem 0.65rem',
                            borderRadius: '20px',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '4px',
                            fontWeight: 600,
                            fontSize: '0.8rem'
                          }}
                          onClick={() => { setSelectedJob(job); setIsEditModalOpen(true); }}
                          title="Otkliklarni ko'rish va boshqarish"
                        >
                          <Users size={13} />
                          {job.applications ? job.applications.length : (job.applications_count || 0)} ta
                        </span>
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem', textAlign: 'center' }}>
                        {getStatusBadge(job.status)}
                      </td>

                      <td style={{ padding: '0.95rem 1.1rem', textAlign: 'right' }}>
                        <div style={{ display: 'inline-flex', gap: '0.4rem', justifyContent: 'flex-end', alignItems: 'center' }}>
                          {/* Ustaga Taklif Qilish Button */}
                          <button
                            className="btn btn-secondary"
                            style={{ 
                              padding: '0.4rem 0.65rem', 
                              fontSize: '0.8rem', 
                              color: '#8b5cf6', 
                              borderColor: 'rgba(139, 92, 246, 0.3)',
                              borderRadius: '8px',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '4px'
                            }}
                            onClick={() => handleOpenOfferModal(job)}
                            title="Ushbu ishni ustaga taklif qilish"
                          >
                            <Send size={13} /> Taklif
                          </button>

                          {/* Status Toggle Quick Buttons */}
                          {job.status === 'active' ? (
                            <button
                              className="btn btn-secondary"
                              style={{ padding: '0.4rem', color: '#f59e0b', borderRadius: '8px', display: 'inline-flex', alignItems: 'center' }}
                              onClick={() => handleStatusChange(job.id, 'paused')}
                              title="Vaqtincha to'xtatish"
                            >
                              <PauseCircle size={15} />
                            </button>
                          ) : (
                            <button
                              className="btn btn-secondary"
                              style={{ padding: '0.4rem', color: '#10b981', borderRadius: '8px', display: 'inline-flex', alignItems: 'center' }}
                              onClick={() => handleStatusChange(job.id, 'active')}
                              title="Faollashtirish"
                            >
                              <PlayCircle size={15} />
                            </button>
                          )}

                          <button
                            className="btn btn-secondary"
                            style={{ padding: '0.4rem', borderRadius: '8px', display: 'inline-flex', alignItems: 'center' }}
                            onClick={() => handleOpenEdit(job)}
                            title="Tahrirlash va Tafsilotlar"
                          >
                            <Edit3 size={15} />
                          </button>

                          <button
                            className="btn btn-secondary"
                            style={{ padding: '0.4rem', color: '#ef4444', borderRadius: '8px', display: 'inline-flex', alignItems: 'center' }}
                            onClick={() => handleDelete(job.id)}
                            title="O'chirish"
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        {jobPosts.length > pageSize && (
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', padding: '0.9rem 1.25rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)', gap: '0.8rem' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, jobPosts.length)}</b> / Jami: <b>{jobPosts.length}</b> ta
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <button
                className="btn btn-secondary"
                style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem', borderRadius: '8px' }}
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              >
                <ChevronLeft size={14} /> Oldingi
              </button>
              
              {Array.from({ length: Math.ceil(jobPosts.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(jobPosts.length / pageSize) || Math.abs(p - currentPage) <= 1)
                .map((p, idx, arr) => (
                  <React.Fragment key={p}>
                    {idx > 0 && arr[idx - 1] !== p - 1 && <span style={{ color: 'var(--text-muted)', padding: '0 4px' }}>...</span>}
                    <button
                      className={`btn ${currentPage === p ? '' : 'btn-secondary'}`}
                      style={{
                        padding: '0.4rem 0.75rem',
                        fontSize: '0.8rem',
                        borderRadius: '8px',
                        background: currentPage === p ? 'var(--primary)' : 'transparent',
                        borderColor: currentPage === p ? 'var(--primary)' : 'var(--border-color)',
                        color: currentPage === p ? '#fff' : 'var(--text-main)',
                        minWidth: '34px',
                        fontWeight: currentPage === p ? 700 : 500
                      }}
                      onClick={() => setCurrentPage(p)}
                    >
                      {p}
                    </button>
                  </React.Fragment>
                ))}

              <button
                className="btn btn-secondary"
                style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem', borderRadius: '8px' }}
                disabled={currentPage === Math.ceil(jobPosts.length / pageSize)}
                onClick={() => setCurrentPage(prev => Math.min(Math.ceil(jobPosts.length / pageSize), prev + 1))}
              >
                Keyingi <ChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* OFFER JOB TO WORKER MODAL */}
      {isOfferModalOpen && selectedJob && (
        <div className="modal-overlay" style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.65)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999, padding: '1rem' }}>
          <div style={{ background: 'var(--bg-card)', width: '100%', maxWidth: '520px', borderRadius: '18px', padding: '1.6rem', border: '1px solid var(--border-color)', boxShadow: '0 10px 40px rgba(0,0,0,0.5)', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800, margin: 0, display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-main)' }}>
                <Send size={18} color="#8b5cf6" /> Ustaga Ish Taklif Qilish
              </h3>
              <button className="btn btn-secondary" style={{ padding: '0.3rem 0.5rem', borderRadius: '8px' }} onClick={() => setIsOfferModalOpen(false)}>
                <X size={16} />
              </button>
            </div>

            <div style={{ padding: '1rem', backgroundColor: 'var(--bg-inner)', border: '1px solid var(--border-color)', borderRadius: '12px', marginBottom: '1.2rem', fontSize: '0.85rem' }}>
              <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)', marginBottom: '4px' }}>
                #{selectedJob.id} — {selectedJob.position_detail?.name_uz || selectedJob.custom_position_name || 'Ish'}
              </div>
              <div style={{ color: 'var(--text-muted)', display: 'flex', gap: '1rem', marginTop: '6px' }}>
                <span>📍 {selectedJob.district || ''} {selectedJob.address || ''}</span>
                <span>💰 {selectedJob.price_amount || 'Kelishilgan'}</span>
              </div>
            </div>

            {offerSuccessMsg ? (
              <div style={{ padding: '1.2rem', backgroundColor: 'rgba(16, 185, 129, 0.12)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#10b981', borderRadius: '12px', fontWeight: 600, textAlign: 'center' }}>
                {offerSuccessMsg}
              </div>
            ) : (
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.5rem', color: 'var(--text-main)' }}>
                  Online ustalardan birini tanlang:
                </label>
                <select
                  className="input-field"
                  value={selectedWorkerId}
                  onChange={(e) => setSelectedWorkerId(e.target.value)}
                  style={{ width: '100%', marginBottom: '1.25rem', height: '42px', borderRadius: '10px' }}
                >
                  <option value="">-- Ustani tanlang --</option>
                  {availableWorkers.map((w) => (
                    <option key={w.id} value={w.id}>
                      {w.first_name || w.username} ({w.specialty || w.district || 'Usta'}) • {w.phone_number || 'TG'} • ⭐ {w.rating || '5.0'}
                    </option>
                  ))}
                </select>

                <div style={{ display: 'flex', gap: '0.8rem', justifyContent: 'flex-end' }}>
                  <button className="btn btn-secondary" style={{ borderRadius: '10px', padding: '0.5rem 1rem' }} onClick={() => setIsOfferModalOpen(false)}>
                    Bekor qilish
                  </button>
                  <button
                    className="btn btn-primary"
                    disabled={!selectedWorkerId || offerLoading}
                    onClick={handleSendOffer}
                    style={{ backgroundColor: '#8b5cf6', borderColor: '#8b5cf6', borderRadius: '10px', padding: '0.5rem 1.2rem' }}
                  >
                    {offerLoading ? "Yuborilmoqda..." : "🚀 Botga Taklif Jo'natish"}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* EDIT / VIEW DETAILS & APPLICANTS MODAL */}
      {isEditModalOpen && selectedJob && (
        <div className="modal-overlay" style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.65)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999, padding: '1rem' }}>
          <div style={{ background: 'var(--bg-card)', width: '100%', maxWidth: '750px', borderRadius: '18px', padding: '1.6rem', border: '1px solid var(--border-color)', boxShadow: '0 10px 40px rgba(0,0,0,0.5)', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem', paddingBottom: '0.8rem', borderBottom: '1px solid var(--border-color)' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, margin: 0, color: 'var(--text-main)' }}>
                  E'lon #{selectedJob.id} — {selectedJob.position_detail?.name_uz || selectedJob.custom_position_name || 'Ish'}
                </h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                  Barcha murojaat qilgan ustalar ro'yxati va e'lon parametrlarini boshqarish
                </div>
              </div>
              <button className="btn btn-secondary" style={{ padding: '0.3rem 0.5rem', borderRadius: '8px' }} onClick={() => setIsEditModalOpen(false)}>
                <X size={16} />
              </button>
            </div>

            {/* Applications List */}
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.8rem', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Users size={16} /> Kelib Tushgan Otkliklar ({selectedJob.applications ? selectedJob.applications.length : 0} ta):
              </h4>
              {selectedJob.applications && selectedJob.applications.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {selectedJob.applications.map((app) => (
                    <div key={app.id} style={{ padding: '1rem', border: '1px solid var(--border-color)', borderRadius: '12px', backgroundColor: 'var(--bg-inner)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-main)' }}>
                          👤 {app.worker_detail?.first_name || app.worker_detail?.username || 'Usta'} 
                          <span style={{ fontSize: '0.82rem', color: 'var(--primary)', marginLeft: '10px', fontWeight: 500 }}>
                            📞 {app.worker_detail?.phone_number || 'Tel mavjud emas'}
                          </span>
                        </div>
                        <span className={`badge ${app.status === 'accepted' ? 'badge-finished' : (app.status === 'rejected' ? 'badge-cancelled' : 'badge-pending')}`}>
                          {app.status === 'accepted' ? '✅ Qabul qilingan' : (app.status === 'rejected' ? '❌ Rad etilgan' : '⏳ Kutilmoqda')}
                        </span>
                      </div>
                      {app.proposal_message && (
                        <div style={{ fontSize: '0.84rem', marginTop: '0.6rem', color: 'var(--text-secondary)', background: 'var(--bg-card)', padding: '0.6rem 0.8rem', borderRadius: '8px', borderLeft: '3px solid var(--primary)' }}>
                          💬 "{app.proposal_message}"
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '1rem', textAlign: 'center', background: 'var(--bg-inner)', borderRadius: '10px', border: '1px solid var(--border-color)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  Hozircha hech qanday usta ushbu ishga otklik yubormagan.
                </div>
              )}
            </div>

            {/* Edit Form */}
            <form onSubmit={handleSaveEdit}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.8rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Edit3 size={16} /> E'lon Ma'lumotlarini Tahrirlash:
              </h4>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.85rem', marginBottom: '0.85rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>Aloqa Ismi:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.contact_name}
                    onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
                    style={{ borderRadius: '8px' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>Aloqa Telefoni:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.contact_phone}
                    onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                    style={{ borderRadius: '8px' }}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.85rem', marginBottom: '0.85rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>To'lov Summasi:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.price_amount}
                    onChange={(e) => setFormData({ ...formData, price_amount: e.target.value })}
                    placeholder="Masalan: 250 000 so'm"
                    style={{ borderRadius: '8px' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>Holati:</label>
                  <select
                    className="input-field"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    style={{ borderRadius: '8px' }}
                  >
                    <option value="active">🟢 Faol / Qidirilmoqda</option>
                    <option value="paused">⏸ Vaqtincha to'xtatilgan</option>
                    <option value="completed">✅ Ishchi topildi / Yopilgan</option>
                    <option value="cancelled">❌ Bekor qilingan</option>
                  </select>
                </div>
              </div>

              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>Manzil / Mo'ljal:</label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  style={{ borderRadius: '8px' }}
                />
              </div>

              <div style={{ marginBottom: '1.2rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.3rem', color: 'var(--text-muted)' }}>Ish Tavsifi:</label>
                <textarea
                  className="input-field"
                  rows="3"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  style={{ borderRadius: '8px' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.8rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" style={{ borderRadius: '10px', padding: '0.5rem 1rem' }} onClick={() => setIsEditModalOpen(false)}>
                  Bekor qilish
                </button>
                <button type="submit" className="btn btn-primary" style={{ borderRadius: '10px', padding: '0.5rem 1.25rem' }}>
                  💾 Saqlash
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

