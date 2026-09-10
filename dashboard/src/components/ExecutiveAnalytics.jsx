import React, { useState } from 'react';
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  CheckCircle2, 
  Clock, 
  XCircle, 
  Award, 
  Zap,
  Layers,
  ArrowUpRight,
  UserCheck,
  Percent,
  Calendar,
  Briefcase,
  MapPin,
  Globe,
  UserPlus,
  BarChart3,
  PieChart,
  Activity,
  ShieldCheck,
  Sparkles,
  Flame,
  FileText,
  Send,
  Compass
} from 'lucide-react';

export default function ExecutiveAnalytics({ stats = {}, loading = false }) {
  const [activeMetricTab, setActiveMetricTab] = useState('overview'); // 'overview' | 'marketing' | 'demographics' | 'categories'

  // 1. Finance & Order KPI
  const totalRevenue = stats.total_revenue || 0;
  const todayRevenue = stats.today_revenue || 0;
  const totalOrders = stats.total_orders || 0;
  const finishedOrders = stats.finished_orders || 0;
  const pendingOrders = stats.pending_orders || 0;
  const dispatchedOrders = stats.dispatched_orders || 0;
  const startedOrders = stats.started_orders || 0;
  const cancelledOrders = stats.cancelled_orders || 0;

  const completionRate = stats.completion_rate || 0;
  const cancellationRate = stats.cancellation_rate || 0;
  const avgOrderValue = stats.avg_order_value || 0;

  // 2. Audience & Marketing KPI
  const totalUsers = stats.total_users || 0;
  const totalBotUsers = stats.total_bot_users || 0;
  const registeredUsers = stats.registered_users || 0;
  const regConversionRate = stats.reg_conversion_rate || 0;
  const totalWorkers = stats.total_workers || 0;
  const activeWorkers = stats.active_workers || 0;
  const busyWorkers = stats.busy_workers || 0;
  const workerOccupancy = stats.worker_occupancy_rate || 0;
  const totalClients = stats.total_clients || 0;
  const bothBotUsers = stats.both_bot_users || 0;

  // 3. Job Posts KPI
  const totalJobPosts = stats.total_job_posts || 0;
  const activeJobPosts = stats.active_job_posts || 0;
  const completedJobPosts = stats.completed_job_posts || 0;
  const cancelledJobPosts = stats.cancelled_job_posts || 0;
  const dailyJobPosts = stats.daily_job_posts || 0;
  const permanentJobPosts = stats.permanent_job_posts || 0;
  const totalApplications = stats.total_applications || 0;
  const acceptedApplications = stats.accepted_applications || 0;

  // 4. Data Arrays
  const regionsData = stats.regions_data || [];
  const languagesData = stats.languages_data || [];
  const genderData = stats.gender_data || { male: 0, female: 0, unknown: 0 };
  const ageGroups = stats.age_groups || { '18_25': 0, '26_35': 0, '36_50': 0, '50_plus': 0, 'unspecified': 0 };
  const growthDays = stats.growth_days || [];
  const categoryDistribution = stats.category_distribution || [];

  // Calculate max values for bar scaling
  const maxGrowthCount = Math.max(...growthDays.map(d => Math.max(d.new_users, d.new_jobs, d.new_orders, 1)), 5);
  const maxRegionUsers = regionsData.length > 0 ? Math.max(...regionsData.map(r => r.total_users), 1) : 1;

  const totalAgeCount = Object.values(ageGroups).reduce((a, b) => a + b, 0) || 1;
  const totalGenderCount = (genderData.male + genderData.female + genderData.unknown) || 1;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2rem' }}>
      
      {/* --- ANALYTICS NAVIGATION TABS --- */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.75rem',
        padding: '0.6rem 0.8rem',
        backgroundColor: 'var(--card-bg)',
        borderRadius: '12px',
        border: '1px solid var(--border-color)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => setActiveMetricTab('overview')}
            className="btn"
            style={{
              padding: '0.45rem 0.9rem',
              fontSize: '0.82rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: activeMetricTab === 'overview' ? 'var(--primary)' : 'var(--bg-inner)',
              color: activeMetricTab === 'overview' ? '#fff' : 'var(--text-secondary)',
              border: '1px solid',
              borderColor: activeMetricTab === 'overview' ? 'var(--primary)' : 'var(--border-color)'
            }}
          >
            <Activity size={15} /> Asosiy Biznes Ko'rsatkichlari
          </button>

          <button
            onClick={() => setActiveMetricTab('marketing')}
            className="btn"
            style={{
              padding: '0.45rem 0.9rem',
              fontSize: '0.82rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: activeMetricTab === 'marketing' ? 'var(--primary)' : 'var(--bg-inner)',
              color: activeMetricTab === 'marketing' ? '#fff' : 'var(--text-secondary)',
              border: '1px solid',
              borderColor: activeMetricTab === 'marketing' ? 'var(--primary)' : 'var(--border-color)'
            }}
          >
            <Compass size={15} /> Hududlar & Marketing Tahlili
          </button>

          <button
            onClick={() => setActiveMetricTab('demographics')}
            className="btn"
            style={{
              padding: '0.45rem 0.9rem',
              fontSize: '0.82rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: activeMetricTab === 'demographics' ? 'var(--primary)' : 'var(--bg-inner)',
              color: activeMetricTab === 'demographics' ? '#fff' : 'var(--text-secondary)',
              border: '1px solid',
              borderColor: activeMetricTab === 'demographics' ? 'var(--primary)' : 'var(--border-color)'
            }}
          >
            <Users size={15} /> Auditoriya & Demografiya
          </button>

          <button
            onClick={() => setActiveMetricTab('categories')}
            className="btn"
            style={{
              padding: '0.45rem 0.9rem',
              fontSize: '0.82rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              background: activeMetricTab === 'categories' ? 'var(--primary)' : 'var(--bg-inner)',
              color: activeMetricTab === 'categories' ? '#fff' : 'var(--text-secondary)',
              border: '1px solid',
              borderColor: activeMetricTab === 'categories' ? 'var(--primary)' : 'var(--border-color)'
            }}
          >
            <Layers size={15} /> Sohalar & Talab-Taklif
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          <Sparkles size={14} color="#f59e0b" /> Real-vaqtli tizim hisoboti
        </div>
      </div>

      {/* --- TOP 4 STRATEGIC KPI CARDS --- */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
        {loading ? (
          Array.from({ length: 4 }).map((_, idx) => (
            <div key={idx} className="skeleton-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="skeleton skeleton-title" style={{ width: '90px', height: '14px', margin: 0 }} />
                <div className="skeleton" style={{ width: '28px', height: '28px', borderRadius: '8px' }} />
              </div>
              <div className="skeleton" style={{ width: '130px', height: '32px', margin: '0.4rem 0' }} />
              <div className="skeleton skeleton-text" style={{ width: '100%', height: '12px' }} />
              <div className="skeleton" style={{ width: '100%', height: '6px', borderRadius: '4px', marginTop: '0.2rem' }} />
            </div>
          ))
        ) : (
          <>
            {/* Total Users */}
            <div className="kpi-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="kpi-title">Jami Auditoriya</span>
                <div className="kpi-icon-box" style={{ background: 'rgba(59, 130, 246, 0.12)', color: '#3b82f6' }}>
                  <Users size={18} />
                </div>
              </div>
              <div className="kpi-value">{totalUsers.toLocaleString()} <span className="kpi-unit">user</span></div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <span>Ishchilar / Ish beruvchilar:</span>
                <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>{totalWorkers} / {totalClients}</span>
              </div>
              <div className="progress-bar-container" style={{ marginTop: '0.4rem' }}>
                <div className="progress-bar-fill" style={{ width: `${regConversionRate}%`, backgroundColor: '#3b82f6' }}></div>
              </div>
              <div style={{ fontSize: '0.72rem', color: '#10b981', marginTop: '0.2rem' }}>
                To'liq ro'yxatdan o'tganlar: <b>{registeredUsers}</b> ({regConversionRate}%)
              </div>
            </div>

            {/* Total Job Posts */}
            <div className="kpi-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="kpi-title">E'lonlar & Arizalar</span>
                <div className="kpi-icon-box" style={{ background: 'rgba(139, 92, 246, 0.12)', color: '#8b5cf6' }}>
                  <Briefcase size={18} />
                </div>
              </div>
              <div className="kpi-value">{totalJobPosts.toLocaleString()} <span className="kpi-unit">e'lon</span></div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <span>Faol / Yopilgan:</span>
                <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>{activeJobPosts} / {completedJobPosts}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
                <span>Yuborilgan arizalar:</span>
                <span style={{ color: '#8b5cf6', fontWeight: 700 }}>{totalApplications} ta</span>
              </div>
            </div>

            {/* Total Orders & Success */}
            <div className="kpi-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="kpi-title">Buyurtmalar Konversiyasi</span>
                <div className="kpi-icon-box" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981' }}>
                  <Award size={18} />
                </div>
              </div>
              <div className="kpi-value" style={{ color: '#10b981' }}>{completionRate}%</div>
              <div className="progress-bar-container" style={{ marginTop: '0.4rem' }}>
                <div className="progress-bar-fill" style={{ width: `${Math.min(completionRate, 100)}%`, backgroundColor: '#10b981' }}></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                <span>Bajarildi: <b>{finishedOrders}</b></span>
                <span>Bekor: <b style={{ color: '#ef4444' }}>{cancelledOrders}</b></span>
              </div>
            </div>

            {/* Revenue / Monetization */}
            <div className="kpi-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="kpi-title">Daromad & Oborot</span>
                <div className="kpi-icon-box" style={{ background: 'rgba(245, 158, 11, 0.12)', color: '#f59e0b' }}>
                  <DollarSign size={18} />
                </div>
              </div>
              <div className="kpi-value">{totalRevenue.toLocaleString()} <span className="kpi-unit">SUM</span></div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <span>Bugungi tushum:</span>
                <span style={{ color: '#10b981', fontWeight: 700 }}>+{todayRevenue.toLocaleString()} SUM</span>
              </div>
              <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                O'rtacha chek (AOV): <b>{avgOrderValue.toLocaleString('en-US', { maximumFractionDigits: 0 })} SUM</b>
              </div>
            </div>
          </>
        )}
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: OVERVIEW & GROWTH TRENDS                                           */}
      {/* ========================================================================= */}
      {(activeMetricTab === 'overview') && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Growth Dynamics Chart (Last 7 Days) */}
          <div className="card" style={{ margin: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <TrendingUp size={18} color="#3b82f6" />
                  <h3 className="card-title" style={{ margin: 0 }}>Haftalik O'sish Dinamikasi (Oxirgi 7 kun)</h3>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0.2rem 0 0 0' }}>
                  Kunlik yangi foydalanuvchilar, joylangan ishlar va buyurtmalar oqimi
                </p>
              </div>
              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.76rem' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-secondary)' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#3b82f6' }}></span> Yangi Userlar
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-secondary)' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#8b5cf6' }}></span> Yangi E'lonlar
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-secondary)' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981' }}></span> Buyurtmalar
                </span>
              </div>
            </div>

            {/* Visual Bar Chart */}
            <div style={{
              display: 'flex',
              alignItems: 'flex-end',
              justifyContent: 'space-between',
              height: '180px',
              padding: '1rem 0.5rem 0.5rem 0.5rem',
              backgroundColor: 'var(--bg-inner)',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              gap: '0.75rem'
            }}>
              {growthDays.map((day, idx) => {
                const userH = (day.new_users / maxGrowthCount) * 120;
                const jobH = (day.new_jobs / maxGrowthCount) * 120;
                const orderH = (day.new_orders / maxGrowthCount) * 120;

                return (
                  <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem', height: '100%', justifyContent: 'flex-end' }}>
                    <div style={{ display: 'flex', alignItems: 'flex-end', gap: '4px', height: '120px' }}>
                      {/* User Bar */}
                      <div 
                        title={`Yangi userlar: ${day.new_users}`}
                        style={{
                          width: '12px',
                          height: `${Math.max(userH, 4)}px`,
                          backgroundColor: '#3b82f6',
                          borderRadius: '3px 3px 0 0',
                          transition: 'height 0.3s ease'
                        }}
                      />
                      {/* Job Bar */}
                      <div 
                        title={`Yangi e'lonlar: ${day.new_jobs}`}
                        style={{
                          width: '12px',
                          height: `${Math.max(jobH, 4)}px`,
                          backgroundColor: '#8b5cf6',
                          borderRadius: '3px 3px 0 0',
                          transition: 'height 0.3s ease'
                        }}
                      />
                      {/* Order Bar */}
                      <div 
                        title={`Yangi buyurtmalar: ${day.new_orders}`}
                        style={{
                          width: '12px',
                          height: `${Math.max(orderH, 4)}px`,
                          backgroundColor: '#10b981',
                          borderRadius: '3px 3px 0 0',
                          transition: 'height 0.3s ease'
                        }}
                      />
                    </div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>{day.date}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Operational Flow & Job Type Split */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
            
            {/* Orders Status Flow */}
            <div className="card" style={{ margin: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
                <Layers size={18} color="#3b82f6" />
                <h3 className="card-title" style={{ margin: 0 }}>Buyurtmalar Operatsion Holati</h3>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1.25rem' }}>
                Barcha buyurtmalarning zanjir bo'yicha harakati
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.3rem' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}>
                      <Clock size={14} color="#ef4444" /> Yangi kutilmoqda (Pending)
                    </span>
                    <span style={{ fontWeight: 700 }}>{pendingOrders} ta ({totalOrders > 0 ? ((pendingOrders/totalOrders)*100).toFixed(1) : 0}%)</span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${totalOrders > 0 ? (pendingOrders/totalOrders)*100 : 0}%`, backgroundColor: '#ef4444' }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.3rem' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}>
                      <UserCheck size={14} color="#3b82f6" /> Usta biriktirilgan (Dispatched)
                    </span>
                    <span style={{ fontWeight: 700 }}>{dispatchedOrders} ta ({totalOrders > 0 ? ((dispatchedOrders/totalOrders)*100).toFixed(1) : 0}%)</span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${totalOrders > 0 ? (dispatchedOrders/totalOrders)*100 : 0}%`, backgroundColor: '#3b82f6' }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.3rem' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}>
                      <Zap size={14} color="#8b5cf6" /> Jarayonda / Yo'lda (Started)
                    </span>
                    <span style={{ fontWeight: 700 }}>{startedOrders} ta ({totalOrders > 0 ? ((startedOrders/totalOrders)*100).toFixed(1) : 0}%)</span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${totalOrders > 0 ? (startedOrders/totalOrders)*100 : 0}%`, backgroundColor: '#8b5cf6' }}></div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.3rem' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-secondary)' }}>
                      <CheckCircle2 size={14} color="#10b981" /> Muvaffaqiyatli yakunlandi
                    </span>
                    <span style={{ fontWeight: 700, color: '#10b981' }}>{finishedOrders} ta ({completionRate}%)</span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${completionRate}%`, backgroundColor: '#10b981' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Employment Type & Market Demand Split */}
            <div className="card" style={{ margin: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
                <Flame size={18} color="#f59e0b" />
                <h3 className="card-title" style={{ margin: 0 }}>Bandlik Formati & Takliflar</h3>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1.25rem' }}>
                Kunbay (bir martalik) va Doimiy (oylik) ishlar nisbati
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {/* Daily vs Permanent */}
                <div style={{ padding: '0.9rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                    <span style={{ color: '#f59e0b' }}>⚡ Kunbay / Bir martalik: {dailyJobPosts} ta</span>
                    <span style={{ color: '#3b82f6' }}>🏢 Doimiy (oylik): {permanentJobPosts} ta</span>
                  </div>
                  <div className="progress-bar-container" style={{ display: 'flex', overflow: 'hidden' }}>
                    <div style={{ width: `${totalJobPosts > 0 ? (dailyJobPosts/totalJobPosts)*100 : 50}%`, backgroundColor: '#f59e0b', height: '100%' }}></div>
                    <div style={{ width: `${totalJobPosts > 0 ? (permanentJobPosts/totalJobPosts)*100 : 50}%`, backgroundColor: '#3b82f6', height: '100%' }}></div>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                    <span>{totalJobPosts > 0 ? ((dailyJobPosts/totalJobPosts)*100).toFixed(1) : 0}%</span>
                    <span>{totalJobPosts > 0 ? ((permanentJobPosts/totalJobPosts)*100).toFixed(1) : 0}%</span>
                  </div>
                </div>

                {/* Job Applications Metric */}
                <div style={{ padding: '0.9rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <Send size={15} color="#8b5cf6" />
                      <span style={{ fontSize: '0.84rem', fontWeight: 600 }}>Nomzodlar Arizalari</span>
                    </div>
                    <span style={{ fontWeight: 700, color: '#8b5cf6', fontSize: '1rem' }}>{totalApplications} ta</span>
                  </div>
                  <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
                    Qabul qilingan nomzodlar: <b style={{ color: '#10b981' }}>{acceptedApplications} ta</b> (Konversiya: {totalApplications > 0 ? ((acceptedApplications/totalApplications)*100).toFixed(1) : 0}%)
                  </div>
                </div>

                {/* Bot Users Overlap */}
                <div style={{ padding: '0.9rem', backgroundColor: 'var(--bg-inner)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <Sparkles size={15} color="#c084fc" />
                      <span style={{ fontSize: '0.84rem', fontWeight: 600 }}>Ikkala Botdan Foydalanuvchilar</span>
                    </div>
                    <span style={{ fontWeight: 700, color: '#c084fc', fontSize: '1rem' }}>{bothBotUsers} user</span>
                  </div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                    Bir vaqtda ham ish beruvchi, ham ish izlovchi bo'lgan faol mijozlar
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: REGIONAL & MARKETING TARGETING                                     */}
      {/* ========================================================================= */}
      {(activeMetricTab === 'marketing') && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          <div className="card" style={{ margin: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <MapPin size={18} color="#ef4444" />
                  <h3 className="card-title" style={{ margin: 0 }}>Viloyatlar Kesimida Marketing & Auditoriya Tahlili</h3>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0.2rem 0 0 0' }}>
                  Qaysi viloyatlarda ishchilar yoki ish beruvchilar soni yuqori ekanligi bo'yicha to'liq reyting
                </p>
              </div>
              <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa' }}>
                Jami faol hududlar: {regionsData.length} ta
              </span>
            </div>

            {regionsData.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                Viloyatlar bo'yicha ma'lumotlar mavjud emas.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {regionsData.map((reg, idx) => {
                  const barWidth = (reg.total_users / maxRegionUsers) * 100;
                  return (
                    <div key={reg.id || idx} style={{
                      padding: '0.9rem 1.1rem',
                      backgroundColor: 'var(--bg-inner)',
                      borderRadius: '8px',
                      border: '1px solid var(--border-color)'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <span style={{ fontWeight: 700, color: 'var(--text-muted)', fontSize: '0.82rem' }}>#{idx + 1}</span>
                          <span style={{ fontWeight: 600, fontSize: '0.92rem', color: 'var(--text-main)' }}>{reg.name}</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1.2rem', fontSize: '0.82rem' }}>
                          <span style={{ color: '#10b981' }}>👷 <b>{reg.workers}</b> ishchi</span>
                          <span style={{ color: '#3b82f6' }}>👔 <b>{reg.clients}</b> mijoz</span>
                          <span style={{ color: '#8b5cf6' }}>📋 <b>{reg.job_posts}</b> e'lon</span>
                          <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>Jami: {reg.total_users} ({reg.percentage}%)</span>
                        </div>
                      </div>

                      <div className="progress-bar-container">
                        <div 
                          className="progress-bar-fill" 
                          style={{ 
                            width: `${Math.max(barWidth, 3)}%`, 
                            backgroundColor: idx === 0 ? '#10b981' : (idx === 1 ? '#3b82f6' : '#8b5cf6') 
                          }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Marketing Strategic Insight Box */}
          <div style={{
            padding: '1.2rem',
            backgroundColor: 'rgba(59, 130, 246, 0.08)',
            border: '1px solid rgba(59, 130, 246, 0.25)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.9rem'
          }}>
            <Sparkles size={22} color="#3b82f6" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <h4 style={{ margin: '0 0 0.3rem 0', color: '#60a5fa', fontSize: '0.92rem' }}>Marketing & Reklama Tavsiyasi</h4>
              <p style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                Eng yuqori talab mavjud bo'lgan viloyatlarga Telegram va Instagram target reklamalarini yo'naltirish orqali konversiyani 2 barobarga oshirish mumkin. Ishchi soni kam bo'lgan hududlarda maxsus jalb qilish aksiyalarini o'tkazish tavsiya etiladi.
              </p>
            </div>
          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: DEMOGRAPHICS & AUDIENCE BREAKDOWN                                   */}
      {/* ========================================================================= */}
      {(activeMetricTab === 'demographics') && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          
          {/* Languages Distribution */}
          <div className="card" style={{ margin: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <Globe size={18} color="#06b6d4" />
              <h3 className="card-title" style={{ margin: 0 }}>Tillar Bo'yicha Taqsimot</h3>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1.25rem' }}>
              Auditoriyaning afzal ko'rgan til sozlamalari
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {languagesData.map((lang) => {
                const langPercent = totalUsers > 0 ? ((lang.count / totalUsers) * 100).toFixed(1) : 0;
                return (
                  <div key={lang.code}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.3rem' }}>
                      <span style={{ fontWeight: 600 }}>{lang.name}</span>
                      <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>{lang.count} ta ({langPercent}%)</span>
                    </div>
                    <div className="progress-bar-container">
                      <div 
                        className="progress-bar-fill" 
                        style={{ width: `${langPercent}%`, backgroundColor: '#06b6d4' }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Age Distribution */}
          <div className="card" style={{ margin: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <Calendar size={18} color="#f59e0b" />
              <h3 className="card-title" style={{ margin: 0 }}>Yosh Toifalari Segmentatsiyasi</h3>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1.25rem' }}>
              Ishchilar va nomzodlarning yosh chegaralari
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {[
                { label: '18 - 25 yosh (Yoshlar)', count: ageGroups['18_25'] || 0, color: '#10b981' },
                { label: '26 - 35 yosh (Asosiy mehnat)', count: ageGroups['26_35'] || 0, color: '#3b82f6' },
                { label: '36 - 50 yosh (Tajribali)', count: ageGroups['36_50'] || 0, color: '#8b5cf6' },
                { label: '50+ yosh (Katta yoshdagilar)', count: ageGroups['50_plus'] || 0, color: '#f59e0b' },
                { label: 'Ko\'rsatilmagan', count: ageGroups['unspecified'] || 0, color: '#64748b' }
              ].map((item, i) => {
                const percent = ((item.count / totalAgeCount) * 100).toFixed(1);
                return (
                  <div key={i}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.3rem' }}>
                      <span style={{ fontWeight: 500 }}>{item.label}</span>
                      <span style={{ fontWeight: 700 }}>{item.count} ta ({percent}%)</span>
                    </div>
                    <div className="progress-bar-container">
                      <div className="progress-bar-fill" style={{ width: `${percent}%`, backgroundColor: item.color }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Gender Split */}
          <div className="card" style={{ margin: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <Users size={18} color="#ec4899" />
              <h3 className="card-title" style={{ margin: 0 }}>Jins Taqsimoti (Gender)</h3>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '1.25rem' }}>
              Platforma foydalanuvchilarining jinsi bo'yicha nisbati
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.3rem' }}>
                  <span style={{ fontWeight: 600, color: '#3b82f6' }}>👨 Erkak</span>
                  <span style={{ fontWeight: 700 }}>{genderData.male} ta ({((genderData.male / totalGenderCount) * 100).toFixed(1)}%)</span>
                </div>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${(genderData.male / totalGenderCount) * 100}%`, backgroundColor: '#3b82f6' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.3rem' }}>
                  <span style={{ fontWeight: 600, color: '#ec4899' }}>👩 Ayol</span>
                  <span style={{ fontWeight: 700 }}>{genderData.female} ta ({((genderData.female / totalGenderCount) * 100).toFixed(1)}%)</span>
                </div>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${(genderData.female / totalGenderCount) * 100}%`, backgroundColor: '#ec4899' }} />
                </div>
              </div>

              {genderData.unknown > 0 && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.3rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Aniq kiritilmagan</span>
                    <span style={{ fontWeight: 600 }}>{genderData.unknown} ta ({((genderData.unknown / totalGenderCount) * 100).toFixed(1)}%)</span>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${(genderData.unknown / totalGenderCount) * 100}%`, backgroundColor: '#64748b' }} />
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 4: CATEGORIES & SUPPLY-DEMAND BALANCE                                 */}
      {/* ========================================================================= */}
      {(activeMetricTab === 'categories') && (
        <div className="card" style={{ margin: 0 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Layers size={18} color="#10b981" />
                <h3 className="card-title" style={{ margin: 0 }}>Sohalar Bo'yicha Talab va Taklif Balansi</h3>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0.2rem 0 0 0' }}>
                Har bir yo'nalish bo'yicha e'lonlar, buyurtmalar, mavjud ustalar va moliyaviy aylanma
              </p>
            </div>
          </div>

          {categoryDistribution.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
              Kategoriyalar bo'yicha ma'lumotlar mavjud emas.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {categoryDistribution.map((cat, idx) => (
                <div key={cat.id || idx} style={{
                  padding: '1rem',
                  backgroundColor: 'var(--bg-inner)',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ fontSize: '1.2rem' }}>{cat.icon || '🛠'}</span>
                      <span style={{ fontWeight: 700, fontSize: '0.94rem', color: 'var(--text-main)' }}>{cat.name}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', fontSize: '0.82rem' }}>
                      <span style={{ color: '#3b82f6' }}>📋 E'lonlar: <b>{cat.job_posts_count || 0} ta</b></span>
                      <span style={{ color: '#10b981' }}>📦 Buyurtmalar: <b>{cat.order_count || 0} ta</b></span>
                      <span style={{ color: '#f59e0b' }}>👷 Ustalar: <b>{cat.workers_count || 0} ta</b></span>
                      <span style={{ fontWeight: 700, color: '#10b981' }}>{cat.revenue.toLocaleString()} SUM</span>
                    </div>
                  </div>

                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar-fill" 
                      style={{ 
                        width: `${Math.max(cat.percentage, 4)}%`, 
                        backgroundColor: idx === 0 ? '#10b981' : (idx === 1 ? '#3b82f6' : '#8b5cf6') 
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
}
