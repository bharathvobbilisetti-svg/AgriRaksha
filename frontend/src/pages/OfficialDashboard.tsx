import React, { useState, useEffect, useRef } from 'react';
import {
  MapPin, ShieldAlert, Bug, BarChart3, TrendingUp, Users,
  CheckCircle2, Clock, Filter, AlertTriangle, Layers, Eye
} from 'lucide-react';
import L from 'leaflet';
import { Language, translations } from '../i18n/translations';
import { api } from '../services/api';
import { DashboardStats } from '../types';

interface OfficialDashboardProps {
  language: Language;
}

export const OfficialDashboard: React.FC<OfficialDashboardProps> = ({ language }) => {
  const t = translations[language];

  // Official statistics state
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [clusters, setClusters] = useState<any[]>([]);
  const [activeCropFilter, setActiveCropFilter] = useState('All');
  const [activeRiskFilter, setActiveRiskFilter] = useState('All');
  const [activeVillageFilter, setActiveVillageFilter] = useState('All');

  // Leaflet map container ref
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerGroupRef = useRef<L.LayerGroup | null>(null);

  // Load dashboard stats & clusters
  const loadDashboardData = async () => {
    try {
      const [statsData, clustersData, geojsonData] = await Promise.all([
        api.getDashboardStats(),
        api.getHotspotClusters(),
        api.getHotspotsGeoJSON()
      ]);
      setStats(statsData);
      setClusters(clustersData);
      renderMapFeatures(geojsonData);
    } catch (err) {
      console.error("Dashboard data load error:", err);
    }
  };

  // Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Centered around the Visakhapatnam sample cluster in Andhra Pradesh.
    const map = L.map(mapContainerRef.current).setView([17.6868, 83.2185], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors | AgriRaksha SIH 2026',
      maxZoom: 18
    }).addTo(map);

    const layerGroup = L.layerGroup().addTo(map);
    layerGroupRef.current = layerGroup;
    mapInstanceRef.current = map;

    loadDashboardData();

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Render GeoJSON features onto Leaflet Map
  const renderMapFeatures = (geojson: any) => {
    if (!layerGroupRef.current || !geojson?.features) return;
    layerGroupRef.current.clearLayers();

    // 1. Add epidemic buffer circle around the Visakhapatnam sample cluster.
    const outbreakBuffer = L.circle([17.6868, 83.2185], {
      color: '#EF4444',
      fillColor: '#F87171',
      fillOpacity: 0.22,
      radius: 5000 // 5km radius buffer
    }).bindPopup(`
      <div style="font-family: sans-serif; padding: 4px;">
        <strong style="color: #991B1B;">⚠️ Priority Epidemic Containment Zone</strong><br/>
        <b>Location:</b> Visakhapatnam, Andhra Pradesh<br/>
        <b>Radius:</b> 5.0 km from Visakhapatnam<br/>
        <b>Active Cluster:</b> 7 Early Blight cases<br/>
        <b>Action:</b> Intensive extension surveillance ordered
      </div>
    `);
    layerGroupRef.current.addLayer(outbreakBuffer);

    // 2. Render individual markers
    geojson.features.forEach((feature: any) => {
      const coords = feature.geometry.coordinates; // [lon, lat]
      const props = feature.properties;

      // Filter check
      if (activeCropFilter !== 'All' && props.crop !== activeCropFilter) return;
      if (activeRiskFilter !== 'All' && props.risk_level !== activeRiskFilter) return;
      if (activeVillageFilter !== 'All' && props.village !== activeVillageFilter) return;

      const markerColor = props.marker_color || '#10B981';
      const isTrap = props.type === 'pest_trap';

      const circleMarker = L.circleMarker([coords[1], coords[0]], {
        radius: isTrap ? 7 : (props.risk_score >= 70 ? 9 : 6),
        fillColor: markerColor,
        color: '#FFFFFF',
        weight: 1.5,
        opacity: 1,
        fillOpacity: 0.85
      });

      const popupContent = isTrap ? `
        <div style="font-family: sans-serif; min-width: 170px; padding: 2px;">
          <strong style="color: #6D28D9;">🐛 Pest Surveillance: ${props.trap_code}</strong><br/>
          <b>Target:</b> ${props.target_pest}<br/>
          <b>Current Count:</b> <span style="color: #DC2626; font-weight: bold;">${props.current_count}</span> (ETL: 20)<br/>
          <b>Trend:</b> ${props.trend}<br/>
          <b>Location:</b> ${props.village}
        </div>
      ` : `
        <div style="font-family: sans-serif; min-width: 190px; padding: 2px;">
          <strong style="color: #1E293B;">Case: ${props.case_number}</strong><br/>
          <b>Crop:</b> ${props.crop}<br/>
          <b>Condition:</b> ${props.condition}<br/>
          <b>Status:</b> ${props.is_confirmed ? '<span style="color:#059669; font-weight:bold;">✓ Confirmed</span>' : 'AI Probabilistic'}<br/>
          <b>Severity:</b> ${props.severity}<br/>
          <b>Risk Score:</b> <span style="color: #DC2626; font-weight: bold;">${props.risk_score}/100 (${props.risk_level})</span><br/>
          <b>Village:</b> ${props.village}, ${props.mandal}
        </div>
      `;

      circleMarker.bindPopup(popupContent);
      layerGroupRef.current?.addLayer(circleMarker);
    });
  };

  // Re-apply filters
  const applyFilters = async () => {
    try {
      const geojson = await api.getHotspotsGeoJSON();
      renderMapFeatures(geojson);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      
      {/* Overview Statistics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: 'Monitored Farms', value: stats?.total_monitored_farms || 105, sub: 'East Godavari District', icon: Users, color: 'text-slate-900', bg: 'bg-white' },
          { label: 'Confirmed Outbreaks', value: stats?.confirmed_outbreaks || 6, sub: 'Pathologist Verified', icon: ShieldAlert, color: 'text-rose-600', bg: 'bg-rose-50/50 border-rose-100' },
          { label: 'High-Risk Farms', value: stats?.high_risk_farms || 8, sub: 'Multimodal Risk > 60', icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-50/50 border-amber-100' },
          { label: 'Active Pest Traps', value: stats?.pest_pressure_summary?.total_active_traps || 25, sub: '4 Traps Exceed ETL', icon: Bug, color: 'text-purple-600', bg: 'bg-purple-50/50 border-purple-100' },
          { label: 'Open Expert Triage', value: stats?.open_expert_triage || 1, sub: 'Pending Verification', icon: Clock, color: 'text-indigo-600', bg: 'bg-indigo-50/50 border-indigo-100' },
          { label: 'Extension Response', value: '94.2%', sub: 'Avg 2.4 Day Resolution', icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50/50 border-emerald-100' }
        ].map((item, idx) => {
          const Icon = item.icon;
          return (
            <div key={idx} className={`p-4 rounded-xl border border-slate-200/80 shadow-sm ${item.bg}`}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-slate-500">{item.label}</span>
                <Icon className={`w-4 h-4 ${item.color}`} />
              </div>
              <p className={`text-2xl font-black ${item.color}`}>{item.value}</p>
              <span className="text-[10px] font-medium text-slate-400 mt-0.5 block">{item.sub}</span>
            </div>
          );
        })}
      </div>

      {/* Main Map & Filter Controls */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden">
        
        {/* Map Header & Multi-Filter Bar */}
        <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-rose-600" />
            <div>
              <h3 className="font-extrabold text-sm text-slate-900">
                Interactive Geospatial Hotspot & Surveillance Map
              </h3>
              <p className="text-[11px] text-slate-500">
                Leaflet GIS Engine • 5 km Outbreak Buffer Zones • Live Pest Trap Vectors
              </p>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <div className="flex items-center space-x-1">
              <span className="font-semibold text-slate-600">Crop:</span>
              <select
                value={activeCropFilter}
                onChange={(e) => { setActiveCropFilter(e.target.value); applyFilters(); }}
                className="bg-white border border-slate-200 rounded-lg px-2 py-1 text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              >
                <option value="All">All Crops</option>
                <option value="Paddy (Rice)">Paddy</option>
                <option value="Cotton">Cotton</option>
                <option value="Chilli">Chilli</option>
              </select>
            </div>

            <div className="flex items-center space-x-1">
              <span className="font-semibold text-slate-600">Risk:</span>
              <select
                value={activeRiskFilter}
                onChange={(e) => { setActiveRiskFilter(e.target.value); applyFilters(); }}
                className="bg-white border border-slate-200 rounded-lg px-2 py-1 text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              >
                <option value="All">All Tiers</option>
                <option value="High">High Risk</option>
                <option value="Moderate">Moderate Risk</option>
                <option value="Low">Low Risk</option>
              </select>
            </div>

            <div className="flex items-center space-x-1">
              <span className="font-semibold text-slate-600">Village:</span>
              <select
                value={activeVillageFilter}
                onChange={(e) => { setActiveVillageFilter(e.target.value); applyFilters(); }}
                className="bg-white border border-slate-200 rounded-lg px-2 py-1 text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              >
                <option value="All">All Villages</option>
                <option value="Visakhapatnam">Visakhapatnam (Cluster)</option>
                <option value="Bheemunipatnam">Bheemunipatnam</option>
                <option value="Anandapuram">Anandapuram</option>
                <option value="Pendurthi">Pendurthi</option>
                <option value="Sabbavaram">Sabbavaram</option>
              </select>
            </div>

            {/* Map Legend */}
            <div className="hidden xl:flex items-center space-x-2 pl-3 border-l border-slate-200 text-[11px] font-semibold text-slate-600">
              <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span><span>High/Severe</span></span>
              <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span><span>Moderate</span></span>
              <span className="flex items-center space-x-1"><span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block"></span><span>Pest Trap</span></span>
            </div>
          </div>
        </div>

        {/* Leaflet Map Canvas */}
        <div ref={mapContainerRef} className="w-full h-[360px] sm:h-[450px] z-10" />

      </div>

      {/* Bottom Analytics & 7-Day Epidemic Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Ranked Village Hotspot Clusters */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h4 className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center space-x-1.5">
              <TrendingUp className="w-4 h-4 text-emerald-600" />
              <span>Ranked Village Outbreak Clusters</span>
            </h4>
            <span className="text-[10px] text-slate-400 font-semibold">Ordered by Avg Risk</span>
          </div>

          <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
            {clusters.map((cluster, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl border border-slate-100 bg-slate-50/60 flex items-center justify-between text-xs"
              >
                <div>
                  <div className="flex items-center space-x-1.5">
                    <span className="font-extrabold text-slate-900">{cluster.village}</span>
                    <span className="text-slate-400">({cluster.mandal})</span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Dominant: <strong className="text-slate-700">{cluster.dominant_crop}</strong> • {cluster.dominant_condition}
                  </p>
                </div>

                <div className="text-right">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                    cluster.average_risk_score >= 70 ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {cluster.average_risk_score} / 100
                  </span>
                  <span className="block text-[10px] text-slate-400 mt-0.5">
                    {cluster.confirmed_cases} Confirmed / {cluster.total_cases} Reported
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: 7-Day Epidemic Outbreak Forecast Curve */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 space-y-3 sm:p-5">
          <div className="flex flex-col gap-2 border-b border-slate-100 pb-3 sm:flex-row sm:items-center sm:justify-between sm:pb-2">
            <h4 className="flex items-start space-x-1.5 text-xs font-extrabold uppercase tracking-wider text-slate-800">
              <BarChart3 className="w-4 h-4 text-blue-600" />
              <span className="leading-5">7-Day Microclimate Disease Risk Forecast</span>
            </h4>
            <span className="self-start rounded-full bg-blue-50 px-2.5 py-1 text-[10px] font-bold text-blue-700 sm:self-auto">
              Epidemiological Model
            </span>
          </div>

          <div className="mobile-scrollbar flex gap-2 overflow-x-auto pt-1 pb-1 sm:grid sm:grid-cols-7 sm:gap-1.5 sm:overflow-visible sm:pb-0">
            {stats?.forecast_next_7_days?.map((day, idx) => (
              <div
                key={idx}
                className="flex min-h-[142px] min-w-[82px] flex-1 flex-col justify-between rounded-xl border border-slate-100 bg-slate-50 p-2.5 text-center sm:min-w-0"
              >
                <span className="text-[10px] font-bold text-slate-500">Day +{day.day_offset}</span>
                <div className="my-2 rounded-lg bg-white px-1 py-1.5 shadow-sm">
                  <span className={`text-lg font-black ${
                    day.predicted_risk_score >= 75 ? 'text-rose-600' : 'text-amber-600'
                  }`}>
                    {day.predicted_risk_score}
                  </span>
                  <span className="block text-[9px] text-slate-400 font-bold">Risk</span>
                </div>
                <span className="rounded-md bg-blue-50 px-1 py-1 text-[9px] font-bold leading-4 text-blue-700">
                  {day.expected_rain_mm}mm Rain
                </span>
              </div>
            ))}
          </div>

          <div className="rounded-xl border border-amber-100 bg-amber-50/70 p-3 text-[11px] leading-5 text-slate-700">
            <strong className="text-amber-900">Epidemiological Advisory:</strong> Persistent warm humid microclimate indicates high sporulation velocity over days 1–3. Pre-emptive biocontrol drenching and drainage verification advised before day 4.
          </div>
        </div>

      </div>

    </div>
  );
};
