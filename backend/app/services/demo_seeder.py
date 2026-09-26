import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import (
    User, Farm, CropCatalog, CropStage, CropVariety, FarmerCrop,
    DiseaseCase, PestTrap, TrapObservation, WeatherRecord,
    MultimodalRiskScore, ExpertReview, IPMRecommendation,
    MultilingualAdvisory, Notification, FollowUpRecord, LaboratoryReferral
)
from app.core.security import get_password_hash
from app.services.multimodal_risk import multimodal_risk_service
from app.services.ipm_service import ipm_service
from app.services.advisory_service import advisory_service
from ml.disease_detection.engine import disease_vision_pipeline
from ml.risk_prediction.weather_risk import weather_risk_engine

VILLAGES = [
    {"name": "Visakhapatnam", "mandal": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "Bheemunipatnam", "mandal": "Bheemunipatnam", "lat": 17.8900, "lon": 83.4520},
    {"name": "Anandapuram", "mandal": "Anandapuram", "lat": 17.9940, "lon": 83.3790},
    {"name": "Pendurthi", "mandal": "Pendurthi", "lat": 17.7800, "lon": 83.2200},
    {"name": "Sabbavaram", "mandal": "Sabbavaram", "lat": 17.9800, "lon": 83.1300},
    {"name": "Padmanabham", "mandal": "Padmanabham", "lat": 17.9200, "lon": 83.3300},
    {"name": "Kothavalasa", "mandal": "Kothavalasa", "lat": 18.1200, "lon": 83.2000}
]

CROPS_DEF = [
    {
        "name": "Tomato",
        "scientific": "Solanum lycopersicum",
        "category": "Horticulture",
        "stages": [
            ("Seedling", 15, 0.8),
            ("Vegetative Growth", 30, 1.0),
            ("Flowering & Fruit Set", 25, 1.3),
            ("Fruiting & Ripening", 35, 1.4),
            ("Harvesting", 20, 1.1)
        ],
        "varieties": [("Arka Rakshak", "Triple disease tolerant"), ("Pusa Ruby", "Early yielding"), ("Abhinav", "Standard hybrid")]
    },
    {
        "name": "Paddy (Rice)",
        "scientific": "Oryza sativa",
        "category": "Cereals",
        "stages": [
            ("Nursery", 25, 0.7),
            ("Tillering", 35, 1.0),
            ("Panicle Initiation", 25, 1.3),
            ("Flowering & Heading", 20, 1.4),
            ("Grain Filling & Maturity", 30, 1.0)
        ],
        "varieties": [("BPT 5204 (Samba Mahsuri)", "Fine grain"), ("MTU 1010", "High yield short duration"), ("Swarna (MTU 7029)", "High-yield Andhra Pradesh variety")]
    },
    {
        "name": "Cotton",
        "scientific": "Gossypium hirsutum",
        "category": "Fiber",
        "stages": [
            ("Germination & Seedling", 20, 0.8),
            ("Vegetative", 45, 1.0),
            ("Squaring & Flowering", 40, 1.4),
            ("Boll Development", 45, 1.3),
            ("Boll Bursting", 30, 0.9)
        ],
        "varieties": [("Bollgard II Hybrid", "Bt cotton"), ("RCH 659", "High retention"), ("Suraj", "Non-Bt arboreum")]
    },
    {
        "name": "Chilli",
        "scientific": "Capsicum annuum",
        "category": "Spices",
        "stages": [
            ("Nursery", 35, 0.7),
            ("Vegetative", 30, 1.0),
            ("Flowering", 25, 1.3),
            ("Fruit Development", 40, 1.4),
            ("Ripening & Picking", 30, 1.1)
        ],
        "varieties": [("Teja (S17)", "High pungency export"), ("Guntur Hope", "Pest resistant"), ("Armoor", "Local popular")]
    }
]

