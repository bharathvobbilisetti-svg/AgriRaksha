export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'farmer' | 'expert' | 'official' | 'extension_worker' | 'admin';
  phone?: string;
  village?: string;
  mandal?: string;
  district?: string;
  state?: string;
  preferred_language: string;
}

export interface FactorExplanation {
  factor: string;
  score: number;
  weight: number;
  impact: string;
  description: string;
}

export interface MultimodalRiskDetail {
  final_score: number;
  risk_tier: string;
  visual_evidence_score: number;
  weather_suitability_score: number;
  crop_susceptibility_score: number;
  geo_proximity_score: number;
  pest_pressure_score: number;
  factors_explanation: FactorExplanation[];
}

export interface IPMDetail {
  condition_name: string;
  cultural_control: string;
  mechanical_control: string;
  biological_control: string;
  chemical_control_regulated?: string;
  safety_precautions: string;
  pre_harvest_interval_days: number;
  extension_consultation_advised: boolean;
  official_disclaimer: string;
}

export interface AdvisoryDetail {
  language_code: string;
  title: string;
  farmer_guidance_text: string;
  action_bullet_points: string[];
  urgency: string;
}

export interface DiseaseCase {
  id: number;
  case_number: string;
  farmer_id: number;
  farm_id: number;
  crop_name: string;
  variety_name?: string;
  stage_name?: string;
  image_url: string;
  ai_predicted_condition: string;
  ai_confidence: number;
  estimated_severity: string;
  severity_percentage: number;
  needs_expert_validation: boolean;
  multimodal_risk_score: number;
  risk_level: string;
  status: string;
  is_confirmed: boolean;
  confirmed_condition?: string;
  heatmap_url?: string;
  created_at: string;
  risk_breakdown?: MultimodalRiskDetail;
  ipm_recommendation?: IPMDetail;
  advisories: AdvisoryDetail[];
  farm_village?: string;
  farm_mandal?: string;
  latitude?: number;
  longitude?: number;
}

export interface WeatherData {
  latitude: number;
  longitude: number;
  temperature_c: number;
  relative_humidity_pct: number;
  rainfall_mm: number;
  leaf_wetness_hours: number;
  wind_speed_kmh: number;
  fungal_spore_germination_risk: number;
  forecast_rain_prob_24h: number;
  forecast_rain_prob_72h: number;
  weather_condition: string;
}

export interface PestTrap {
  id: number;
  trap_code: string;
  trap_type: string;
  target_pest: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
  current_count: number;
  previous_count: number;
  population_trend: string;
  risk_level: string;
  economic_threshold_level: number;
  village: string;
}

export interface DashboardStats {
  total_monitored_farms: number;
  active_cases: number;
  confirmed_outbreaks: number;
  high_risk_farms: number;
  open_expert_triage: number;
  laboratory_referrals: number;
  crop_distribution: Record<string, number>;
  disease_distribution: Record<string, number>;
  pest_pressure_summary: {
    total_active_traps: number;
    traps_exceeding_etl: number;
    total_specimens_counted_24h: number;
    dominant_pest_vector: string;
  };
  extension_response_rate_pct: number;
  average_resolution_days: number;
  forecast_next_7_days: Array<{
    day_offset: number;
    date: string;
    predicted_risk_score: number;
    risk_tier: string;
    expected_rain_mm: number;
    recommended_action: string;
  }>;
}
