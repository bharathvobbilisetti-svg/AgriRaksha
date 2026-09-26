import React, { useEffect, useRef, useState } from 'react';
import {
  Sprout, AlertTriangle, Camera, CloudRain, Bug, MapPin, Bell, Volume2, VolumeX,
  FileText, UserCheck, ShieldAlert, CheckCircle2, ChevronRight,
  TrendingUp, Info, Activity, Clock, RefreshCw, Upload, Eye
} from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { api } from '../services/api';
import { DiseaseCase, WeatherData, PestTrap } from '../types';

interface FarmerPortalProps {
  language: Language;
  onNavigateToExpert?: () => void;
  onNavigateToGIS?: () => void;
}

export const FarmerPortal: React.FC<FarmerPortalProps> = ({
  language,
  onNavigateToExpert,
  onNavigateToGIS
}) => {
  const t = translations[language];

  // Active sub-tab / view
  const [activeTile, setActiveTile] = useState<'check' | 'crops' | 'risks' | 'weather' | 'pests' | 'nearby' | 'ipm' | 'followup'>('check');

  // Diagnostic Wizard State
  const [selectedCrop, setSelectedCrop] = useState('Maize');
  const [selectedVariety, setSelectedVariety] = useState('DHM 117');
  const [selectedStage, setSelectedStage] = useState('Seedling');
  const [symptomNotes, setSymptomNotes] = useState('Leaf spots and early signs of maize crop stress');
  const maizeSampleImage = 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=800';
  const paddySampleImage = 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=800';
  const groundnutSampleImage = 'https://images.unsplash.com/photo-1492496913980-501348b61469?auto=format&fit=crop&q=80&w=800';
  const [imagePreview, setImagePreview] = useState<string>(maizeSampleImage);
  const [selectedFile, setSelectedFile] = useState<File | Blob | null>(null);
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState('');
  const videoRef = useRef<HTMLVideoElement>(null);
  const captureInputRef = useRef<HTMLInputElement>(null);
  const cameraStreamRef = useRef<MediaStream | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // Diagnostic Result State
  const [diagnosisResult, setDiagnosisResult] = useState<any>(null);
  const [expertRequested, setExpertRequested] = useState(false);
  const [followupSubmitted, setFollowupSubmitted] = useState(false);
  const sectionRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const handleCropChange = (crop: string) => {
    setSelectedCrop(crop);
    setSelectedFile(null);
    setShowHeatmap(true);
    if (crop === 'Paddy (Rice)') {
      setSelectedVariety('Swarna (MTU-1038)');
      setSelectedStage('Nursery / Seedling');
      setSymptomNotes('Brown lesions and drying tips on paddy leaves');
      setImagePreview(paddySampleImage);
      return;
    }

    if (crop === 'Groundnut') {
      setSelectedVariety('TAG 24');
      setSelectedStage('Germination');
      setSymptomNotes('Leaf spots or yellowing on groundnut plants');
      setImagePreview(groundnutSampleImage);
      return;
    }

    setSelectedVariety('DHM 117');
    setSelectedStage('Seedling');
    setSymptomNotes('Leaf spots and early signs of maize crop stress');
    setImagePreview(maizeSampleImage);
  };

  const growthStageValues = selectedCrop === 'Paddy (Rice)'
    ? ['Nursery / Seedling', 'Tillering', 'Panicle Initiation', 'Flowering & Grain Filling', 'Maturity']
    : selectedCrop === 'Groundnut'
      ? ['Germination', 'Vegetative Growth', 'Flowering & Pegging', 'Pod Development', 'Maturity']
      : ['Seedling', 'Vegetative Growth', 'Tasseling', 'Silking & Grain Filling', 'Maturity'];
  const growthStageLabels = selectedCrop === 'Paddy (Rice)'
    ? t.paddyStages
    : selectedCrop === 'Groundnut'
      ? t.groundnutStages
      : t.maizeStages;
  const nearbyRiskDetails = selectedCrop === 'Paddy (Rice)'
    ? { cropLabel: 'Paddy farms', condition: 'Rice blast', cases: 4 }
    : selectedCrop === 'Groundnut'
      ? { cropLabel: 'Groundnut farms', condition: 'Groundnut leaf spot', cases: 5 }
      : { cropLabel: 'Maize farms', condition: 'Maize leaf blight', cases: 3 };
  useEffect(() => {
    if (!isCameraOpen) return;

    let isMounted = true;
    const startCamera = async () => {
      try {
        setCameraError('');
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          setCameraError('Direct camera preview is unavailable here. Use the camera or photo picker below.');
          return;
        }

        let stream: MediaStream;
        try {
          // Attempt back camera (ideal for crop field inspection)
          stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false
          });
        } catch {
          // Fallback to any available webcam or front camera
          stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        }

        if (!isMounted) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
        cameraStreamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play().catch(() => {});
        }
      } catch (error) {
        console.error('Camera access error:', error);
        setCameraError('Camera access was blocked or is unavailable. Please allow camera permissions in your browser.');
      }
    };

    startCamera();
    return () => {
      isMounted = false;
      cameraStreamRef.current?.getTracks().forEach((track) => track.stop());
      cameraStreamRef.current = null;
    };
  }, [isCameraOpen]);

  const applySelectedPhoto = (file: File) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onloadend = () => setImagePreview(reader.result as string);
    reader.readAsDataURL(file);
    setIsCameraOpen(false);
  };

  const openCropCamera = () => {
    // LAN HTTP pages are not secure contexts, so browsers block getUserMedia.
    // Use the native camera/photo picker there instead.
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      captureInputRef.current?.click();
      return;
    }

    setCameraError('');
    setIsCameraOpen(true);
  };

  const captureLivePhoto = () => {
    const video = videoRef.current;
    if (!video || !video.videoWidth || !video.videoHeight) return;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      // Paint the actual live video frame onto the canvas
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => {
        if (blob) {
          setSelectedFile(blob);
        }
      }, 'image/jpeg', 0.92);
      setImagePreview(canvas.toDataURL('image/jpeg', 0.92));
    }
    setIsCameraOpen(false);
  };

  // Live Microclimate Weather state
  const [weather, setWeather] = useState<WeatherData>({
    latitude: 17.6868,
    longitude: 83.2185,
    temperature_c: 24.5,
    relative_humidity_pct: 86.0,
    rainfall_mm: 18.5,
    leaf_wetness_hours: 6.5,
    wind_speed_kmh: 7.5,
    fungal_spore_germination_risk: 82.0,
    forecast_rain_prob_24h: 75.0,
    forecast_rain_prob_72h: 80.0,
    weather_condition: 'Humid & Overcast with Afternoon Rain Showers'
  });
  const [weatherUpdatedAt, setWeatherUpdatedAt] = useState<Date | null>(null);
  const [isWeatherRefreshing, setIsWeatherRefreshing] = useState(false);

  useEffect(() => {
    let isMounted = true;
    const refreshWeather = async () => {
      setIsWeatherRefreshing(true);
      try {
        const data = await api.getWeather(17.6868, 83.2185);
        if (data && data.temperature_c) {
          if (isMounted) {
            setWeather(data);
            setWeatherUpdatedAt(new Date());
          }
        }
      } catch (err) {
        console.warn('Could not fetch live weather:', err);
      } finally {
        if (isMounted) setIsWeatherRefreshing(false);
      }
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') refreshWeather();
    };

    refreshWeather();
    const refreshTimer = window.setInterval(refreshWeather, 15 * 60 * 1000);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      isMounted = false;
      window.clearInterval(refreshTimer);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  const [rainAlertsEnabled, setRainAlertsEnabled] = useState(false);
  const [rainAlertDismissed, setRainAlertDismissed] = useState(false);

  const rainAlertLevel = weather.forecast_rain_prob_24h >= 80
    ? 'critical'
    : weather.forecast_rain_prob_24h >= 60
      ? 'high'
      : 'watch';
  const isStrongRainAlert = rainAlertLevel === 'critical' || rainAlertLevel === 'high';

  const playRainAlarm = () => {
    const AudioContextClass = window.AudioContext || (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!AudioContextClass) return;

    const audioContext = new AudioContextClass();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = 'square';
    oscillator.frequency.setValueAtTime(880, audioContext.currentTime);
    oscillator.frequency.setValueAtTime(660, audioContext.currentTime + 0.18);
    gain.gain.setValueAtTime(0.0001, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.18, audioContext.currentTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 0.38);
    oscillator.connect(gain);
    gain.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.4);
    oscillator.addEventListener('ended', () => void audioContext.close());
  };

  const enableRainAlerts = async () => {
    setRainAlertsEnabled(true);
    playRainAlarm();
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(t.rainAlertTitle, {
        body: `${weather.forecast_rain_prob_24h}% ${t.rainProbability}. ${t.rainAlertAction}`,
        tag: 'agriraksha-rain-alert'
      });
    }
  };

  // Pest Trap Surveillance State
  const [trap102] = useState<PestTrap>({
    id: 1,
    trap_code: 'TRAP-102',
    trap_type: 'Pheromone Trap',
    target_pest: 'Fruit Fly (Bactrocera dorsalis)',
    latitude: 17.6871,
    longitude: 83.2189,
    is_active: true,
    current_count: 37,
    previous_count: 18,
    population_trend: 'Increasing',
    risk_level: 'High',
    economic_threshold_level: 20,
    village: 'Visakhapatnam'
  });

  // Handle running multimodal AI diagnosis
  const handleRunDiagnosis = async () => {
    if (isAnalyzing) return;
    setIsAnalyzing(true);
    try {
      let targetImageUrl = selectedCrop === 'Paddy (Rice)' ? 'sample_paddy_rice_blast.jpg' : 'sample_maize_leaf_blight.jpg';
      if (selectedFile) {
        try {
          const upRes = await api.uploadImage(selectedFile, `${selectedCrop.toLowerCase()}_leaf.jpg`);
          if (upRes?.image_url) {
            targetImageUrl = upRes.image_url;
          }
        } catch (e) {
          console.warn("Upload failed, falling back to sample image:", e);
        }
      }

      // 1. Run disease prediction
      const form = new FormData();
      form.append('crop_name', selectedCrop);
      form.append('image_url', targetImageUrl);
      form.append('symptom_notes', symptomNotes);
      const diseaseRes = await api.predictDisease(form);

      // 2. Run multimodal risk fusion
      const riskRes = await api.calculateRisk(selectedCrop, diseaseRes.predicted_condition, diseaseRes.confidence);

      // 3. Fetch IPM & advisories
      const ipmRes = await api.getIPM(diseaseRes.predicted_condition);
      const advRes = await api.getAdvisories(diseaseRes.predicted_condition);

      setDiagnosisResult({
        ...diseaseRes,
        risk: riskRes,
        ipm: ipmRes,
        advisories: advRes
      });
    } catch (err) {
      console.error("Diagnosis error:", err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDiagnosticKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement;
    const isNativeControl = ['BUTTON', 'SELECT', 'INPUT', 'TEXTAREA'].includes(target.tagName);

    if (event.key === 'Enter' && !isNativeControl && !isAnalyzing) {
      event.preventDefault();
      handleRunDiagnosis();
    }
  };

  // Select localized advisory text
  const currentAdvisory = diagnosisResult?.advisories?.find(
    (a: any) => a.language_code === language
  ) || diagnosisResult?.advisories?.[0];

  const handleTileAction = (tileId: string) => {
    setActiveTile(tileId as typeof activeTile);

    if (tileId === 'nearby') {
      onNavigateToGIS?.();
      return;
    }

    if (tileId === 'followup') {
      onNavigateToExpert?.();
      return;
    }

    if (tileId === 'ipm') {
      (sectionRefs.current.ipm || sectionRefs.current.diagnostic)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

    const targetId = tileId === 'check' || tileId === 'crops' || tileId === 'risks' ? 'diagnostic' : tileId;
    sectionRefs.current[targetId]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="farmer-portal-background relative isolate overflow-hidden">
      <div className="relative z-10 max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 space-y-4 sm:space-y-6">
      
      {/* 8 Quick Farmer Tiles */}
      <div className="mobile-scrollbar flex gap-2 overflow-x-auto pb-1 sm:grid sm:grid-cols-4 sm:gap-2.5 sm:overflow-visible sm:pb-0 lg:grid-cols-8">
        {[
          { id: 'check', label: t.checkPlant, icon: Camera, color: 'bg-emerald-600 text-white shadow-emerald-900/20' },
          { id: 'crops', label: t.myCrops, icon: Sprout, color: 'bg-white hover:bg-emerald-50 text-slate-700 border border-slate-200' },
          { id: 'risks', label: t.currentRisks, icon: AlertTriangle, color: 'bg-rose-50 text-rose-700 border border-rose-200' },
          { id: 'weather', label: t.weather, icon: CloudRain, color: 'bg-white hover:bg-blue-50 text-slate-700 border border-slate-200' },
          { id: 'pests', label: t.pestMonitoring, icon: Bug, color: 'bg-white hover:bg-amber-50 text-slate-700 border border-slate-200' },
          { id: 'nearby', label: t.nearbyRisk, icon: MapPin, color: 'bg-white hover:bg-purple-50 text-slate-700 border border-slate-200' },
          { id: 'ipm', label: t.recommendations, icon: FileText, color: 'bg-white hover:bg-green-50 text-slate-700 border border-slate-200' },
          { id: 'followup', label: t.askExpert, icon: UserCheck, color: 'bg-white hover:bg-indigo-50 text-slate-700 border border-slate-200' },
        ].map((tile) => {
          const Icon = tile.icon;
          const isActive = activeTile === tile.id;
          return (
            <button
              key={tile.id}
              onClick={() => handleTileAction(tile.id)}
              className={`flex h-[72px] min-w-[86px] shrink-0 flex-col items-center justify-center rounded-xl p-2 transition-all font-semibold text-[11px] shadow-sm sm:h-auto sm:min-w-0 sm:p-3 sm:text-xs ${
                isActive
                  ? 'bg-emerald-700 text-white ring-2 ring-emerald-500 shadow-md scale-[1.02]'
                  : tile.color
              }`}
            >
              <Icon className={`w-5 h-5 mb-1.5 ${isActive ? 'text-white' : ''}`} />
              <span className="text-center leading-tight">{tile.label}</span>
            </button>
          );
        })}
      </div>

      {/* Primary Container */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Interactive Diagnostic Studio */}
        <div className="lg:col-span-7 space-y-6">
          
          <div
            ref={(element) => { sectionRefs.current.diagnostic = element; }}
            className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 scroll-mt-6 sm:p-6"
            onKeyDown={handleDiagnosticKeyDown}
            tabIndex={0}
            aria-label="Multimodal diagnosis workspace. Press Enter to run diagnosis."
          >
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-900">{t.stepSelectCrop}</h2>
                  <p className="text-xs text-slate-500">Visakhapatnam, Andhra Pradesh</p>
                </div>
              </div>
              <span className="hidden text-xs bg-emerald-50 text-emerald-700 font-bold px-2.5 py-1 rounded-full border border-emerald-200 sm:inline-flex">
                Plot A • 2.0 Acres
              </span>
            </div>

            {/* Crop, Variety, Stage Selection */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">{t.selectCrop}</label>
                <select
                  value={selectedCrop}
                  onChange={(e) => handleCropChange(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="Maize">Maize / Corn (మొక్కజొన్న / मक्का)</option>
                  <option value="Paddy (Rice)">Paddy / Rice (వరి / धान)</option>
                  <option value="Groundnut">Groundnut / Peanut (వేరుశనగ / मूंगफली)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">{t.selectVariety}</label>
                <select
                  value={selectedVariety}
                  onChange={(e) => setSelectedVariety(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  {selectedCrop === 'Paddy (Rice)' ? (
                    <>
                      <option value="Swarna (MTU-1038)">Swarna (MTU-1038)</option>
                      <option value="BPT 5204">BPT 5204 (Sona Masuri)</option>
                      <option value="MTU-1010">MTU-1010</option>
                    </>
                  ) : selectedCrop === 'Groundnut' ? (
                    <>
                      <option value="TAG 24">TAG 24</option>
                      <option value="Kadiri 6">Kadiri 6</option>
                      <option value="Dharani">Dharani</option>
                    </>
                  ) : (
                    <>
                      <option value="DHM 117">DHM 117</option>
                      <option value="Pioneer 3355">Pioneer 3355</option>
                      <option value="NK 6240">NK 6240</option>
                    </>
                  )}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">{t.selectStage}</label>
                <select
                  value={selectedStage}
                  onChange={(e) => setSelectedStage(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  {selectedCrop === 'Paddy (Rice)' ? (
                    <>
                      <option value="Nursery / Seedling">Nursery / Seedling</option>
                      <option value="Tillering">Tillering</option>
                      <option value="Panicle Initiation">Panicle Initiation</option>
                      <option value="Flowering & Grain Filling">Flowering & Grain Filling</option>
                      <option value="Maturity">Maturity</option>
                    </>
                  ) : selectedCrop === 'Groundnut' ? (
                    <>
                      <option value="Germination">Germination</option>
                      <option value="Vegetative Growth">Vegetative Growth</option>
                      <option value="Flowering & Pegging">Flowering & Pegging</option>
                      <option value="Pod Development">Pod Development</option>
                      <option value="Maturity">Maturity</option>
                    </>
                  ) : (
                    <>
                      <option value="Seedling">Seedling</option>
                      <option value="Vegetative Growth">Vegetative Growth</option>
                      <option value="Tasseling">Tasseling</option>
                      <option value="Silking & Grain Filling">Silking & Grain Filling</option>
                      <option value="Maturity">Maturity</option>
                    </>
                  )}
                </select>
              </div>
            </div>

            {/* Plant Leaf Image Capture / Chooser */}
            <div className="space-y-3">
              <label className="block text-xs font-semibold text-slate-600">{t.captureOrUpload}</label>
              
              <div className="relative border-2 border-dashed border-emerald-300 rounded-xl p-3 bg-emerald-50/40 text-center flex flex-col items-center justify-center space-y-3 sm:p-4">
                <img
                  src={imagePreview}
                  alt={`${selectedCrop} sample specimen`}
                  className="h-40 w-full max-w-sm object-cover rounded-lg shadow-sm border border-slate-200 sm:h-36 sm:w-48"
                  onError={() => setImagePreview(maizeSampleImage)}
                />
                <div className="flex w-full flex-col items-stretch justify-center gap-2 sm:flex-row sm:flex-wrap sm:items-center">
                  <button
                    onClick={() => setImagePreview(
                      selectedCrop === 'Paddy (Rice)'
                        ? paddySampleImage
                        : selectedCrop === 'Groundnut'
                          ? groundnutSampleImage
                          : maizeSampleImage
                    )}
                    className="flex items-center justify-center space-x-1.5 rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 sm:py-1.5"
                  >
                    <Eye className="w-3.5 h-3.5 text-emerald-600" />
                    <span>{t.sampleImageOption}</span>
                  </button>

                  <button
                    type="button"
                    onClick={openCropCamera}
                    className="flex items-center justify-center space-x-1.5 rounded-lg bg-emerald-600 px-3 py-2.5 text-xs font-bold text-white shadow-sm hover:bg-emerald-700 active:scale-95 transition-transform sm:py-1.5"
                  >
                    <Camera className="w-3.5 h-3.5" />
                    <span>Take Live Photo</span>
                  </button>

                  <input
                    ref={captureInputRef}
                    type="file"
                    accept="image/*"
                    capture="environment"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) applySelectedPhoto(file);
                      e.currentTarget.value = '';
                    }}
                  />

                  <label className="flex cursor-pointer items-center justify-center space-x-1.5 rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 active:scale-95 transition-transform sm:py-1.5">
                    <Upload className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Choose from Gallery</span>
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) {
                          setSelectedFile(file);
                          const reader = new FileReader();
                          reader.onloadend = () => setImagePreview(reader.result as string);
                          reader.readAsDataURL(file);
                        }
                      }}
                    />
                  </label>
                </div>
              </div>
            </div>

            {/* Live Camera Viewfinder Modal */}
            {isCameraOpen && (
              <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-sm p-4 flex items-center justify-center" role="dialog" aria-modal="true" aria-label="Live camera viewfinder">
                <div className="w-full max-w-lg rounded-2xl bg-slate-900 border border-slate-800 p-4 shadow-2xl space-y-3.5 text-white">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                    <div className="flex items-center space-x-2">
                      <Camera className="w-4 h-4 text-emerald-400" />
                      <h3 className="font-bold text-sm text-slate-100">Live Crop Leaf Camera</h3>
                    </div>
                    <button
                      type="button"
                      onClick={() => setIsCameraOpen(false)}
                      className="text-xs font-semibold text-slate-400 hover:text-white px-2.5 py-1 rounded-md bg-slate-800"
                    >
                      Close
                    </button>
                  </div>

                  <div className="relative overflow-hidden rounded-xl bg-black aspect-video flex items-center justify-center border border-slate-700">
                    {cameraError ? (
                      <div className="p-6 text-center space-y-3">
                        <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
                        <p className="text-xs text-slate-300">{cameraError}</p>
                        <label className="inline-flex cursor-pointer items-center space-x-1.5 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white shadow-sm hover:bg-emerald-700">
                          <Upload className="w-3.5 h-3.5" />
                          <span>Open Camera or Choose Photo</span>
                          <input
                            type="file"
                            accept="image/*"
                            capture="environment"
                            className="hidden"
                            onChange={(e) => {
                              const file = e.target.files?.[0];
                              if (file) {
                                applySelectedPhoto(file);
                              }
                            }}
                          />
                        </label>
                      </div>
                    ) : (
                      <>
                        <video ref={videoRef} autoPlay playsInline muted className="h-full w-full object-cover" />
                        {/* Leaf alignment guide reticle */}
                        <div className="absolute inset-8 border-2 border-dashed border-emerald-400/60 rounded-xl pointer-events-none flex items-center justify-center">
                          <span className="text-[11px] font-semibold text-emerald-200 bg-slate-900/80 px-2 py-0.5 rounded shadow">
                            Center Diseased Leaf Here
                          </span>
                        </div>
                      </>
                    )}
                  </div>

                  {!cameraError && (
                    <div className="flex items-center justify-center pt-1">
                      <button
                        type="button"
                        onClick={captureLivePhoto}
                        className="group flex items-center space-x-2 rounded-full bg-emerald-600 px-6 py-2.5 text-xs font-bold text-white shadow-lg hover:bg-emerald-500 active:scale-95 transition-all"
                      >
                        <span className="w-3.5 h-3.5 rounded-full bg-white group-hover:scale-110 transition-transform"></span>
                        <span>Capture Photo</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Primary Diagnosis Execution CTA */}
            <button
              onClick={handleRunDiagnosis}
              disabled={isAnalyzing}
              className="mt-4 w-full py-3.5 px-4 bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white font-extrabold text-sm rounded-xl shadow-md shadow-emerald-900/20 flex items-center justify-center space-x-2 transition-all transform active:scale-[0.99] sm:mt-5"
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-white" />
                  <span>{t.analyzing}</span>
                </>
              ) : (
                <>
                  <Sprout className="w-4 h-4" />
                  <span>{t.analyzeButton}</span>
                </>
              )}
            </button>

          </div>

          {/* Diagnostic Result Card */}
          {diagnosisResult && (
            <div
              ref={(element) => { sectionRefs.current.ipm = element; }}
              className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 space-y-5 animate-in fade-in duration-300 scroll-mt-6 sm:p-6"
            >
              
              {/* Header with Uncertainty Alert */}
              <div className="bg-amber-50 border-l-4 border-amber-500 p-3.5 rounded-r-xl">
                <div className="flex items-start space-x-2.5">
                  <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-bold text-amber-900">
                      {t.uncertaintyWarning}
                    </p>
                    <p className="text-[11px] text-amber-700 mt-0.5">
                      {diagnosisResult.disclaimer}
                    </p>
                  </div>
                </div>
              </div>

              {/* Diagnosis Badges & Multimodal Score Dial */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center bg-slate-50 p-4 rounded-xl border border-slate-100">
                <div>
                  <span className="text-[11px] uppercase tracking-wider text-slate-500 font-bold">
                    Probable Condition
                  </span>
                  <h3 className="text-xl font-extrabold text-slate-900">
                    {diagnosisResult.predicted_condition}
                  </h3>
                  <p className="text-xs italic text-slate-500">
                    {selectedCrop === 'Paddy (Rice)'
                      ? 'Magnaporthe oryzae (Rice Blast Pathogen)'
                      : selectedCrop === 'Groundnut'
                        ? 'Cercospora arachidicola (Leaf Spot Pathogen)'
                        : 'Bipolaris maydis (Maize Leaf Blight Pathogen)'}
                  </p>
                  
                  <div className="flex items-center space-x-3 mt-3">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-blue-100 text-blue-800">
                      {t.confidence}: {(diagnosisResult.confidence * 100).toFixed(0)}%
                    </span>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800">
                      {t.severity}: {diagnosisResult.severity} ({diagnosisResult.severity_percentage ? `${diagnosisResult.severity_percentage}%` : '28.5%'})
                    </span>
                  </div>
                </div>

                {/* Multimodal Composite Score Dial */}
                <div className="bg-white p-3.5 rounded-xl border border-rose-200/80 text-center shadow-sm">
                  <span className="text-xs font-bold text-slate-600 block">
                    {t.multimodalRiskScore}
                  </span>
                  <div className="flex items-baseline justify-center space-x-1 mt-1">
                    <span className="text-4xl font-black text-rose-600">
                      {diagnosisResult.risk?.final_score || 78}
                    </span>
                    <span className="text-slate-400 font-bold text-sm">/ 100</span>
                  </div>
                  <span className="inline-block mt-1 px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-rose-600 text-white uppercase tracking-wider">
                    {diagnosisResult.risk?.risk_tier || 'HIGH'} RISK
                  </span>
                </div>
              </div>

              {/* Explainable AI (XAI) Visual Lesion Segmentation Heatmap */}
              {diagnosisResult.heatmap_url && (
                <div className="bg-slate-900 rounded-xl p-3 sm:p-4 text-white space-y-3 border border-slate-800 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
                    <div className="flex items-center space-x-2">
                      <Activity className="w-4 h-4 text-emerald-400 shrink-0" />
                      <span className="text-xs font-bold uppercase tracking-wider text-emerald-300">
                        Explainable AI (XAI) Lesion Heatmap
                      </span>
                    </div>
                    <div className="flex bg-slate-800 rounded-lg p-0.5 text-xs font-semibold self-stretch sm:self-auto justify-center">
                      <button
                        type="button"
                        onClick={() => setShowHeatmap(false)}
                        className={`flex-1 sm:flex-none px-3 py-1.5 sm:py-1 rounded-md transition-all text-center ${!showHeatmap ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-300 hover:text-white'}`}
                      >
                        Original Leaf
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowHeatmap(true)}
                        className={`flex-1 sm:flex-none px-3 py-1.5 sm:py-1 rounded-md transition-all text-center ${showHeatmap ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-300 hover:text-white'}`}
                      >
                        AI Heatmap
                      </button>
                    </div>
                  </div>
                  <div className="relative aspect-video max-h-72 w-full rounded-lg overflow-hidden border border-slate-700 bg-black flex items-center justify-center">
                    <img
                      src={showHeatmap ? diagnosisResult.heatmap_url : imagePreview}
                      alt="Lesion Segmentation Heatmap"
                      className="h-full w-full object-contain"
                    />
                    {showHeatmap && (
                      <div className="absolute bottom-2 left-2 right-2 bg-slate-950/90 backdrop-blur-sm border border-slate-700 px-2.5 py-1.5 rounded-lg text-[10px] flex flex-wrap items-center justify-between gap-1.5 text-slate-200 shadow-md">
                        <div className="flex items-center space-x-2.5">
                          <span className="flex items-center space-x-1">
                            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block shadow-sm"></span>
                            <span className="font-medium">Necrotic</span>
                          </span>
                          <span className="flex items-center space-x-1">
                            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block shadow-sm"></span>
                            <span className="font-medium">Chlorotic</span>
                          </span>
                        </div>
                        <span className="font-bold text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/60">
                          Foliage Damage: {diagnosisResult.severity_percentage}%
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Contributing Factors (Explainable AI) */}
              <div>
                <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-600 mb-2.5 flex items-center space-x-1.5">
                  <Activity className="w-4 h-4 text-emerald-600" />
                  <span>{t.contributingFactors}</span>
                </h4>
                
                <div className="space-y-2">
                  {diagnosisResult.risk?.factors_explanation?.map((fac: any, idx: number) => (
                    <div
                      key={idx}
                      className="p-2.5 rounded-lg border border-slate-200/80 bg-white flex items-start justify-between text-xs space-x-3"
                    >
                      <div>
                        <span className="font-bold text-slate-800">{fac.factor}</span>
                        <p className="text-[11px] text-slate-500 mt-0.5">{fac.description}</p>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase shrink-0 ${
                        fac.impact === 'High' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {fac.impact} Impact
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Multilingual Farmer Advisory Box */}
              {currentAdvisory && (
                <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                  <div className="flex items-center space-x-2 text-emerald-900 font-bold text-sm mb-2">
                    <FileText className="w-4 h-4 text-emerald-700" />
                    <span>{currentAdvisory.title}</span>
                  </div>
                  <p className="text-xs text-emerald-800 leading-relaxed mb-3">
                    {currentAdvisory.farmer_guidance_text}
                  </p>
                  <ul className="space-y-1.5">
                    {currentAdvisory.action_bullet_points?.map((pt: string, idx: number) => (
                      <li key={idx} className="flex items-start space-x-2 text-xs text-emerald-900">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{pt}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Expert Validation Request Card */}
              {diagnosisResult.needs_expert_validation && (
                <div className="p-4 rounded-xl bg-indigo-50 border border-indigo-200 space-y-3">
                  <div className="flex items-center space-x-2 text-xs font-bold text-indigo-900">
                    <UserCheck className="w-4 h-4 text-indigo-700" />
                    <span>{t.expertVerificationNeeded}</span>
                  </div>
                  
                  {expertRequested ? (
                    <div className="p-2.5 bg-emerald-100 border border-emerald-300 text-emerald-900 rounded-lg text-xs font-bold flex items-center space-x-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
                      <span>{t.expertRequested}</span>
                    </div>
                  ) : (
                    <button
                      onClick={() => setExpertRequested(true)}
                      className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold shadow transition-all flex items-center justify-center space-x-1.5"
                    >
                      <UserCheck className="w-4 h-4" />
                      <span>{t.requestExpertBtn}</span>
                    </button>
                  )}
                </div>
              )}

            </div>
          )}

        </div>

        {/* Right Column: Environmental & Geospatial Context Cards */}
        <div className="lg:col-span-5 space-y-5">
          
          {/* Microclimate Weather Widget */}
          <div
            ref={(element) => { sectionRefs.current.weather = element; }}
            className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 scroll-mt-6"
          >
            {!rainAlertDismissed && isStrongRainAlert && (
              <div className="mb-4 rounded-xl border-2 border-rose-400 bg-rose-50 p-3.5 shadow-[0_0_0_4px_rgba(251,113,133,0.12)] rain-alarm-pulse" role="alert">
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 rounded-full bg-rose-600 p-2 text-white">
                    <Bell className="h-4 w-4" aria-hidden="true" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-xs font-black uppercase tracking-wide text-rose-900">{t.rainAlertTitle}</p>
                      <button
                        type="button"
                        onClick={() => setRainAlertDismissed(true)}
                        className="text-[10px] font-bold text-rose-700 underline underline-offset-2"
                      >
                        {t.dismiss}
                      </button>
                    </div>
                    <p className="mt-1 text-xs font-semibold leading-relaxed text-rose-800">
                      {weather.forecast_rain_prob_24h}% {t.rainProbability} • {t.rainAlertAction}
                    </p>
                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <button
                        type="button"
                        onClick={enableRainAlerts}
                        className="inline-flex items-center gap-1.5 rounded-lg bg-rose-600 px-2.5 py-2 text-[11px] font-extrabold text-white shadow-sm hover:bg-rose-700"
                      >
                        {rainAlertsEnabled ? <Volume2 className="h-3.5 w-3.5" /> : <VolumeX className="h-3.5 w-3.5" />}
                        {rainAlertsEnabled ? t.alertsEnabled : t.enableAlarm}
                      </button>
                      <span className="text-[10px] font-bold text-rose-700">{t.rainAlertWindow}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <CloudRain className="w-4 h-4 text-blue-600" />
                <h3 className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {t.weather} • Visakhapatnam AWS
                </h3>
              </div>
              <span className="text-[10px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded-full border border-blue-200">
                {isWeatherRefreshing ? 'Updating...' : weatherUpdatedAt ? `Updated ${weatherUpdatedAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : 'Live Sensor'}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[11px] text-slate-500 font-medium">{t.temp}</span>
                <p className="text-xl font-black text-slate-900">{weather.temperature_c}°C</p>
                <span className="text-[10px] text-emerald-600 font-bold">Optimal Spore Range</span>
              </div>

              <div className="p-3 bg-blue-50/60 rounded-xl border border-blue-100">
                <span className="text-[11px] text-blue-700 font-medium">{t.humidity}</span>
                <p className="text-xl font-black text-blue-900">{weather.relative_humidity_pct}%</p>
                <span className="text-[10px] text-rose-600 font-bold">Very High Moisture</span>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[11px] text-slate-500 font-medium">{t.rainfall}</span>
                <p className="text-xl font-black text-slate-900">{weather.rainfall_mm} mm</p>
                <span className="text-[10px] text-slate-500">Rainfall Dispersal</span>
              </div>

              <div className="p-3 bg-rose-50/60 rounded-xl border border-rose-100">
                <span className="text-[11px] text-rose-700 font-medium">{t.sporeRisk}</span>
                <p className="text-xl font-black text-rose-700">{weather.fungal_spore_germination_risk}%</p>
                <span className="text-[10px] text-rose-600 font-bold">Severe Risk Tier</span>
              </div>
            </div>

            <p className="text-[11px] text-slate-500 mt-3 italic">
              {weather.weather_condition}. Leaf wetness duration: {weather.leaf_wetness_hours} hours.
            </p>
          </div>

          {/* Pest Trap Surveillance Card */}
          <div
            ref={(element) => { sectionRefs.current.pests = element; }}
            className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 scroll-mt-6"
          >
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <Bug className="w-4 h-4 text-purple-600" />
                <h3 className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {t.pestMonitoring} • {trap102.trap_code}
                </h3>
              </div>
              <span className="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded-full">
                Exceeds ETL
              </span>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500 font-medium">{t.targetPest}</span>
                <span className="font-bold text-slate-900">{trap102.target_pest}</span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500 font-medium">{t.count}</span>
                <div className="flex items-center space-x-1.5">
                  <span className="text-lg font-black text-rose-600">{trap102.current_count}</span>
                  <span className="text-slate-400 font-semibold">(Threshold: {trap102.economic_threshold_level})</span>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500 font-medium">{t.trend}</span>
                <span className="inline-flex items-center space-x-1 text-rose-600 font-bold">
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>{trap102.population_trend} (+19 vs previous)</span>
                </span>
              </div>
            </div>

            <div className="mt-3 p-2.5 bg-purple-50 rounded-lg text-[11px] text-purple-900 border border-purple-100">
              Adult fruit fly surge detected. Install 6-8 pheromone traps/acre and collect fallen fruits.
            </div>
          </div>

          {/* Nearby Outbreak Hotspot Alerts */}
          <div
            ref={(element) => { sectionRefs.current.nearby = element; }}
            className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 scroll-mt-6"
          >
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-rose-600" />
                <h3 className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {t.nearbyRisk} • 5 km Radius
                </h3>
              </div>
                <span className="text-[10px] bg-rose-600 text-white font-extrabold px-2 py-0.5 rounded-full">
                {nearbyRiskDetails.cases} Confirmed Cases
              </span>
            </div>

            <p className="text-xs text-slate-600 mb-3">
              Visakhapatnam cluster exhibits {nearbyRiskDetails.cases} laboratory-confirmed {nearbyRiskDetails.condition} cases on {nearbyRiskDetails.cropLabel} within 5 km of your location.
            </p>

            <button
              onClick={onNavigateToGIS}
              className="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-bold transition-all flex items-center justify-center space-x-1.5"
            >
              <MapPin className="w-3.5 h-3.5 text-rose-600" />
              <span>View On Geospatial Hotspot Map</span>
            </button>
          </div>

          {/* 7-Day Follow-Up Tracker Card */}
          <div
            ref={(element) => { sectionRefs.current.followup = element; }}
            className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 scroll-mt-6"
          >
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-emerald-600" />
                <h3 className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {t.followupTitle}
                </h3>
              </div>
              <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                Day 7 Follow-Up
              </span>
            </div>

            <p className="text-xs text-slate-600 mb-3">
              {followupSubmitted
                ? t.statusImproving
                : "Farmer submitted second image 7 days after bio-fungicide treatment to monitor canopy recovery."}
            </p>

            {followupSubmitted ? (
              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs font-semibold text-emerald-900 flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Case updated! 35% lesion area reduction recorded. Case marked Resolved.</span>
              </div>
            ) : (
              <button
                onClick={() => setFollowupSubmitted(true)}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow transition-all flex items-center justify-center space-x-1.5"
              >
                <Upload className="w-3.5 h-3.5" />
                <span>{t.submitFollowup}</span>
              </button>
            )}
          </div>

        </div>

      </div>

      </div>
    </div>
  );
};
