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
  SlidersHorizontal,
  Radio,
  Zap,
  Activity
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

      L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a>',
        maxZoom: 19,
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
    // 1. RENDER JOB POSTS (Jonli Ish E'lonlari)
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
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2.5px solid #ffffff;
            box-shadow: 0 4px 18px rgba(236, 72, 153, 0.6);
            font-size: 22px;
            cursor: pointer;
            transition: transform 0.2s ease;
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
              padding: 2px 5px;
              border-radius: 6px;
              border: 1.5px solid white;
              box-shadow: 0 2px 5px rgba(0,0,0,0.3);
              letter-spacing: 0.3px;
            ">ISH</span>
          </div>
        `;

        const jobIcon = L.divIcon({
          className: 'custom-job-pin',
          html: jobMarkerHtml,
          iconSize: [44, 44],
          iconAnchor: [22, 22],
          popupAnchor: [0, -24],
        });

        const popupHtml = `
          <div style="font-family: inherit; min-width: 250px; padding: 6px 2px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
              <span style="font-size: 26px; background: rgba(236, 72, 153, 0.12); padding: 4px; border-radius: 8px;">${catIcon}</span>
              <div>
                <span style="background: rgba(236, 72, 153, 0.18); color: #ec4899; font-size: 10px; font-weight: 800; padding: 2px 7px; border-radius: 6px; text-transform: uppercase;">
                  ${jp.category_detail?.name_uz || 'Soha'}
                </span>
                <div style="font-weight: 800; font-size: 14px; color: var(--text-main); margin-top: 3px;">
                  #${jp.id} ${posName}
                </div>
              </div>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 4px; margin-bottom: 8px;">
              <div style="font-size: 13px; color: #10b981; font-weight: 700;">
                💰 Haq / Oylik: ${price}
              </div>
              <div style="font-size: 12px; color: #f59e0b; font-weight: 600;">
                ⏱ Boshlanish: ${startType}
              </div>
              <div style="font-size: 12px; color: var(--text-secondary);">
                👤 Ish beruvchi: <strong>${empName}</strong>
              </div>
              <div style="font-size: 11px; color: var(--text-muted);">
                📍 Manzil: ${jp.region_detail?.name || ''} ${jp.district || ''} ${jp.address || ''}
              </div>
              ${jp.description ? `<div style="font-size: 11px; color: var(--text-secondary); font-style: italic; background: var(--bg-inner); padding: 6px 8px; border-radius: 6px; margin-top: 2px; border-left: 3px solid #ec4899;">"${jp.description}"</div>` : ''}
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; border-top: 1px solid var(--border-color); padding-top: 6px;">
              <span>👥 Talab: <b>${jp.workers_count || '1 nafar'}</b></span>
              <a href="tel:${jp.contact_phone}" style="color: #3b82f6; text-decoration: none; font-weight: 800; background: rgba(59, 130, 246, 0.1); padding: 3px 8px; border-radius: 6px;">
                📞 ${jp.contact_phone}
              </a>
            </div>
          </div>
        `;

        const tooltipHtml = `<b>💼 #${jp.id} ${posName}</b><br/><span style="color:#10b981;">💰 ${price}</span>`;

        L.marker([lat, lng], { icon: jobIcon })
          .addTo(markersLayerRef.current)
          .bindTooltip(tooltipHtml, { direction: 'top', offset: [0, -22] })
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

      let pinBg = '#10b981';
      let pinSvg = workerHatSvg;
      let badgeText = 'USTA';
      let badgeColor = '#10b981';
      let pulseRing = '';
      let statusLabel = 'Offline';
      let statusColor = '#94a3b8';

      if (user.user_type === 'DUAL') {
        // Dual: Both Employer and Worker
        pinBg = 'linear-gradient(135deg, #0284c7, #f97316)';
        pinSvg = dualUserSvg;
        badgeText = 'USTA + MIJOZ';
        badgeColor = '#f97316';
        statusLabel = user.is_online ? 'Online' : 'Offline';
        statusColor = user.is_online ? '#10b981' : '#94a3b8';
      } else if (user.user_type === 'EMPLOYER') {
        // Pure Employer
        pinBg = 'linear-gradient(135deg, #8b5cf6, #6366f1)';
        pinSvg = employerBldgSvg;
        badgeText = 'ISH BERUVCHI';
        badgeColor = '#8b5cf6';
        statusLabel = 'Mijoz';
        statusColor = '#8b5cf6';
      } else {
        // Pure Worker
        if (user.is_online && user.is_busy) {
          pinBg = 'linear-gradient(135deg, #f59e0b, #d97706)'; // busy
          badgeColor = '#f59e0b';
          badgeText = 'BAND';
          statusLabel = 'Band (Ishda)';
          statusColor = '#f59e0b';
        } else if (user.is_online) {
          pinBg = 'linear-gradient(135deg, #10b981, #059669)'; // online
          badgeColor = '#10b981';
          badgeText = 'ONLINE';
          statusLabel = 'Online (Bo\'sh)';
          statusColor = '#10b981';
          pulseRing = `
            <span style="
              position: absolute;
              width: 100%;
              height: 100%;
              border-radius: 50%;
              border: 2px solid #10b981;
              animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
              opacity: 0.75;
            "></span>
          `;
        } else {
          pinBg = '#64748b'; // offline
          badgeColor = '#64748b';
          badgeText = 'OFFLINE';
          statusLabel = 'Offline';
          statusColor = '#94a3b8';
        }
      }

      const userMarkerHtml = `
        <div style="
          position: relative;
          background: ${pinBg};
          width: 42px;
          height: 42px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2.5px solid #ffffff;
          box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
          color: #ffffff;
          cursor: pointer;
          transition: transform 0.2s ease;
        ">
          ${pulseRing}
          ${pinSvg}
          <span style="
            position: absolute;
            bottom: -6px;
            right: -6px;
            background: ${badgeColor};
            color: white;
            font-size: 8px;
            font-weight: 800;
            padding: 1.5px 4px;
            border-radius: 5px;
            border: 1px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.35);
            white-space: nowrap;
          ">${badgeText}</span>
        </div>
      `;

      const userIcon = L.divIcon({
        className: 'custom-user-pin',
        html: userMarkerHtml,
        iconSize: [42, 42],
        iconAnchor: [21, 21],
        popupAnchor: [0, -22],
      });

      const fullName = `${user.first_name || user.username || 'Foydalanuvchi'} ${user.last_name || ''}`.trim();
      const specialtyName = user.specialty || user.position_details?.name_uz || user.category_details?.name_uz || 'Mutaxassis';

      const userPopup = `
        <div style="font-family: inherit; min-width: 240px; padding: 6px 2px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; border-bottom: 1px solid var(--border-color); padding-bottom: 6px;">
            <span style="background: ${badgeColor}; color: white; font-size: 9px; font-weight: 800; padding: 2px 7px; border-radius: 5px; text-transform: uppercase;">
              ${badgeText}
            </span>
            <span style="font-size: 11px; font-weight: 700; color: ${statusColor};">
              ● ${statusLabel}
            </span>
          </div>

          <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px; color: var(--text-main);">
            ${fullName}
          </div>

          ${user.user_type !== 'EMPLOYER' ? `
            <div style="font-size: 12px; color: #38bdf8; font-weight: 700; margin-bottom: 3px;">
              🛠 ${specialtyName}
            </div>
            <div style="font-size: 12px; color: #fbbf24; font-weight: 700; margin-bottom: 4px;">
              ⭐️ Reyting: ${user.rating || 5.0} / 5.0 (${user.completed_jobs_count || 0} ta ish)
            </div>
          ` : `
            <div style="font-size: 12px; color: #a78bfa; font-weight: 700; margin-bottom: 4px;">
              🏢 Buyurtmachi / Ish beruvchi
            </div>
          `}

          <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
            📍 ${user.region_name || ''} ${user.district || ''} ${user.street_address || user.address_title || ''}
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 6px; margin-top: 4px;">
            <span style="font-size: 11px; color: var(--text-muted);">
              TG ID: <b>${user.telegram_id || user.id}</b>
            </span>
            ${user.phone_number ? `
              <a href="tel:${user.phone_number}" style="color: #10b981; text-decoration: none; font-weight: 800; font-size: 11px; background: rgba(16, 185, 129, 0.12); padding: 3px 8px; border-radius: 6px;">
                📞 ${user.phone_number}
              </a>
            ` : '<span style="font-size: 11px; color: var(--text-muted);">Tel yo\'q</span>'}
          </div>
        </div>
      `;

      const tooltipText = `<b>${fullName}</b><br/><span style="color:${statusColor};">● ${badgeText}: ${specialtyName}</span>`;

      L.marker([lat, lng], { icon: userIcon })
        .addTo(markersLayerRef.current)
        .bindTooltip(tooltipText, { direction: 'top', offset: [0, -22] })
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
            background: linear-gradient(135deg, #ef4444, #b91c1c);
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #ffffff;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.6);
            color: #ffffff;
            font-size: 18px;
            cursor: pointer;
          ">📦</div>`,
          iconSize: [36, 36],
          iconAnchor: [18, 18],
          popupAnchor: [0, -20],
        });

        const popupHtml = `
          <div style="font-family: inherit; min-width: 230px; padding: 6px 2px;">
            <div style="font-weight: 800; font-size: 14px; margin-bottom: 4px; color: var(--text-main); border-bottom: 1px solid var(--border-color); padding-bottom: 4px;">
              Buyurtma #${order.id}: ${order.title}
            </div>
            <div style="font-size: 12px; color: #10b981; font-weight: 700; margin-bottom: 4px;">
              Narx: ${order.price ? Number(order.price).toLocaleString() : 0} SUM
            </div>
            <div style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary);">
              Mijoz: <strong>${order.customer_name}</strong>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">
              📍 Manzil: ${order.address}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; border-top: 1px solid var(--border-color); padding-top: 4px;">
              <span style="font-weight: 700; color: #ef4444;">Status: ${order.status}</span>
              <a href="tel:${order.customer_phone}" style="color: #3b82f6; text-decoration: none; font-weight: 800;">
                📞 ${order.customer_phone}
              </a>
            </div>
          </div>
        `;

        L.marker([lat, lng], { icon: orderIcon })
          .addTo(markersLayerRef.current)
          .bindTooltip(`<b>📦 #${order.id} ${order.title}</b>`, { direction: 'top', offset: [0, -20] })
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
              Jonli ish e'lonlari (soha logosi bilan), ishchilar, mijozlar va ikkala botdan foydalanuvchilarning interaktiv xaritasi
            </p>
          </div>

          {/* Right Action Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              onClick={handleManualRecenter}
              style={{
                padding: '0.45rem 0.85rem',
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
              <Compass size={15} color="#3b82f6" />
              <span>Markazga qaytarish</span>
            </button>

            {/* Category Dropdown Filter */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', background: 'var(--bg-inner)', padding: '0.4rem 0.75rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
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
            <span>Ustalar / Ishchilar ({pureWorkersWithLoc})</span>
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
              borderColor: showDualUsers ? '#f97316' : 'var(--border-color)',
              background: showDualUsers ? 'rgba(249, 115, 22, 0.15)' : 'var(--bg-inner)',
              color: showDualUsers ? '#f97316' : 'var(--text-muted)',
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
            <span>Ham Usta + Ham Ish Beruvchi ({dualUsersCount})</span>
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
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Xaritadagi Ustalar</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981', marginTop: '0.15rem' }}>{pureWorkersWithLoc} nafar</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Ish Beruvchilar</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#8b5cf6', marginTop: '0.15rem' }}>{employersWithLoc} nafar</div>
          </div>
          <div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 600 }}>Dual (Ikkala roldagi)</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f97316', marginTop: '0.15rem' }}>{dualUsersCount} nafar</div>
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
        <span style={{ fontWeight: 700, color: 'var(--text-main)' }}>Xarita shartli belgilari (Legend):</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '14px', height: '14px', borderRadius: '4px', background: 'linear-gradient(135deg, #ec4899, #8b5cf6)', border: '1px solid white' }}></span>
            <span><b>Ish E'loni</b> (Kategoriya belgisi bilan)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '14px', height: '14px', borderRadius: '50%', background: '#10b981', border: '1px solid white' }}></span>
            <span><b>Usta / Ishchi</b> (🟢 Online / 🟡 Band / ⚫️ Offline)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '14px', height: '14px', borderRadius: '50%', background: 'linear-gradient(135deg, #8b5cf6, #6366f1)', border: '1px solid white' }}></span>
            <span><b>Ish Beruvchi</b> (Mijoz)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ display: 'inline-block', width: '14px', height: '14px', borderRadius: '50%', background: 'linear-gradient(135deg, #0284c7, #f97316)', border: '1px solid white' }}></span>
            <span><b>Dual User</b> (Ham Usta + Ham Ish Beruvchi)</span>
          </div>
        </div>
      </div>

    </div>
  );
}
