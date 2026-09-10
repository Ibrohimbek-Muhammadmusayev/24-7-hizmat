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
    <div className="section-container" style={{ padding: '1.2rem' }}>
      {/* Top Filter Bar */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.8rem', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.6rem', alignItems: 'center', flex: 1 }}>
          <div style={{ position: 'relative', minWidth: '220px' }}>
            <Search size={16} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              className="input-field"
              placeholder="E'lon, usta, manzil yoki tel..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: '32px' }}
            />
          </div>

          <select
            className="input-field"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ width: 'auto', minWidth: '150px' }}
          >
            <option value="">Barcha Statuslar</option>
            <option value="active">🟢 Faol / Qidirilmoqda</option>
            <option value="paused">⏸ Vaqtincha to'xtatilgan</option>
            <option value="completed">✅ Ishchi topildi / Yopilgan</option>
            <option value="cancelled">❌ Bekor qilingan</option>
          </select>

          <select
            className="input-field"
            value={empTypeFilter}
            onChange={(e) => setEmpTypeFilter(e.target.value)}
            style={{ width: 'auto', minWidth: '150px' }}
          >
            <option value="">Barcha Bandlik turi</option>
            <option value="daily">⚡️ Kunbay / Bir martalik</option>
            <option value="permanent">💼 Doimiy ish (oylik)</option>
          </select>

          <select
            className="input-field"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            style={{ width: 'auto', minWidth: '160px' }}
          >
            <option value="">Barcha Sohalar</option>
            {categories && categories.map(c => (
              <option key={c.id} value={c.id}>{c.name_uz || c.name}</option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', gap: '0.6rem' }}>
          <button className="btn btn-secondary" onClick={loadJobPosts}>
            🔄 Yangilash
          </button>
        </div>
      </div>

      {/* Stats Quick Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.8rem', marginBottom: '1.2rem' }}>
        <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #3b82f6' }}>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>Jami E'lonlar</div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, marginTop: '0.2rem' }}>{jobPosts.length} ta</div>
        </div>
        <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #10b981' }}>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>Faol / Qidirilmoqda</div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981', marginTop: '0.2rem' }}>
            {jobPosts.filter(j => j.status === 'active').length} ta
          </div>
        </div>
        <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #f59e0b' }}>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>Jami Otkliklar (Murojaatlar)</div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f59e0b', marginTop: '0.2rem' }}>
            {jobPosts.reduce((acc, j) => acc + (j.applications_count || (j.applications ? j.applications.length : 0)), 0)} ta
          </div>
        </div>
        <div className="card" style={{ padding: '1rem', borderLeft: '4px solid #8b5cf6' }}>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>Ishchi Biriktirilgan</div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#8b5cf6', marginTop: '0.2rem' }}>
            {jobPosts.filter(j => j.status === 'completed').length} ta
          </div>
        </div>
      </div>

      {/* Job Posts Table / Cards */}
      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table className="custom-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'left' }}>#ID & Lavozim</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'left' }}>Ish Beruvchi</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'left' }}>Manzil & Vaqt</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'left' }}>To'lov & Talab</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>Otkliklar</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>Holat</th>
              <th style={{ padding: '0.8rem 1rem', textAlign: 'right' }}>Amallar</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array.from({ length: 6 }).map((_, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '0.8rem 1rem' }}>
                    <div className="skeleton skeleton-title" style={{ width: '70%', height: '16px' }} />
                    <div className="skeleton skeleton-text" style={{ width: '45%', height: '12px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem' }}>
                    <div className="skeleton skeleton-text" style={{ width: '80%', height: '14px', marginBottom: '4px' }} />
                    <div className="skeleton skeleton-text" style={{ width: '60%', height: '12px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem' }}>
                    <div className="skeleton skeleton-text" style={{ width: '90%', height: '14px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem' }}>
                    <div className="skeleton skeleton-text" style={{ width: '75%', height: '14px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>
                    <div className="skeleton" style={{ width: '45px', height: '20px', borderRadius: '12px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>
                    <div className="skeleton" style={{ width: '70px', height: '22px', borderRadius: '12px' }} />
                  </td>
                  <td style={{ padding: '0.8rem 1rem', textAlign: 'right' }}>
                    <div style={{ display: 'inline-flex', gap: '4px' }}>
                      <div className="skeleton" style={{ width: '28px', height: '28px', borderRadius: '6px' }} />
                      <div className="skeleton" style={{ width: '28px', height: '28px', borderRadius: '6px' }} />
                    </div>
                  </td>
                </tr>
              ))
            ) : jobPosts.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                  E'lonlar topilmadi.
                </td>
              </tr>
            ) : (
              jobPosts.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((job) => {
                const posName = job.position_detail ? job.position_detail.name_uz : (job.custom_position_name || 'Ish');
                const catName = job.category_detail ? job.category_detail.name_uz : 'Boshqa';
                const priceDisp = job.price_amount ? job.price_amount : 'Kelishilgan';

                return (
                  <tr key={job.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: '0.8rem 1rem' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)' }}>
                        #{job.id}: {posName}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {catName} • {job.employment_type === 'daily' ? '⚡️ Kunbay' : '💼 Doimiy'}
                      </div>
                    </td>

                    <td style={{ padding: '0.8rem 1rem' }}>
                      <div style={{ fontWeight: 600, fontSize: '0.88rem' }}>
                        {job.contact_name || (job.employer_detail && job.employer_detail.first_name) || 'Ish beruvchi'}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#3b82f6', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Phone size={12} /> {job.contact_phone || (job.employer_detail && job.employer_detail.phone_number) || '—'}
                      </div>
                    </td>

                    <td style={{ padding: '0.8rem 1rem' }}>
                      <div style={{ fontSize: '0.85rem' }}>
                        <MapPin size={12} style={{ display: 'inline', marginRight: '3px' }} />
                        {job.region_detail ? job.region_detail.name_uz : ''} {job.district || ''}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        <Clock size={11} style={{ display: 'inline', marginRight: '3px' }} />
                        {job.start_time_type === 'urgent' ? '🔥 Shoshilinch (Bugun)' : (job.start_time_type === 'tomorrow' ? 'Ertaga' : job.custom_start_date || 'Kelishilgan')}
                      </div>
                    </td>

                    <td style={{ padding: '0.8rem 1rem' }}>
                      <div style={{ fontWeight: 700, color: '#10b981', fontSize: '0.88rem' }}>
                        💰 {priceDisp}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        👥 {job.workers_count || '1 nafar'} ({job.gender_requirement === 'male' ? 'Erkak' : (job.gender_requirement === 'female' ? 'Ayol' : 'Farqi yo\'q')})
                      </div>
                    </td>

                    <td style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>
                      <span 
                        className={`badge ${job.applications && job.applications.length > 0 ? 'badge-started' : 'badge-pending'}`}
                        style={{ cursor: 'pointer', padding: '0.3rem 0.6rem' }}
                        onClick={() => { setSelectedJob(job); setIsEditModalOpen(true); }}
                        title="Otkliklarni ko'rish"
                      >
                        <Users size={12} style={{ marginRight: '3px' }} />
                        {job.applications ? job.applications.length : (job.applications_count || 0)} ta
                      </span>
                    </td>

                    <td style={{ padding: '0.8rem 1rem', textAlign: 'center' }}>
                      {getStatusBadge(job.status)}
                    </td>

                    <td style={{ padding: '0.8rem 1rem', textAlign: 'right' }}>
                      <div style={{ display: 'flex', gap: '0.4rem', justifyContent: 'flex-end' }}>
                        {/* Ustaga Taklif Qilish Button */}
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.35rem 0.6rem', fontSize: '0.78rem', color: '#8b5cf6', borderColor: 'rgba(139, 92, 246, 0.3)' }}
                          onClick={() => handleOpenOfferModal(job)}
                          title="Ushbu ishni ustaga taklif qilish"
                        >
                          <Send size={13} style={{ marginRight: '3px' }} /> Taklif
                        </button>

                        {/* Status Toggle Quick Buttons */}
                        {job.status === 'active' ? (
                          <button
                            className="btn btn-secondary"
                            style={{ padding: '0.35rem 0.5rem', color: '#f59e0b' }}
                            onClick={() => handleStatusChange(job.id, 'paused')}
                            title="Vaqtincha to'xtatish"
                          >
                            <PauseCircle size={14} />
                          </button>
                        ) : (
                          <button
                            className="btn btn-secondary"
                            style={{ padding: '0.35rem 0.5rem', color: '#10b981' }}
                            onClick={() => handleStatusChange(job.id, 'active')}
                            title="Faollashtirish"
                          >
                            <PlayCircle size={14} />
                          </button>
                        )}

                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.35rem 0.5rem' }}
                          onClick={() => handleOpenEdit(job)}
                          title="Tahrirlash va ko'rish"
                        >
                          <Edit3 size={14} />
                        </button>

                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.35rem 0.5rem', color: '#ef4444' }}
                          onClick={() => handleDelete(job.id)}
                          title="O'chirish"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>

        {/* Pagination Bar */}
        {jobPosts.length > pageSize && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1.2rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-inner)' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Ko'rsatilmoqda: <b>{(currentPage - 1) * pageSize + 1} - {Math.min(currentPage * pageSize, jobPosts.length)}</b> / Jami: <b>{jobPosts.length}</b> ta
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
              
              {Array.from({ length: Math.ceil(jobPosts.length / pageSize) }, (_, idx) => idx + 1)
                .filter(p => p === 1 || p === Math.ceil(jobPosts.length / pageSize) || Math.abs(p - currentPage) <= 1)
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
        <div className="modal-overlay" style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div className="card" style={{ width: '100%', maxWidth: '500px', padding: '1.5rem', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Send size={18} color="#8b5cf6" /> Ustaga Ish Taklif Qilish
              </h3>
              <button className="btn btn-secondary" style={{ padding: '0.2rem 0.4rem' }} onClick={() => setIsOfferModalOpen(false)}>
                <X size={16} />
              </button>
            </div>

            <div style={{ padding: '0.8rem', backgroundColor: 'var(--bg-secondary)', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.85rem' }}>
              <div>📢 <b>E'lon:</b> #{selectedJob.id} — {selectedJob.position_detail?.name_uz || selectedJob.custom_position_name || 'Ish'}</div>
              <div>📍 <b>Manzil:</b> {selectedJob.district || ''} {selectedJob.address || ''}</div>
              <div>💰 <b>Haq:</b> {selectedJob.price_amount || 'Kelishilgan'}</div>
            </div>

            {offerSuccessMsg ? (
              <div style={{ padding: '1rem', backgroundColor: 'rgba(16, 185, 129, 0.15)', color: '#10b981', borderRadius: '8px', fontWeight: 600, textAlign: 'center' }}>
                {offerSuccessMsg}
              </div>
            ) : (
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                  Kerakli Ustani Tanlang (Online Ustalar):
                </label>
                <select
                  className="input-field"
                  value={selectedWorkerId}
                  onChange={(e) => setSelectedWorkerId(e.target.value)}
                  style={{ width: '100%', marginBottom: '1.2rem' }}
                >
                  <option value="">-- Ustani tanlang --</option>
                  {availableWorkers.map((w) => (
                    <option key={w.id} value={w.id}>
                      {w.first_name || w.username} ({w.specialty || w.district || 'Usta'}) • {w.phone_number || 'TG'} • {w.rating}⭐️
                    </option>
                  ))}
                </select>

                <div style={{ display: 'flex', gap: '0.8rem', justifyContent: 'flex-end' }}>
                  <button className="btn btn-secondary" onClick={() => setIsOfferModalOpen(false)}>
                    Bekor qilish
                  </button>
                  <button
                    className="btn btn-primary"
                    disabled={!selectedWorkerId || offerLoading}
                    onClick={handleSendOffer}
                    style={{ backgroundColor: '#8b5cf6', borderColor: '#8b5cf6' }}
                  >
                    {offerLoading ? "Yuborilmoqda..." : "🚀 Taklifni Botga Jo'natish"}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* EDIT / VIEW DETAILS & APPLICANTS MODAL */}
      {isEditModalOpen && selectedJob && (
        <div className="modal-overlay" style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999 }}>
          <div className="card" style={{ width: '100%', maxWidth: '750px', padding: '1.5rem', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 800, margin: 0 }}>
                E'lon #{selectedJob.id} — Tafsilotlar & Otkliklar
              </h3>
              <button className="btn btn-secondary" style={{ padding: '0.2rem 0.4rem' }} onClick={() => setIsEditModalOpen(false)}>
                <X size={16} />
              </button>
            </div>

            {/* Applications List */}
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.6rem', color: '#3b82f6' }}>
                👥 Kelib Tushgan Otkliklar ({selectedJob.applications ? selectedJob.applications.length : 0} ta):
              </h4>
              {selectedJob.applications && selectedJob.applications.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                  {selectedJob.applications.map((app) => (
                    <div key={app.id} style={{ padding: '0.8rem', border: '1px solid var(--border-color)', borderRadius: '8px', backgroundColor: 'var(--bg-secondary)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>
                          👤 {app.worker_detail?.first_name || app.worker_detail?.username || 'Usta'} 
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginLeft: '8px' }}>
                            (Tel: {app.worker_detail?.phone_number || '—'})
                          </span>
                        </div>
                        <span className={`badge ${app.status === 'accepted' ? 'badge-finished' : (app.status === 'rejected' ? 'badge-cancelled' : 'badge-pending')}`}>
                          {app.status === 'accepted' ? '✅ Qabul qilingan' : (app.status === 'rejected' ? '❌ Rad etilgan' : '⏳ Kutilmoqda')}
                        </span>
                      </div>
                      {app.proposal_message && (
                        <div style={{ fontSize: '0.82rem', marginTop: '0.4rem', color: 'var(--text-main)', fontStyle: 'italic' }}>
                          💬 "{app.proposal_message}"
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Hozircha otkliklar mavjud emas.</div>
              )}
            </div>

            {/* Edit Form */}
            <form onSubmit={handleSaveEdit}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.6rem' }}>
                ✏️ E'lon Ma'lumotlarini Tahrirlash:
              </h4>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', marginBottom: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Aloqa Ismi:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.contact_name}
                    onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Aloqa Telefoni:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.contact_phone}
                    onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', marginBottom: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>To'lov Summasi:</label>
                  <input
                    type="text"
                    className="input-field"
                    value={formData.price_amount}
                    onChange={(e) => setFormData({ ...formData, price_amount: e.target.value })}
                    placeholder="Masalan: 250 000 so'm/kun"
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Holati:</label>
                  <select
                    className="input-field"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="active">🟢 Faol / Qidirilmoqda</option>
                    <option value="paused">⏸ Vaqtincha to'xtatilgan</option>
                    <option value="completed">✅ Ishchi topildi / Yopilgan</option>
                    <option value="cancelled">❌ Bekor qilingan</option>
                  </select>
                </div>
              </div>

              <div style={{ marginBottom: '0.8rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Manzil / Mo'ljal:</label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                />
              </div>

              <div style={{ marginBottom: '1.2rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Ish Tavsifi:</label>
                <textarea
                  className="input-field"
                  rows="3"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.8rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setIsEditModalOpen(false)}>
                  Bekor qilish
                </button>
                <button type="submit" className="btn btn-primary">
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
