const API_BASE = '/api';

export const api = {
  async login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Unable to sign in');
    return data;
  },

  async register(userData: Record<string, string>) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Unable to create account');
    return data;
  },

  async switchRole(role: string) {
    const res = await fetch(`${API_BASE}/auth/switch-role/${role}`, { method: 'POST' });
    return res.json();
  },

  async getCrops() {
    const res = await fetch(`${API_BASE}/farms/crops`);
    return res.json();
  },

  async getWeather(lat = 17.6868, lon = 83.2185) {
    const res = await fetch(`${API_BASE}/weather?lat=${lat}&lon=${lon}`);
    return res.json();
  },

  async uploadImage(file: File | Blob, filename = 'leaf.jpg') {
    const formData = new FormData();
    formData.append('file', file, filename);
    const res = await fetch(`${API_BASE}/disease/upload-image`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  async predictDisease(formData: FormData) {
    const res = await fetch(`${API_BASE}/disease/predict`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  async calculateRisk(cropName: string, conditionName: string, confidence: number, stageName = 'Tillering to Panicle Initiation') {
    const body = new URLSearchParams();
    body.append('crop_name', cropName);
    body.append('condition_name', conditionName);
    body.append('ai_confidence', confidence.toString());
    body.append('latitude', '17.6868');
    body.append('longitude', '83.2185');
    body.append('crop_stage_multiplier', '1.35');
    body.append('crop_stage_name', stageName);

    const res = await fetch(`${API_BASE}/risk/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    });
    return res.json();
  },

  async createCase(caseData: any) {
    const res = await fetch(`${API_BASE}/cases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData)
    });
    return res.json();
  },

  async getCases(limit = 20) {
    const res = await fetch(`${API_BASE}/cases?limit=${limit}`);
    return res.json();
  },

  async getTraps() {
    const res = await fetch(`${API_BASE}/pest/traps`);
    return res.json();
  },

  async getHotspotsGeoJSON() {
    const res = await fetch(`${API_BASE}/hotspots/geojson`);
    return res.json();
  },

  async getHotspotClusters() {
    const res = await fetch(`${API_BASE}/hotspots/clusters`);
    return res.json();
  },

  async getTriageQueue() {
    const res = await fetch(`${API_BASE}/expert/queue`);
    return res.json();
  },

  async submitExpertReview(review: any) {
    const res = await fetch(`${API_BASE}/expert/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(review)
    });
    return res.json();
  },

  async getIPM(condition: string) {
    const res = await fetch(`${API_BASE}/ipm/recommendations?condition=${encodeURIComponent(condition)}`);
    return res.json();
  },

  async getAdvisories(condition: string) {
    const res = await fetch(`${API_BASE}/advisories?condition=${encodeURIComponent(condition)}`);
    return res.json();
  },

  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/statistics`);
    return res.json();
  },

  async seedDemo() {
    const res = await fetch(`${API_BASE}/demo/seed`, { method: 'POST' });
    return res.json();
  },

  async submitFollowup(caseId: number, imageUrl: string, notes: string) {
    const res = await fetch(`${API_BASE}/cases/followup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case_id: caseId, image_url: imageUrl, farmer_notes: notes })
    });
    return res.json();
  }
};
