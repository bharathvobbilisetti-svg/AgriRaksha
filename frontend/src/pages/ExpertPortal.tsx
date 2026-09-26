import React, { useState, useEffect } from 'react';
import {
  ShieldCheck, CheckCircle2, AlertOctagon, Microscope,
  Send, FileCheck, RefreshCw, MapPin, CloudRain, Check, AlertCircle, Database,
  Repeat2, Sprout, MessageCircle, BarChart3
} from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { api } from '../services/api';
import { DashboardStats, WeatherData } from '../types';

interface ExpertPortalProps {
  language: Language;
}

export const ExpertPortal: React.FC<ExpertPortalProps> = ({ language }) => {
  const t = translations[language];

  const [queue, setQueue] = useState<any[]>([]);
  const [selectedCase, setSelectedCase] = useState<any>(null);
  const [confirmedCondition, setConfirmedCondition] = useState('Early Blight');
  const [previousCrop, setPreviousCrop] = useState('');
  const [expertSeverity, setExpertSeverity] = useState('Moderate');
  const [agreement, setAgreement] = useState('Confirmed');
  const [notes, setNotes] = useState('Observed characteristic concentric target-board lesions. Early Blight (Alternaria solani) confirmed. Recommended immediate canopy aeration and prophylactic bio-fungicide spray.');
  const [farmerReply, setFarmerReply] = useState('Your crop symptoms are being reviewed. Follow the recommended field steps and contact your local extension officer if the lesions spread.');
  const [recommendFieldVisit, setRecommendFieldVisit] = useState(true);
  const [recommendLabTest, setRecommendLabTest] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [rainAlertDismissed, setRainAlertDismissed] = useState(false);
  const [forecastDays, setForecastDays] = useState<DashboardStats['forecast_next_7_days']>([]);

  const rotationSuggestions: Record<string, { next: string; reason: string }> = {
    'Maize': { next: 'Groundnut or another legume', reason: 'Legumes can add nitrogen to the soil and break cereal pest and disease cycles.' },
    'Paddy (Rice)': { next: 'Green gram or black gram', reason: 'Repeating paddy can draw down nitrogen and organic matter, especially when straw is removed.' },
    'Groundnut': { next: 'Maize or another cereal', reason: 'Alternating a legume with a cereal helps diversify nutrient use and reduce crop-specific pest pressure.' },
    'Wheat': { next: 'Chickpea or another legume', reason: 'A legume break can improve soil nitrogen and interrupt repeated cereal disease cycles.' },
    'Cotton': { next: 'Sorghum or another cereal', reason: 'Changing crop families helps reduce the build-up of cotton-specific pests and diseases.' }
  };
  const cropSuggestion = previousCrop ? rotationSuggestions[previousCrop] : undefined;

  // Load triage queue
  const fetchQueue = async () => {
    try {
      const data = await api.getTriageQueue();
      setQueue(data);
      if (data.length > 0 && !selectedCase) {
        setSelectedCase(data[0]);
        setConfirmedCondition(data[0].ai_predicted_condition);
      }
    } catch (err) {
      console.error("Queue load error:", err);
    }
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  useEffect(() => {
    let isMounted = true;
    const refreshWeather = async () => {
      try {
        const data = await api.getWeather();
        if (isMounted && data && typeof data.forecast_rain_prob_24h === 'number') {
          setWeather(data as WeatherData);
        }
      } catch (err) {
        console.error('Weather alert load error:', err);
      }
    };
    refreshWeather();
    api.getDashboardStats()
      .then((data) => {
        if (isMounted && Array.isArray(data?.forecast_next_7_days)) {
          setForecastDays(data.forecast_next_7_days);
        }
      })
      .catch((err) => console.error('Disease risk forecast load error:', err));
    const intervalId = window.setInterval(refreshWeather, 5 * 60 * 1000);
    return () => {
      isMounted = false;
      window.clearInterval(intervalId);
    };
  }, []);

  const rainAlertActive = Boolean(weather && (
    weather.rainfall_mm > 0 || weather.forecast_rain_prob_24h >= 60
  ));

  const handleSubmitReview = async () => {
    if (!selectedCase) return;
    setIsSubmitting(true);
    try {
      await api.submitExpertReview({
        case_id: selectedCase.case_id,
        confirmed_condition: confirmedCondition,
        diagnostic_agreement: agreement,
        expert_severity: expertSeverity,
        advisory_notes: `${notes}\n\nMessage to farmer: ${farmerReply}`,
        recommend_field_visit: recommendFieldVisit,
        recommend_lab_test: recommendLabTest,
        lab_name: "Regional Krishi Vigyan Kendra (KVK) Plant Pathology Laboratory"
      });

      setReviewSuccess(true);
      setTimeout(() => {
        setReviewSuccess(false);
        fetchQueue();
      }, 2000);
    } catch (err) {
      console.error("Review submission error:", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-indigo-900 to-slate-900 text-white p-5 rounded-2xl border border-indigo-800/60 flex flex-col sm:flex-row items-start sm:items-center justify-between shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center font-bold">
            <Microscope className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-extrabold text-base tracking-tight">
              Agronomist Diagnostic Triage & Ground-Truth Portal
            </h2>
            <p className="text-xs text-indigo-300">
              Senior Pathologist Review • Continuous ML Dataset Enrichment
            </p>
          </div>
        </div>

        <div className="mt-3 sm:mt-0 flex items-center space-x-2">
          <span className="text-xs bg-indigo-800 text-indigo-200 px-3 py-1 rounded-full font-bold border border-indigo-700">
            {queue.length} Cases Requiring Validation
          </span>
          <button
            onClick={fetchQueue}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs"
            title="Refresh Queue"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Queue List */}
        <div className="lg:col-span-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-600 uppercase tracking-wider">
            Review Queue (Ordered by Risk Score)
          </h3>

          {queue.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-xl border border-slate-200 text-slate-500 text-xs">
              <CheckCircle2 className="w-6 h-6 text-emerald-500 mx-auto mb-2" />
              All pending cases reviewed and validated!
            </div>
          ) : (
            queue.map((item) => {
              const isSelected = selectedCase?.case_id === item.case_id;
              return (
                <div
                  key={item.case_id}
                  onClick={() => {
                    setSelectedCase(item);
                    setConfirmedCondition(item.ai_predicted_condition);
                  }}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-indigo-50/80 border-indigo-300 ring-2 ring-indigo-400 shadow-sm'
                      : 'bg-white border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-extrabold text-xs text-slate-900">{item.case_number}</span>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-rose-100 text-rose-800">
                      Risk {item.risk_score}/100
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 text-xs text-slate-600 mb-1">
                    <span className="font-semibold text-slate-800">{item.crop}</span>
                    <span>•</span>
                    <span className="font-medium text-slate-700">{item.village}</span>
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-500">
                    <span>AI: {item.ai_predicted_condition} ({item.ai_confidence}%)</span>
                    <span className="font-semibold text-amber-700">{item.severity}</span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right Detail & Validation Inspector */}
        <div className="lg:col-span-8 space-y-6">
          {selectedCase ? (
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200/80 space-y-6">
              
              {/* Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="text-base font-extrabold text-slate-900">
                      Case {selectedCase.case_number}
                    </h3>
                    <span className="text-xs bg-amber-100 text-amber-900 font-bold px-2 py-0.5 rounded">
                      Needs Expert Review
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Farmer: {selectedCase.farmer_name} • Village: {selectedCase.village}, Visakhapatnam, Andhra Pradesh
                  </p>
                </div>

                <span className="text-xs font-bold text-rose-600 bg-rose-50 px-3 py-1 rounded-full border border-rose-200 self-start sm:self-auto">
                  Composite Multimodal Risk: {selectedCase.risk_score} / 100
                </span>
              </div>

              {/* Farmer-to-Expert Interaction */}
              <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 space-y-3">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-sky-900">
                    <MessageCircle className="h-4 w-4 text-sky-700" />
                    <span>Farmer Interaction</span>
                  </div>
                  <span className="rounded-full bg-sky-100 px-2.5 py-1 text-[10px] font-bold text-sky-800">Reply with validation</span>
                </div>
                <div className="rounded-xl border border-sky-200 bg-white p-3">
                  <p className="mb-1 text-[10px] font-extrabold uppercase tracking-wide text-sky-800">Farmer report</p>
                  <p className="text-xs leading-relaxed text-slate-700">
                    {selectedCase.symptom_notes || 'The farmer has not added a written symptom report.'}
                  </p>
                </div>
                <div>
                  <label className="mb-1 block text-[10px] font-extrabold uppercase tracking-wide text-sky-800">Expert reply</label>
                  <textarea
                    rows={2}
                    value={farmerReply}
                    onChange={(e) => setFarmerReply(e.target.value)}
                    className="w-full rounded-lg border border-sky-200 bg-white p-3 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-sky-500"
                    placeholder="Write clear guidance for the farmer"
                  />
                  <p className="mt-1.5 text-[10px] text-sky-800">This reply is delivered with the expert validation notification.</p>
                </div>
              </div>

              {/* Model Assessment & Environmental Context */}
              <div className="space-y-3 p-4 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                  <span className="text-xs font-bold text-slate-700 block uppercase tracking-wider">
                    Model Assessment & Field Signals
                  </span>

                  <div className="flex justify-between border-b border-slate-200 pb-2">
                    <span className="text-slate-500">AI Predicted Condition:</span>
                    <span className="font-extrabold text-slate-900">{selectedCase.ai_predicted_condition}</span>
                  </div>

                  <div className="flex justify-between border-b border-slate-200 pb-2">
                    <span className="text-slate-500">AI Confidence:</span>
                    <span className="font-bold text-blue-700">{selectedCase.ai_confidence}%</span>
                  </div>

                  <div className="flex justify-between border-b border-slate-200 pb-2">
                    <span className="text-slate-500">Severity Rating:</span>
                    <span className="font-bold text-amber-700">{selectedCase.severity}</span>
                  </div>

                  <div className="flex justify-between border-b border-slate-200 pb-2">
                    <span className="text-slate-500">Weather Microclimate:</span>
                    <span className="font-bold text-slate-800">
                      {weather
                        ? `${weather.temperature_c}°C, ${weather.relative_humidity_pct}% RH, ${weather.rainfall_mm} mm rain`
                        : 'Weather data unavailable'}
                    </span>
                  </div>

                  {rainAlertActive && !rainAlertDismissed && weather && (
                    <div className="rain-alarm-pulse rounded-xl border border-rose-300 bg-rose-50 p-3 text-rose-900" role="alert">
                      <div className="flex items-start gap-2">
                        <div className="rounded-full bg-rose-600 p-1.5 text-white">
                          <CloudRain className="h-4 w-4" />
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-[11px] font-extrabold uppercase tracking-wide">{t.rainAlertTitle}</span>
                            <button
                              type="button"
                              onClick={() => setRainAlertDismissed(true)}
                              className="text-[10px] font-bold underline underline-offset-2"
                            >
                              {t.dismiss}
                            </button>
                          </div>
                          <p className="mt-1 text-[11px] font-semibold leading-relaxed">
                            {weather.rainfall_mm > 0 && `Rainfall recorded: ${weather.rainfall_mm} mm. `}
                            {weather.forecast_rain_prob_24h}% {t.rainProbability}. {t.rainAlertAction}
                          </p>
                          <p className="mt-1 text-[10px] font-bold text-rose-700">{t.rainAlertWindow}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex justify-between">
                    <span className="text-slate-500">Surrounding Outbreaks:</span>
                    <span className="font-bold text-rose-700">6 Confirmed Cases (5km)</span>
                  </div>
              </div>

              {/* 7-Day Microclimate Disease Risk Forecast */}
              <section className="space-y-3 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm sm:p-5" aria-labelledby="expert-risk-forecast-heading">
                <div className="flex flex-col gap-2 border-b border-slate-100 pb-3 sm:flex-row sm:items-center sm:justify-between sm:pb-2">
                  <h4 id="expert-risk-forecast-heading" className="flex items-start gap-1.5 text-xs font-extrabold uppercase tracking-wider text-slate-800">
                    <BarChart3 className="h-4 w-4 shrink-0 text-blue-600" />
                    <span className="leading-5">7-Day Microclimate Disease Risk Forecast</span>
                  </h4>
                  <span className="self-start rounded-full bg-blue-50 px-2.5 py-1 text-[10px] font-bold text-blue-700 sm:self-auto">Epidemiological Model</span>
                </div>

                {forecastDays.length > 0 ? (
                  <div className="mobile-scrollbar flex gap-2 overflow-x-auto pt-1 pb-1 sm:grid sm:grid-cols-7 sm:gap-1.5 sm:overflow-visible sm:pb-0">
                    {forecastDays.slice(0, 7).map((day) => (
                      <div key={day.day_offset} className="flex min-h-[142px] min-w-[82px] flex-1 flex-col justify-between rounded-xl border border-slate-100 bg-slate-50 p-2.5 text-center sm:min-w-0">
                        <span className="text-[10px] font-bold text-slate-500">Day +{day.day_offset}</span>
                        <div className="my-2 rounded-lg bg-white px-1 py-1.5 shadow-sm">
                          <span className={`text-lg font-black ${day.predicted_risk_score >= 75 ? 'text-rose-600' : day.predicted_risk_score >= 50 ? 'text-amber-600' : 'text-emerald-600'}`}>
                            {Number(day.predicted_risk_score).toFixed(1)}
                          </span>
                          <span className="block text-[9px] font-bold text-slate-400">Risk</span>
                        </div>
                        <span className="rounded-md bg-blue-50 px-1 py-1 text-[9px] font-bold leading-4 text-blue-700">
                          {Number(day.expected_rain_mm).toFixed(1)}mm Rain
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="rounded-xl bg-slate-50 p-4 text-xs text-slate-500">7-day forecast is currently unavailable.</p>
                )}

                {forecastDays.length > 0 && (
                  <div className="rounded-xl border border-amber-100 bg-amber-50/70 p-3 text-[11px] leading-5 text-slate-700">
                    <strong className="text-amber-900">Epidemiological Advisory:</strong>{' '}
                    {forecastDays[0].predicted_risk_score >= 75
                      ? 'Forecast indicates very high disease pressure. Inspect the crop daily, ensure field drainage, and plan preventive integrated pest management before wet conditions favor further spread.'
                      : 'Monitor the crop and local weather closely. Maintain field drainage and follow integrated pest management guidance as conditions change.'}
                  </div>
                )}
              </section>

              {/* Expert Action & Diagnostic Form */}
              <div className="space-y-4 pt-4 border-t border-slate-100">
                <h4 className="text-xs font-extrabold uppercase tracking-wider text-indigo-900">
                  Expert Validation & Diagnostic Action
                </h4>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Agreement</label>
                    <select
                      value={agreement}
                      onChange={(e) => setAgreement(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="Confirmed">Confirm Diagnosis</option>
                      <option value="Modified">Modify Condition</option>
                      <option value="Refuted">Refute / False Positive</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Confirmed Condition</label>
                    <input
                      type="text"
                      value={confirmedCondition}
                      onChange={(e) => setConfirmedCondition(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Expert Severity</label>
                    <select
                      value={expertSeverity}
                      onChange={(e) => setExpertSeverity(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="Mild">Mild (&lt; 15%)</option>
                      <option value="Moderate">Moderate (15-40%)</option>
                      <option value="Severe">Severe (&gt; 40%)</option>
                    </select>
                  </div>
                </div>

                <div className="rounded-2xl border border-amber-200 bg-gradient-to-br from-white to-amber-50/70 p-4 shadow-sm space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 text-[11px] font-extrabold uppercase tracking-wide text-slate-600">
                      <Repeat2 className="h-4 w-4 text-amber-700" />
                      <span>Next Crop Suggestion</span>
                    </div>
                    <span className="rounded-full bg-amber-100 px-2.5 py-1 text-[10px] font-bold text-amber-800">Soil health</span>
                  </div>

                  <div className="rounded-xl border border-amber-200 bg-white/90 p-3">
                    <label className="mb-1 block text-[10px] font-extrabold uppercase tracking-wide text-amber-800">Previously planted crop</label>
                    <select
                      value={previousCrop}
                      onChange={(e) => setPreviousCrop(e.target.value)}
                      className="mb-2 w-full rounded-lg border border-slate-200 bg-white px-2.5 py-2 text-xs font-semibold text-slate-800 focus:ring-2 focus:ring-amber-500"
                    >
                      <option value="">Select previous crop</option>
                      {Object.keys(rotationSuggestions).map((crop) => (
                        <option key={crop} value={crop}>{crop}</option>
                      ))}
                    </select>
                    {cropSuggestion ? (
                      <>
                        <p className="text-xs font-extrabold text-slate-900">Plant next: {cropSuggestion.next}</p>
                        <p className="mt-1.5 text-[11px] leading-relaxed text-slate-600">{cropSuggestion.reason}</p>
                      </>
                    ) : (
                      <p className="text-[11px] text-slate-500">Choose the crop most recently grown to see a rotation suggestion.</p>
                    )}
                  </div>

                  <div className="flex items-start gap-2 text-[11px] leading-relaxed text-slate-600">
                    <Sprout className="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
                    <span>Rotate with a pulse crop after harvest and return crop residue to the soil where practical. Check local season, soil, and water conditions before planting.</span>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Agronomist Advisory & Treatment Guidance
                  </label>
                  <textarea
                    rows={3}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                {/* Additional Actions */}
                <div className="flex flex-wrap gap-4 pt-1">
                  <label className="flex items-center space-x-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={recommendFieldVisit}
                      onChange={(e) => setRecommendFieldVisit(e.target.checked)}
                      className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                    />
                    <span>Dispatch Extension Officer (MAO) Field Inspection</span>
                  </label>

                  <label className="flex items-center space-x-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={recommendLabTest}
                      onChange={(e) => setRecommendLabTest(e.target.checked)}
                      className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                    />
                    <span>Refer to KVK Pathology Lab (Pathogen Isolation)</span>
                  </label>
                </div>

                {/* Continuous Learning Ground-Truth Tag */}
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                  <div className="flex items-center space-x-2">
                    <Database className="w-4 h-4 text-emerald-700 shrink-0" />
                    <span className="text-xs font-bold text-emerald-900">
                      Include in Future ML Retraining Dataset (Ground-Truth Annotation)
                    </span>
                  </div>
                  <span className="text-[10px] bg-emerald-700 text-white px-2 py-0.5 rounded font-extrabold shrink-0">
                    ACTIVE LOOP
                  </span>
                </div>

                {/* Submit Review CTA */}
                {reviewSuccess ? (
                  <div className="p-3 bg-emerald-600 text-white rounded-xl text-center text-xs font-extrabold flex items-center justify-center space-x-2">
                    <Check className="w-4 h-4" />
                    <span>Expert validation confirmed! Hotspot map & farmer alerts updated.</span>
                  </div>
                ) : (
                  <button
                    onClick={handleSubmitReview}
                    disabled={isSubmitting}
                    className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs rounded-xl shadow transition-all flex items-center justify-center space-x-2"
                  >
                    {isSubmitting ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin text-white" />
                        <span>Submitting validation...</span>
                      </>
                    ) : (
                      <>
                        <ShieldCheck className="w-4 h-4" />
                        <span>Confirm Expert Diagnosis & Publish Verified Advisory</span>
                      </>
                    )}
                  </button>
                )}

              </div>

            </div>
          ) : (
            <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-slate-500 text-sm">
              Select a case from the triage queue to begin diagnostic inspection.
            </div>
          )}
        </div>

      </div>

    </div>
  );
};