def seed_complete_sih_demo_data(db: Session):
    """
    Seeds realistic SIH demonstration data with 100+ farms, multiple villages,
    pest trap surveillance networks, confirmed outbreak clusters, and the
    complete end-to-end Tomato Early Blight outbreak scenario.
    """
    # 1. Clean existing records if any
    db.query(LaboratoryReferral).delete()
    db.query(FollowUpRecord).delete()
    db.query(Notification).delete()
    db.query(MultilingualAdvisory).delete()
    db.query(IPMRecommendation).delete()
    db.query(ExpertReview).delete()
    db.query(MultimodalRiskScore).delete()
    db.query(DiseaseCase).delete()
    db.query(TrapObservation).delete()
    db.query(PestTrap).delete()
    db.query(WeatherRecord).delete()
    db.query(FarmerCrop).delete()
    db.query(CropVariety).delete()
    db.query(CropStage).delete()
    db.query(CropCatalog).delete()
    db.query(Farm).delete()
    db.query(User).delete()
    db.commit()

    print("Seeding core roles & catalog...")

    # 2. Create Core Stakeholder Users
    farmer_user = User(
        email="farmer@agriraksha.in",
        hashed_password=get_password_hash("farmer123"),
        full_name="Ramesh Reddy",
        role="farmer",
        phone="+91 98480 12345",
        village="Visakhapatnam",
        mandal="Visakhapatnam",
        district="Visakhapatnam",
        state="Andhra Pradesh",
        preferred_language="te"
    )
    db.add(farmer_user)

    expert_user = User(
        email="expert@agriraksha.in",
        hashed_password=get_password_hash("expert123"),
        full_name="Dr. K. Sreenivas Rao (Sr. Pathologist KVK)",
        role="expert",
        phone="+91 94401 56789",
        village="Visakhapatnam",
        mandal="Visakhapatnam",
        district="Visakhapatnam",
        state="Andhra Pradesh",
        preferred_language="en"
    )
    db.add(expert_user)

    official_user = User(
        email="official@agriraksha.in",
        hashed_password=get_password_hash("official123"),
        full_name="P. Lakshmi (Assistant Director of Agriculture - ADA)",
        role="official",
        phone="+91 98499 87654",
        village="Visakhapatnam",
        mandal="Visakhapatnam",
        district="Visakhapatnam",
        state="Andhra Pradesh",
        preferred_language="en"
    )
    db.add(official_user)

    ext_user = User(
        email="extension@agriraksha.in",
        hashed_password=get_password_hash("extension123"),
        full_name="M. Anji Reddy (Mandal Agricultural Officer - MAO)",
        role="extension_worker",
        phone="+91 94901 11223",
        village="Visakhapatnam",
        mandal="Visakhapatnam",
        district="Visakhapatnam",
        state="Andhra Pradesh",
        preferred_language="te"
    )
    db.add(ext_user)
    db.commit()
    db.refresh(farmer_user)
    db.refresh(expert_user)
    db.refresh(official_user)

    # 3. Create Crops Catalog
    crop_entities = {}
    stage_entities = {}
    variety_entities = {}

    for c_data in CROPS_DEF:
        crop = CropCatalog(
            name=c_data["name"],
            scientific_name=c_data["scientific"],
            category=c_data["category"],
            description=f"Standard commercial crop: {c_data['name']}"
        )
        db.add(crop)
        db.commit()
        db.refresh(crop)
        crop_entities[crop.name] = crop

        stage_entities[crop.name] = []
        for s_name, days, mult in c_data["stages"]:
            stage = CropStage(
                crop_id=crop.id,
                stage_name=s_name,
                typical_days=f"{days} days",
                susceptibility_multiplier=mult,
                description=f"{s_name} phase of {crop.name}"
            )
            db.add(stage)
            db.commit()
            db.refresh(stage)
            stage_entities[crop.name].append(stage)

        variety_entities[crop.name] = []
        for v_name, traits in c_data["varieties"]:
            var = CropVariety(
                crop_id=crop.id,
                variety_name=v_name,
                resistance_traits=traits,
                maturity_days=120
            )
            db.add(var)
            db.commit()
            db.refresh(var)
            variety_entities[crop.name].append(var)

    # 4. Create Primary Farmer's Farm (Visakhapatnam)
    primary_farm = Farm(
        farmer_id=farmer_user.id,
        name="Ramesh Reddy Farm - Plot A",
        latitude=17.6868,
        longitude=83.2185,
        village="Visakhapatnam",
        mandal="Visakhapatnam",
        district="Visakhapatnam",
        state="Andhra Pradesh",
        soil_type="Red Loam",
        irrigation_source="Drip Irrigation",
        total_area_acres=3.5
    )
    db.add(primary_farm)
    db.commit()
    db.refresh(primary_farm)

    # Crop on primary farm: Tomato (Arka Rakshak, Fruiting & Ripening)
    tomato_crop = crop_entities["Tomato"]
    tomato_fruiting_stage = stage_entities["Tomato"][3]  # Fruiting & Ripening (mult 1.4)
    tomato_variety = variety_entities["Tomato"][0]      # Arka Rakshak

    primary_farmer_crop = FarmerCrop(
        farm_id=primary_farm.id,
        crop_id=tomato_crop.id,
        variety_id=tomato_variety.id,
        current_stage_id=tomato_fruiting_stage.id,
        sowing_date=datetime.utcnow() - timedelta(days=65),
        area_allocated_acres=2.0,
        is_active=True
    )
    db.add(primary_farmer_crop)
    db.commit()

    # Weather Record for primary farm (Warm, High Humidity, Recent Rain)
    primary_weather = WeatherRecord(
        farm_id=primary_farm.id,
        latitude=17.6868,
        longitude=83.2185,
        recorded_at=datetime.utcnow(),
        temperature_c=24.5,
        relative_humidity_pct=86.0,
        rainfall_mm=18.5,
        leaf_wetness_hours=6.5,
        wind_speed_kmh=7.5,
        fungal_spore_germination_risk=82.0,
        forecast_rain_prob_24h=75.0,
        forecast_rain_prob_72h=80.0
    )
    db.add(primary_weather)
    db.commit()

    # 5. Create 100+ Additional Farms across Villages
    print("Generating 105 realistic farms across Visakhapatnam district, Andhra Pradesh...")
    farmer_names = [
        "Venkatesh", "Srinivas", "Kishan", "Anil", "Bhaskar", "Ravinder",
        "Sammaiah", "Mallesh", "Laxman", "Prabhakar", "Komuraiah", "Narsaiah",
        "Rajamouli", "Satyanarayana", "Mogili", "Gopal", "Devender", "Chandramouli"
    ]
    surnames = ["Goud", "Reddy", "Rao", "Yadav", "Kuruma", "Chary", "Patel", "Naidu"]

    created_farms = [primary_farm]
    for i in range(104):
        village_info = VILLAGES[i % len(VILLAGES)]
        f_name = f"{random.choice(farmer_names)} {random.choice(surnames)}"
        f_user = User(
            email=f"farmer_{i+2}@agriraksha-demo.in",
            hashed_password=get_password_hash("demo123"),
            full_name=f_name,
            role="farmer",
            phone=f"+91 9{random.randint(4000, 9999)} {random.randint(10000, 99999)}",
            village=village_info["name"],
            mandal=village_info["mandal"],
            district="Visakhapatnam",
            state="Andhra Pradesh",
            preferred_language=random.choice(["te", "hi", "en"])
        )
        db.add(f_user)
        db.commit()
        db.refresh(f_user)

        # Disperse coordinates within ~2.5km of village center
        jitter_lat = (random.random() - 0.5) * 0.035
        jitter_lon = (random.random() - 0.5) * 0.035
        farm_lat = village_info["lat"] + jitter_lat
        farm_lon = village_info["lon"] + jitter_lon

        farm = Farm(
            farmer_id=f_user.id,
            name=f"{f_name}'s Farm",
            latitude=farm_lat,
            longitude=farm_lon,
            village=village_info["name"],
            mandal=village_info["mandal"],
            district="Visakhapatnam",
            state="Andhra Pradesh",
            soil_type=random.choice(["Red Loam", "Black Cotton Soil", "Clay Loam"]),
            irrigation_source=random.choice(["Drip Irrigation", "Borewell", "Canal Water"]),
            total_area_acres=round(random.uniform(1.5, 6.0), 1)
        )
        db.add(farm)
        db.commit()
        db.refresh(farm)
        created_farms.append(farm)

        # Allocate crop
        c_choice_name = random.choice(["Tomato", "Paddy (Rice)", "Cotton", "Chilli"])
        c_obj = crop_entities[c_choice_name]
        st_obj = random.choice(stage_entities[c_choice_name])
        var_obj = random.choice(variety_entities[c_choice_name])

        fcrop = FarmerCrop(
            farm_id=farm.id,
            crop_id=c_obj.id,
            variety_id=var_obj.id,
            current_stage_id=st_obj.id,
            sowing_date=datetime.utcnow() - timedelta(days=random.randint(20, 80)),
            area_allocated_acres=round(farm.total_area_acres * 0.7, 1)
        )
        db.add(fcrop)

    db.commit()

    # 6. Seed Pest Traps & TRAP-102 (Fruit Fly count 37, Increasing, High)
    print("Seeding 25 smart pest surveillance traps...")
    # Target Demo Trap: TRAP-102 on Primary Farm / Visakhapatnam
    trap_102 = PestTrap(
        farm_id=primary_farm.id,
        trap_code="TRAP-102",
        trap_type="Pheromone Trap",
        target_pest="Fruit Fly",
        latitude=17.6871,
        longitude=83.2189,
        is_active=True,
        installed_at=datetime.utcnow() - timedelta(days=21)
    )
    db.add(trap_102)
    db.commit()
    db.refresh(trap_102)

    # Observation for TRAP-102 (Count: 37, Trend: Increasing, Risk: High)
    obs_102 = TrapObservation(
        trap_id=trap_102.id,
        observation_date=datetime.utcnow(),
        image_url="/assets/traps/trap_102_fruitfly.jpg",
        pest_species="Fruit Fly (Bactrocera dorsalis)",
        pest_count=37,
        previous_count=18,
        population_trend="Increasing",
        economic_threshold_level=20,
        risk_level="High",
        notes="Sharp increase in adult fruit flies detected. Exceeds ETL by 85%."
    )
    db.add(obs_102)

    # Additional 24 traps across villages
    pest_targets = [
        ("Fruit Fly", "Pheromone Trap", 20),
        ("Fall Armyworm", "Funnel Pheromone Trap", 10),
        ("Whitefly", "Yellow Sticky Trap", 25),
        ("Stem Borer", "Light Trap", 15)
    ]
    for idx in range(24):
        target, t_type, etl = pest_targets[idx % len(pest_targets)]
        target_farm = created_farms[idx * 4 + 1]
        cnt = random.randint(5, 42)
        prev = random.randint(5, 30)
        tr = "Increasing" if cnt > prev + 4 else ("Decreasing" if cnt < prev - 4 else "Stable")
        r_level = "High" if cnt >= etl else ("Moderate" if cnt >= etl * 0.6 else "Low")

        p_trap = PestTrap(
            farm_id=target_farm.id,
            trap_code=f"TRAP-{103 + idx}",
            trap_type=t_type,
            target_pest=target,
            latitude=target_farm.latitude,
            longitude=target_farm.longitude,
            is_active=True,
            installed_at=datetime.utcnow() - timedelta(days=30)
        )
        db.add(p_trap)
        db.commit()
        db.refresh(p_trap)

        p_obs = TrapObservation(
            trap_id=p_trap.id,
            observation_date=datetime.utcnow() - timedelta(hours=random.randint(1, 48)),
            image_url=f"/assets/traps/trap_{103 + idx}.jpg",
            pest_species=target,
            pest_count=cnt,
            previous_count=prev,
            population_trend=tr,
            economic_threshold_level=etl,
            risk_level=r_level,
            notes=f"Surveillance observation for {target}"
        )
        db.add(p_obs)

    db.commit()

    # 7. Seed 6 Confirmed Outbreak Cases in Visakhapatnam within 5 km
    print("Seeding 6 confirmed Tomato Early Blight outbreak cases within 5km radius...")
    visakhapatnam_farms = [f for f in created_farms if f.village == "Visakhapatnam" and f.id != primary_farm.id][:6]
    for c_idx, cf in enumerate(visakhapatnam_farms):
        case_no = f"AGR-2026-CONF-{101 + c_idx}"
        c_case = DiseaseCase(
            case_number=case_no,
            farmer_id=cf.farmer_id,
            farm_id=cf.id,
            crop_id=tomato_crop.id,
            variety_id=tomato_variety.id,
            stage_id=tomato_fruiting_stage.id,
            image_url="/assets/samples/tomato_early_blight_confirmed.jpg",
            is_leaf_or_plant=True,
            plant_verification_confidence=0.99,
            symptom_notes="Concentric dark brown rings observed across lower foliage.",
            ai_predicted_condition="Early Blight",
            ai_confidence=0.88,
            estimated_severity="Moderate",
            severity_percentage=32.0,
            needs_expert_validation=False,
            multimodal_risk_score=76.5,
            risk_level="High",
            status="expert_verified",
            is_confirmed=True,
            confirmed_condition="Early Blight",
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 4))
        )
        db.add(c_case)
        db.commit()
        db.refresh(c_case)

        # Expert review confirming the case
        rev = ExpertReview(
            case_id=c_case.id,
            expert_id=expert_user.id,
            reviewed_at=datetime.utcnow() - timedelta(days=1),
            original_ai_condition="Early Blight",
            confirmed_condition="Early Blight",
            diagnostic_agreement="Confirmed",
            expert_severity="Moderate",
            advisory_notes="Early Blight confirmed by KVK Pathology wing. Recommended immediate canopy sanitation and bio-fungicide protective spray.",
            recommend_field_visit=True,
            recommend_lab_test=False,
            approved_for_training_dataset=True
        )
        db.add(rev)

    db.commit()

    # 8. Create the Primary Demo Case (Paddy Rice Blast scenario)
    paddy_crop = crop_entities["Paddy (Rice)"]
    paddy_stage = stage_entities["Paddy (Rice)"][3]
    paddy_variety = variety_entities["Paddy (Rice)"][0]
    print("Seeding primary SIH demonstration case: AGR-2026-PAD-01...")
    demo_case = DiseaseCase(
        case_number="AGR-2026-PAD-01",
        farmer_id=farmer_user.id,
        farm_id=primary_farm.id,
        crop_id=paddy_crop.id,
        variety_id=paddy_variety.id,
        stage_id=paddy_stage.id,
        image_url="/assets/samples/paddy_rice_blast_sample.jpg",
        is_leaf_or_plant=True,
        plant_verification_confidence=0.98,
        symptom_notes="Spindle-shaped gray-centered lesions with brown margins on paddy leaves.",
        ai_predicted_condition="Rice Blast",
        ai_confidence=0.84,
        estimated_severity="Moderate",
        severity_percentage=32.0,
        needs_expert_validation=True,  # Recommended expert validation
        multimodal_risk_score=78.0,
        risk_level="High",
        status="pending_expert",       # Ready for Expert to confirm
        is_confirmed=False,
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    db.add(demo_case)
    db.commit()
    db.refresh(demo_case)

    # Multimodal Risk Score breakdown
    risk_calc = multimodal_risk_service.calculate_risk(
        ai_confidence=0.84,
        condition_name="Rice Blast",
        weather_score=82.0,
        crop_stage_multiplier=1.4,
        nearby_confirmed_cases=6,
        nearby_radius_km=5.0,
        pest_trap_count=37,
        pest_etl=20,
        weather_drivers=[
            "Elevated relative humidity (86.0%) and rainfall (18.5 mm)",
            "Leaf wetness exceeding 6.5 hours creates rapid spore germination window"
        ],
        crop_stage_name="Flowering & Heading"
    )

    risk_score_entity = MultimodalRiskScore(
        case_id=demo_case.id,
        visual_evidence_score=risk_calc["visual_evidence_score"],
        weather_suitability_score=risk_calc["weather_suitability_score"],
        crop_susceptibility_score=risk_calc["crop_susceptibility_score"],
        geo_proximity_score=risk_calc["geo_proximity_score"],
        pest_pressure_score=risk_calc["pest_pressure_score"],
        final_score=78.0,
        risk_tier="High",
        factors_explanation=risk_calc["factors_explanation"]
    )
    db.add(risk_score_entity)

    # IPM Guidance
    ipm_info = ipm_service.get_recommendation("Rice Blast")
    ipm_entity = IPMRecommendation(
        case_id=demo_case.id,
        condition_name="Rice Blast",
        cultural_control=ipm_info["cultural_control"],
        mechanical_control=ipm_info["mechanical_control"],
        biological_control=ipm_info["biological_control"],
        chemical_control_regulated=ipm_info["chemical_control_regulated"],
        safety_precautions=ipm_info["safety_precautions"],
        pre_harvest_interval_days=ipm_info["pre_harvest_interval_days"],
        extension_consultation_advised=True,
        official_disclaimer=ipm_info["official_disclaimer"]
    )
    db.add(ipm_entity)

    # Multilingual Advisories (EN, HI, TE)
    adv_list = advisory_service.generate_advisories("Rice Blast")
    for adv in adv_list:
        db.add(MultilingualAdvisory(
            case_id=demo_case.id,
            language_code=adv["language_code"],
            title=adv["title"],
            farmer_guidance_text=adv["farmer_guidance_text"],
            action_bullet_points=adv["action_bullet_points"],
            urgency=adv["urgency"]
        ))

    # Follow-up Record (Case after 7 days showing disease recovery)
    follow_up = FollowUpRecord(
        case_id=demo_case.id,
        follow_up_number=1,
        submission_date=datetime.utcnow() - timedelta(days=7),
        image_url="/assets/samples/paddy_rice_blast_followup.jpg",
        farmer_notes="Improved field drainage and applied the recommended paddy blast management treatment. New leaves show no expanding lesions.",
        foliage_condition="Improving",
        difference_score_pct=-35.0
    )
    db.add(follow_up)

    # Notifications
    db.add(Notification(
        user_id=farmer_user.id,
        title="High Disease Risk Alert (Paddy Rice Blast)",
        message="Risk: 78/100 — HIGH. Microclimate conditions and 6 nearby confirmed cases in Visakhapatnam indicate rapid fungal spread. Follow recommended IPM practices.",
        alert_type="disease_risk",
        severity="high"
    ))
    db.add(Notification(
        user_id=farmer_user.id,
        title="Pest Surge Alert: Fruit Fly Trap TRAP-102",
        message="Trap count reached 37 adults (exceeds economic threshold of 20). Inspect fruit clusters for oviposition puncture marks.",
        alert_type="pest_surge",
        severity="high"
    ))
    db.add(Notification(
        user_id=official_user.id,
        title="Epidemic Cluster Alert: Visakhapatnam Mandal",
        message="Active hotspot detected with 7 linked Rice Blast cases and rising Fruit Fly counts. High priority surveillance recommended.",
        alert_type="outbreak_warning",
        severity="critical"
    ))

    # Laboratory Referral sample
    db.add(LaboratoryReferral(
        case_id=demo_case.id,
        lab_name="Regional Krishi Vigyan Kendra (KVK) Plant Pathology Laboratory, Visakhapatnam",
        sample_type="Leaf Tissue",
        referral_reason="Confirmation of Magnaporthe oryzae spores and testing for paddy blast resistance.",
        status="In Analysis",
        findings="Microscopic observation: Rice blast spores observed. Confirmed Magnaporthe oryzae."
    ))

    db.commit()
    print("Successfully seeded SIH 2026 dataset!")
    return {
        "status": "success",
        "total_farms": len(created_farms),
        "total_traps": 25,
        "confirmed_cases_in_cluster": 6,
        "primary_demo_case": "AGR-2026-PAD-01",
        "demo_accounts": {
            "farmer": "farmer@agriraksha.in (farmer123)",
            "expert": "expert@agriraksha.in (expert123)",
            "official": "official@agriraksha.in (official123)",
            "extension": "extension@agriraksha.in (extension123)"
        }
    }
