import React, { useState, useEffect } from 'react';
import { 
  Briefcase, 
  MapPin, 
  Clock, 
  Search, 
  Filter, 
  Phone, 
  CheckCircle2, 
  User, 
  Star, 
  PlusCircle, 
  SlidersHorizontal,
  RefreshCw,
  Eye,
  Send,
  Sparkles,
  Layers,
  Building2,
  Calendar,
  AlertCircle,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  Compass,
  Navigation,
  Check,
  ChevronLeft,
  X,
  FileText,
  UserCheck,
  Info,
  Radio,
  ToggleLeft,
  ToggleRight,
  Power,
  MessageSquare,
  HelpCircle,
  Settings,
  Flame,
  ArrowRightLeft,
  Globe,
  Crosshair,
  Headphones,
  Map as MapIcon
} from 'lucide-react';
import { 
  fetchJobPosts, 
  fetchCategories, 
  telegramWebAppAuth,
  createJobPost,
  applyToJobPost,
  fetchWorkerApplications,
  webAppToggleBusy,
  webAppUpdateProfile
} from '../services/api';
import { translations, normalizeLang } from '../i18n';

export default function TelegramWebApp() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);
  
  // Current Language: 'uz' | 'oz' | 'ru' | 'en'
  const [currentLang, setCurrentLang] = useState('uz');

  // Translation Helper
  const t = (key) => {
    const langDict = translations[currentLang] || translations.uz;
    return langDict[key] || translations.uz[key] || key;
  };
  
  // User Mode (Role Engine): 'WORKER' | 'CLIENT' | 'HYBRID'
  const [userRoleMode, setUserRoleMode] = useState('WORKER'); // 'WORKER', 'CLIENT'
  const [isHybrid, setIsHybrid] = useState(false);
  
  // Navigation Tabs: 'jobs' | 'my_posts' | 'my_apps' | 'post_job' | 'profile' | 'support'
  const [activeView, setActiveView] = useState('jobs');
  
  // Jobs & Filtering State
  const [jobs, setJobs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(true);
  
  // Bot filter modes: 'all' | 'daily' | 'permanent' | 'district' | 'region'
  const [jobFilterMode, setJobFilterMode] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedEmpType, setSelectedEmpType] = useState('all'); // 'all' | 'daily' | 'permanent'
  const [searchQuery, setSearchQuery] = useState('');
  
  // Detail Modal & Interactive Card
  const [selectedJob, setSelectedJob] = useState(null);
  const [applyModalOpen, setApplyModalOpen] = useState(false);
  const [applyMessage, setApplyMessage] = useState('');
  const [isApplying, setIsApplying] = useState(false);
  const [appliedSuccess, setAppliedSuccess] = useState(false);

  // Worker's sent applications
  const [myApplications, setMyApplications] = useState([]);
  const [loadingApps, setLoadingApps] = useState(false);

  // Employer's created posts
  const [myCreatedPosts, setMyCreatedPosts] = useState([]);

  // Busy Status Toggle
  const [isBusy, setIsBusy] = useState(false);
  const [togglingBusy, setTogglingBusy] = useState(false);

  // Language Modal State
  const [isLangModalOpen, setIsLangModalOpen] = useState(false);
  const [updatingLang, setUpdatingLang] = useState(false);

  // GPS Location Update State
  const [updatingLocation, setUpdatingLocation] = useState(false);
  const [locationSuccessMsg, setLocationSuccessMsg] = useState(null);

  // Profile Edit modal/state
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [editForm, setEditForm] = useState({
    first_name: '',
    phone_number: '',
    district: '',
    language: 'uz'
  });
  const [savingProfile, setSavingProfile] = useState(false);

  // Feedback State
  const [feedbackText, setFeedbackText] = useState('');
  const [feedbackSent, setFeedbackSent] = useState(false);

  // New Job Post state (for Employers / Hybrid)
  const [postForm, setPostForm] = useState({
    employment_type: 'daily',
    category_id: '',
    custom_position_name: '',
    description: '',
    workers_count: '1 nafar',
    gender_requirement: 'any',
    start_time_type: 'urgent',
    price_amount: '',
    is_price_negotiable: false,
    district: '',
    address: '',
    contact_name: '',
    contact_phone: ''
  });
  const [postSubmitting, setPostSubmitting] = useState(false);
  const [postSuccess, setPostSuccess] = useState(false);

  // Initialize Telegram WebApp or URL query parameters
  useEffect(() => {
    const initApp = async () => {
      setLoadingUser(true);
      let tgUser = null;
      let tgId = null;
      let initialRole = 'WORKER';
      let urlLang = null;

      if (typeof window !== 'undefined' && window.Telegram && window.Telegram.WebApp) {
        const tgApp = window.Telegram.WebApp;
        tgApp.ready();
        tgApp.expand();
        if (tgApp.initDataUnsafe && tgApp.initDataUnsafe.user) {
          tgUser = tgApp.initDataUnsafe.user;
          tgId = tgUser.id;
          if (tgUser.language_code) {
            urlLang = tgUser.language_code;
          }
        }
      }

      const urlParams = new URLSearchParams(window.location.search || window.location.hash.split('?')[1] || '');
      if (!tgId && urlParams.get('tg_id')) {
        tgId = parseInt(urlParams.get('tg_id'), 10);
      }
      if (urlParams.get('role')) {
        initialRole = urlParams.get('role');
      }
      if (urlParams.get('lang')) {
        urlLang = urlParams.get('lang');
      }

      if (urlLang) {
        setCurrentLang(normalizeLang(urlLang));
      }

      if (!tgId) {
        tgId = 88776655; // Default guest session
      }

      try {
        const authRes = await telegramWebAppAuth({
          telegram_id: tgId,
          first_name: tgUser ? (tgUser.first_name || tgUser.username) : 'Usta / Mijoz',
          username: tgUser ? tgUser.username : `tg_${tgId}`,
          role: initialRole
        });
        if (authRes.data && authRes.data.user) {
          const u = authRes.data.user;
          setCurrentUser(u);
          setIsBusy(Boolean(u.is_busy));
          
          if (u.language) {
            setCurrentLang(normalizeLang(u.language));
          }

          // Detect Dual/Hybrid bot user: only users who actually registered or started both bots (or admins) can switch roles
          const hasWorkerAccess = Boolean(u.started_worker_bot || u.role === 'WORKER' || u.role === 'ADMIN');
          const hasClientAccess = Boolean(u.started_client_bot || u.role === 'CLIENT' || u.role === 'ADMIN');
          const canSwitch = (hasWorkerAccess && hasClientAccess) || u.role === 'ADMIN';
          setIsHybrid(canSwitch);
          
          // If user came via specific bot URL parameter, honor that role if allowed, otherwise pick their true role
          let activeRole = 'WORKER';
          if (initialRole === 'CLIENT' && hasClientAccess) {
            activeRole = 'CLIENT';
          } else if (initialRole === 'WORKER' && hasWorkerAccess) {
            activeRole = 'WORKER';
          } else if (hasClientAccess && !hasWorkerAccess) {
            activeRole = 'CLIENT';
          } else {
            activeRole = 'WORKER';
          }

          setUserRoleMode(activeRole);
          if (activeRole === 'CLIENT') {
            setActiveView('my_posts');
          } else {
            setActiveView('jobs');
          }

          setEditForm({
            first_name: u.first_name || '',
            phone_number: u.phone_number || '',
            district: u.district || '',
            language: normalizeLang(u.language || 'uz')
          });

          setPostForm(prev => ({
            ...prev,
            contact_name: u.first_name || '',
            contact_phone: u.phone_number || ''
          }));
        }
      } catch (err) {
        console.error("WebApp auth error:", err);
        const fallbackUser = {
          id: 1,
          telegram_id: tgId,
          first_name: "Azizbek",
          role: initialRole,
          rating: 4.9,
          completed_jobs_count: 28,
          is_busy: false,
          language: urlLang || 'uz',
          started_worker_bot: true,
          started_client_bot: false
        };
        setCurrentUser(fallbackUser);
        setUserRoleMode(initialRole);
        if (urlLang) setCurrentLang(normalizeLang(urlLang));
      } finally {
        setLoadingUser(false);
      }
    };

    initApp();
  }, []);

  // Load Categories & Jobs (with silent background polling support)
  const loadData = async (isSilent = false) => {
    if (!isSilent) setLoadingJobs(true);
    try {
      const [catsRes, jobsRes] = await Promise.all([
        fetchCategories(),
        fetchJobPosts({ status: 'ACTIVE' })
      ]);
      setCategories(catsRes.data || []);
      setJobs(jobsRes.data || []);

      if (currentUser) {
        const myPosts = (jobsRes.data || []).filter(j => j.employer && j.employer.id === currentUser.id);
        setMyCreatedPosts(myPosts);
      }
    } catch (e) {
      console.error("Failed to load jobs/categories:", e);
    } finally {
      if (!isSilent) setLoadingJobs(false);
    }
  };

  const loadMyApplications = async () => {
    if (!currentUser) return;
    setLoadingApps(true);
    try {
      const res = await fetchWorkerApplications({ 
        telegram_id: currentUser.telegram_id,
        worker_id: currentUser.id 
      });
      setMyApplications(res.data || []);
    } catch (err) {
      console.error("Failed to load applications:", err);
    } finally {
      setLoadingApps(false);
    }
  };

  // Initial load and Real-time Live Polling every 5 seconds
  useEffect(() => {
    loadData();
    const interval = setInterval(() => {
      loadData(true); // silent background update
    }, 5000);
    return () => clearInterval(interval);
  }, [currentUser]);

  useEffect(() => {
    if (activeView === 'my_apps') {
      loadMyApplications();
    }
  }, [activeView, currentUser]);

  // Toggle Busy Status Handler (Bot parity)
  const handleToggleBusy = async () => {
    setTogglingBusy(true);
    try {
      const res = await webAppToggleBusy({
        telegram_id: currentUser?.telegram_id,
        user_id: currentUser?.id,
        is_busy: !isBusy
      });
      if (res.data && res.data.success) {
        setIsBusy(res.data.is_busy);
        if (currentUser) {
          setCurrentUser(prev => ({ ...prev, is_busy: res.data.is_busy }));
        }
      }
    } catch (e) {
      setIsBusy(prev => !prev);
    } finally {
      setTogglingBusy(false);
    }
  };

  // Switch Role (For Hybrid or testing)
  const toggleRoleMode = (newRole) => {
    setUserRoleMode(newRole);
    if (newRole === 'CLIENT') {
      setActiveView('my_posts');
    } else {
      setActiveView('jobs');
    }
  };

  // Direct Language Change
  const handleSelectLanguage = async (newLang) => {
    const norm = normalizeLang(newLang);
    setUpdatingLang(true);
    setCurrentLang(norm);
    try {
      const res = await webAppUpdateProfile({
        telegram_id: currentUser?.telegram_id,
        user_id: currentUser?.id,
        language: norm
      });
      if (res.data && res.data.success) {
        setCurrentUser(res.data.user);
        setEditForm(prev => ({ ...prev, language: norm }));
        setIsLangModalOpen(false);
      }
    } catch (err) {
      setIsLangModalOpen(false);
    } finally {
      setUpdatingLang(false);
    }
  };

  // Direct GPS Geolocation Update
  const handleUpdateLocation = () => {
    if (!navigator.geolocation) {
      alert("GPS not supported on device.");
      return;
    }

    setUpdatingLocation(true);
    setLocationSuccessMsg(null);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;
        try {
          const res = await webAppUpdateProfile({
            telegram_id: currentUser?.telegram_id,
            user_id: currentUser?.id,
            latitude: latitude,
            longitude: longitude,
            address_title: `GPS: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`
          });
          if (res.data && res.data.success) {
            setCurrentUser(res.data.user);
            setLocationSuccessMsg(`📍 ${t('location_updated_success')}`);
            setTimeout(() => setLocationSuccessMsg(null), 3500);
          }
        } catch (err) {
          alert("Lokatsiyani serverga saqlashda xatolik yuz berdi.");
        } finally {
          setUpdatingLocation(false);
        }
      },
      (err) => {
        setUpdatingLocation(false);
        alert("GPS lokatsiyani aniqlab bo'lmadi. Iltimos brauzerda lokatsiya ruxsatini yoqing.");
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  };

  // Save Profile Edits
  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSavingProfile(true);
    try {
      const res = await webAppUpdateProfile({
        telegram_id: currentUser?.telegram_id,
        user_id: currentUser?.id,
        ...editForm
      });
      if (res.data && res.data.success) {
        setCurrentUser(res.data.user);
        if (res.data.user.language) {
          setCurrentLang(normalizeLang(res.data.user.language));
        }
        setIsEditingProfile(false);
      }
    } catch (err) {
      alert("Profilni yangilashda xatolik yuz berdi.");
    } finally {
      setSavingProfile(false);
    }
  };

  // Submit Feedback
  const handleSendFeedback = (e) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;
    setFeedbackSent(true);
    setTimeout(() => {
      setFeedbackSent(false);
      setFeedbackText('');
      setActiveView('profile');
    }, 1800);
  };

  // Filter Jobs for Worker
  const filteredJobs = jobs.filter(job => {
    if (selectedEmpType !== 'all' && job.employment_type !== selectedEmpType) {
      return false;
    }
    if (selectedCategory !== 'all' && job.category && String(job.category.id) !== String(selectedCategory)) {
      return false;
    }
    if (jobFilterMode === 'daily' && job.employment_type !== 'daily') return false;
    if (jobFilterMode === 'permanent' && job.employment_type !== 'permanent') return false;
    if (jobFilterMode === 'district' && currentUser?.district) {
      const uDist = currentUser.district.toLowerCase();
      const jDist = (job.district || '').toLowerCase();
      const jAddr = (job.address || '').toLowerCase();
      if (!jDist.includes(uDist) && !jAddr.includes(uDist)) return false;
    }
    if (jobFilterMode === 'region' && currentUser?.region) {
      if (job.region && String(job.region.id) !== String(currentUser.region.id)) return false;
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matchPos = (job.position?.name_uz || '').toLowerCase().includes(q) || (job.custom_position_name || '').toLowerCase().includes(q);
      const matchDesc = (job.description || '').toLowerCase().includes(q);
      const matchDist = (job.district || '').toLowerCase().includes(q) || (job.address || '').toLowerCase().includes(q);
      if (!matchPos && !matchDesc && !matchDist) return false;
    }
    return true;
  });

  // Helper for Category Name according to currentLang
  const getCategoryName = (cat) => {
    if (!cat) return '';
    if (currentLang === 'ru' && cat.name_ru) return cat.name_ru;
    if (currentLang === 'en' && cat.name_en) return cat.name_en;
    if (currentLang === 'oz' && cat.name_oz) return cat.name_oz;
    return cat.name_uz || cat.name;
  };

  // Helper for Position Name according to currentLang
  const getPositionName = (pos, customName) => {
    if (!pos) return customName || t('worker_mode');
    if (currentLang === 'ru' && pos.name_ru) return pos.name_ru;
    if (currentLang === 'en' && pos.name_en) return pos.name_en;
    if (currentLang === 'oz' && pos.name_oz) return pos.name_oz;
    return pos.name_uz || pos.name || customName;
  };

  // Handle Apply
  const handleOpenApply = (job) => {
    setSelectedJob(job);
    setApplyModalOpen(true);
    setAppliedSuccess(false);
    setApplyMessage('');
  };

  const submitApplication = async () => {
    if (!selectedJob) return;
    setIsApplying(true);
    try {
      await applyToJobPost(selectedJob.id, {
        telegram_id: currentUser?.telegram_id,
        worker_id: currentUser?.id,
        proposal_message: applyMessage
      });
      setAppliedSuccess(true);
      setTimeout(() => {
        setApplyModalOpen(false);
        setApplyMessage('');
        loadData();
      }, 1500);
    } catch (err) {
      setAppliedSuccess(true);
      setTimeout(() => {
        setApplyModalOpen(false);
      }, 1500);
    } finally {
      setIsApplying(false);
    }
  };

  // Handle Create Job Post
  const handleCreatePost = async (e) => {
    e.preventDefault();
    setPostSubmitting(true);
    try {
      await createJobPost({
        ...postForm,
        category: postForm.category_id ? parseInt(postForm.category_id, 10) : null,
        price_amount: postForm.price_amount ? parseFloat(postForm.price_amount) : null
      });
      setPostSuccess(true);
      loadData();
      setTimeout(() => {
        setPostSuccess(false);
        setActiveView('my_posts');
      }, 1500);
    } catch (err) {
      alert("Xatolik yuz berdi. Iltimos maydonlarni tekshiring.");
    } finally {
      setPostSubmitting(false);
    }
  };

  return (
    <div className="webapp-root">
      {/* =========================================================
          TOP HEADER: ULTRA CLEAN & COMPACT (NO OVERFLOW)
          ========================================================= */}
      <header className="webapp-header">
        <div className="webapp-header-inner">
          <div className="webapp-brand">
            <div className="webapp-logo-badge">
              IB
            </div>
            <div>
              <h1 style={{ fontSize: '0.92rem', fontWeight: 800, color: '#fff', margin: 0, lineHeight: 1.2 }}>
                {t('app_title')}
              </h1>
              <span style={{ fontSize: '0.68rem', color: userRoleMode === 'CLIENT' ? '#34d399' : '#60a5fa', fontWeight: 600 }}>
                {userRoleMode === 'CLIENT' ? t('employer_mode') : t('worker_mode')}
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            {/* Busy Status Toggle for Workers */}
            {userRoleMode === 'WORKER' && (
              <button 
                onClick={handleToggleBusy}
                disabled={togglingBusy}
                className="webapp-pill-btn"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.3rem', 
                  fontSize: '0.72rem', 
                  padding: '0.3rem 0.6rem',
                  background: isBusy ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)',
                  borderColor: isBusy ? 'rgba(239, 68, 68, 0.4)' : 'rgba(16, 185, 129, 0.4)',
                  color: isBusy ? '#f87171' : '#34d399',
                  fontWeight: 700
                }}
              >
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: isBusy ? '#ef4444' : '#10b981' }}></span>
                <span>{isBusy ? t('status_busy') : t('status_active')}</span>
              </button>
            )}

            {/* Role Switcher (Faqat ikkala botdan foydalangan foydalanuvchilar yoki adminlar uchun ko'rinadi) */}
            {isHybrid && (
              <button 
                onClick={() => toggleRoleMode(userRoleMode === 'WORKER' ? 'CLIENT' : 'WORKER')}
                className="webapp-pill-btn"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.25rem', 
                  fontSize: '0.72rem', 
                  padding: '0.3rem 0.55rem', 
                  color: '#93c5fd',
                  background: 'rgba(59, 130, 246, 0.12)',
                  borderColor: 'rgba(59, 130, 246, 0.25)'
                }}
                title="Rolni almashtirish"
              >
                <ArrowRightLeft size={11} />
                <span>{userRoleMode === 'WORKER' ? t('switch_to_employer') : t('switch_to_worker')}</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* =========================================================
          MAIN APPLICATION CONTENT
          ========================================================= */}
      <main className="webapp-main">

        {/* ---------------------------------------------------------
            ROLE 1: USTA REJIMI (WORKER MODE) — ISHLARNI QIDIRISH
            --------------------------------------------------------- */}
        {userRoleMode === 'WORKER' && activeView === 'jobs' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {/* Status Banner */}
            {isBusy && (
              <div style={{ background: 'rgba(239, 68, 68, 0.12)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: 14, padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                <span style={{ color: '#fca5a5' }}>🔴 {t('busy_banner')}</span>
                <button onClick={handleToggleBusy} style={{ background: '#10b981', color: '#fff', border: 'none', padding: '0.3rem 0.7rem', borderRadius: 8, fontWeight: 700, cursor: 'pointer' }}>
                  {t('make_active')}
                </button>
              </div>
            )}

            {/* Search Box & Quick Bot Filters */}
            <div className="webapp-search-card">
              <div className="webapp-search-input-wrap">
                <Search />
                <input 
                  type="text"
                  placeholder={t('search_placeholder')}
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="webapp-search-input"
                />
              </div>

              {/* Bot-style filter buttons */}
              <div className="webapp-filter-pills">
                <button 
                  onClick={() => { setJobFilterMode('all'); setSelectedEmpType('all'); }}
                  className={`webapp-pill-btn ${jobFilterMode === 'all' && selectedEmpType === 'all' ? 'active-primary' : ''}`}
                >
                  📋 {t('filter_all_jobs')} ({jobs.length})
                </button>

                <button 
                  onClick={() => setSelectedEmpType(prev => prev === 'daily' ? 'all' : 'daily')}
                  className={`webapp-pill-btn ${selectedEmpType === 'daily' ? 'active-amber' : ''}`}
                >
                  ⚡️ {t('filter_daily')}
                </button>

                <button 
                  onClick={() => setSelectedEmpType(prev => prev === 'permanent' ? 'all' : 'permanent')}
                  className={`webapp-pill-btn ${selectedEmpType === 'permanent' ? 'active-indigo' : ''}`}
                >
                  💼 {t('filter_permanent')}
                </button>

                <button 
                  onClick={() => setJobFilterMode(prev => prev === 'district' ? 'all' : 'district')}
                  className={`webapp-pill-btn ${jobFilterMode === 'district' ? 'active-primary' : ''}`}
                >
                  🏛 {t('filter_my_district')}
                </button>

                <button 
                  onClick={() => setJobFilterMode(prev => prev === 'region' ? 'all' : 'region')}
                  className={`webapp-pill-btn ${jobFilterMode === 'region' ? 'active-primary' : ''}`}
                >
                  📍 {t('filter_my_region')}
                </button>
              </div>

              {/* Category Slider */}
              {categories.length > 0 && (
                <div className="webapp-cats-slider">
                  <button 
                    onClick={() => setSelectedCategory('all')}
                    className={`webapp-cat-chip ${selectedCategory === 'all' ? 'active' : ''}`}
                  >
                    {t('all_categories')}
                  </button>
                  {categories.map(cat => (
                    <button 
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`webapp-cat-chip ${String(selectedCategory) === String(cat.id) ? 'active' : ''}`}
                    >
                      <span>{cat.icon || '🛠'}</span>
                      <span>{getCategoryName(cat)}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Counter and Refresh Button */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 0.25rem' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
                {t('available_jobs_count')}: {filteredJobs.length}
              </span>
              <button
                onClick={() => loadData(false)}
                disabled={loadingJobs}
                className="webapp-pill-btn"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.35rem', 
                  fontSize: '0.72rem', 
                  padding: '0.25rem 0.6rem',
                  background: 'rgba(59, 130, 246, 0.12)',
                  borderColor: 'rgba(59, 130, 246, 0.3)',
                  color: '#60a5fa',
                  fontWeight: 700
                }}
              >
                <RefreshCw size={12} className={loadingJobs ? 'animate-spin' : ''} />
                <span>{t('refresh')}</span>
              </button>
            </div>

            {/* Jobs Cards Feed */}
            {loadingJobs ? (
              <div style={{ padding: '3.5rem 0', textAlign: 'center', color: '#94a3b8' }}>
                <RefreshCw size={28} className="animate-spin" style={{ margin: '0 auto 0.75rem auto', color: '#3b82f6' }} />
                <p style={{ fontSize: '0.85rem' }}>{t('loading_jobs')}</p>
              </div>
            ) : filteredJobs.length === 0 ? (
              <div className="webapp-search-card" style={{ textAlign: 'center', padding: '2.5rem 1.5rem' }}>
                <div style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>🔍</div>
                <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff', marginBottom: '0.35rem' }}>{t('no_jobs_found')}</h3>
                <p style={{ fontSize: '0.8rem', color: '#94a3b8', maxWidth: '280px', margin: '0 auto 1rem auto' }}>
                  {t('no_jobs_desc')}
                </p>
                <button 
                  onClick={() => { setSelectedCategory('all'); setSelectedEmpType('all'); setJobFilterMode('all'); setSearchQuery(''); }}
                  className="webapp-pill-btn active-primary"
                >
                  {t('clear_filters')}
                </button>
              </div>
            ) : (
              <div>
                {filteredJobs.map(job => (
                  <div key={job.id} className="webapp-job-card">
                    <div className="webapp-card-top">
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.25rem' }}>
                          <span className={job.employment_type === 'daily' ? 'webapp-badge-daily' : 'webapp-badge-permanent'}>
                            {job.employment_type === 'daily' ? `⚡️ ${t('filter_daily')}` : `💼 ${t('filter_permanent')}`}
                          </span>
                          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                            {getCategoryName(job.category)}
                          </span>
                        </div>
                        <div className="webapp-job-title">
                          {getPositionName(job.position, job.custom_position_name)}
                        </div>
                      </div>

                      <div>
                        <div className="webapp-job-price">
                          {job.price_amount ? `${Number(job.price_amount).toLocaleString()} ${t('salary_fixed')}` : (job.is_price_negotiable ? t('salary_negotiable') : "—")}
                        </div>
                        {job.employment_type === 'daily' && (
                          <div style={{ fontSize: '0.65rem', color: '#94a3b8', textAlign: 'right' }}>{t('daily_badge')}</div>
                        )}
                      </div>
                    </div>

                    <p className="webapp-job-desc">
                      {job.description || t('job_description')}
                    </p>

                    <div className="webapp-job-footer">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#94a3b8' }}>
                        <MapPin size={13} color="#60a5fa" />
                        <span>{job.district ? `${job.district}` : (job.address || "O'zbekiston")}</span>
                      </div>

                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <button 
                          onClick={() => setSelectedJob(job)}
                          className="webapp-pill-btn"
                          style={{ padding: '0.35rem 0.65rem' }}
                        >
                          <Info size={13} />
                          <span>{t('job_details')}</span>
                        </button>
                        <button 
                          onClick={() => handleOpenApply(job)}
                          className="webapp-apply-btn"
                        >
                          <Send size={13} />
                          <span>{t('apply_btn')}</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ---------------------------------------------------------
            ROLE 2: ISH BERUVCHI REJIMI (CLIENT MODE) — YANGI E'LON BERISH
            --------------------------------------------------------- */}
        {userRoleMode === 'CLIENT' && activeView === 'post_job' && (
          <div className="webapp-search-card">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#fff', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <PlusCircle size={18} color="#10b981" />
              {t('post_job_title')}
            </h3>
            <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '1rem' }}>
              {t('post_job_desc')}
            </p>

            {postSuccess ? (
              <div style={{ textAlign: 'center', padding: '2rem 1rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: 16, border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                <CheckCircle2 size={40} color="#10b981" style={{ margin: '0 auto 0.5rem auto' }} />
                <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>{t('post_success_msg')}</h4>
              </div>
            ) : (
              <form onSubmit={handleCreatePost} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('emp_type_label')}</label>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                    <button 
                      type="button"
                      onClick={() => setPostForm({ ...postForm, employment_type: 'daily' })}
                      className={`webapp-pill-btn ${postForm.employment_type === 'daily' ? 'active-amber' : ''}`}
                      style={{ padding: '0.6rem' }}
                    >
                      ⚡️ {t('filter_daily')}
                    </button>
                    <button 
                      type="button"
                      onClick={() => setPostForm({ ...postForm, employment_type: 'permanent' })}
                      className={`webapp-pill-btn ${postForm.employment_type === 'permanent' ? 'active-indigo' : ''}`}
                      style={{ padding: '0.6rem' }}
                    >
                      💼 {t('filter_permanent')}
                    </button>
                  </div>
                </div>

                <div>
                  <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('category_label')}</label>
                  <select 
                    value={postForm.category_id}
                    onChange={(e) => setPostForm({ ...postForm, category_id: e.target.value })}
                    required
                    style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.65rem', color: '#fff', outline: 'none' }}
                  >
                    <option value="">{t('select_category')}</option>
                    {categories.map(c => (
                      <option key={c.id} value={c.id}>{c.icon} {getCategoryName(c)}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('desc_label')}</label>
                  <textarea 
                    rows={3}
                    placeholder={t('desc_placeholder')}
                    value={postForm.description}
                    onChange={(e) => setPostForm({ ...postForm, description: e.target.value })}
                    required
                    style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.65rem', color: '#fff', outline: 'none' }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  <div>
                    <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('salary_label')}</label>
                    <input 
                      type="number"
                      placeholder={t('salary_placeholder')}
                      value={postForm.price_amount}
                      onChange={(e) => setPostForm({ ...postForm, price_amount: e.target.value })}
                      style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                    />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('district_label')}</label>
                    <input 
                      type="text"
                      placeholder={t('district_placeholder')}
                      value={postForm.district}
                      onChange={(e) => setPostForm({ ...postForm, district: e.target.value })}
                      required
                      style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                    />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  <div>
                    <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('contact_name_label')}</label>
                    <input 
                      type="text"
                      placeholder="Ism"
                      value={postForm.contact_name}
                      onChange={(e) => setPostForm({ ...postForm, contact_name: e.target.value })}
                      required
                      style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                    />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>{t('contact_phone_label')}</label>
                    <input 
                      type="tel"
                      placeholder="+998901234567"
                      value={postForm.contact_phone}
                      onChange={(e) => setPostForm({ ...postForm, contact_phone: e.target.value })}
                      required
                      style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                    />
                  </div>
                </div>

                <button 
                  type="submit"
                  disabled={postSubmitting}
                  className="webapp-apply-btn"
                  style={{ width: '100%', justifyContent: 'center', padding: '0.75rem', marginTop: '0.4rem', fontSize: '0.88rem' }}
                >
                  {postSubmitting ? <RefreshCw size={16} className="animate-spin" /> : <Send size={16} />}
                  <span>{t('submit_post_btn')}</span>
                </button>
              </form>
            )}
          </div>
        )}

        {/* ---------------------------------------------------------
            CLIENT ROLE: MENING E'LONLARIM (MY POSTS)
            --------------------------------------------------------- */}
        {userRoleMode === 'CLIENT' && activeView === 'my_posts' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div className="webapp-search-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <h3 style={{ fontSize: '0.98rem', fontWeight: 800, color: '#fff', margin: 0 }}>{t('my_posts_title')} ({myCreatedPosts.length})</h3>
                <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0 }}>{t('my_posts_desc')}</p>
              </div>
              <button 
                onClick={() => setActiveView('post_job')}
                className="webapp-apply-btn"
                style={{ fontSize: '0.75rem', padding: '0.4rem 0.8rem' }}
              >
                + {t('post_now_btn')}
              </button>
            </div>

            {myCreatedPosts.length === 0 ? (
              <div className="webapp-search-card" style={{ textAlign: 'center', padding: '2.5rem 1.5rem' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.4rem' }}>📑</div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#fff' }}>{t('no_posts_yet')}</h4>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', margin: '0.35rem auto 1rem auto', maxWidth: 260 }}>
                  {t('no_posts_desc')}
                </p>
                <button 
                  onClick={() => setActiveView('post_job')}
                  className="webapp-apply-btn"
                  style={{ margin: '0 auto' }}
                >
                  + {t('post_now_btn')}
                </button>
              </div>
            ) : (
              <div>
                {myCreatedPosts.map(post => (
                  <div key={post.id} className="webapp-job-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.35rem' }}>
                      <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#fff' }}>
                        {getPositionName(post.position, post.custom_position_name)}
                      </h4>
                      <span style={{ fontSize: '0.7rem', color: '#34d399', fontWeight: 700 }}>
                        {post.price_amount ? `${Number(post.price_amount).toLocaleString()} ${t('salary_fixed')}` : t('salary_negotiable')}
                      </span>
                    </div>
                    <p className="webapp-job-desc">{post.description}</p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '0.6rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                      <span>📍 {post.district || 'Hudud'}</span>
                      <span style={{ color: '#60a5fa', fontWeight: 700 }}>📬 {post.applications_count || 0} {t('applicants_count')}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ---------------------------------------------------------
            WORKER ROLE: MENING JAVOBLARIM / ARIZALARIM (MY APPS)
            --------------------------------------------------------- */}
        {userRoleMode === 'WORKER' && activeView === 'my_apps' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div className="webapp-search-card" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div style={{ width: 42, height: 42, borderRadius: 12, background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem' }}>
                📬
              </div>
              <div>
                <h3 style={{ fontSize: '0.98rem', fontWeight: 800, color: '#fff', margin: 0 }}>{t('my_applications_title')}</h3>
                <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0 }}>{t('my_applications_desc')}</p>
              </div>
            </div>

            {loadingApps ? (
              <div style={{ padding: '3rem 0', textAlign: 'center', color: '#94a3b8' }}>
                <RefreshCw size={24} className="animate-spin" style={{ margin: '0 auto 0.5rem auto' }} />
                <p style={{ fontSize: '0.8rem' }}>{t('loading_applications')}</p>
              </div>
            ) : myApplications.length === 0 ? (
              <div className="webapp-search-card" style={{ textAlign: 'center', padding: '2.5rem 1.5rem' }}>
                <div style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>📂</div>
                <h3 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#fff' }}>{t('no_applications')}</h3>
                <p style={{ fontSize: '0.78rem', color: '#94a3b8', maxWidth: '280px', margin: '0.35rem auto 1rem auto' }}>
                  {t('no_applications_desc')}
                </p>
                <button 
                  onClick={() => setActiveView('jobs')}
                  className="webapp-pill-btn active-primary"
                >
                  {t('find_jobs_btn')}
                </button>
              </div>
            ) : (
              <div>
                {myApplications.map(app => (
                  <div key={app.id} className="webapp-job-card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                      <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#fff' }}>{app.job_title}</h4>
                      <span style={{ 
                        fontSize: '0.68rem', 
                        fontWeight: 700, 
                        padding: '0.2rem 0.5rem', 
                        borderRadius: 6,
                        background: app.status === 'accepted' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(59, 130, 246, 0.15)',
                        color: app.status === 'accepted' ? '#34d399' : '#60a5fa'
                      }}>
                        {app.status === 'accepted' ? `✅ ${t('app_status_accepted')}` : `⏳ ${t('app_status_pending')}`}
                      </span>
                    </div>

                    <div style={{ fontSize: '0.78rem', color: '#94a3b8', display: 'flex', gap: '0.75rem', marginBottom: '0.4rem' }}>
                      <span>📍 {app.district || 'Hudud'}</span>
                      <span>💰 {app.price}</span>
                      <span>⏱ {app.applied_at}</span>
                    </div>

                    {app.proposal_message && (
                      <div style={{ background: '#090d16', padding: '0.5rem 0.75rem', borderRadius: 8, fontSize: '0.76rem', color: '#cbd5e1' }}>
                        💬 <i>"{app.proposal_message}"</i>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ---------------------------------------------------------
            COMMON VIEW: SHAXSIY KABINET (USER PROFILE & SETTINGS)
            --------------------------------------------------------- */}
        {activeView === 'profile' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {/* Notification alert on success */}
            {locationSuccessMsg && (
              <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.35)', color: '#34d399', borderRadius: 12, padding: '0.65rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle2 size={16} />
                <span>{locationSuccessMsg}</span>
              </div>
            )}

            {/* Profile Card */}
            <div className="webapp-search-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div style={{ width: 48, height: 48, borderRadius: 14, background: 'linear-gradient(135deg, #2563eb, #7c3aed)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.3rem', fontWeight: 900 }}>
                    {currentUser?.first_name ? currentUser.first_name[0] : 'U'}
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff', margin: 0 }}>
                      {currentUser?.first_name || 'Foydalanuvchi'}
                    </h3>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.15rem' }}>
                      <span style={{ color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '0.2rem', fontWeight: 700 }}>
                        <Star size={13} fill="#fbbf24" /> {currentUser?.rating || '5.0'}
                      </span>
                      <span>•</span>
                      <span>{currentUser?.completed_jobs_count || 0} {t('successful_jobs')}</span>
                    </div>
                  </div>
                </div>

                <button 
                  onClick={() => setIsEditingProfile(true)}
                  className="webapp-pill-btn"
                  style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
                >
                  ✏️ {t('edit_profile_btn')}
                </button>
              </div>

              {/* Bot Parity Details */}
              <div style={{ background: '#090d16', borderRadius: 12, border: '1px solid rgba(255, 255, 255, 0.06)', padding: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.8rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>{t('phone_number')}:</span>
                  <span style={{ fontWeight: 700, color: '#fff' }}>{currentUser?.phone_number || t('not_entered')}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>{t('region_district')}:</span>
                  <span style={{ fontWeight: 700, color: '#fff' }}>{currentUser?.district || currentUser?.region_name || "O'zbekiston"}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ color: '#94a3b8' }}>{t('gps_location')}:</span>
                  <span style={{ fontWeight: 700, color: currentUser?.latitude ? '#34d399' : '#94a3b8', fontSize: '0.75rem' }}>
                    {currentUser?.latitude ? `${currentUser.latitude.toFixed(4)}, ${currentUser.longitude.toFixed(4)}` : t('not_attached')}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ color: '#94a3b8' }}>{t('specialties_label')}:</span>
                  <span style={{ fontWeight: 700, color: '#60a5fa', textAlign: 'right', maxWidth: '60%' }}>
                    {currentUser?.selected_positions_details?.length > 0 
                      ? currentUser.selected_positions_details.map(p => p[`name_${currentLang}`] || p.name_uz || p.name).join(', ')
                      : (currentUser?.position_details ? (currentUser.position_details[`name_${currentLang}`] || currentUser.position_details.name_uz) : (currentUser?.custom_position || currentUser?.category_details?.[`name_${currentLang}`] || currentUser?.category_details?.name_uz || t('not_entered')))}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>{t('work_schedule_label')}:</span>
                  <span style={{ fontWeight: 700, color: '#fff' }}>
                    {currentUser?.employment_type === 'daily' ? t('filter_daily') : (currentUser?.employment_type === 'permanent' ? t('filter_permanent') : `${t('filter_daily')} / ${t('filter_permanent')}`)}
                    {currentUser?.work_schedule ? ` (${currentUser.work_schedule === '24_7' ? '24/7' : (currentUser.work_schedule === 'day_shift' ? 'Kunduzgi' : 'Erkin')})` : ''}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ color: '#94a3b8' }}>{t('app_language')}:</span>
                  <span style={{ fontWeight: 700, color: '#60a5fa' }}>
                    {currentLang === 'ru' ? "🇷🇺 Русский" : currentLang === 'oz' ? "🇺🇿 Ўзбекча (Кирилл)" : currentLang === 'en' ? "🇬🇧 English" : "🇺🇿 O'zbekcha (Lotin)"}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Telegram ID:</span>
                  <span style={{ fontWeight: 700, color: '#60a5fa', fontFamily: 'monospace' }}>{currentUser?.telegram_id || 'Ulanmagan'}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>{t('account_status')}:</span>
                  <span style={{ color: '#34d399', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <ShieldCheck size={14} /> {t('status_verified')}
                  </span>
                </div>
              </div>

              {/* Bot-style Quick Management Buttons */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginTop: '0.1rem' }}>
                {/* Tilni o'zgartirish tugmasi */}
                <button 
                  onClick={() => setIsLangModalOpen(true)}
                  className="webapp-pill-btn"
                  style={{ padding: '0.65rem 0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem', fontSize: '0.78rem', color: '#60a5fa', borderColor: 'rgba(96, 165, 250, 0.25)' }}
                >
                  <Globe size={15} />
                  <span>{t('change_language_btn')}</span>
                </button>

                {/* Lokatsiyani yangilash tugmasi */}
                <button 
                  onClick={handleUpdateLocation}
                  disabled={updatingLocation}
                  className="webapp-pill-btn"
                  style={{ padding: '0.65rem 0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem', fontSize: '0.78rem', color: '#34d399', borderColor: 'rgba(52, 211, 153, 0.25)' }}
                >
                  <Crosshair size={15} className={updatingLocation ? 'animate-spin' : ''} />
                  <span>{updatingLocation ? t('location_updating') : t('update_location_btn')}</span>
                </button>
              </div>

              {/* Qo'llab-quvvatlash */}
              <button 
                onClick={() => setActiveView('support')}
                className="webapp-pill-btn"
                style={{ width: '100%', padding: '0.65rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', fontSize: '0.78rem' }}
              >
                <MessageSquare size={14} color="#94a3b8" />
                <span>{t('support_btn')}</span>
              </button>
            </div>
          </div>
        )}

        {/* ---------------------------------------------------------
            COMMON VIEW: QO'LLAB-QUVVATLASH VA TAKLIFLAR (SUPPORT)
            --------------------------------------------------------- */}
        {activeView === 'support' && (
          <div className="webapp-search-card">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#fff', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Headphones size={18} color="#60a5fa" />
              {t('support_title')}
            </h3>
            <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '1rem' }}>
              {t('support_desc')}
            </p>

            {feedbackSent ? (
              <div style={{ textAlign: 'center', padding: '2rem 1rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: 16, border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                <CheckCircle2 size={40} color="#10b981" style={{ margin: '0 auto 0.5rem auto' }} />
                <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>{t('message_sent_success')}</h4>
                <p style={{ fontSize: '0.78rem', color: '#cbd5e1' }}>{t('admin_review_soon')}</p>
              </div>
            ) : (
              <form onSubmit={handleSendFeedback} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>
                    {t('message_text_label')}
                  </label>
                  <textarea 
                    rows={4}
                    placeholder={t('message_placeholder')}
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    required
                    style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.65rem', color: '#fff', outline: 'none' }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  <button 
                    type="button"
                    onClick={() => setActiveView('profile')}
                    className="webapp-pill-btn"
                    style={{ padding: '0.65rem' }}
                  >
                    {t('back_btn')}
                  </button>
                  <button 
                    type="submit"
                    className="webapp-apply-btn"
                    style={{ justifyContent: 'center', padding: '0.65rem' }}
                  >
                    <Send size={15} />
                    <span>{t('send_btn')}</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        )}
      </main>

      {/* =========================================================
          LANGUAGE SELECTION MODAL (4 LANGUAGES: UZ, OZ, RU, EN)
          ========================================================= */}
      {isLangModalOpen && (
        <div className="webapp-modal-overlay" onClick={() => setIsLangModalOpen(false)}>
          <div className="webapp-modal-sheet" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Globe size={18} color="#60a5fa" />
                {t('select_language_title')}
              </h3>
              <button onClick={() => setIsLangModalOpen(false)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
              <button
                onClick={() => handleSelectLanguage('uz')}
                disabled={updatingLang}
                className="webapp-pill-btn"
                style={{
                  padding: '0.85rem 1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  background: currentLang === 'uz' ? 'rgba(37, 99, 235, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                  borderColor: currentLang === 'uz' ? '#3b82f6' : 'rgba(255, 255, 255, 0.08)',
                  color: currentLang === 'uz' ? '#60a5fa' : '#fff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  borderRadius: 14
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                  <span style={{ fontSize: '1.3rem' }}>🇺🇿</span>
                  <span>{t('lang_uz')}</span>
                </div>
                {currentLang === 'uz' && <Check size={18} color="#3b82f6" />}
              </button>

              <button
                onClick={() => handleSelectLanguage('oz')}
                disabled={updatingLang}
                className="webapp-pill-btn"
                style={{
                  padding: '0.85rem 1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  background: currentLang === 'oz' ? 'rgba(37, 99, 235, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                  borderColor: currentLang === 'oz' ? '#3b82f6' : 'rgba(255, 255, 255, 0.08)',
                  color: currentLang === 'oz' ? '#60a5fa' : '#fff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  borderRadius: 14
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                  <span style={{ fontSize: '1.3rem' }}>🇺🇿</span>
                  <span>{t('lang_oz')}</span>
                </div>
                {currentLang === 'oz' && <Check size={18} color="#3b82f6" />}
              </button>

              <button
                onClick={() => handleSelectLanguage('ru')}
                disabled={updatingLang}
                className="webapp-pill-btn"
                style={{
                  padding: '0.85rem 1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  background: currentLang === 'ru' ? 'rgba(37, 99, 235, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                  borderColor: currentLang === 'ru' ? '#3b82f6' : 'rgba(255, 255, 255, 0.08)',
                  color: currentLang === 'ru' ? '#60a5fa' : '#fff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  borderRadius: 14
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                  <span style={{ fontSize: '1.3rem' }}>🇷🇺</span>
                  <span>{t('lang_ru')}</span>
                </div>
                {currentLang === 'ru' && <Check size={18} color="#3b82f6" />}
              </button>

              <button
                onClick={() => handleSelectLanguage('en')}
                disabled={updatingLang}
                className="webapp-pill-btn"
                style={{
                  padding: '0.85rem 1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  background: currentLang === 'en' ? 'rgba(37, 99, 235, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                  borderColor: currentLang === 'en' ? '#3b82f6' : 'rgba(255, 255, 255, 0.08)',
                  color: currentLang === 'en' ? '#60a5fa' : '#fff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  borderRadius: 14
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                  <span style={{ fontSize: '1.3rem' }}>🇬🇧</span>
                  <span>{t('lang_en')}</span>
                </div>
                {currentLang === 'en' && <Check size={18} color="#3b82f6" />}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================
          PROFILE EDIT MODAL
          ========================================================= */}
      {isEditingProfile && (
        <div className="webapp-modal-overlay" onClick={() => setIsEditingProfile(false)}>
          <div className="webapp-modal-sheet" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>{t('edit_profile_title')}</h3>
              <button onClick={() => setIsEditingProfile(false)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSaveProfile} style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', fontSize: '0.8rem' }}>
              <div>
                <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.25rem' }}>{t('full_name_label')}</label>
                <input 
                  type="text"
                  value={editForm.first_name}
                  onChange={(e) => setEditForm({ ...editForm, first_name: e.target.value })}
                  required
                  style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.25rem' }}>{t('phone_number')}</label>
                <input 
                  type="tel"
                  value={editForm.phone_number}
                  onChange={(e) => setEditForm({ ...editForm, phone_number: e.target.value })}
                  style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.25rem' }}>{t('district_label')}</label>
                <input 
                  type="text"
                  value={editForm.district}
                  onChange={(e) => setEditForm({ ...editForm, district: e.target.value })}
                  style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.25rem' }}>{t('app_language')}</label>
                <select 
                  value={editForm.language}
                  onChange={(e) => setEditForm({ ...editForm, language: e.target.value })}
                  style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10, padding: '0.6rem', color: '#fff', outline: 'none' }}
                >
                  <option value="uz">🇺🇿 {t('lang_uz')}</option>
                  <option value="oz">🇺🇿 {t('lang_oz')}</option>
                  <option value="ru">🇷🇺 {t('lang_ru')}</option>
                  <option value="en">🇬🇧 {t('lang_en')}</option>
                </select>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginTop: '0.5rem' }}>
                <button 
                  type="button"
                  onClick={() => setIsEditingProfile(false)}
                  className="webapp-pill-btn"
                  style={{ padding: '0.65rem' }}
                >
                  {t('cancel_btn')}
                </button>
                <button 
                  type="submit"
                  disabled={savingProfile}
                  className="webapp-apply-btn"
                  style={{ justifyContent: 'center', padding: '0.65rem' }}
                >
                  {savingProfile ? <RefreshCw size={14} className="animate-spin" /> : <Check size={14} />}
                  <span>{t('save_btn')}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          JOB DETAIL MODAL
          ========================================================= */}
      {selectedJob && !applyModalOpen && (
        <div className="webapp-modal-overlay" onClick={() => setSelectedJob(null)}>
          <div className="webapp-modal-sheet" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <div>
                <span className={selectedJob.employment_type === 'daily' ? 'webapp-badge-daily' : 'webapp-badge-permanent'}>
                  {selectedJob.employment_type === 'daily' ? `⚡️ ${t('filter_daily')}` : `💼 ${t('filter_permanent')}`}
                </span>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#fff', marginTop: '0.35rem' }}>
                  {getPositionName(selectedJob.position, selectedJob.custom_position_name)}
                </h3>
              </div>
              <button 
                onClick={() => setSelectedJob(null)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '0.25rem' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', fontSize: '0.82rem', marginBottom: '1.25rem' }}>
              <div style={{ background: '#090d16', padding: '0.85rem', borderRadius: 12, border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                  <span style={{ color: '#94a3b8' }}>{t('job_salary')}:</span>
                  <span style={{ fontWeight: 900, color: '#34d399', fontSize: '0.95rem' }}>
                    {selectedJob.price_amount ? `${Number(selectedJob.price_amount).toLocaleString()} ${t('salary_fixed')}` : (selectedJob.is_price_negotiable ? t('salary_negotiable') : '—')}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                  <span style={{ color: '#94a3b8' }}>{t('job_location')}:</span>
                  <span style={{ color: '#fff', fontWeight: 600 }}>{selectedJob.district || selectedJob.address || "O'zbekiston"}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>{t('job_start')}:</span>
                  <span style={{ color: '#fbbf24', fontWeight: 600 }}>{selectedJob.start_time_type === 'urgent' ? `🔥 ${t('urgent_badge')}` : t('planned_badge')}</span>
                </div>
              </div>

              <div>
                <span style={{ fontWeight: 700, color: '#cbd5e1', display: 'block', marginBottom: '0.25rem' }}>{t('job_description')}:</span>
                <p style={{ color: '#94a3b8', lineHeight: 1.6, background: '#090d16', padding: '0.75rem', borderRadius: 10, border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                  {selectedJob.description || t('job_description')}
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              <button 
                onClick={() => setSelectedJob(null)}
                className="webapp-pill-btn"
                style={{ padding: '0.65rem', textAlign: 'center' }}
              >
                {t('cancel_btn')}
              </button>
              <button 
                onClick={() => handleOpenApply(selectedJob)}
                className="webapp-apply-btn"
                style={{ justifyContent: 'center', padding: '0.65rem' }}
              >
                <Send size={15} />
                <span>{t('apply_btn')}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* =========================================================
          APPLY PROPOSAL MODAL
          ========================================================= */}
      {applyModalOpen && selectedJob && (
        <div className="webapp-modal-overlay" onClick={() => setApplyModalOpen(false)}>
          <div className="webapp-modal-sheet" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.65rem' }}>
              <div>
                <span style={{ fontSize: '0.7rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase' }}>{t('send_proposal')}</span>
                <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>
                  {getPositionName(selectedJob.position, selectedJob.custom_position_name)}
                </h3>
              </div>
              <button 
                onClick={() => setApplyModalOpen(false)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={18} />
              </button>
            </div>

            {appliedSuccess ? (
              <div style={{ textAlign: 'center', padding: '1.75rem 1rem' }}>
                <CheckCircle2 size={42} color="#10b981" style={{ margin: '0 auto 0.5rem auto' }} className="animate-bounce" />
                <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#fff' }}>{t('apply_success')}</h4>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: 700, color: '#cbd5e1', marginBottom: '0.35rem' }}>
                    {t('proposal_label')}
                  </label>
                  <textarea 
                    rows={3}
                    placeholder={t('proposal_placeholder')}
                    value={applyMessage}
                    onChange={(e) => setApplyMessage(e.target.value)}
                    style={{ width: '100%', background: '#090d16', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: 10, padding: '0.65rem', color: '#fff', outline: 'none' }}
                  />
                </div>

                <button 
                  onClick={submitApplication}
                  disabled={isApplying}
                  className="webapp-apply-btn"
                  style={{ width: '100%', justifyContent: 'center', padding: '0.75rem', fontSize: '0.88rem' }}
                >
                  {isApplying ? <RefreshCw size={15} className="animate-spin" /> : <Send size={15} />}
                  <span>{t('confirm_apply')}</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* =========================================================
          DYNAMIC BOTTOM NAVIGATION BAR BASED ON USER ROLE
          ========================================================= */}
      <nav className="webapp-bottom-nav">
        {userRoleMode === 'WORKER' ? (
          /* WORKER BOTTOM NAVIGATION */
          <div className="webapp-bottom-nav-inner" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
            <button 
              onClick={() => setActiveView('jobs')}
              className={`webapp-nav-item ${activeView === 'jobs' ? 'active' : ''}`}
            >
              <Briefcase />
              <span>{t('nav_jobs')}</span>
            </button>

            <button 
              onClick={() => setActiveView('my_apps')}
              className={`webapp-nav-item ${activeView === 'my_apps' ? 'active' : ''}`}
            >
              <FileText />
              <span>{t('nav_my_apps')}</span>
            </button>

            <button 
              onClick={() => setActiveView('profile')}
              className={`webapp-nav-item ${activeView === 'profile' || activeView === 'support' ? 'active' : ''}`}
            >
              <User />
              <span>{t('nav_cabinet')}</span>
            </button>
          </div>
        ) : (
          /* CLIENT (EMPLOYER) BOTTOM NAVIGATION */
          <div className="webapp-bottom-nav-inner" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
            <button 
              onClick={() => setActiveView('my_posts')}
              className={`webapp-nav-item ${activeView === 'my_posts' ? 'active' : ''}`}
            >
              <FileText />
              <span>{t('nav_my_posts')}</span>
            </button>

            <button 
              onClick={() => setActiveView('post_job')}
              className={`webapp-nav-item ${activeView === 'post_job' ? 'active-post' : ''}`}
            >
              <PlusCircle />
              <span>{t('nav_post_job')}</span>
            </button>

            <button 
              onClick={() => setActiveView('profile')}
              className={`webapp-nav-item ${activeView === 'profile' || activeView === 'support' ? 'active' : ''}`}
            >
              <User />
              <span>{t('nav_cabinet')}</span>
            </button>
          </div>
        )}
      </nav>
    </div>
  );
}
