export type Language = 'en' | 'hi' | 'te';

export const translations = {
  en: {
    appTitle: "AgriRaksha",
    tagline: "AI-Powered Crop Health Early Warning & Decision Support",
    farmerPortal: "Farmer Portal",
    expertPortal: "Expert Review",
    officialPortal: "GIS Surveillance",
    loadDemo: "Load Demo Dataset",
    loadingDemo: "Seeding Demo Data...",
    demoLoaded: "Demo Data Loaded! (105 Farms, Outbreaks, Traps)",
    switchRole: "Switch Role",
    
    // Farmer Quick Tiles
    myCrops: "My Crops",
    currentRisks: "Current Risks",
    checkPlant: "Check Plant",
    weather: "Weather",
    pestMonitoring: "Pest Monitoring",
    nearbyRisk: "Nearby Risk",
    recommendations: "IPM Advice",
    askExpert: "Ask Expert",

    // Crop Diagnostic
    stepSelectCrop: "Select Crop & Phenological Stage",
    selectCrop: "Crop",
    selectVariety: "Variety (if known)",
    selectStage: "Growth Stage",
    captureOrUpload: "Capture or Upload Leaf Image",
    takePhoto: "Take Photo / Choose Image",
    sampleImageOption: "Use Sample Image",
    growthReference: "Growth Reference",
    currentStage: "Current",
    maizeStages: ["Seedling", "Vegetative Growth", "Tasseling", "Silking & Grain Filling", "Maturity"],
    paddyStages: ["Nursery / Seedling", "Tillering", "Panicle Initiation", "Flowering & Grain Filling", "Maturity"],
    groundnutStages: ["Germination", "Vegetative Growth", "Flowering & Pegging", "Pod Development", "Maturity"],
    analyzeButton: "Run Multimodal AI Diagnosis",
    analyzing: "Analyzing foliage, microclimate & local traps...",

    // Diagnostic Results
    diagnosisTitle: "Preliminary AI Diagnostic Assessment",
    confidence: "Confidence",
    severity: "Severity",
    multimodalRiskScore: "Multimodal Risk Score",
    uncertaintyWarning: "Notice: Probabilistic AI detection. Not a confirmed diagnosis.",
    expertVerificationNeeded: "⚠️ High Disease Risk — Agronomist Verification Recommended",
    requestExpertBtn: "Request Official Expert Verification",
    expertRequested: "✓ Request sent to Mandal Agricultural Officer & KVK Pathologist",
    
    // Factors
    contributingFactors: "Contributing Risk Factors (Explainable AI)",
    visualEvidence: "Visual Symptoms",
    weatherSuitability: "Weather & Humidity",
    cropSusceptibility: "Growth Stage Sensitivity",
    geoHistory: "Nearby Confirmed Outbreaks",
    pestPressure: "Pest-Trap Surge",

    // IPM & Safety
    ipmTitle: "Integrated Pest Management (IPM) Protocols",
    culturalControl: "Cultural Management",
    mechanicalControl: "Mechanical / Physical Control",
    biologicalControl: "Biological Control",
    chemicalControl: "Regulated Chemical (Advisory Only)",
    safetyPrecautions: "Safety & PPE Precautions",
    disclaimer: "Non-Fabrication Notice: Chemical recommendations comply with CIB&RC statutory guidelines. Do not apply unverified chemicals.",

    // Weather
    temp: "Temperature",
    humidity: "Relative Humidity",
    rainfall: "Rainfall (24h)",
    leafWetness: "Leaf Wetness",
    sporeRisk: "Spore Germination Risk",
    rainAlertTitle: "Heavy Rain Alert",
    rainProbability: "rain probability in 24 hours",
    rainAlertAction: "Secure harvested produce, pause spraying, and check field drainage.",
    rainAlertWindow: "High-priority weather alarm",
    enableAlarm: "Enable alarm",
    alertsEnabled: "Alarm enabled",
    dismiss: "Dismiss",

    // Pest Traps
    trapId: "Trap ID",
    targetPest: "Target Pest",
    count: "Count",
    trend: "Trend",
    etl: "Economic Threshold Level (ETL)",

    // Follow-up
    followupTitle: "7-Day Case Monitoring & Recovery",
    submitFollowup: "Submit Follow-Up Leaf Image",
    statusImproving: "Foliage Condition: Improving (-35% lesion area)"
  },
  hi: {
    appTitle: "कृषि रक्षा (AgriRaksha)",
    tagline: "एआई-संचालित फसल स्वास्थ्य पूर्व चेतावनी और निर्णय समर्थन प्रणाली",
    farmerPortal: "किसान पोर्टल",
    expertPortal: "विशेषज्ञ समीक्षा",
    officialPortal: "जीआईएस निगरानी",
    loadDemo: "डेमो डेटा लोड करें",
    loadingDemo: "डेटा लोड हो रहा है...",
    demoLoaded: "डेमो डेटा तैयार है! (105 खेत, प्रकोप, ट्रैप)",
    switchRole: "भूमिका बदलें",

    // Farmer Quick Tiles
    myCrops: "मेरी फसलें",
    currentRisks: "वर्तमान जोखिम",
    checkPlant: "पौधे की जांच करें",
    weather: "मौसम",
    pestMonitoring: "कीट निगरानी",
    nearbyRisk: "नजदीकी जोखिम",
    recommendations: "आईपीएम सलाह",
    askExpert: "विशेषज्ञ से पूछें",

    // Crop Diagnostic
    stepSelectCrop: "फसल और विकास अवस्था चुनें",
    selectCrop: "फसल",
    selectVariety: "किस्म (यदि ज्ञात हो)",
    selectStage: "विकास अवस्था",
    captureOrUpload: "पत्ती की तस्वीर लें या अपलोड करें",
    takePhoto: "फोटो लें / तस्वीर चुनें",
    sampleImageOption: "नमूना छवि का उपयोग करें",
    growthReference: "विकास अवस्था संदर्भ",
    currentStage: "वर्तमान अवस्था",
    maizeStages: ["अंकुर अवस्था", "वानस्पतिक विकास", "टैसलिंग", "सिल्किंग और दाना भरना", "परिपक्वता"],
    paddyStages: ["नर्सरी / अंकुर", "कल्ले निकलना", "बालियां बनना", "फूल और दाना भरना", "परिपक्वता"],
    groundnutStages: ["अंकुरण", "वानस्पतिक विकास", "फूल और पेगिंग", "फली विकास", "परिपक्वता"],
    analyzeButton: "मल्टीमॉडल एआई निदान शुरू करें",
    analyzing: "पत्ती, मौसम और स्थानीय कीट ट्रैप का विश्लेषण जारी है...",

    // Diagnostic Results
    diagnosisTitle: "प्रारंभिक एआई निदान मूल्यांकन",
    confidence: "सटीकता / विश्वास",
    severity: "गंभीरता",
    multimodalRiskScore: "मल्टीमॉडल जोखिम स्कोर",
    uncertaintyWarning: "सूचना: यह एआई आधारित संभावित निदान है, प्रमाणित प्रयोगशाला रिपोर्ट नहीं।",
    expertVerificationNeeded: "⚠️ उच्च रोग जोखिम — कृषि विशेषज्ञ द्वारा सत्यापन की सिफारिश की जाती है",
    requestExpertBtn: "कृषि विशेषज्ञ से सत्यापन का अनुरोध करें",
    expertRequested: "✓ मंडल कृषि अधिकारी और केवीके विशेषज्ञ को अनुरोध भेज दिया गया है",

    // Factors
    contributingFactors: "जोखिम के मुख्य कारक (व्याख्यात्मक एआई)",
    visualEvidence: "पत्ती पर दृश्य लक्षण",
    weatherSuitability: "मौसम और नमी की अनुकूलता",
    cropSusceptibility: "फसल अवस्था संवेदनशीलता",
    geoHistory: "आसपास के प्रमाणित प्रकोप",
    pestPressure: "कीट ट्रैप में वृद्धि",

    // IPM & Safety
    ipmTitle: "एकीकृत कीट प्रबंधन (IPM) प्रोटोकॉल",
    culturalControl: "कृषि प्रबंधन (कल्चरल उपाय)",
    mechanicalControl: "यांत्रिक / भौतिक नियंत्रण",
    biologicalControl: "जैविक नियंत्रण (बायोकंट्रोल)",
    chemicalControl: "विनियमित रासायनिक छिड़काव (केवल सलाह)",
    safetyPrecautions: "सुरक्षा एवं व्यक्तिगत सुरक्षा उपकरण (PPE)",
    disclaimer: "सुरक्षा सूचना: रासायनिक सलाह सीआईबी एवं आरसी वैधानिक दिशा-निर्देशों के अनुरूप है। बिना विशेषज्ञ सलाह रासायनिक छिड़काव न करें।",

    // Weather
    temp: "तापमान",
    humidity: "सापेक्ष आर्द्रता",
    rainfall: "वर्षा (24 घंटे)",
    leafWetness: "पत्ती का गीलापन",
    sporeRisk: "फफूंद बीजाणु अंकुरण जोखिम",
    rainAlertTitle: "भारी वर्षा चेतावनी",
    rainProbability: "24 घंटे में वर्षा की संभावना",
    rainAlertAction: "कटी फसल सुरक्षित करें, छिड़काव रोकें और खेत की जल निकासी जांचें।",
    rainAlertWindow: "उच्च प्राथमिकता मौसम अलार्म",
    enableAlarm: "अलार्म चालू करें",
    alertsEnabled: "अलार्म चालू है",
    dismiss: "बंद करें",

    // Pest Traps
    trapId: "ट्रैप आईडी",
    targetPest: "लक्षित कीट",
    count: "कीट संख्या",
    trend: "रुझान",
    etl: "आर्थिक क्षति स्तर (ETL)",

    // Follow-up
    followupTitle: "7-दिवसीय अनुवर्ती निगरानी व सुधार",
    submitFollowup: "अनुवर्ती पत्ती की तस्वीर भेजें",
    statusImproving: "फसल स्वास्थ्य: सुधार जारी (-35% धब्बे कम)"
  },
  te: {
    appTitle: "అగ్రి రక్ష (AgriRaksha)",
    tagline: "కృత్రిమ మేధస్సు (AI) ఆధారిత పంట ఆరోగ్య ముందస్తు హెచ్చరిక & నిర్ణయ సహాయ వేదిక",
    farmerPortal: "రైతు వేదిక",
    expertPortal: "నిపుణుల సమీక్ష",
    officialPortal: "అధికారుల మ్యాప్ డాష్‌బోర్డ్",
    loadDemo: "డెమో డేటా లోడ్ చేయండి",
    loadingDemo: "డేటా సిద్ధమవుతోంది...",
    demoLoaded: "డెమో డేటా సిద్ధమైంది! (105 పొలాలు, తెగుళ్ల హాట్‌స్పాట్‌లు)",
    switchRole: "పాత్ర మార్చండి",

    // Farmer Quick Tiles
    myCrops: "నా పంటలు",
    currentRisks: "ప్రస్తుత ముప్పులు",
    checkPlant: "మొక్కను తనిఖీ చేయండి",
    weather: "వాతావరణం",
    pestMonitoring: "పురుగుల పర్యవేక్షణ",
    nearbyRisk: "చుట్టుపక్కల ముప్పు",
    recommendations: "సమగ్ర సలహాలు (IPM)",
    askExpert: "నిపుణుడిని అడగండి",

    // Crop Diagnostic
    stepSelectCrop: "పంట మరియు దశను ఎంచుకోండి",
    selectCrop: "పంట",
    selectVariety: "రకం (తెలిస్తే)",
    selectStage: "ఎదుగుదల దశ",
    captureOrUpload: "ఆకు ఫోటో తీయండి లేదా అప్‌లోడ్ చేయండి",
    takePhoto: "ఫోటో తీయండి / ఎంచుకోండి",
    sampleImageOption: "నమూనా చిత్రాన్ని ఉపయోగించండి",
    growthReference: "ఎదుగుదల దశల సూచన",
    currentStage: "ప్రస్తుత దశ",
    maizeStages: ["మొలక దశ", "శాఖీయ ఎదుగుదల", "టాసెలింగ్", "సిల్కింగ్ & గింజ నింపడం", "పక్వ దశ"],
    paddyStages: ["నర్సరీ / మొలక", "కలుపుల దశ", "పానికిల్ ప్రారంభం", "పూత & గింజ నింపడం", "పక్వ దశ"],
    groundnutStages: ["మొలకెత్తడం", "శాఖీయ ఎదుగుదల", "పూత & పెగ్గింగ్", "కాయ అభివృద్ధి", "పక్వ దశ"],
    analyzeButton: "మల్టీమోడల్ AI నిర్ధారణ చేయండి",
    analyzing: "ఆకు లక్షణాలు, వాతావరణం, పురుగుల ట్రాప్‌లను విశ్లేషిస్తోంది...",

    // Diagnostic Results
    diagnosisTitle: "ప్రాథమిక AI విశ్లేషణ నివేదిక",
    confidence: "ఖచ్చితత్వం",
    severity: "తీవ్రత",
    multimodalRiskScore: "సమగ్ర ముప్పు స్కోరు",
    uncertaintyWarning: "గమనిక: ఇది AI ఆధారిత సంభావ్యత మాత్రమే, ధృవీకరించబడిన ల్యాబ్ రిపోర్ట్ కాదు.",
    expertVerificationNeeded: "⚠️ అధిక తెగులు ముప్పు — వ్యవసాయ నిపుణుల ధృవీకరణ అవసరం",
    requestExpertBtn: "వ్యవసాయ అధికారి / నిపుణుడి ధృవీకరణ కోరండి",
    expertRequested: "✓ మండల వ్యవసాయ అధికారి & KVK నిపుణుడికి అభ్యర్థన చేరింది",

    // Factors
    contributingFactors: "ముప్పుకు గల ముఖ్య కారణాలు (వివరణాత్మక AI)",
    visualEvidence: "ఆకుపై కనిపించే లక్షణాలు",
    weatherSuitability: "తేమ & వాతావరణ అనుకూలత",
    cropSusceptibility: "పంట ఎదుగుదల దశ సున్నితత్వం",
    geoHistory: "చుట్టుపక్కల నమోదైన తెగుళ్ల వ్యాప్తి",
    pestPressure: "పురుగుల ట్రాప్‌లలో తీవ్రత",

    // IPM & Safety
    ipmTitle: "సమగ్ర సస్యరక్షణ (IPM) విధానాలు",
    culturalControl: "సాగు పద్ధతులు (కల్చరల్ చర్యలు)",
    mechanicalControl: "యాంత్రిక / భౌతిక నివారణ",
    biologicalControl: "జీవ నియంత్రణ (బయోకంట్రోల్)",
    chemicalControl: "పరిమిత రసాయన పిచికారీ (సలహా మాత్రమే)",
    safetyPrecautions: "రక్షణ చర్యలు & జాగ్రత్తలు",
    disclaimer: "భద్రతా సూచన: రసాయన సిఫార్సులు CIB&RC మార్గదర్శకాలకు లోబడి ఉంటాయి. నిపుణుల ధృవీకరణ లేకుండా రసాయనాలు వాడవద్దు.",

    // Weather
    temp: "ఉష్ణోగ్రత",
    humidity: "గాలిలో తేమ",
    rainfall: "వర్షపాతం (24 గం)",
    leafWetness: "ఆకుపై తడి సమయం",
    sporeRisk: "శిలీంధ్ర వ్యాప్తి ముప్పు",
    rainAlertTitle: "భారీ వర్షం హెచ్చరిక",
    rainProbability: "24 గంటల్లో వర్షం వచ్చే అవకాశం",
    rainAlertAction: "కోత చేసిన పంటను భద్రపరచండి, పిచికారీ ఆపండి, పొలంలోని నీటి పారుదలను తనిఖీ చేయండి.",
    rainAlertWindow: "అత్యవసర వాతావరణ అలారం",
    enableAlarm: "అలారం ప్రారంభించండి",
    alertsEnabled: "అలార్మ్ ప్రారంభమైంది",
    dismiss: "తీసివేయండి",

    // Pest Traps
    trapId: "ట్రాప్ కోడ్",
    targetPest: "లక్ష్య పురుగు",
    count: "పురుగుల సంఖ్య",
    trend: "ధోరణి",
    etl: "ఆర్థిక నష్ట స్థాయి (ETL)",

    // Follow-up
    followupTitle: "7-రోజుల పర్యవేక్షణ & పంట కోలుకోవడం",
    submitFollowup: "మరలా ఆకు ఫోటోను పంపండి",
    statusImproving: "పంట ఆరోగ్యం: మెరుగుపడుతోంది (-35% మచ్చలు తగ్గాయి)"
  }
};
