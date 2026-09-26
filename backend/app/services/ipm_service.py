from typing import Dict, Any

IPM_KNOWLEDGE_BASE = {
    "Early Blight": {
        "condition_name": "Early Blight (Alternaria solani)",
        "cultural_control": "Prune and destroy infected lower leaves exhibiting concentric spots. Maintain adequate plant spacing to facilitate sunlight and air movement through the canopy. Irrigate strictly at the soil base (drip) rather than overhead sprinklers to prevent leaf moisture persistence. Implement a 3-year crop rotation avoiding Solanaceous crops.",
        "mechanical_control": "Apply straw or organic mulch around base of plants to prevent soil-splashing during rain. Stake and trellis tomato vines to keep foliage off wet soil.",
        "biological_control": "Foliar application of biocontrol agents such as Trichoderma viride or Pseudomonas fluorescens @ 5-10 g/liter of water in the evening hours. In early stages, apply 5% Neem Seed Kernel Extract (NSKE) as an organic deterrent.",
        "chemical_control_regulated": "Consult local Krishi Vigyan Kendra (KVK) or Assistant Director of Agriculture (ADA) before chemical application. Authoritative guidelines (CIB&RC approved): Mancozeb 75% WP or Copper Oxychloride 50% WP as protective sprays if weather forecast indicates persistent rainy overcast conditions.",
        "safety_precautions": "Wear personal protective equipment (PPE) including chemical-resistant nitrile gloves, face shield, and rubber boots. Do not spray during windy hours or prior to imminent rainfall. Store all agricultural formulations out of reach of children and livestock.",
        "pre_harvest_interval_days": 7,
        "extension_consultation_advised": True,
        "official_disclaimer": "All pesticide usage must strictly adhere to the Central Insecticides Board & Registration Committee (CIB&RC) label claims and Department of Agriculture regulations. The system does not prescribe chemical treatments without certified agronomist review."
    },
    "Late Blight": {
        "condition_name": "Late Blight (Phytophthora infestans)",
        "cultural_control": "Immediately rogue out and safely bury heavily infected plants in deep pits away from field borders. Avoid furrow flooding. Ensure rapid field drainage.",
        "mechanical_control": "Disinfect pruning shears and agricultural implements with 1% sodium hypochlorite solution between rows to halt mechanical transmission.",
        "biological_control": "Soil drenching and prophylactic foliar spray with Trichoderma harzianum formulation.",
        "chemical_control_regulated": "Contact local extension officer immediately for high-risk epidemic containment. Officially registered fungicide formulations such as Cymoxanil + Mancozeb or Dimethomorph applied strictly in accordance with ICAR package of practices.",
        "safety_precautions": "Mandatory use of N95 respirator mask and chemical overalls. Maintain a 48-hour restricted entry interval into the treated field.",
        "pre_harvest_interval_days": 10,
        "extension_consultation_advised": True,
        "official_disclaimer": "Emergency notification: Late Blight is highly contagious. Promptly report suspect foliage to the Mandal Agricultural Officer."
    },
    "Rice Blast": {
        "condition_name": "Rice Blast (Magnaporthe oryzae)",
        "cultural_control": "Avoid excessive split applications of nitrogenous fertilizers. Maintain shallow intermittent irrigation rather than severe drying or prolonged deep flooding.",
        "mechanical_control": "Clear weed hosts such as Echinochloa on bunds that serve as alternate reservoirs.",
        "biological_control": "Seed treatment and seedling root dip with Pseudomonas fluorescens @ 10g/kg seed.",
        "chemical_control_regulated": "ICAR approved protective spray: Tricyclazole 75% WP @ 0.6 g/L or Kasugamycin 3% SL @ 2.5 ml/L applied at early neck blast emergence as advised by extension staff.",
        "safety_precautions": "Ensure safety goggles and protective apron are worn during spray preparation. Avoid runoff into aquaculture ponds.",
        "pre_harvest_interval_days": 14,
        "extension_consultation_advised": True,
        "official_disclaimer": "Consult local Rice Research Station agronomists for variety-specific blast resistance ratings."
    },
    "Bacterial Leaf Blight": {
        "condition_name": "Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae)",
        "cultural_control": "Drain field flood water temporarily during early epidemic phase. Avoid excessive top-dressing of nitrogen; split nitrogen into smaller doses. Disinfect seed with hot water treatment (52-54°C for 10 min) before sowing.",
        "mechanical_control": "Clip leaf tips only if nursery clipping practice is avoided; clipping facilitates pathogen entry. Remove collateral weed hosts like Leersia oryzoides along water channels.",
        "biological_control": "Foliar spray with Pseudomonas fluorescens @ 10 g/L or application of fresh cow dung slurry extract (20%) which has proven antagonistic activity against Xanthomonas.",
        "chemical_control_regulated": "Copper Oxychloride 50% WP (1 kg/ha) + Streptomycin sulphate + Tetracycline hydrochloride combination (100 g/ha) strictly as approved by CIB&RC upon certified extension recommendation.",
        "safety_precautions": "Avoid spraying against wind direction. Wear face shield and protective nitrile gloves during bactericide mixing.",
        "pre_harvest_interval_days": 15,
        "extension_consultation_advised": True,
        "official_disclaimer": "Bacterial Leaf Blight is seed-borne and water-borne. Consult local Mandal Agricultural Officer immediately upon wavy margin symptom appearance."
    },
    "Brown Spot": {
        "condition_name": "Brown Spot (Bipolaris oryzae)",
        "cultural_control": "Correct soil nutritional deficiencies, especially potassium, silicon, and zinc. Avoid drought stress and water stagnation; maintain alternate wetting and drying (AWD).",
        "mechanical_control": "Plough in rice stubble immediately after harvest to accelerate decomposition of fungal perithecia.",
        "biological_control": "Seed treatment with Trichoderma harzianum @ 10 g/kg seed + soil enrichment with neem cake @ 150 kg/acre.",
        "chemical_control_regulated": "Protective foliar application: Mancozeb 75% WP @ 2 g/L or Propiconazole 25% EC @ 1 ml/L at tillering and boot leaf stages.",
        "safety_precautions": "Wear protective gear. Keep domestic animals away from treated field bunds for 48 hours.",
        "pre_harvest_interval_days": 14,
        "extension_consultation_advised": True,
        "official_disclaimer": "Brown spot is aggravated in nutrient-depleted soils. Conduct soil testing at local Rythu Bharosa Kendram (RBK)."
    },
    "Leaf Scald": {
        "condition_name": "Leaf Scald (Microdochium albescens)",
        "cultural_control": "Ensure balanced NPK fertilization (120:60:40 kg/ha); avoid excess nitrogenous manure. Maintain wider plant spacing (20 x 15 cm) to reduce canopy humidity.",
        "mechanical_control": "Rogue out infected tillers showing concentric brown banded scald lesions on tips and bury away from field.",
        "biological_control": "Seed bio-priming with Bacillus subtilis @ 10 ml/kg seed to suppress seed-borne inoculum.",
        "chemical_control_regulated": "Carbendazim 50% WP @ 1 g/L or Hexaconazole 5% EC @ 2 ml/L sprayed when lesions first appear on upper leaves.",
        "safety_precautions": "Store chemicals in locked original containers. Wear respirator and gloves during application.",
        "pre_harvest_interval_days": 12,
        "extension_consultation_advised": True,
        "official_disclaimer": "Leaf scald can lead to substantial glume discoloration. Consult agronomist for resistant cultivar recommendations."
    },
    "Sheath Blight": {
        "condition_name": "Sheath Blight (Rhizoctonia solani)",
        "cultural_control": "Maintain adequate plant spacing; avoid dense planting. Apply slow-release nitrogen fertilizers. Skim floating sclerotia during puddling and burn or bury crop debris.",
        "mechanical_control": "Remove infected lower sheaths showing greenish-grey water-soaked lesions before the pathogen reaches the upper canopy.",
        "biological_control": "Soil application of Trichoderma viride @ 2.5 kg/ha mixed with 50 kg well-decomposed FYM at planting time.",
        "chemical_control_regulated": "Hexaconazole 5% SC @ 2 ml/L or Validamycin 3% L @ 2.5 ml/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L applied at boot leaf stage.",
        "safety_precautions": "Ensure protective footwear; avoid direct skin contact. Maintain 14-day pre-harvest interval.",
        "pre_harvest_interval_days": 14,
        "extension_consultation_advised": True,
        "official_disclaimer": "Sheath Blight spreads rapidly in high humidity (>85%). Monitor field bunds and lower culms regularly."
    },
    "Healthy Rice Leaf": {
        "condition_name": "Healthy Rice Foliage (Oryza sativa)",
        "cultural_control": "Maintain optimal irrigation schedule with alternate wetting and drying. Adhere to recommended balanced fertilizer dosage (NPK) according to soil health card.",
        "mechanical_control": "Keep field bunds free from weed hosts. Monitor pest sticky traps weekly.",
        "biological_control": "Conserve beneficial natural predators (spiders, dragonflies, mirid bugs) by avoiding unnecessary chemical applications.",
        "chemical_control_regulated": "No chemical treatment required. Crop foliage is vibrant, vigorous, and disease-free.",
        "safety_precautions": "Continue standard field hygiene and periodic surveillance.",
        "pre_harvest_interval_days": 0,
        "extension_consultation_advised": False,
        "official_disclaimer": "Healthy crop foliage confirmed. Regular scouting recommended every 5-7 days."
    },
    "Default": {
        "condition_name": "General Plant Health Concern",
        "cultural_control": "Inspect the field systematically using a 'W' or 'Z' walking pattern. Remove chlorotic or pest-damaged foliage.",
        "mechanical_control": "Install appropriate yellow sticky or pheromone traps to identify pest presence before visible plant damage occurs.",
        "biological_control": "Encourage natural predator insects (ladybird beetles, green lacewings) and avoid broad-spectrum non-targeted sprays.",
        "chemical_control_regulated": "No chemical application recommended without confirmed diagnosis. Consult your local agricultural extension officer.",
        "safety_precautions": "Always wear protective gear during any field maintenance.",
        "pre_harvest_interval_days": 0,
        "extension_consultation_advised": True,
        "official_disclaimer": "Always consult with your nearest Krishi Vigyan Kendra (KVK) officer for personalized on-field diagnosis."
    }
}

class IPMService:
    @staticmethod
    def get_recommendation(condition_name: str) -> Dict[str, Any]:
        rec = IPM_KNOWLEDGE_BASE.get(condition_name)
        if not rec:
            for k in IPM_KNOWLEDGE_BASE:
                if k.lower() in condition_name.lower():
                    rec = IPM_KNOWLEDGE_BASE[k]
                    break
        if not rec:
            rec = IPM_KNOWLEDGE_BASE["Default"]
        return rec

ipm_service = IPMService()
