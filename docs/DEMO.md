# SIH 2026 Presentation Walkthrough Script — AgriRaksha

Use this guided script to present the AgriRaksha prototype to **Smart India Hackathon 2026** evaluators.

---

## 🔑 Demo Account Credentials

| Role | Email | Password | Pre-loaded Context |
| :--- | :--- | :--- | :--- |
| **Farmer** | `farmer@agriraksha.in` | `farmer123` | Ramesh Reddy, Geesugonda (Tomato Plot A) |
| **Expert Agronomist** | `expert@agriraksha.in` | `expert123` | Dr. K. Sreenivas Rao, Sr. Pathologist KVK |
| **Agriculture Official** | `official@agriraksha.in` | `official123` | P. Lakshmi, ADA Warangal Urban |
| **Extension Worker** | `extension@agriraksha.in` | `extension123` | M. Anji Reddy, MAO Geesugonda |

---

## 🎬 5-Minute Live Presentation Script

### Part 1: Problem Context & Product Vision (30 Seconds)
* **What to say:**
  > *"Respected evaluators, existing agricultural apps follow a dangerous pattern: upload a photo, make a guess, and immediately tell the farmer to buy a pesticide. In real agriculture, diseases spread because of weather microclimates, susceptible growth stages, and nearby outbreaks. AgriRaksha is a multimodal early-warning and decision support system combining visual symptoms, weather data, crop stages, pest traps, and expert validation into proactive intelligence."*

---

### Part 2: One-Click Demo Seeder (30 Seconds)
* **What to do:**
  1. Open `http://localhost:3000`.
  2. Point out the green **"Load Demo Dataset"** button on the navbar and click it.
  3. Notice the live confirmation badge: `Demo Data Loaded! (105 Farms, Outbreaks, Traps)`.
* **What to say:**
  > *"With one click, our system has initialized a realistic agro-climatic zone in Warangal district: 105 monitored farms across 7 villages, 25 smart pest surveillance traps, and 6 active confirmed outbreak cases."*

---

### Part 3: Farmer Workflow & Multimodal Risk (2 Minutes)
* **What to do:**
  1. On the **Farmer Portal**, switch the language dropdown from **English** to **తెలుగు (Telugu)** or **हिंदी (Hindi)**.
  2. Show the 8 farmer quick tiles: *My Crops, Current Risks, Check Plant, Weather, Pest Monitoring, Nearby Risk, IPM Advice, Ask Expert*.
  3. Under Step 1, select:
     - Crop: **Tomato**
     - Variety: **Arka Rakshak**
     - Growth Stage: **Fruiting & Ripening**
  4. Click **"Or use SIH Demo Leaf (Tomato Early Blight)"**.
  5. Click **"Run Multimodal AI Diagnosis"**.
* **What to highlight to judges:**
  - **AI Probabilistic Assessment**: Condition: *Early Blight* (*Alternaria solani*), Confidence: *87%*, Severity: *Moderate* ($28.5\%$).
  - **Uncertainty Alert**: Clear warning stating AI predictions are not certified laboratory diagnoses.
  - **Multimodal Composite Risk**: **78 / 100 — HIGH RISK**.
  - **Explainable AI (XAI)**: Expand the contributing factors:
    1. *Visual Evidence (87.0 | High Impact)*: Concentric target-board lesions observed.
    2. *Microclimate Suitability (82.0 | High Impact)*: 86% RH, 18.5mm rain, 6.5h leaf wetness.
    3. *Growth Stage (77.0 | High Impact)*: Dense fruiting canopy restricts air flow.
    4. *Neighborhood Proximity (87.0 | High Impact)*: 6 confirmed cases within 5 km.
    5. *Pest Trap Vector (77.7 | High Impact)*: Trap `TRAP-102` caught 37 fruit flies (exceeds ETL of 20).
  - **Integrated Pest Management (IPM)**: Cultural, mechanical, and biological controls (*Trichoderma viride*) are prioritized. Regulated chemical guidance follows CIB&RC statutory rules.
  - **Click "Request Official Expert Verification"**: The farmer requests certified agronomist review.

---

### Part 4: Expert Agronomist Diagnostic Triage (1 Minute)
* **What to do:**
  1. Click **"Expert Review"** in the top navigation bar.
  2. Highlight the **Review Queue** displaying the high-risk case `AGR-2026-TOM-01`.
  3. Click the case to open the side-by-side diagnostic inspector.
  4. Point out the original leaf specimen, AI confidence, microclimate parameters, and surrounding trap counts.
  5. Check **"Dispatch Extension Officer Field Inspection"**.
  6. Highlight the **"Approved for Continuous Learning ML Dataset"** badge.
  7. Click **"Confirm Expert Diagnosis & Publish Verified Advisory"**.
* **What to say:**
  > *"Our expert agronomist confirms the diagnosis, dispatches the Mandal Agricultural Officer to inspect the field, and approves this confirmed specimen to enter our ground-truth training dataset. This completes the human-in-the-loop continuous learning cycle."*

---

### Part 5: Agriculture Official GIS Surveillance (1 Minute)
* **What to do:**
  1. Click **"GIS Surveillance"** in the top navigation bar.
  2. Show the interactive **Leaflet Map**:
     - Red circle: 5.0 km epidemic containment buffer around Geesugonda.
     - Red/Amber markers: Confirmed and reported cases.
     - Purple markers: Smart pest traps.
     - Click any marker to view the live popup with farmer details, crop, condition, and risk score.
  3. Demonstrate the multi-filters: Filter by Crop (*Tomato*), Risk (*High*), or Village (*Geesugonda*).
  4. Show the **7-Day Microclimate Disease Risk Forecast Curve** predicting daily progression and precipitation trends.

---

### Part 6: Longitudinal Follow-Up & Resolution (30 Seconds)
* **What to do:**
  1. Switch back to the **Farmer Portal**.
  2. Scroll to the **7-Day Case Monitoring & Recovery** card.
  3. Click **"Submit Follow-Up Leaf Image"**.
  4. Notice the case status updates to **Resolved** with a verified $35\%$ lesion area reduction.
* **Closing Statement:**
  > *"AgriRaksha closes the entire loop: from early detection, through microclimate fusion and expert validation, to containment and verified field recovery. Thank you!"*
