import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { 
  Compass, 
  Users, 
  Briefcase, 
  HardHat, 
  Building, 
  Repeat, 
  CheckCircle2, 
  Clock, 
  MapPin, 
  Filter, 
  Layers, 
  Flame, 
  Calendar, 
  Phone, 
  Eye,
  SlidersHorizontal
} from 'lucide-react';

export default function LiveMap({ 
  workers = [], 
  locations = [], 
  orders = [], 
  jobPosts = [], 
  allUsers = [], 
  categories = [] 
}) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);
  const initialFitDoneRef = useRef(false);

  // Filters State
  const [showJobPosts, setShowJobPosts] = useState(true);
  const [showWorkers, setShowWorkers] = useState(true);
  const [showEmployers, setShowEmployers] = useState(true);
  const [showDualUsers, setShowDualUsers] = useState(true);
  const [showDirectOrders, setShowDirectOrders] = useState(true);
  
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [onlyOnline, setOnlyOnline] = useState(false);
  const [onlyActiveJobs, setOnlyActiveJobs] = useState(true);

  // Prepare categorized data
  // 1. Dual-role users (Started both worker and client bot OR marked as worker and created jobs)
  // 2. Pure Workers (Only worker)
  // 3. Pure Employers / Clients
  const processedUsers = React.useMemo(() => {
    return allUsers.map(user => {
      const isDual = (user.started_worker_bot && user.started_client_bot) || 
                     (user.role === 'WORKER' && user.started_client_bot) ||
                     (user.role === 'CLIENT' && user.started_worker_bot);
      const isPureWorker = !isDual && (user.role === 'WORKER' || user.started_worker_bot);
      const isPureEmployer = !isDual && (user.role === 'CLIENT' || user.started_client_bot);
      
      return {
        ...user,
        user_type: isDual ? 'DUAL' : (isPureWorker ? 'WORKER' : (isPureEmployer ? 'EMPLOYER' : 'OTHER'))
      };
    });
  }, [allUsers]);

  // Live active jobs
  const activeJobPosts = React.useMemo(() => {
    return jobPosts.filter(jp => {
      if (onlyActiveJobs && jp.status !== 'active') return false;
      if (selectedCategory !== 'ALL' && jp.category !== parseInt(selectedCategory) && jp.category_detail?.id !== parseInt(selectedCategory)) {
        return false;
      }
      return Boolean(jp.latitude && jp.longitude);
    });
  }, [jobPosts, onlyActiveJobs, selectedCategory]);

  // Active Direct Orders (Call Center)
  const activeOrders = React.useMemo(() => {
    return orders.filter(o => {
      if (selectedCategory !== 'ALL' && o.category !== parseInt(selectedCategory) && o.category_detail?.id !== parseInt(selectedCategory)) {
        return false;
      }
      return Boolean(o.latitude && o.longitude && o.status !== 'CANCELLED' && o.status !== 'FINISHED');
    });
  }, [orders, selectedCategory]);

  // Online & Busy stats
  const onlineWorkersCount = workers.filter(w => w.is_online).length;
  const dualUsersCount = processedUsers.filter(u => u.user_type === 'DUAL' && (u.latitude || locations.some(l => l.worker === u.id))).length;
  const pureWorkersWithLoc = processedUsers.filter(u => u.user_type === 'WORKER' && (u.latitude || locations.some(l => l.worker === u.id))).length;
  const employersWithLoc = processedUsers.filter(u => u.user_type === 'EMPLOYER' && u.latitude).length;

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize Leaflet Map once
    if (!mapInstanceRef.current) {
      const map = L.map(mapRef.current, {
        center: [41.311081, 69.240562], // Tashkent
        zoom: 12,
        zoomControl: true,
      });

      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20,
      }).addTo(map);

      const markersGroup = L.layerGroup().addTo(map);
      markersLayerRef.current = markersGroup;
      mapInstanceRef.current = map;
    }

    // Clear previous markers
    if (markersLayerRef.current) {
      markersLayerRef.current.clearLayers();
    }

    const bounds = [];

    // Helper SVG Icons
    const workerHatSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6h0"/><path d="M14 6h0a6 6 0 0 1 6 6v3"/></svg>`;
    const employerBldgSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>`;
    const dualUserSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/></svg>`;

    // =========================================================================
    // 1. RENDER JOB POSTS (Ayni paytdagi jonli ishlar - Kategoriya logolari bilan)
    // =========================================================================
    if (showJobPosts) {
      activeJobPosts.forEach(jp => {
        const lat = parseFloat(jp.latitude);
        const lng = parseFloat(jp.longitude);
        if (isNaN(lat) || isNaN(lng)) return;
        bounds.push([lat, lng]);

        const catIcon = jp.category_detail?.icon || '💼';
        const posName = jp.position_detail?.name_uz || jp.custom_position_name || 'Ish e\'loni';
        const empName = jp.contact_name || jp.employer_detail?.first_name || 'Ish beruvchi';
        const price = jp.price_amount ? `${jp.price_amount}` : (jp.is_price_negotiable ? 'Kelishiladi' : 'Narx ko\'rsatilmagan');
        const startType = jp.start_time_type === 'urgent' ? '🔥 Shoshilinch (Bugun)' : (jp.start_time_type === 'tomorrow' ? '🗓 Ertaga' : (jp.custom_start_date || 'Kelishilgan'));

        const jobMarkerHtml = `
          <div style="
            position: relative;
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2.5px solid #ffffff;
            box-shadow: 0 4px 16px rgba(236, 72, 153, 0.55);
            font-size: 20px;
            cursor: pointer;
            transition: transform 0.2s;
          ">
            <span>${catIcon}</span>
            <span style="
              position: absolute;
              bottom: -6px;
              right: -6px;
              background: #10b981;
              color: white;
              font-size: 9px;
              font-weight: 800;
              padding: 1px 4px;
              border-radius: 6px;
              border: 1px solid white;
              box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            ">ISH</span>
          </div>
        `;

        const jobIcon = L.divIcon({
          className: 'custom-job-pin',
          html: jobMarkerHtml,
          iconSize: [42, 42],
          iconAnchor: [21, 21],
          popupAnchor: [0, -22],
        });

        const popupHtml = `
          <div style="font-family: inherit; min-width: 230px; padding: 4px;">
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
              <span style="font-size: 22px;">${catIcon}</span>
              <div>
                <span style="background: rgba(236, 72, 153, 0.15); color: #ec4899; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">
                  ${jp.category_detail?.name_uz || 'Soha'}
                </span>
                <div style="font-weight: 800; font-size: 14px; color: var(--text-main); margin-top: 2px;">
                  #${jp.id} ${posName}
                </div>
              </div>
            </div>
            
            <div style="font-size: 12px; color: #10b981; font-weight: 700; margin-bottom: 4px;">
              💰 Ish haqi: ${price}
            </div>
            <div style="font-size: 12px; color: #f59e0b; font-weight: 600; margin-bottom: 4px;">
              ⏱ Vaqt: ${startType}
            </div>
            <div style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary);">
              👤 Ish beruvchi: <strong>${empName}</strong>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
              📍 Manzil: ${jp.region_detail?.name || ''} ${jp.district || ''} ${jp.address || ''}
            </div>
            ${jp.description ? `<div style="font-size: 11px; color: var(--text-muted); font-style: italic; background: var(--bg-inner); padding: 4px 6px; border-radius: 4px; margin-bottom: 6px;">"${jp.description}"</div>` : ''}
            <div style="display: flex; justify-content: space-between; font-size: 11px; border-top: 1px solid var(--border-color); padding-top: 4px;">
              <span>👥 Talab: <b>${jp.workers_count || '1 nafar'}</b></span>
              <span>📞 <b>${jp.contact_phone}</b></span>
            </div>
          </div>
        `;

        L.marker([lat, lng], { icon: jobIcon })
          .addTo(markersLayerRef.current)
          .bindPopup(popupHtml);
      });
    }

    // =========================================================================
    // 2. RENDER USERS (Workers, Employers, Dual-Role Users)
    // =========================================================================
    processedUsers.forEach(user => {
      // Find location (either direct user lat/lng or from live locations)
      let lat = parseFloat(user.latitude);
      let lng = parseFloat(user.longitude);

      const liveLoc = locations.find(l => l.worker === user.id);
      if (liveLoc && liveLoc.latitude && liveLoc.longitude) {
        lat = parseFloat(liveLoc.latitude);
        lng = parseFloat(liveLoc.longitude);
      }

      if (isNaN(lat) || isNaN(lng)) return;

      // Filter checks
      if (user.user_type === 'DUAL' && !showDualUsers) return;
      if (user.user_type === 'WORKER' && !showWorkers) return;
      if (user.user_type === 'EMPLOYER' && !showEmployers) return;
      if (onlyOnline && !user.is_online) return;

      if (selectedCategory !== 'ALL') {
        const matchesCat = user.category === parseInt(selectedCategory) || 
                           user.category_details?.id === parseInt(selectedCategory) ||
                           (user.selected_positions && user.selected_positions.some(p => p.category === parseInt(selectedCategory)));
        if (!matchesCat) return;
      }

      bounds.push([lat, lng]);

      let pinBg = '#3b82f6';
      let pinSvg = workerHatSvg;
      let badgeText = 'USTA';
      let badgeColor = '#3b82f6';
      let statusHtml = '';

      if (user.user_type === 'DUAL') {
        // Dual: Both Employer and Worker
        pinBg = 'linear-gradient(135deg, #3b82f6, #f59e0b)';
        pinSvg = dualUserSvg;
        badgeText = 'USTA + MIJOZ';
        badgeColor = '#f59e0b';
      } else if (user.user_type === 'EMPLOYER') {
        // Pure Employer
        pinBg = '#8b5cf6';
        pinSvg = employerBldgSvg;
        badgeText = 'ISH BERUVCHI';
        badgeColor = '#8b5cf6';
      } else {
        // Pure Worker
        if (user.is_online && user.is_busy) {
          pinBg = '#f59e0b'; // busy
          statusHtml = '<span style="color:#f59e0b; font-weight:700;">Band (Ishda)</span>';
        } else if (user.is_online) {
          pinBg = '#10b981'; // online
          statusHtml = '<span style="color:#10b981; font-weight:700;">Online (Bo\'sh)</span>';
        } else {
          pinBg = '#64748b'; // offline
          statusHtml = '<span style="color:#94a3b8; font-weight:700;">Offline</span>';
        }
      }

      const userMarkerHtml = `
        <div style="
          position: relative;
          background: ${pinBg};
          width: 38px;
          height: 38px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid #ffffff;
          box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4);
          color: #ffffff;
          cursor: pointer;
        ">
          ${pinSvg}
          <span style="
            position: absolute;
            bottom: -5px;
            right: -5px;
            background: ${badgeColor};
            color: white;
            font-size: 8px;
            font-weight: 800;
            padding: 1px 4px;
            border-radius: 4px;
            border: 1px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
          ">${badgeText}</span>
        </div>
      `;

      const userIcon = L.divIcon({
        className: 'custom-user-pin',
        html: userMarkerHtml,
        iconSize: [38, 38],
        iconAnchor: [19, 19],
        popupAnchor: [0, -20],
      });

      const fullName = `${user.first_name || user.username || 'Foydalanuvchi'} ${user.last_name || ''}`.trim();
      const specialtyName = user.specialty || user.position_details?.name_uz || user.category_details?.name_uz || 'Mutaxassis';

      const userPopup = `
        <div style="font-family: inherit; min-width: 210px; padding: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="background: ${badgeColor}; color: white; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 4px;">
              ${badgeText}
            </span>
            ${user.user_type === 'WORKER' || user.user_type === 'DUAL' ? `<span style="font-size: 11px;">${statusHtml}</span>` : ''}
          </div>

          <div style="font-weight: 800; font-size: 14px; margin-bottom: 3px; color: var(--text-main);">
            ${fullName}
          </div>

          ${user.user_type !== 'EMPLOYER' ? `
            <div style="font-size: 12px; color: #38bdf8; font-weight: 600; margin-bottom: 3px;">
              🛠 ${specialtyName}
            </div>
            <div style="font-size: 12px; color: #fbbf24; font-weight: 700; margin-bottom: 3px;">
              ⭐️ Reyting: ${user.rating || 5.0} / 5.0 (${user.completed_jobs_count || 0} ta ish)
            </div>
          ` : `
            <div style="font-size: 12px; color: #a78bfa; font-weight: 600; margin-bottom: 3px;">
              🏢 Buyurtmachi / Ish beruvchi
            </div>
          `}

          <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 3px;">
            📍 ${user.region_name || ''} ${user.district || ''} ${user.street_address || user.address_title || ''}
          </div>
          <div style="font-size: 11px; color: var(--text-muted); border-top: 1px solid var(--border-color); padding-top: 4px; margin-top: 4px;">
            📞 Tel: <b>${user.phone_number || 'Ko\'rsatilmagan'}</b>
          </div>
        </div>
      `;

      L.marker([lat, lng], { icon: userIcon })
        .addTo(markersLayerRef.current)
        .bindPopup(userPopup);
    });

    // =========================================================================
    // 3. RENDER CALL-CENTER DIRECT ORDERS (Agar mavjud bo'lsa)
    // =========================================================================
    if (showDirectOrders) {
      activeOrders.forEach(order => {
        const lat = parseFloat(order.latitude);
        const lng = parseFloat(order.longitude);
        if (isNaN(lat) || isNaN(lng)) return;
        bounds.push([lat, lng]);

        const orderIcon = L.divIcon({
          className: 'custom-order-pin',
          html: `<div style="
            background: #ef4444;
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #ffffff;
            box-shadow: 0 0 12px #ef4444;
            color: #ffffff;
            font-size: 16px;
          ">📦</div>`,
          iconSize: [34, 34],
          iconAnchor: [17, 17],
          popupAnchor: [0, -17],
        });

        const popupHtml = `
          <div style="font-family: inherit; min-width: 210px; padding: 4px;">
            <div style="font-weight: 800; font-size: 14px; margin-bottom: 4px; color: var(--text-main);">
              Buyurtma #${order.id}: ${order.title}
            </div>
            <div style="font-size: 12px; color: #10b981; font-weight: 700; margin-bottom: 4px;">
              Narx: ${order.price ? Number(order.price).toLocaleString() : 0} SUM
            </div>
            <div style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary);">
              Mijoz: <strong>${order.customer_name}</strong> (Tel: ${order.customer_phone})
            </div>
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">
              Manzil: ${order.address}
            </div>
            <div style="font-size: 11px; font-weight: 700;">
              Status: <span style="color: #ef4444;">${order.status}</span>
            </div>
          </div>
        `;

        L.marker([lat, lng], { icon: orderIcon })
          .addTo(markersLayerRef.current)
          .bindPopup(popupHtml);
      });
    }

    // Auto fit bounds only ONCE on initial load (not on every 5s polling refresh)
    if (!initialFitDoneRef.current && bounds.length > 0 && mapInstanceRef.current) {
      mapInstanceRef.current.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
      initialFitDoneRef.current = true;
    }

  }, [
    activeJobPosts, 
    processedUsers, 
    activeOrders, 
    locations, 
    showJobPosts, 
    showWorkers, 
    showEmployers, 
    showDualUsers, 
    showDirectOrders, 
    onlyOnline,
    selectedCategory
  ]);

  const handleManualRecenter = () => {
    if (!mapInstanceRef.current) return;
    const bounds = [];
    
    activeJobPosts.forEach(jp => {
      if (jp.latitude && jp.longitude) bounds.push([parseFloat(jp.latitude), parseFloat(jp.longitude)]);
    });
    processedUsers.forEach(u => {
      if (u.latitude && u.longitude) bounds.push([parseFloat(u.latitude), parseFloat(u.longitude)]);
    });
    locations.forEach(l => {
      if (l.latitude && l.longitude) bounds.push([parseFloat(l.latitude), parseFloat(l.longitude)]);
    });

    if (bounds.length > 0) {
      mapInstanceRef.current.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    } else {
      mapInstanceRef.current.setView([41.311081, 69.240562], 12);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      
      {/* Top Controls & Metrics Bar */}
      <div className="card" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <h2 className="card-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Compass size={22} color="#3b82f6" />
              Jonli Xarita & GPS Monitoring (E'lonlar, Ishchilar va Ish beruvchilar)
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.2rem' }}>
              Jonli ish e'lonlari (kategoriyalar logosi bilan), ish izlovchilar, ish beruvchilar va ikkala botda faol foydalanuvchilarning interaktiv xaritasi
            </p>
          </div>

          {/* Right Action Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              onClick={handleManualRecenter}
              style={{
                padding: '0.4rem 0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                background: 'var(--bg-inner)',
                color: 'var(--text-main)',
                fontSize: '0.82rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem',
                cursor: 'pointer',
                transition: 'all 0.15s'
              }}
              title="Xaritani markazlashtirish"
            >
              <Compass size={14} color="#3b82f6" />
              <span>Markazga qaytarish</span>
            </button>

            {/* Category Dropdown Filter */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', background: 'var(--bg-inner)', padding: '0.35rem 0.65rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <Filter size={15} color="var(--text-muted)" />
              <select 
                value={selectedCategory} 
                onChange={(e) => setSelectedCategory(e.target.value)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-main)',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                <option value="ALL">Barcha Sohalar (Kategoriyalar)</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.icon} {c.name_uz || c.name}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Layer Toggle Badges */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
          <button
            onClick={() => setShowJobPosts(!showJobPosts)}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid',
              borderColor: showJobPosts ? '#ec4899' : 'var(--border-color)',
              background: showJobPosts ? 'rgba(236, 72, 153, 0.15)' : 'var(--bg-inner)',
              color: showJobPosts ? '#ec4899' : 'var(--text-muted)',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              cursor: 'pointer',
              transition: 'all 0.15s'
            }}
          >
            <span>💼</span>
            <span>Ish E'lonlari ({activeJobPosts.length})</span>
          </button>

          <button
            onClick={() => setShowWorkers(!showWorkers)}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid',
              borderColor: showWorkers ? '#10b981' : 'var(--border-color)',
              background: showWorkers ? 'rgba(16, 185, 129, 0.15)' : 'var(--bg-inner)',
              color: showWorkers ? '#10b981' : 'var(--text-muted)',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              cursor: 'pointer',
              transition: 'all 0.15s'
            }}
          >
            <HardHat size={15} />
            <span>Ishchilar / Ustalar ({pureWorkersWithLoc})</span>
          </button>

          <button
            onClick={() => setShowEmployers(!showEmployers)}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid',
              borderColor: showEmployers ? '#8b5cf6' : 'var(--border-color)',
              background: showEmployers ? 'rgba(139, 92, 246, 0.15)' : 'var(--bg-inner)',
              color: showEmployers ? '#8b5cf6' : 'var(--text-muted)',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              cursor: 'pointer',
              transition: 'all 0.15s'
            }}
          >
            <Building size={15} />
            <span>Ish Beruvchilar ({employersWithLoc})</span>
          </button>

          <button
            onClick={() => setShowDualUsers(!showDualUsers)}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid',
              borderColor: showDualUsers ? '#f59e0b' : 'var(--border-color)',
              background: showDualUsers ? 'rgba(245, 158, 11, 0.15)' : 'var(--bg-inner)',
              color: showDualUsers ? '#f59e0b' : 'var(--text-muted)',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              cursor: 'pointer',
              transition: 'all 0.15s'
            }}
          >
            <Repeat size={15} />
            <span>Ham Ishchi + Ham Ish Beruvchi ({dualUsersCount})</span>
          </button>

          <button
            onClick={() => setOnlyOnline(!onlyOnline)}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid',
              borderColor: onlyOnline ? '#3b82f6' : 'var(--border-color)',
              background: onlyOnline ? 'rgba(59, 130, 246, 0.15)' : 'var(--bg-inner)',
              color: onlyOnline ? '#3b82f6' : 'var(--text-muted)',
              fontSize: '0.82rem',
              fontWeight: 700,
              cursor: 'pointer',
              marginLeft: 'auto',
              transition: 'all 0.15s'
            }}
          >
            Faqat Online ({onlyOnline ? 'Ha' : 'Barchasi'})
          </button>
        </div>

        {/* Live Counters */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '1rem',
          padding: '0.85rem 1rem',
          backgroundColor: 'var(--bg-inner)',
          borderRadius: '10px',
          border: '1px solid var(--border-color)'
        }}>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Faol Ish E'lonlari</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#ec4899', marginTop: '0.15rem' }}>{activeJobPosts.length} ta</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Xaritadagi Ishchilar</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981', marginTop: '0.15rem' }}>{pureWorkersWithLoc} nafar</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Ish Beruvchilar</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#8b5cf6', marginTop: '0.15rem' }}>{employersWithLoc} nafar</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Dual (Ikkala roldagi) Userlar</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f59e0b', marginTop: '0.15rem' }}>{dualUsersCount} nafar</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Call Center Buyurtmalari</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#3b82f6', marginTop: '0.15rem' }}>{activeOrders.length} ta</div>
          </div>
        </div>
      </div>

      {/* Map Container */}
      <div className="card" style={{ padding: '0.5rem', overflow: 'hidden' }}>
        <div id="map-container" ref={mapRef} style={{ width: '100%', height: '580px', borderRadius: '10px' }}></div>
      </div>

      {/* Legend & Help Info */}
      <div className="card" style={{ padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', fontSize: '0.8rem' }}>
        <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>Xarita shartli belgilari:</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '3px', background: 'linear-gradient(135deg, #ec4899, #8b5cf6)' }}></span>
            <span>Ish e'loni (soha logosi bilan)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#10b981' }}></span>
            <span>Ishchi / Usta</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#8b5cf6' }}></span>
            <span>Ish beruvchi (Mijoz)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: 'linear-gradient(135deg, #3b82f6, #f59e0b)' }}></span>
            <span>Ham Ishchi + Ham Ish beruvchi</span>
          </div>
        </div>
      </div>

    </div>
  );
}
