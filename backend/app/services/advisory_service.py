from typing import Dict, Any, List

ADVISORY_TEMPLATES = {
    "Early Blight": {
        "en": {
            "title": "Tomato Early Blight Alert — Action Required",
            "farmer_guidance_text": "Weather conditions are favorable for early blight development. Inspect lower leaves for dark circular spots and monitor your field closely. Avoid overhead watering and remove spotted bottom leaves.",
            "action_bullet_points": [
                "Inspect lower leaves of tomato plants for concentric brown spots.",
                "Remove and safely dispose of infected bottom leaves.",
                "Water plants at the base (drip) rather than wetting the leaves.",
                "Spray organic Trichoderma viride bio-fungicide in the late afternoon.",
                "If spots spread rapidly, request extension officer verification."
            ],
            "urgency": "Urgent"
        },
        "hi": {
            "title": "टमाटर अगेती झुलसा (अर्ली ब्लाइट) चेतावनी — त्वरित कदम उठाएं",
            "farmer_guidance_text": "मौसम की स्थिति अगेती झुलसा रोग के प्रसार के अनुकूल है। निचली पत्तियों पर गहरे गोल धब्बों की जांच करें और खेत की बारीकी से निगरानी करें। पत्तियों पर पानी छिड़कने से बचें और रोगग्रस्त पत्तियों को तुरंत हटा दें।",
            "action_bullet_points": [
                "टमाटर के पौधों की निचली पत्तियों पर गहरे गोल छल्लेदार धब्बों की जांच करें।",
                "संक्रमित निचली पत्तियों को तोड़कर खेत से दूर नष्ट कर दें।",
                "फव्वारे की जगह जड़ों में बूंद-बूंद (ड्रिप) पानी दें ताकि पत्तियां सूखी रहें।",
                "शाम के समय ट्राइकोडर्मा विरिडी जैव-फफूंदनाशी का छिड़काव करें।",
                "यदि धब्बे बढ़ें, तो कृषि विस्तार अधिकारी से सलाह लें।"
            ],
            "urgency": "Urgent"
        },
        "te": {
            "title": "టమోటా ముందస్తు తెగులు (ఎర్లీ బ్లైట్) హెచ్చరిక — తక్షణ చర్యలు",
            "farmer_guidance_text": "వాతావరణ పరిస్థితులు ఎర్లీ బ్లైట్ తెగులు వ్యాప్తికి అనుకూలంగా ఉన్నాయి. క్రింది ఆకులపై ముదురు రంగు వలయాకార మచ్చలను గమనించి, పంటను నిశితంగా పరిశీలించండి. పైనుండి నీరు చిలకరించవద్దు, మచ్చలున్న క్రింది ఆకులను తుంచివేయండి.",
            "action_bullet_points": [
                "టమోటా మొక్కల క్రింది ఆకులపై వలయాకారపు గోధుమ రంగు మచ్చలను పరిశీలించండి.",
                "తెగులు సోకిన క్రింది ఆకులను తుంచి, పొలానికి దూరంగా నాశనం చేయండి.",
                "ఆకులపై నీరు పడకుండా డ్రిప్ ద్వారా మొదట్లోనే నీరు అందించండి.",
                "సాయంత్రం వేళల్లో ట్రైకోడెర్మా విరిడి వంటి జీవ శిలీంద్రనాశని పిచికారీ చేయండి.",
                "మచ్చలు వేగంగా వ్యాపిస్తే వెంటనే వ్యవసాయ విస్తరణ అధికారిని సంప్రదించండి."
            ],
            "urgency": "Urgent"
        }
    },
    "Late Blight": {
        "en": {
            "title": "Severe Late Blight Risk — Immediate Inspection",
            "farmer_guidance_text": "High humidity and cool damp weather are rapidly multiplying late blight risk. Check leaves for large water-soaked spots with white mold underneath.",
            "action_bullet_points": [
                "Scout fields every morning for water-soaked lesions.",
                "Pull out and bury severely infected plants immediately.",
                "Ensure standing water drains quickly from furrows.",
                "Contact local agricultural extension staff right away."
            ],
            "urgency": "Immediate Action"
        },
        "hi": {
            "title": "पछेती झुलसा (लेट ब्लाइट) का गंभीर खतरा — तुरंत जांच करें",
            "farmer_guidance_text": "अधिक नमी और ठंडे नम मौसम के कारण पछेती झुलसा का खतरा बहुत बढ़ गया है। पत्तियों के नीचे सफेद फफूंद वाले पानी जैसे धब्बों की जांच करें।",
            "action_bullet_points": [
                "रोज सुबह खेत में पानी जैसे धब्बों की जांच करें।",
                "गंभीर रूप से खराब पौधों को उखाड़कर गहरे गड्ढे में दबा दें।",
                "खेत में जमा पानी को तुरंत बाहर निकालें।",
                "तुरंत स्थानीय कृषि अधिकारी से संपर्क करें।"
            ],
            "urgency": "Immediate Action"
        },
        "te": {
            "title": "లేట్ బ్లైట్ తీవ్రమైన ముప్పు — వెంటనే పొలాన్ని పరిశీలించండి",
            "farmer_guidance_text": "అధిక తేమ మరియు చల్లని వాతావరణం లేట్ బ్లైట్ వ్యాప్తికి కారణమవుతాయి. ఆకుల అడుగున తెల్లటి బూజు మరియు నీటి మచ్చలను గమనించండి.",
            "action_bullet_points": [
                "రోజూ ఉదయం ఆకులపై నీటి మచ్చలు ఉన్నాయేమో పరిశీలించండి.",
                "ఎక్కువగా దెబ్బతిన్న మొక్కలను పీకి భూమిలో పాతిపెట్టండి.",
                "మడులలో నిలిచిన నీటిని వెంటనే బయటకు పంపండి.",
                "వెంటనే మండల వ్యవసాయ అధికారికి తెలియజేయండి."
            ],
            "urgency": "Immediate Action"
        }
    },
    "Bacterial Leaf Blight": {
        "en": {
            "title": "Rice Bacterial Leaf Blight Alert — Urgent Action",
            "farmer_guidance_text": "Water-soaked streaks with wavy margins detected along leaf blades. Drain standing flood water immediately and pause top-dressing nitrogen to halt bacterial multiplication.",
            "action_bullet_points": [
                "Drain standing water from paddy fields temporarily for 3-4 days.",
                "Avoid applying excess urea/nitrogen fertilizer.",
                "Spray fresh cow-dung extract (20%) or Pseudomonas fluorescens @ 10g/L.",
                "Report suspect field borders to the Mandal Agricultural Officer (MAO)."
            ],
            "urgency": "Urgent"
        },
        "hi": {
            "title": "धान जीवाणु पत्ती झुलसा चेतावनी — तत्काल कार्रवाई",
            "farmer_guidance_text": "पत्तियों के किनारों पर लहरदार पानी जैसे धब्बे दिखे हैं। खेत से अतिरिक्त पानी तुरंत निकालें और यूरिया का छिड़काव रोकें।",
            "action_bullet_points": [
                "धान के खेत से 3-4 दिनों के लिए जमा पानी निकाल दें।",
                "अधिक नाइट्रोजन (यूरिया) खाद का प्रयोग न करें।",
                "स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/लीटर) का छिड़काव करें।",
                "कृषि अधिकारी से तुरंत संपर्क करें।"
            ],
            "urgency": "Urgent"
        },
        "te": {
            "title": "వరి బాక్టీరియల్ ఆకు ఎండు తెగులు హెచ్చరిక — తక్షణ చర్యలు",
            "farmer_guidance_text": "ఆకుల అంచుల వెంట అలల రూపంలో తడి మచ్చలు గమనించబడ్డాయి. పొలంలో నిల్వ ఉన్న నీటిని వెంటనే తీసివేసి, యూరియా వాడకాన్ని తాత్కాలికంగా ఆపండి.",
            "action_bullet_points": [
                "వరి మడుల్లో నిల్వ ఉన్న నీటిని 3-4 రోజులు తీసివేయండి.",
                "యూరియా పైపాటుగా చల్లడం ఆపండి.",
                "సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "మండల వ్యవసాయ అధికారి (MAO) ని సంప్రదించండి."
            ],
            "urgency": "Urgent"
        }
    },
    "Brown Spot": {
        "en": {
            "title": "Rice Brown Spot Warning — Soil & Foliar Care",
            "farmer_guidance_text": "Oval dark brown spots with yellow halos detected. This condition indicates potential potash or zinc deficiency aggravated by drought or flooding stress.",
            "action_bullet_points": [
                "Apply recommended muriate of potash and zinc sulphate according to soil test.",
                "Maintain Alternate Wetting and Drying (AWD) irrigation.",
                "Apply Trichoderma harzianum or Mancozeb 75% WP @ 2g/L if spotting spreads.",
                "Visit local Rythu Bharosa Kendram (RBK) for soil health verification."
            ],
            "urgency": "Moderate"
        },
        "hi": {
            "title": "धान भूरा धब्बा रोग चेतावनी — मिट्टी व फसल की देखभाल",
            "farmer_guidance_text": "पत्तियों पर पीले घेरे वाले गहरे भूरे धब्बे दिखे हैं। यह पोटाश व जिंक की कमी और जल असंतुलन से बढ़ता है।",
            "action_bullet_points": [
                "खेत में पोटाश और जिंक सल्फेट की उचित मात्रा डालें।",
                "खेत में आवश्यकतानुसार हल्का पानी दें और सूखने दें।",
                "मैनकोज़ेब 75% WP (2 ग्राम/लीटर) का छिड़काव करें।",
                "स्थानीय कृषि केंद्र पर संपर्क करें।"
            ],
            "urgency": "Moderate"
        },
        "te": {
            "title": "వరి ఎండి మచ్చ తెగులు హెచ్చరిక — పోషక నిర్వహణ",
            "farmer_guidance_text": "ఆకులపై పసుపు రంగు వలయంతో కూడిన గోధుమ రంగు మచ్చలు గమనించబడ్డాయి. ఇది పొటాష్ లేదా జింక్ లోపం వల్ల తీవ్రమవుతుంది.",
            "action_bullet_points": [
                "సిఫార్సు చేసిన పొటాష్ మరియు జింక్ సల్ఫేట్ ఎరువులను వేయండి.",
                "ఆరుతడి పద్ధతిలో నీటి యాజమాన్యం పాటించండి.",
                "మ్యాంకోజెబ్ 2 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "రైతు భరోసా కేంద్రం (RBK) లో సంప్రదించండి."
            ],
            "urgency": "Moderate"
        }
    },
    "Leaf Blast": {
        "en": {
            "title": "Rice Leaf Blast Epidemic Warning — Immediate Containment",
            "farmer_guidance_text": "Spindle-shaped elliptical lesions with gray centers observed on paddy foliage. High atmospheric humidity and leaf wetness accelerate blast spore dissemination.",
            "action_bullet_points": [
                "Scout all tillers for neck blast or node infection.",
                "Avoid high nitrogen split doses.",
                "Prophylactic bio-spray of Pseudomonas fluorescens @ 10g/L.",
                "Consult KVK or Agriculture Officer for CIB&RC approved Tricyclazole 75% WP guidelines."
            ],
            "urgency": "Immediate Action"
        },
        "hi": {
            "title": "धान ब्लास्ट (झोंका रोग) गंभीर चेतावनी — तत्काल बचाव",
            "farmer_guidance_text": "पत्तियों पर धूसर केंद्र वाले नाव के आकार के धब्बे दिखे हैं। अधिक नमी इस रोग को तेजी से फैलाती है।",
            "action_bullet_points": [
                "सभी पौधों की तुरंत जांच करें।",
                "अत्यधिक नाइट्रोजन का प्रयोग रोकें।",
                "स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/लीटर) का छिड़काव करें।",
                "कृषि अधिकारी से सलाह लेकर ट्राइसाइक्लाजोल 75% WP का प्रयोग करें।"
            ],
            "urgency": "Immediate Action"
        },
        "te": {
            "title": "వరి అగ్గితెగులు (బ్లాస్ట్) తీవ్ర హెచ్చరిక — అత్యవసర చర్యలు",
            "farmer_guidance_text": "ఆకులపై నూలు కండె ఆకారపు మచ్చలు కనిపించాయి. అధిక తేమ మరియు మంచు వల్ల అగ్గితెగులు వేగంగా వ్యాపిస్తుంది.",
            "action_bullet_points": [
                "పిలకలు మరియు కణుపులను రోజూ పరిశీలించండి.",
                "నత్రజని ఎరువుల వాడకాన్ని తగ్గించండి.",
                "సూడోమోనాస్ ఫ్లోరోసెన్స్ జీవ శిలీంద్రనాశని పిచికారీ చేయండి.",
                "వ్యవసాయ అధికారి సలహా మేరకు ట్రైసైక్లాజోల్ 0.6 గ్రాములు లీటరు నీటికి పిచికారీ చేయండి."
            ],
            "urgency": "Immediate Action"
        }
    },
    "Sheath Blight": {
        "en": {
            "title": "Rice Sheath Blight Alert — Microclimate Threat",
            "farmer_guidance_text": "Greenish-grey water-soaked lesions developing along lower leaf sheaths. Dense canopy and humidity favor upward spread to flag leaves.",
            "action_bullet_points": [
                "Clear crop residue and weed hosts from field bunds.",
                "Maintain wider aeration spacing between rows.",
                "Apply Validamycin 3% L @ 2.5 ml/L or Hexaconazole 5% SC @ 2 ml/L at boot leaf stage.",
                "Ensure protective boots and gloves during field treatment."
            ],
            "urgency": "Urgent"
        },
        "hi": {
            "title": "धान शीथ ब्लाइट चेतावनी — तना झुलसा रोग",
            "farmer_guidance_text": "निचले तनों पर हरे-धूसर पानी जैसे धब्बे दिख रहे हैं। घनी फसल और अधिक नमी से यह रोग तेजी से ऊपर फैलता है।",
            "action_bullet_points": [
                "खेत की मेड़ों को खरपतवार मुक्त रखें।",
                "हवा के प्रवाह के लिए पौधों के बीच दूरी बनाए रखें।",
                "वैलिडामाइसिन (2.5 मिली/लीटर) या हेक्साकोनाजोल का छिड़काव करें।",
                "सुरक्षात्मक उपकरण पहनें।"
            ],
            "urgency": "Urgent"
        },
        "te": {
            "title": "వరి పాము పొడ తెగులు (షీత్ బ్లైట్) హెచ్చరిక",
            "farmer_guidance_text": "క్రింది మొదళ్లపై పాము పొడ వంటి ఆకుపచ్చ-బూడిద మచ్చలు గమనించబడ్డాయి. అధిక తేమ వల్ల ఇది పై ఆకులకు పాకుతుంది.",
            "action_bullet_points": [
                "గట్లపై ఉన్న కలుపు మొక్కలను తొలగించండి.",
                "గాలి వెలుతురు సోకేలా పాయలు తీయండి.",
                "వాలిడామైసిన్ 2.5 మి.లీ లేదా హెక్సాకొనజోల్ 2.0 మి.లీ లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "వ్యవసాయ నిపుణుడిని సంప్రదించండి."
            ],
            "urgency": "Urgent"
        }
    },
    "Leaf scald": {
        "en": {
            "title": "Rice Leaf Scald Alert — Foliage Protection",
            "farmer_guidance_text": "Zonate scald lesions with alternating light and dark bands expanding from leaf tips. Keep plant nutrition balanced.",
            "action_bullet_points": [
                "Avoid high doses of nitrogenous fertilizers.",
                "Ensure proper field drainage.",
                "Apply Carbendazim 50% WP @ 1g/L if lesions expand.",
                "Consult extension officer for variety susceptibility."
            ],
            "urgency": "Moderate"
        },
        "hi": {
            "title": "धान लीफ स्काल्ड (पत्ती झुलसा) अलर्ट",
            "farmer_guidance_text": "पत्तियों की नोक से हल्के व गहरे रंग की धारियों वाले धब्बे फैल रहे हैं। संतुलित खाद का प्रयोग करें।",
            "action_bullet_points": [
                "नाइट्रोजन खाद का अत्यधिक प्रयोग न करें।",
                "खेत में जल निकासी की उचित व्यवस्था रखें।",
                "कार्बेन्डाजिम (1 ग्राम/लीटर) का छिड़काव करें।",
                "कृषि अधिकारी से सलाह लें।"
            ],
            "urgency": "Moderate"
        },
        "te": {
            "title": "వరి లీఫ్ స్కాల్డ్ హెచ్చరిక — ఆకు సంరక్షణ",
            "farmer_guidance_text": "ఆకు కొనల నుండి ముదురు, లేత గోధుమ రంగు పట్టెలతో కూడిన మచ్చలు విస్తరిస్తున్నాయి. సమతుల్య ఎరువులు వాడండి.",
            "action_bullet_points": [
                "అధిక నత్రజని వాడకాన్ని నివారించండి.",
                "పొలంలో నీటి పారుదల సక్రమంగా ఉండేలా చూడండి.",
                "కార్బండజిమ్ 1 గ్రాము లీటరు నీటికి పిచికారీ చేయండి.",
                "స్థానిక వ్యవసాయ విస్తరణ అధికారిని సంప్రదించండి."
            ],
            "urgency": "Moderate"
        }
    },
    "Healthy Rice Leaf": {
        "en": {
            "title": "Healthy Crop Status Confirmed — Routine Scouting",
            "farmer_guidance_text": "Crop foliage is vibrant, upright, and free from disease lesions. Maintain current balanced nutrition and scouting practices.",
            "action_bullet_points": [
                "No pesticide or fungicide application needed.",
                "Maintain balanced NPK fertilization per soil health card.",
                "Scout fields weekly for early symptoms or insect pests.",
                "Preserve natural beneficial predators (spiders, dragonflies)."
            ],
            "urgency": "Routine"
        },
        "hi": {
            "title": "फसल पूरी तरह स्वस्थ है — नियमित निगरानी रखें",
            "farmer_guidance_text": "धान की पत्तियां हरी और रोगमुक्त हैं। किसी भी रासायनिक छिड़काव की आवश्यकता नहीं है।",
            "action_bullet_points": [
                "किसी कीटनाशक या फफूंदनाशी की जरूरत नहीं है।",
                "मृदा स्वास्थ्य कार्ड के अनुसार खाद डालें।",
                "सप्ताह में एक बार खेत का सामान्य निरीक्षण करें।",
                "मित्र कीटों (मकड़ी, ड्रैगनफ्लाई) को सुरक्षित रखें।"
            ],
            "urgency": "Routine"
        },
        "te": {
            "title": "వరి పంట ఆరోగ్యంగా ఉంది — సాధారణ పర్యవేక్షణ",
            "farmer_guidance_text": "వరి ఆకులు ఏవిధమైన తెగులు మచ్చలు లేకుండా పచ్చగా, బలంగా ఉన్నాయి. రసాయన మందుల పిచికారీ అవసరం లేదు.",
            "action_bullet_points": [
                "ఎటువంటి పురుగు లేదా తెగులు మందులు చల్లవద్దు.",
                "భూసార పరీక్ష ప్రకారం సమతుల్య ఎరువులు వేయండి.",
                "వారానికి ఒకసారి సాధారణ పరిశీలన చేయండి.",
                "మిత్రపురుగులను (సాలీళ్ళు, తూనీగలు) సంరక్షించండి."
            ],
            "urgency": "Routine"
        }
    },
    "Default": {
        "en": {
            "title": "Crop Health Advisory",
            "farmer_guidance_text": "Monitor your field closely and ensure proper irrigation and aeration.",
            "action_bullet_points": [
                "Walk through your field regularly to spot early symptoms.",
                "Maintain clean farm borders and clean tools.",
                "Consult your extension officer if abnormal leaf spotting occurs."
            ],
            "urgency": "Routine"
        },
        "hi": {
            "title": "फसल स्वास्थ्य सलाह",
            "farmer_guidance_text": "अपने खेत की नियमित निगरानी करें और उचित सिंचाई व हवा का प्रवाह बनाए रखें।",
            "action_bullet_points": [
                "शुरुआती लक्षणों को देखने के लिए नियमित रूप से खेत का निरीक्षण करें।",
                "खेत की मेड़ों और औजारों को साफ रखें।",
                "असामान्य लक्षण दिखने पर कृषि अधिकारी से संपर्क करें।"
            ],
            "urgency": "Routine"
        },
        "te": {
            "title": "పంట ఆరోగ్య సలహా",
            "farmer_guidance_text": "మీ పొలాన్ని నిరంతరం పరిశీలించండి మరియు సరైన నీటి పారుదల ఉండేలా చూసుకోండి.",
            "action_bullet_points": [
                "ముందస్తు లక్షణాలను గుర్తించడానికి రోజూ పొలాన్ని గమనించండి.",
                "పొలం గట్లు మరియు పరికరాలను శుభ్రంగా ఉంచండి.",
                "అనుమానాస్పద మచ్చలు కనిపిస్తే వ్యవసాయ అధికారిని సంప్రదించండి."
            ],
            "urgency": "Routine"
        }
    }
}

class AdvisoryService:
    @staticmethod
    def generate_advisories(condition_name: str) -> List[Dict[str, Any]]:
        cond_key = "Default"
        for k in ADVISORY_TEMPLATES:
            if k.lower() in condition_name.lower():
                cond_key = k
                break

        lang_data = ADVISORY_TEMPLATES.get(cond_key, ADVISORY_TEMPLATES["Default"])
        
        advisories = []
        for lang_code in ["en", "hi", "te"]:
            template = lang_data.get(lang_code, lang_data["en"])
            advisories.append({
                "language_code": lang_code,
                "title": template["title"],
                "farmer_guidance_text": template["farmer_guidance_text"],
                "action_bullet_points": template["action_bullet_points"],
                "urgency": template["urgency"]
            })
        return advisories

advisory_service = AdvisoryService()
