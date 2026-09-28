import streamlit as st
import requests
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Crop Disease Risk",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# TRANSLATIONS
# =========================================================

LANG = {

"English": {
"title":"🌱 AI-Based Crop Disease Risk & Farming Advisory System",
"subtitle":"Early warning system for crop disease risk",
"language":"Select Language",
"crop":"Select Crop",
"location":"Select Location",
"mode":"Input Mode",
"simple":"Simple Mode",
"detailed":"Detailed Mode",
"conditions":"🌾 Farm Environmental Conditions",
"temperature":"Temperature (°C)",
"humidity":"Humidity (%)",
"soil":"Soil Condition",
"soil_moisture":"Soil Moisture (%)",
"rainfall":"Rainfall",
"weather":"Weather Condition",
"dry":"Dry",
"normal":"Normal",
"wet":"Wet",
"low":"Low",
"medium":"Medium",
"high":"High",
"sunny":"Sunny",
"cloudy":"Cloudy",
"rainy":"Rainy",
"automatic_weather":"🌦️ Automatic Weather Information",
"get_weather":"🌦️ Get Automatic Weather",
"analyze":"🔍 Analyze Crop Risk",
"prediction":"🤖 AI Risk Prediction",
"risk_score":"Risk Score",
"risk_level":"Risk Level",
"low_risk":"🟢 Low Risk",
"medium_risk":"🟠 Medium Risk",
"high_risk":"🔴 High Risk",
"why":"❓ Why is the risk high?",
"no_factors":"No major risk factors detected.",
"advisory":"🌾 Farming Advisory",
"early_warning":"🚨 Early Warning",
"high_alert":"High crop disease risk detected. Preventive action is recommended.",
"medium_alert":"Environmental conditions may increase crop disease risk.",
"low_alert":"No major environmental risk detected currently.",
"farm_conditions":"📊 Current Farm Conditions",
"crop_info":"🌱 Crop Information",
"about":"About",
"risk_conditions":"Risk Conditions",
"prevention":"Prevention",
"what_if":"🔄 What-If Risk Simulator",
"calculate_whatif":"🔄 Calculate What-If Risk",
"whatif_result":"What-If Result",
"predicted_score":"Predicted Risk Score",
"farm_report":"📋 My Farm Report",
"analyze_first":"Analyze your crop first to generate your farm report.",
"download":"📥 Download Report",
"simple_info":"💡 Simple Mode uses farmer-friendly conditions. Approximate values are used internally.",
"weather_success":"✅ Automatic weather data loaded successfully!",
"weather_error":"❌ Unable to get weather data. Please try again.",
"voice":"🎤 Voice Assistance",
"listen":"🔊 Listen to Result",
"voice_text":"Risk level is",
"history":"📜 Risk History",
"clear_history":"🗑️ Clear History",
"no_history":"No risk history available yet.",
"help":"🆘 Farmer Help",
"help_title":"How can we help?",
"help_1":"Check your crop regularly for unusual changes.",
"help_2":"Avoid excessive irrigation and waterlogging.",
"help_3":"Maintain proper field drainage.",
"help_4":"Monitor temperature, humidity and rainfall conditions.",
"help_5":"Take preventive action when risk becomes high.",
"help_note":"This system provides early-warning guidance and does not replace agricultural experts.",
"date":"Date",
"risk":"Risk",
"location_name":"Location",
"footer":"🌱 AI-Based Crop Disease Risk & Farming Advisory System",
"disclaimer":"⚠️ Prototype disclaimer: This system provides environmental crop disease risk prediction and early-warning guidance. It is not a disease diagnosis system."
},

"Tamil": {
"title":"🌱 செயற்கை நுண்ணறிவு அடிப்படையிலான பயிர் நோய் அபாயம் மற்றும் விவசாய ஆலோசனை அமைப்பு",
"subtitle":"பயிர் நோய் அபாயத்திற்கான முன் எச்சரிக்கை அமைப்பு",
"language":"மொழியை தேர்வு செய்யவும்",
"crop":"பயிரை தேர்வு செய்யவும்",
"location":"இடத்தை தேர்வு செய்யவும்",
"mode":"உள்ளீட்டு முறை",
"simple":"எளிய முறை",
"detailed":"விரிவான முறை",
"conditions":"🌾 பண்ணையின் சுற்றுச்சூழல் நிலை",
"temperature":"வெப்பநிலை (°C)",
"humidity":"ஈரப்பதம் (%)",
"soil":"மண் நிலை",
"soil_moisture":"மண் ஈரப்பதம் (%)",
"rainfall":"மழைப்பொழிவு",
"weather":"வானிலை",
"dry":"உலர்",
"normal":"சாதாரணம்",
"wet":"ஈரமான",
"low":"குறைவு",
"medium":"மிதமான",
"high":"அதிகம்",
"sunny":"வெயில்",
"cloudy":"மேகமூட்டம்",
"rainy":"மழை",
"automatic_weather":"🌦️ தானியங்கி வானிலை தகவல்",
"get_weather":"🌦️ தானியங்கி வானிலையை பெறுக",
"analyze":"🔍 பயிர் அபாயத்தை பகுப்பாய்வு செய்யவும்",
"prediction":"🤖 AI அபாய கணிப்பு",
"risk_score":"அபாய மதிப்பெண்",
"risk_level":"அபாய நிலை",
"low_risk":"🟢 குறைந்த அபாயம்",
"medium_risk":"🟠 மிதமான அபாயம்",
"high_risk":"🔴 அதிக அபாயம்",
"why":"❓ அபாயம் ஏன் அதிகமாக உள்ளது?",
"no_factors":"முக்கியமான அபாய காரணிகள் எதுவும் கண்டறியப்படவில்லை.",
"advisory":"🌾 விவசாய ஆலோசனை",
"early_warning":"🚨 முன் எச்சரிக்கை",
"high_alert":"பயிருக்கு அதிக நோய் அபாயம் கண்டறியப்பட்டுள்ளது. தடுப்பு நடவடிக்கை பரிந்துரைக்கப்படுகிறது.",
"medium_alert":"சுற்றுச்சூழல் நிலைமைகள் பயிர் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"low_alert":"தற்போது பெரிய சுற்றுச்சூழல் அபாயம் கண்டறியப்படவில்லை.",
"farm_conditions":"📊 தற்போதைய பண்ணை நிலை",
"crop_info":"🌱 பயிர் தகவல்",
"about":"பற்றி",
"risk_conditions":"அபாய நிலைகள்",
"prevention":"தடுப்பு",
"what_if":"🔄 What-If அபாய சிமுலேட்டர்",
"calculate_whatif":"🔄 What-If அபாயத்தை கணக்கிடுக",
"whatif_result":"What-If முடிவு",
"predicted_score":"கணிக்கப்பட்ட அபாய மதிப்பெண்",
"farm_report":"📋 எனது பண்ணை அறிக்கை",
"analyze_first":"பண்ணை அறிக்கையை உருவாக்க முதலில் உங்கள் பயிரை பகுப்பாய்வு செய்யவும்.",
"download":"📥 அறிக்கையை பதிவிறக்கவும்",
"simple_info":"💡 எளிய முறையில் விவசாயிகளுக்கு எளிதான நிலைகள் பயன்படுத்தப்படுகின்றன. மதிப்பீட்டு எண்கள் உள்முறையாக பயன்படுத்தப்படுகின்றன.",
"weather_success":"✅ தானியங்கி வானிலை தகவல் வெற்றிகரமாக பெறப்பட்டது!",
"weather_error":"❌ வானிலை தகவலை பெற முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
"voice":"🎤 குரல் உதவி",
"listen":"🔊 முடிவை கேட்கவும்",
"voice_text":"அபாய நிலை",
"history":"📜 அபாய வரலாறு",
"clear_history":"🗑️ வரலாற்றை அழிக்கவும்",
"no_history":"இதுவரை அபாய வரலாறு இல்லை.",
"help":"🆘 விவசாயி உதவி",
"help_title":"எவ்வாறு உதவலாம்?",
"help_1":"பயிரில் ஏற்படும் அசாதாரண மாற்றங்களை தொடர்ந்து கவனிக்கவும்.",
"help_2":"அதிக நீர்ப்பாசனம் மற்றும் நீர் தேங்குவதை தவிர்க்கவும்.",
"help_3":"சரியான வயல் வடிகால் வசதியை பராமரிக்கவும்.",
"help_4":"வெப்பநிலை, ஈரப்பதம் மற்றும் மழைப்பொழிவை கண்காணிக்கவும்.",
"help_5":"அபாயம் அதிகமாகும்போது தடுப்பு நடவடிக்கை எடுக்கவும்.",
"help_note":"இந்த அமைப்பு முன் எச்சரிக்கை வழிகாட்டுதலை வழங்குகிறது. விவசாய நிபுணர்களின் ஆலோசனைக்கு இது மாற்றாகாது.",
"date":"தேதி",
"risk":"அபாயம்",
"location_name":"இடம்",
"footer":"🌱 AI அடிப்படையிலான பயிர் நோய் அபாயம் மற்றும் விவசாய ஆலோசனை அமைப்பு",
"disclaimer":"⚠️ இது ஒரு முன்மாதிரி அமைப்பு. சுற்றுச்சூழல் நிலைமைகளின் அடிப்படையில் பயிர் நோய் அபாயத்தை கணித்து முன் எச்சரிக்கை வழங்குகிறது. இது நோய் கண்டறிதல் அமைப்பு அல்ல."
},

"Hindi": {
"title":"🌱 AI आधारित फसल रोग जोखिम और कृषि सलाह प्रणाली",
"subtitle":"फसल रोग जोखिम के लिए प्रारंभिक चेतावनी प्रणाली",
"language":"भाषा चुनें",
"crop":"फसल चुनें",
"location":"स्थान चुनें",
"mode":"इनपुट मोड",
"simple":"सरल मोड",
"detailed":"विस्तृत मोड",
"conditions":"🌾 खेत की पर्यावरणीय स्थिति",
"temperature":"तापमान (°C)",
"humidity":"नमी (%)",
"soil":"मिट्टी की स्थिति",
"soil_moisture":"मिट्टी की नमी (%)",
"rainfall":"वर्षा",
"weather":"मौसम",
"dry":"सूखी",
"normal":"सामान्य",
"wet":"गीली",
"low":"कम",
"medium":"मध्यम",
"high":"अधिक",
"sunny":"धूप",
"cloudy":"बादल",
"rainy":"बारिश",
"automatic_weather":"🌦️ स्वचालित मौसम जानकारी",
"get_weather":"🌦️ स्वचालित मौसम प्राप्त करें",
"analyze":"🔍 फसल जोखिम का विश्लेषण करें",
"prediction":"🤖 AI जोखिम पूर्वानुमान",
"risk_score":"जोखिम स्कोर",
"risk_level":"जोखिम स्तर",
"low_risk":"🟢 कम जोखिम",
"medium_risk":"🟠 मध्यम जोखिम",
"high_risk":"🔴 अधिक जोखिम",
"why":"❓ जोखिम अधिक क्यों है?",
"no_factors":"कोई प्रमुख जोखिम कारक नहीं मिला।",
"advisory":"🌾 कृषि सलाह",
"early_warning":"🚨 प्रारंभिक चेतावनी",
"high_alert":"फसल में रोग का अधिक जोखिम पाया गया है। रोकथाम के उपाय करने की सलाह दी जाती है।",
"medium_alert":"पर्यावरणीय परिस्थितियां फसल रोग के जोखिम को बढ़ा सकती हैं।",
"low_alert":"वर्तमान में कोई बड़ा पर्यावरणीय जोखिम नहीं पाया गया।",
"farm_conditions":"📊 वर्तमान खेत की स्थिति",
"crop_info":"🌱 फसल जानकारी",
"about":"जानकारी",
"risk_conditions":"जोखिम की स्थितियां",
"prevention":"रोकथाम",
"what_if":"🔄 What-If जोखिम सिम्युलेटर",
"calculate_whatif":"🔄 What-If जोखिम की गणना करें",
"whatif_result":"What-If परिणाम",
"predicted_score":"अनुमानित जोखिम स्कोर",
"farm_report":"📋 मेरी खेत रिपोर्ट",
"analyze_first":"खेत की रिपोर्ट बनाने के लिए पहले अपनी फसल का विश्लेषण करें।",
"download":"📥 रिपोर्ट डाउनलोड करें",
"simple_info":"💡 सरल मोड में किसानों के लिए आसान परिस्थितियों का उपयोग किया जाता है। अनुमानित संख्यात्मक मान अंदर उपयोग किए जाते हैं।",
"weather_success":"✅ स्वचालित मौसम जानकारी सफलतापूर्वक प्राप्त हुई!",
"weather_error":"❌ मौसम की जानकारी प्राप्त नहीं हो सकी। कृपया पुनः प्रयास करें।",
"voice":"🎤 आवाज सहायता",
"listen":"🔊 परिणाम सुनें",
"voice_text":"जोखिम स्तर",
"history":"📜 जोखिम इतिहास",
"clear_history":"🗑️ इतिहास साफ करें",
"no_history":"अभी तक कोई जोखिम इतिहास उपलब्ध नहीं है।",
"help":"🆘 किसान सहायता",
"help_title":"हम कैसे मदद कर सकते हैं?",
"help_1":"फसल में होने वाले असामान्य बदलावों की नियमित जांच करें।",
"help_2":"अधिक सिंचाई और जलभराव से बचें।",
"help_3":"उचित खेत जल निकासी बनाए रखें।",
"help_4":"तापमान, नमी और वर्षा की निगरानी करें।",
"help_5":"जोखिम अधिक होने पर रोकथाम के उपाय करें।",
"help_note":"यह प्रणाली प्रारंभिक चेतावनी मार्गदर्शन देती है और कृषि विशेषज्ञों की सलाह का विकल्प नहीं है।",
"date":"तारीख",
"risk":"जोखिम",
"location_name":"स्थान",
"footer":"🌱 AI आधारित फसल रोग जोखिम और कृषि सलाह प्रणाली",
"disclaimer":"⚠️ यह एक प्रोटोटाइप प्रणाली है। यह पर्यावरणीय परिस्थितियों के आधार पर फसल रोग जोखिम का अनुमान और प्रारंभिक चेतावनी प्रदान करती है। यह रोग निदान प्रणाली नहीं है।"
},

"Telugu": {
"title":"🌱 AI ఆధారిత పంట వ్యాధి ప్రమాదం మరియు వ్యవసాయ సలహా వ్యవస్థ",
"subtitle":"పంట వ్యాధి ప్రమాదానికి ముందస్తు హెచ్చరిక వ్యవస్థ",
"language":"భాషను ఎంచుకోండి",
"crop":"పంటను ఎంచుకోండి",
"location":"ప్రాంతాన్ని ఎంచుకోండి",
"mode":"ఇన్‌పుట్ మోడ్",
"simple":"సులభమైన మోడ్",
"detailed":"వివరణాత్మక మోడ్",
"conditions":"🌾 పొలం పర్యావరణ పరిస్థితులు",
"temperature":"ఉష్ణోగ్రత (°C)",
"humidity":"తేమ (%)",
"soil":"నేల పరిస్థితి",
"soil_moisture":"నేల తేమ (%)",
"rainfall":"వర్షపాతం",
"weather":"వాతావరణం",
"dry":"పొడి",
"normal":"సాధారణం",
"wet":"తడి",
"low":"తక్కువ",
"medium":"మధ్యస్థం",
"high":"ఎక్కువ",
"sunny":"ఎండ",
"cloudy":"మేఘావృతం",
"rainy":"వర్షం",
"automatic_weather":"🌦️ ఆటోమేటిక్ వాతావరణ సమాచారం",
"get_weather":"🌦️ ఆటోమేటిక్ వాతావరణాన్ని పొందండి",
"analyze":"🔍 పంట ప్రమాదాన్ని విశ్లేషించండి",
"prediction":"🤖 AI ప్రమాద అంచనా",
"risk_score":"ప్రమాద స్కోర్",
"risk_level":"ప్రమాద స్థాయి",
"low_risk":"🟢 తక్కువ ప్రమాదం",
"medium_risk":"🟠 మధ్యస్థ ప్రమాదం",
"high_risk":"🔴 అధిక ప్రమాదం",
"why":"❓ ప్రమాదం ఎందుకు ఎక్కువగా ఉంది?",
"no_factors":"ప్రధాన ప్రమాద కారకాలు ఏవీ గుర్తించబడలేదు.",
"advisory":"🌾 వ్యవసాయ సలహా",
"early_warning":"🚨 ముందస్తు హెచ్చరిక",
"high_alert":"పంటలో అధిక వ్యాధి ప్రమాదం గుర్తించబడింది. నివారణ చర్యలు తీసుకోవాలని సూచించబడింది.",
"medium_alert":"పర్యావరణ పరిస్థితులు పంట వ్యాధి ప్రమాదాన్ని పెంచవచ్చు.",
"low_alert":"ప్రస్తుతం పెద్ద పర్యావరణ ప్రమాదం గుర్తించబడలేదు.",
"farm_conditions":"📊 ప్రస్తుత పొలం పరిస్థితులు",
"crop_info":"🌱 పంట సమాచారం",
"about":"గురించి",
"risk_conditions":"ప్రమాద పరిస్థితులు",
"prevention":"నివారణ",
"what_if":"🔄 What-If ప్రమాద సిమ్యులేటర్",
"calculate_whatif":"🔄 What-If ప్రమాదాన్ని లెక్కించండి",
"whatif_result":"What-If ఫలితం",
"predicted_score":"అంచనా ప్రమాద స్కోర్",
"farm_report":"📋 నా పొలం నివేదిక",
"analyze_first":"పొలం నివేదికను రూపొందించడానికి ముందుగా మీ పంటను విశ్లేషించండి.",
"download":"📥 నివేదికను డౌన్‌లోడ్ చేయండి",
"simple_info":"💡 సులభమైన మోడ్‌లో రైతులకు సులభంగా అర్థమయ్యే పరిస్థితులను ఉపయోగిస్తాము. అంచనా సంఖ్యా విలువలు లోపల ఉపయోగించబడతాయి.",
"weather_success":"✅ ఆటోమేటిక్ వాతావరణ సమాచారం విజయవంతంగా పొందబడింది!",
"weather_error":"❌ వాతావరణ సమాచారాన్ని పొందలేకపోయాము. దయచేసి మళ్లీ ప్రయత్నించండి.",
"voice":"🎤 వాయిస్ సహాయం",
"listen":"🔊 ఫలితాన్ని వినండి",
"voice_text":"ప్రమాద స్థాయి",
"history":"📜 ప్రమాద చరిత్ర",
"clear_history":"🗑️ చరిత్రను తొలగించండి",
"no_history":"ఇప్పటివరకు ప్రమాద చరిత్ర లేదు.",
"help":"🆘 రైతు సహాయం",
"help_title":"మేము ఎలా సహాయం చేయగలం?",
"help_1":"పంటలో అసాధారణ మార్పులను క్రమం తప్పకుండా పరిశీలించండి.",
"help_2":"అధిక నీటిపారుదల మరియు నీరు నిల్వ ఉండటాన్ని నివారించండి.",
"help_3":"సరైన పొలం డ్రైనేజీని నిర్వహించండి.",
"help_4":"ఉష్ణోగ్రత, తేమ మరియు వర్షపాతాన్ని పరిశీలించండి.",
"help_5":"ప్రమాదం ఎక్కువగా ఉన్నప్పుడు నివారణ చర్యలు తీసుకోండి.",
"help_note":"ఈ వ్యవస్థ ముందస్తు హెచ్చరిక మార్గదర్శకాన్ని అందిస్తుంది. ఇది వ్యవసాయ నిపుణుల సలహాకు ప్రత్యామ్నాయం కాదు.",
"date":"తేదీ",
"risk":"ప్రమాదం",
"location_name":"ప్రాంతం",
"footer":"🌱 AI ఆధారిత పంట వ్యాధి ప్రమాదం మరియు వ్యవసాయ సలహా వ్యవస్థ",
"disclaimer":"⚠️ ఇది ఒక ప్రోటోటైప్ వ్యవస్థ. పర్యావరణ పరిస్థితుల ఆధారంగా పంట వ్యాధి ప్రమాదాన్ని అంచనా వేసి ముందస్తు హెచ్చరికను అందిస్తుంది. ఇది వ్యాధి నిర్ధారణ వ్యవస్థ కాదు."
}
}

# =========================================================
# CROP NAMES
# =========================================================

CROPS = {
"English":[
"Tomato","Rice","Groundnut","Chilli","Maize","Cotton",
"Sugarcane","Banana","Mango","Onion","Potato","Brinjal",
"Okra","Black Gram","Green Gram","Wheat"
],

"Tamil":[
"தக்காளி","நெல்","நிலக்கடலை","மிளகாய்","சோளம்","பருத்தி",
"கரும்பு","வாழை","மாம்பழம்","வெங்காயம்","உருளைக்கிழங்கு",
"கத்தரிக்காய்","வெண்டைக்காய்","உளுந்து","பச்சைப்பயறு","கோதுமை"
],

"Hindi":[
"टमाटर","चावल","मूंगफली","मिर्च","मक्का","कपास",
"गन्ना","केला","आम","प्याज","आलू","बैंगन",
"भिंडी","उड़द","मूंग","गेहूं"
],

"Telugu":[
"టమోటా","వరి","వేరుశెనగ","మిరప","మొక్కజొన్న","పత్తి",
"చెరకు","అరటి","మామిడి","ఉల్లిపాయ","బంగాళాదుంప","వంకాయ",
"బెండకాయ","మినుములు","పెసలు","గోధుమ"
]
}

# =========================================================
# CROP RULES
# =========================================================

CROP_RULES = {
"Tomato":{"temp":(25,30),"humidity":80,"soil":70},
"Rice":{"temp":(25,32),"humidity":80,"soil":75},
"Groundnut":{"temp":(25,30),"humidity":75,"soil":65},
"Chilli":{"temp":(24,30),"humidity":75,"soil":65},
"Maize":{"temp":(24,32),"humidity":75,"soil":65},
"Cotton":{"temp":(25,32),"humidity":75,"soil":65},
"Sugarcane":{"temp":(25,32),"humidity":80,"soil":75},
"Banana":{"temp":(24,32),"humidity":75,"soil":70},
"Mango":{"temp":(24,32),"humidity":75,"soil":65},
"Onion":{"temp":(20,30),"humidity":70,"soil":60},
"Potato":{"temp":(15,25),"humidity":75,"soil":65},
"Brinjal":{"temp":(24,30),"humidity":75,"soil":65},
"Okra":{"temp":(24,32),"humidity":75,"soil":65},
"Black Gram":{"temp":(25,32),"humidity":75,"soil":65},
"Green Gram":{"temp":(25,32),"humidity":75,"soil":65},
"Wheat":{"temp":(18,25),"humidity":70,"soil":60}
}

# =========================================================
# CROP INFORMATION
# =========================================================

CROP_INFO = {

"Tomato":{
"about":{
"English":"Tomato is a widely cultivated vegetable crop.",
"Tamil":"தக்காளி பரவலாக பயிரிடப்படும் காய்கறி பயிராகும்.",
"Hindi":"टमाटर एक व्यापक रूप से उगाई जाने वाली सब्जी फसल है।",
"Telugu":"టమోటా విస్తృతంగా సాగు చేయబడే కూరగాయ పంట."
},
"risk":{
"English":"High humidity, excess moisture and wet weather can increase disease risk.",
"Tamil":"அதிக ஈரப்பதம், அதிக மண் ஈரம் மற்றும் ஈரமான வானிலை நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी और गीला मौसम रोग के जोखिम को बढ़ा सकता है।",
"Telugu":"అధిక తేమ మరియు తడి వాతావరణం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid excessive irrigation and maintain good air circulation.",
"Tamil":"அதிக நீர்ப்பாசனத்தை தவிர்த்து நல்ல காற்றோட்டத்தை பராமரிக்கவும்.",
"Hindi":"अधिक सिंचाई से बचें और अच्छी हवा का संचार बनाए रखें।",
"Telugu":"అధిక నీటిపారుదలని నివారించి మంచి గాలి ప్రసరణను నిర్వహించండి."
}
},

"Rice":{
"about":{
"English":"Rice is an important cereal crop requiring adequate water.",
"Tamil":"நெல் போதுமான நீர் தேவைப்படும் முக்கிய தானியப் பயிராகும்.",
"Hindi":"चावल एक महत्वपूर्ण अनाज फसल है जिसे पर्याप्त पानी की आवश्यकता होती है।",
"Telugu":"వరి తగినంత నీరు అవసరమయ్యే ముఖ్యమైన ధాన్య పంట."
},
"risk":{
"English":"High humidity, heavy rainfall and excess soil moisture may increase disease risk.",
"Tamil":"அதிக ஈரப்பதம், கனமழை மற்றும் அதிக மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी, भारी वर्षा और अधिक मिट्टी की नमी रोग जोखिम बढ़ा सकती है।",
"Telugu":"అధిక తేమ, భారీ వర్షపాతం మరియు అధిక నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper water management and field drainage.",
"Tamil":"சரியான நீர் மேலாண்மை மற்றும் வயல் வடிகால் வசதியை பராமரிக்கவும்.",
"Hindi":"उचित जल प्रबंधन और खेत की जल निकासी बनाए रखें।",
"Telugu":"సరైన నీటి నిర్వహణ మరియు పొలం డ్రైనేజీని నిర్వహించండి."
}
},

"Groundnut":{
"about":{
"English":"Groundnut is an important oilseed crop.",
"Tamil":"நிலக்கடலை ஒரு முக்கிய எண்ணெய் விதைப் பயிராகும்.",
"Hindi":"मूंगफली एक महत्वपूर्ण तिलहन फसल है।",
"Telugu":"వేరుశెనగ ఒక ముఖ్యమైన నూనెగింజ పంట."
},
"risk":{
"English":"High humidity and excessive soil moisture may increase disease risk.",
"Tamil":"அதிக ஈரப்பதம் மற்றும் அதிக மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी और मिट्टी की अधिक नमी रोग जोखिम बढ़ा सकती है।",
"Telugu":"అధిక తేమ మరియు అధిక నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid waterlogging and monitor crop conditions regularly.",
"Tamil":"நீர் தேங்குவதை தவிர்த்து பயிர் நிலையை தொடர்ந்து கண்காணிக்கவும்.",
"Hindi":"जलभराव से बचें और फसल की स्थिति की नियमित निगरानी करें।",
"Telugu":"నీరు నిల్వ ఉండకుండా చూసి పంట పరిస్థితిని క్రమం తప్పకుండా పరిశీలించండి."
}
},

"Chilli":{
"about":{
"English":"Chilli is an important spice crop.",
"Tamil":"மிளகாய் ஒரு முக்கியமான மசாலா பயிராகும்.",
"Hindi":"मिर्च एक महत्वपूर्ण मसाला फसल है।",
"Telugu":"మిరప ఒక ముఖ్యమైన మసాలా పంట."
},
"risk":{
"English":"Warm, humid and wet conditions can increase disease risk.",
"Tamil":"சூடான, ஈரமான மற்றும் மழையான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म, नम और गीली परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"వెచ్చని, తేమ మరియు తడి పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper irrigation and monitor leaves regularly.",
"Tamil":"சரியான நீர்ப்பாசனத்தை பராமரித்து இலைகளை தொடர்ந்து கண்காணிக்கவும்.",
"Hindi":"उचित सिंचाई बनाए रखें और पत्तियों की नियमित निगरानी करें।",
"Telugu":"సరైన నీటిపారుదలని నిర్వహించి ఆకులను క్రమం తప్పకుండా పరిశీలించండి."
}
},

"Maize":{
"about":{
"English":"Maize is an important cereal crop.",
"Tamil":"சோளம் ஒரு முக்கியமான தானியப் பயிராகும்.",
"Hindi":"मक्का एक महत्वपूर्ण अनाज फसल है।",
"Telugu":"మొక్కజొన్న ఒక ముఖ్యమైన ధాన్య పంట."
},
"risk":{
"English":"Warm and humid conditions can increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain field sanitation and avoid excessive moisture.",
"Tamil":"வயல் சுகாதாரத்தை பராமரித்து அதிக ஈரப்பதத்தை தவிர்க்கவும்.",
"Hindi":"खेत की स्वच्छता बनाए रखें और अधिक नमी से बचें।",
"Telugu":"పొలం పరిశుభ్రతను నిర్వహించి అధిక తేమను నివారించండి."
}
},

"Cotton":{
"about":{
"English":"Cotton is an important fibre crop.",
"Tamil":"பருத்தி ஒரு முக்கிய நார் பயிராகும்.",
"Hindi":"कपास एक महत्वपूर्ण रेशेदार फसल है।",
"Telugu":"పత్తి ఒక ముఖ్యమైన నార పంట."
},
"risk":{
"English":"Warm and humid weather can increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான வானிலை நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम मौसम रोग जोखिम बढ़ा सकता है।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన వాతావరణం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Monitor plants regularly and avoid excess irrigation.",
"Tamil":"தாவரங்களை தொடர்ந்து கண்காணித்து அதிக நீர்ப்பாசனத்தை தவிர்க்கவும்.",
"Hindi":"पौधों की नियमित निगरानी करें और अधिक सिंचाई से बचें।",
"Telugu":"మొక్కలను క్రమం తప్పకుండా పరిశీలించి అధిక నీటిపారుదలని నివారించండి."
}
},

"Sugarcane":{
"about":{
"English":"Sugarcane is a major commercial crop.",
"Tamil":"கரும்பு ஒரு முக்கியமான வணிகப் பயிராகும்.",
"Hindi":"गन्ना एक प्रमुख व्यावसायिक फसल है।",
"Telugu":"చెరకు ఒక ముఖ్యమైన వాణిజ్య పంట."
},
"risk":{
"English":"High moisture and humidity may increase disease risk.",
"Tamil":"அதிக ஈரப்பதம் மற்றும் மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी और आर्द्रता रोग जोखिम बढ़ा सकती है।",
"Telugu":"అధిక తేమ మరియు నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper drainage and irrigation.",
"Tamil":"சரியான வடிகால் மற்றும் நீர்ப்பாசனத்தை பராமரிக்கவும்.",
"Hindi":"उचित जल निकासी और सिंचाई बनाए रखें।",
"Telugu":"సరైన డ్రైనేజీ మరియు నీటిపారుదలని నిర్వహించండి."
}
},

"Banana":{
"about":{
"English":"Banana is a tropical fruit crop.",
"Tamil":"வாழை ஒரு வெப்பமண்டல பழப் பயிராகும்.",
"Hindi":"केला एक उष्णकटिबंधीय फल फसल है।",
"Telugu":"అరటి ఒక ఉష్ణమండల పండ్ల పంట."
},
"risk":{
"English":"Warm and humid conditions can increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain good drainage and field sanitation.",
"Tamil":"நல்ல வடிகால் மற்றும் வயல் சுகாதாரத்தை பராமரிக்கவும்.",
"Hindi":"अच्छी जल निकासी और खेत की स्वच्छता बनाए रखें।",
"Telugu":"మంచి డ్రైనేజీ మరియు పొలం పరిశుభ్రతను నిర్వహించండి."
}
},

"Mango":{
"about":{
"English":"Mango is an important fruit crop.",
"Tamil":"மாம்பழம் ஒரு முக்கியமான பழப் பயிராகும்.",
"Hindi":"आम एक महत्वपूर्ण फल फसल है।",
"Telugu":"మామిడి ఒక ముఖ్యమైన పండ్ల పంట."
},
"risk":{
"English":"Warm, humid and rainy weather can increase disease risk.",
"Tamil":"சூடான, ஈரமான மற்றும் மழையான வானிலை நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म, नम और बारिश वाला मौसम रोग जोखिम बढ़ा सकता है।",
"Telugu":"వెచ్చని, తేమతో కూడిన మరియు వర్షపు వాతావరణం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain canopy airflow and monitor leaves and fruits.",
"Tamil":"நல்ல காற்றோட்டத்தை பராமரித்து இலைகள் மற்றும் பழங்களை கண்காணிக்கவும்.",
"Hindi":"पेड़ में अच्छा हवा का संचार बनाए रखें और पत्तियों व फलों की निगरानी करें।",
"Telugu":"మొక్కలో మంచి గాలి ప్రసరణను నిర్వహించి ఆకులు మరియు పండ్లను పరిశీలించండి."
}
},

"Onion":{
"about":{
"English":"Onion is an important vegetable crop.",
"Tamil":"வெங்காயம் ஒரு முக்கியமான காய்கறிப் பயிராகும்.",
"Hindi":"प्याज एक महत्वपूर्ण सब्जी फसल है।",
"Telugu":"ఉల్లిపాయ ఒక ముఖ్యమైన కూరగాయ పంట."
},
"risk":{
"English":"Excess humidity and soil moisture can increase disease risk.",
"Tamil":"அதிக ஈரப்பதம் மற்றும் மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी और मिट्टी की नमी रोग जोखिम बढ़ा सकती है।",
"Telugu":"అధిక తేమ మరియు నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid waterlogging and maintain proper irrigation.",
"Tamil":"நீர் தேங்குவதை தவிர்த்து சரியான நீர்ப்பாசனத்தை பராமரிக்கவும்.",
"Hindi":"जलभराव से बचें और उचित सिंचाई बनाए रखें।",
"Telugu":"నీరు నిల్వ ఉండకుండా చూసి సరైన నీటిపారుదలని నిర్వహించండి."
}
},

"Potato":{
"about":{
"English":"Potato is an important tuber crop.",
"Tamil":"உருளைக்கிழங்கு ஒரு முக்கியமான கிழங்கு பயிராகும்.",
"Hindi":"आलू एक महत्वपूर्ण कंद फसल है।",
"Telugu":"బంగాళాదుంప ఒక ముఖ్యమైన దుంప పంట."
},
"risk":{
"English":"Cool and humid conditions can increase disease risk.",
"Tamil":"குளிர்ச்சியான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"ठंडी और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"చల్లని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid excess moisture and monitor foliage.",
"Tamil":"அதிக ஈரப்பதத்தை தவிர்த்து இலைகளை கண்காணிக்கவும்.",
"Hindi":"अधिक नमी से बचें और पत्तियों की निगरानी करें।",
"Telugu":"అధిక తేమను నివారించి ఆకులను పరిశీలించండి."
}
},

"Brinjal":{
"about":{
"English":"Brinjal is a common vegetable crop.",
"Tamil":"கத்தரிக்காய் ஒரு பொதுவான காய்கறிப் பயிராகும்.",
"Hindi":"बैंगन एक सामान्य सब्जी फसल है।",
"Telugu":"వంకాయ ఒక సాధారణ కూరగాయ పంట."
},
"risk":{
"English":"Warm and humid conditions can increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper spacing and irrigation.",
"Tamil":"சரியான இடைவெளி மற்றும் நீர்ப்பாசனத்தை பராமரிக்கவும்.",
"Hindi":"उचित दूरी और सिंचाई बनाए रखें।",
"Telugu":"సరైన మొక్కల దూరం మరియు నీటిపారుదలని నిర్వహించండి."
}
},

"Okra":{
"about":{
"English":"Okra is a warm-season vegetable crop.",
"Tamil":"வெண்டைக்காய் ஒரு வெப்பமான பருவ காய்கறிப் பயிராகும்.",
"Hindi":"भिंडी गर्म मौसम की सब्जी फसल है।",
"Telugu":"బెండకాయ వెచ్చని కాలంలో సాగు చేసే కూరగాయ పంట."
},
"risk":{
"English":"Warm and humid weather can increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான வானிலை நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम मौसम रोग जोखिम बढ़ा सकता है।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన వాతావరణం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid excessive moisture and inspect plants regularly.",
"Tamil":"அதிக ஈரப்பதத்தை தவிர்த்து தாவரங்களை தொடர்ந்து கண்காணிக்கவும்.",
"Hindi":"अधिक नमी से बचें और पौधों की नियमित जांच करें।",
"Telugu":"అధిక తేమను నివారించి మొక్కలను క్రమం తప్పకుండా పరిశీలించండి."
}
},

"Black Gram":{
"about":{
"English":"Black gram is an important pulse crop.",
"Tamil":"உளுந்து ஒரு முக்கியமான பருப்பு வகைப் பயிராகும்.",
"Hindi":"उड़द एक महत्वपूर्ण दलहन फसल है।",
"Telugu":"మినుములు ఒక ముఖ్యమైన పప్పు పంట."
},
"risk":{
"English":"High humidity and excess moisture may increase disease risk.",
"Tamil":"அதிக ஈரப்பதம் மற்றும் அதிக மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"अधिक नमी और अतिरिक्त मिट्टी की नमी रोग जोखिम बढ़ा सकती है।",
"Telugu":"అధిక తేమ మరియు అధిక నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper drainage and avoid excess irrigation.",
"Tamil":"சரியான வடிகால் வசதியை பராமரித்து அதிக நீர்ப்பாசனத்தை தவிர்க்கவும்.",
"Hindi":"उचित जल निकासी बनाए रखें और अधिक सिंचाई से बचें।",
"Telugu":"సరైన డ్రైనేజీని నిర్వహించి అధిక నీటిపారుదలని నివారించండి."
}
},

"Green Gram":{
"about":{
"English":"Green gram is an important pulse crop.",
"Tamil":"பச்சைப்பயறு ஒரு முக்கியமான பருப்பு வகைப் பயிராகும்.",
"Hindi":"मूंग एक महत्वपूर्ण दलहन फसल है।",
"Telugu":"పెసలు ఒక ముఖ్యమైన పప్పు పంట."
},
"risk":{
"English":"Warm and humid conditions may increase disease risk.",
"Tamil":"சூடான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"गर्म और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"వెచ్చని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Maintain proper field drainage.",
"Tamil":"சரியான வயல் வடிகால் வசதியை பராமரிக்கவும்.",
"Hindi":"उचित खेत जल निकासी बनाए रखें।",
"Telugu":"సరైన పొలం డ్రైనేజీని నిర్వహించండి."
}
},

"Wheat":{
"about":{
"English":"Wheat is an important cereal crop.",
"Tamil":"கோதுமை ஒரு முக்கியமான தானியப் பயிராகும்.",
"Hindi":"गेहूं एक महत्वपूर्ण अनाज फसल है।",
"Telugu":"గోధుమ ఒక ముఖ్యమైన ధాన్య పంట."
},
"risk":{
"English":"Cool and humid conditions can increase disease risk.",
"Tamil":"குளிர்ச்சியான மற்றும் ஈரமான நிலைமைகள் நோய் அபாயத்தை அதிகரிக்கலாம்.",
"Hindi":"ठंडी और नम परिस्थितियां रोग जोखिम बढ़ा सकती हैं।",
"Telugu":"చల్లని మరియు తేమతో కూడిన పరిస్థితులు వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
},
"prevention":{
"English":"Avoid excessive irrigation and monitor crop health.",
"Tamil":"அதிக நீர்ப்பாசனத்தை தவிர்த்து பயிர் ஆரோக்கியத்தை கண்காணிக்கவும்.",
"Hindi":"अधिक सिंचाई से बचें और फसल के स्वास्थ्य की निगरानी करें।",
"Telugu":"అధిక నీటిపారుదలని నివారించి పంట ఆరోగ్యాన్ని పరిశీలించండి."
}
}
}

# =========================================================
# LOCATIONS
# =========================================================

LOCATIONS = {
"Chennai":(13.0827,80.2707),
"Coimbatore":(11.0168,76.9558),
"Madurai":(9.9252,78.1198),
"Thanjavur":(10.7870,79.1378),
"Salem":(11.6643,78.1460),
"Tiruchirappalli":(10.7905,78.7047),
"Tirunelveli":(8.7139,77.7567),
"Erode":(11.3410,77.7172),
"Dindigul":(10.3673,77.9803),
"Villupuram":(11.9401,79.4861),
"Vellore":(12.9165,79.1325),
"Thoothukudi":(8.7642,78.1348),
"Cuddalore":(11.7480,79.7714),
"Kanchipuram":(12.8342,79.7036),
"Namakkal":(11.2194,78.1677)
}

# =========================================================
# LOCATION TRANSLATIONS
# =========================================================

LOCATION_NAMES = {

"English":{
"Chennai":"Chennai","Coimbatore":"Coimbatore","Madurai":"Madurai",
"Thanjavur":"Thanjavur","Salem":"Salem",
"Tiruchirappalli":"Tiruchirappalli","Tirunelveli":"Tirunelveli",
"Erode":"Erode","Dindigul":"Dindigul","Villupuram":"Villupuram",
"Vellore":"Vellore","Thoothukudi":"Thoothukudi",
"Cuddalore":"Cuddalore","Kanchipuram":"Kanchipuram","Namakkal":"Namakkal"
},

"Tamil":{
"Chennai":"சென்னை","Coimbatore":"கோயம்புத்தூர்","Madurai":"மதுரை",
"Thanjavur":"தஞ்சாவூர்","Salem":"சேலம்",
"Tiruchirappalli":"திருச்சிராப்பள்ளி","Tirunelveli":"திருநெல்வேலி",
"Erode":"ஈரோடு","Dindigul":"திண்டுக்கல்","Villupuram":"விழுப்புரம்",
"Vellore":"வேலூர்","Thoothukudi":"தூத்துக்குடி",
"Cuddalore":"கடலூர்","Kanchipuram":"காஞ்சிபுரம்","Namakkal":"நாமக்கல்"
},

"Hindi":{
"Chennai":"चेन्नई","Coimbatore":"कोयंबटूर","Madurai":"मदुरै",
"Thanjavur":"तंजावुर","Salem":"सेलम",
"Tiruchirappalli":"तिरुचिरापल्ली","Tirunelveli":"तिरुनेलवेली",
"Erode":"इरोड","Dindigul":"डिंडीगुल","Villupuram":"विल्लुपुरम",
"Vellore":"वेल्लोर","Thoothukudi":"तूतीकोरिन",
"Cuddalore":"कुड्डालोर","Kanchipuram":"कांचीपुरम","Namakkal":"नमक्कल"
},

"Telugu":{
"Chennai":"చెన్నై","Coimbatore":"కోయంబత్తూరు","Madurai":"మదురై",
"Thanjavur":"తంజావూరు","Salem":"సేలం",
"Tiruchirappalli":"తిరుచిరాపల్లి","Tirunelveli":"తిరునెల్వేలి",
"Erode":"ఈరోడ్","Dindigul":"దిండిగల్","Villupuram":"విల్లుపురం",
"Vellore":"వెల్లూరు","Thoothukudi":"తూత్తుకుడి",
"Cuddalore":"కడలూరు","Kanchipuram":"కాంచీపురం","Namakkal":"నామక్కల్"
}
}

# =========================================================
# WEATHER FUNCTION
# =========================================================

def get_weather(location):

    lat,lon = LOCATIONS[location]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code"
    )

    try:

        response = requests.get(url,timeout=10)

        if response.status_code == 200:

            data=response.json()
            current=data["current"]

            temperature=current["temperature_2m"]
            humidity=current["relative_humidity_2m"]
            precipitation=current["precipitation"]
            code=current["weather_code"]

            if precipitation>=5:
                rainfall="High"
            elif precipitation>0:
                rainfall="Medium"
            else:
                rainfall="Low"

            if code==0:
                weather="Sunny"
            elif code in [1,2,3,45,48]:
                weather="Cloudy"
            else:
                weather="Rainy"

            return temperature,humidity,rainfall,weather

    except:
        return None

    return None

# =========================================================
# RISK CALCULATION
# =========================================================

def calculate_risk(
    crop,
    location,
    temperature,
    humidity,
    rainfall,
    soil_moisture,
    weather
):

    rule=CROP_RULES[crop]

    score=0
    factors=[]

    min_temp,max_temp=rule["temp"]

    if min_temp<=temperature<=max_temp:

        score+=20

        factors.append({
        "English":"Temperature is within the crop risk range.",
        "Tamil":"வெப்பநிலை பயிரின் அபாய வரம்பிற்குள் உள்ளது.",
        "Hindi":"तापमान फसल की जोखिम सीमा के अंदर है।",
        "Telugu":"ఉష్ణోగ్రత పంట ప్రమాద పరిధిలో ఉంది."
        })

    if humidity>=rule["humidity"]:

        score+=25

        factors.append({
        "English":"High humidity may increase disease risk.",
        "Tamil":"அதிக ஈரப்பதம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
        "Hindi":"अधिक नमी रोग जोखिम को बढ़ा सकती है।",
        "Telugu":"అధిక తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
        })

    if rainfall=="High":

        score+=20

        factors.append({
        "English":"Heavy rainfall may increase disease risk.",
        "Tamil":"அதிக மழைப்பொழிவு நோய் அபாயத்தை அதிகரிக்கலாம்.",
        "Hindi":"भारी वर्षा रोग जोखिम को बढ़ा सकती है।",
        "Telugu":"భారీ వర్షపాతం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
        })

    if soil_moisture>=rule["soil"]:

        score+=20

        factors.append({
        "English":"High soil moisture may increase disease risk.",
        "Tamil":"அதிக மண் ஈரம் நோய் அபாயத்தை அதிகரிக்கலாம்.",
        "Hindi":"अधिक मिट्टी की नमी रोग जोखिम को बढ़ा सकती है।",
        "Telugu":"అధిక నేల తేమ వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
        })

    if weather in ["Cloudy","Rainy"]:

        score+=15

        factors.append({
        "English":"Cloudy or rainy weather may increase disease risk.",
        "Tamil":"மேகமூட்டமான அல்லது மழையான வானிலை நோய் அபாயத்தை அதிகரிக்கலாம்.",
        "Hindi":"बादल या बारिश वाला मौसम रोग जोखिम बढ़ा सकता है।",
        "Telugu":"మేఘావృతమైన లేదా వర్షపు వాతావరణం వ్యాధి ప్రమాదాన్ని పెంచవచ్చు."
        })

    location_bonus={
    "Chennai":3,"Coimbatore":2,"Madurai":1,"Thanjavur":3,
    "Salem":1,"Tiruchirappalli":2,"Tirunelveli":2,
    "Erode":2,"Dindigul":1,"Villupuram":2,"Vellore":1,
    "Thoothukudi":2,"Cuddalore":3,"Kanchipuram":2,"Namakkal":1
    }

    score+=location_bonus.get(location,0)

    if score>=70:
        risk="High"
    elif score>=40:
        risk="Medium"
    else:
        risk="Low"

    return min(score,100),risk,factors

# =========================================================
# ADVISORY
# =========================================================

def advisory_text(risk,humidity,rainfall,soil,language):

    if risk=="High":

        if humidity>=80 and rainfall=="High":

            messages={
            "English":"Improve drainage and avoid excessive irrigation.",
            "Tamil":"வடிகால் வசதியை மேம்படுத்தி அதிக நீர்ப்பாசனத்தை தவிர்க்கவும்.",
            "Hindi":"जल निकासी में सुधार करें और अधिक सिंचाई से बचें।",
            "Telugu":"డ్రైనేజీని మెరుగుపరచి అధిక నీటిపారుదలని నివారించండి."
            }

        elif soil>=70:

            messages={
            "English":"Reduce excess watering and monitor crop conditions.",
            "Tamil":"அதிக நீர்ப்பாசனத்தை குறைத்து பயிர் நிலையை கண்காணிக்கவும்.",
            "Hindi":"अधिक पानी देना कम करें और फसल की स्थिति की निगरानी करें।",
            "Telugu":"అధిక నీటిపారుదలని తగ్గించి పంట పరిస్థితిని పరిశీలించండి."
            }

        else:

            messages={
            "English":"Monitor the crop closely and take preventive action.",
            "Tamil":"பயிரை கவனமாக கண்காணித்து தடுப்பு நடவடிக்கை எடுக்கவும்.",
            "Hindi":"फसल की ध्यानपूर्वक निगरानी करें और रोकथाम के उपाय करें।",
            "Telugu":"పంటను జాగ్రత్తగా పరిశీలించి నివారణ చర్యలు తీసుకోండి."
            }

    elif risk=="Medium":

        messages={
        "English":"Monitor crop conditions and maintain proper irrigation.",
        "Tamil":"பயிர் நிலையை கண்காணித்து சரியான நீர்ப்பாசனத்தை பராமரிக்கவும்.",
        "Hindi":"फसल की स्थिति की निगरानी करें और उचित सिंचाई बनाए रखें।",
        "Telugu":"పంట పరిస్థితిని పరిశీలించి సరైన నీటిపారుదలని నిర్వహించండి."
        }

    else:

        messages={
        "English":"Continue regular monitoring and maintain current conditions.",
        "Tamil":"தொடர்ந்து பயிரை கண்காணித்து தற்போதைய நிலையை பராமரிக்கவும்.",
        "Hindi":"नियमित निगरानी जारी रखें और वर्तमान परिस्थितियों को बनाए रखें।",
        "Telugu":"క్రమం తప్పకుండా పంటను పరిశీలిస్తూ ప్రస్తుత పరిస్థితులను కొనసాగించండి."
        }

    return messages[language]

# =========================================================
# LANGUAGE
# =========================================================

language=st.sidebar.selectbox(
    "🌐 Language / மொழி / भाषा / భాష",
    ["English","Tamil","Hindi","Telugu"]
)

T=LANG[language]

# =========================================================
# HEADER
# =========================================================

st.title(T["title"])
st.write(T["subtitle"])

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🌾 Farm Details")

crop_display=st.sidebar.selectbox(
    T["crop"],
    CROPS[language]
)

crop=list(CROP_RULES.keys())[
    CROPS[language].index(crop_display)
]

location_display=st.sidebar.selectbox(
    T["location"],
    list(LOCATION_NAMES[language].values())
)

location=list(LOCATION_NAMES[language].keys())[
    list(LOCATION_NAMES[language].values()).index(location_display)
]

mode=st.sidebar.radio(
    T["mode"],
    [T["simple"],T["detailed"]]
)

# =========================================================
# INPUTS
# =========================================================

st.subheader(T["conditions"])

temperature=None
humidity=None
rainfall=None
weather=None
soil_moisture=None

# =========================================================
# SIMPLE MODE
# =========================================================

if mode==T["simple"]:

    c1,c2=st.columns(2)

    with c1:

        soil_option=st.selectbox(
            T["soil"],
            [T["dry"],T["normal"],T["wet"]]
        )

        rainfall_option=st.selectbox(
            T["rainfall"],
            [T["low"],T["medium"],T["high"]]
        )

    with c2:

        weather_option=st.selectbox(
            T["weather"],
            [T["sunny"],T["cloudy"],T["rainy"]]
        )

    soil_map={
    T["dry"]:35,
    T["normal"]:55,
    T["wet"]:80
    }

    rainfall_map={
    T["low"]:"Low",
    T["medium"]:"Medium",
    T["high"]:"High"
    }

    weather_map={
    T["sunny"]:"Sunny",
    T["cloudy"]:"Cloudy",
    T["rainy"]:"Rainy"
    }

    soil_moisture=soil_map[soil_option]
    rainfall=rainfall_map[rainfall_option]
    weather=weather_map[weather_option]

    st.info(T["simple_info"])

# =========================================================
# DETAILED MODE
# =========================================================

else:

    c1,c2=st.columns(2)

    with c1:

        temperature=st.number_input(
            T["temperature"],
            0.0,50.0,28.0
        )

        humidity=st.number_input(
            T["humidity"],
            0.0,100.0,75.0
        )

        soil_moisture=st.number_input(
            T["soil_moisture"],
            0.0,100.0,60.0
        )

    with c2:

        rainfall_display=st.selectbox(
            T["rainfall"],
            [T["low"],T["medium"],T["high"]]
        )

        weather_display=st.selectbox(
            T["weather"],
            [T["sunny"],T["cloudy"],T["rainy"]]
        )

        rainfall={
        T["low"]:"Low",
        T["medium"]:"Medium",
        T["high"]:"High"
        }[rainfall_display]

        weather={
        T["sunny"]:"Sunny",
        T["cloudy"]:"Cloudy",
        T["rainy"]:"Rainy"
        }[weather_display]

# =========================================================
# AUTOMATIC WEATHER
# =========================================================

st.divider()

st.subheader(T["automatic_weather"])

if st.button(T["get_weather"]):

    result=get_weather(location)

    if result:

        temperature,humidity,rainfall,weather=result

        st.session_state["temperature"]=temperature
        st.session_state["humidity"]=humidity
        st.session_state["rainfall"]=rainfall
        st.session_state["weather"]=weather

        st.success(T["weather_success"])

    else:

        st.error(T["weather_error"])

if "temperature" in st.session_state:

    temperature=st.session_state["temperature"]
    humidity=st.session_state["humidity"]
    rainfall=st.session_state["rainfall"]
    weather=st.session_state["weather"]

    a,b,c,d=st.columns(4)

    a.metric(T["temperature"],f"{temperature} °C")
    b.metric(T["humidity"],f"{humidity} %")

    c.metric(
        T["rainfall"],
        {"Low":T["low"],"Medium":T["medium"],"High":T["high"]}[rainfall]
    )

    d.metric(
        T["weather"],
        {"Sunny":T["sunny"],"Cloudy":T["cloudy"],"Rainy":T["rainy"]}[weather]
    )

# =========================================================
# ANALYZE
# =========================================================

st.divider()

if st.button(T["analyze"],type="primary"):

    if temperature is None:

        result=get_weather(location)

        if result:
            temperature,humidity,rainfall,weather=result
        else:
            temperature=28
            humidity=75
            rainfall="Medium"
            weather="Cloudy"

    score,risk,factors=calculate_risk(
        crop,
        location,
        temperature,
        humidity,
        rainfall,
        soil_moisture,
        weather
    )

    advisory=advisory_text(
        risk,
        humidity,
        rainfall,
        soil_moisture,
        language
    )

    st.session_state["score"]=score
    st.session_state["risk"]=risk
    st.session_state["factors"]=factors
    st.session_state["advisory"]=advisory
    st.session_state["crop"]=crop
    st.session_state["location"]=location
    st.session_state["temperature"]=temperature
    st.session_state["humidity"]=humidity
    st.session_state["rainfall"]=rainfall
    st.session_state["soil"]=soil_moisture
    st.session_state["weather"]=weather

    # -----------------------------------------------------
    # RISK HISTORY
    # -----------------------------------------------------

    if "history_data" not in st.session_state:
        st.session_state["history_data"]=[]

    history_item={
        "date":datetime.now().strftime("%d-%m-%Y %H:%M"),
        "crop":crop,
        "location":location,
        "score":score,
        "risk":risk
    }

    st.session_state["history_data"].append(history_item)

# =========================================================
# RESULTS
# =========================================================

if "risk" in st.session_state:

    st.divider()

    st.subheader(T["prediction"])

    c1,c2=st.columns(2)

    with c1:

        st.metric(
            T["risk_score"],
            f"{st.session_state['score']}/100"
        )

    with c2:

        risk=st.session_state["risk"]

        if risk=="High":
            st.error(T["high_risk"])

        elif risk=="Medium":
            st.warning(T["medium_risk"])

        else:
            st.success(T["low_risk"])

    # =====================================================
    # EARLY WARNING
    # =====================================================

    st.subheader(T["early_warning"])

    if risk=="High":

        st.error("🚨 "+T["high_alert"])

    elif risk=="Medium":

        st.warning("⚠️ "+T["medium_alert"])

    else:

        st.success("✅ "+T["low_alert"])

    # =====================================================
    # WHY
    # =====================================================

    st.subheader(T["why"])

    if st.session_state["factors"]:

        for factor in st.session_state["factors"]:
            st.write("• "+factor[language])

    else:
        st.write(T["no_factors"])

    # =====================================================
    # ADVISORY
    # =====================================================

    st.subheader(T["advisory"])

    st.info(
        st.session_state["advisory"]
    )

    # =====================================================
    # VOICE ASSISTANCE
    # =====================================================

    st.subheader(T["voice"])

    voice_risk={
    "English":{
        "High":"High risk",
        "Medium":"Medium risk",
        "Low":"Low risk"
    },
    "Tamil":{
        "High":"அதிக அபாயம்",
        "Medium":"மிதமான அபாயம்",
        "Low":"குறைந்த அபாயம்"
    },
    "Hindi":{
        "High":"अधिक जोखिम",
        "Medium":"मध्यम जोखिम",
        "Low":"कम जोखिम"
    },
    "Telugu":{
        "High":"అధిక ప్రమాదం",
        "Medium":"మధ్యస్థ ప్రమాదం",
        "Low":"తక్కువ ప్రమాదం"
    }
    }

    voice_message=(
        T["voice_text"]
        +" "
        +voice_risk[language][risk]
        +". "
        +st.session_state["advisory"]
    )

    if st.button(T["listen"]):

        safe_text=voice_message.replace("`","")

        html=f"""
        <script>
        var text = {safe_text!r};
        var speech = new SpeechSynthesisUtterance(text);
        speech.lang =
        "{'en-IN' if language=='English' else 'ta-IN' if language=='Tamil' else 'hi-IN' if language=='Hindi' else 'te-IN'}";
        speech.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(speech);
        </script>
        """

        st.components.v1.html(
            html,
            height=0
        )

        st.success(
            "🔊 "+voice_message
        )

    # =====================================================
    # CURRENT FARM CONDITIONS
    # =====================================================

    st.subheader(T["farm_conditions"])

    c1,c2,c3,c4=st.columns(4)

    c1.metric(
        T["crop"],
        CROPS[language][
            list(CROP_RULES.keys()).index(
                st.session_state["crop"]
            )
        ]
    )

    c2.metric(
        T["location"],
        LOCATION_NAMES[language][
            st.session_state["location"]
        ]
    )

    c3.metric(
        T["temperature"],
        f"{st.session_state['temperature']} °C"
    )

    c4.metric(
        T["humidity"],
        f"{st.session_state['humidity']} %"
    )

    c5,c6,c7=st.columns(3)

    c5.metric(
        T["rainfall"],
        {
        "Low":T["low"],
        "Medium":T["medium"],
        "High":T["high"]
        }[st.session_state["rainfall"]]
    )

    c6.metric(
        T["soil_moisture"],
        f"{st.session_state['soil']} %"
    )

    c7.metric(
        T["weather"],
        {
        "Sunny":T["sunny"],
        "Cloudy":T["cloudy"],
        "Rainy":T["rainy"]
        }[st.session_state["weather"]]
    )

# =========================================================
# CROP INFORMATION
# =========================================================

st.divider()

st.subheader(T["crop_info"])

info=CROP_INFO[crop]

st.write("### "+T["about"])
st.write(info["about"][language])

st.write("### "+T["risk_conditions"])
st.write(info["risk"][language])

st.write("### "+T["prevention"])
st.write(info["prevention"][language])

# =========================================================
# WHAT-IF SIMULATOR
# =========================================================

st.divider()

st.subheader(T["what_if"])

c1,c2=st.columns(2)

with c1:

    what_temp=st.slider(
        T["temperature"],
        10,45,28,
        key="what_temp"
    )

    what_humidity=st.slider(
        T["humidity"],
        0,100,75,
        key="what_humidity"
    )

with c2:

    what_soil=st.slider(
        T["soil_moisture"],
        0,100,60,
        key="what_soil"
    )

    what_rain_display=st.selectbox(
        T["rainfall"],
        [T["low"],T["medium"],T["high"]],
        key="what_rain"
    )

    what_weather_display=st.selectbox(
        T["weather"],
        [T["sunny"],T["cloudy"],T["rainy"]],
        key="what_weather"
    )

what_rain={
T["low"]:"Low",
T["medium"]:"Medium",
T["high"]:"High"
}[what_rain_display]

what_weather={
T["sunny"]:"Sunny",
T["cloudy"]:"Cloudy",
T["rainy"]:"Rainy"
}[what_weather_display]

if st.button(T["calculate_whatif"]):

    ws,wr,wf=calculate_risk(
        crop,
        location,
        what_temp,
        what_humidity,
        what_rain,
        what_soil,
        what_weather
    )

    st.write("### "+T["whatif_result"])

    st.metric(
        T["predicted_score"],
        f"{ws}/100"
    )

    if wr=="High":
        st.error(T["high_risk"])

    elif wr=="Medium":
        st.warning(T["medium_risk"])

    else:
        st.success(T["low_risk"])

# =========================================================
# RISK HISTORY
# =========================================================

st.divider()

st.subheader(T["history"])

if "history_data" not in st.session_state:
    st.session_state["history_data"]=[]

if st.session_state["history_data"]:

    for item in reversed(st.session_state["history_data"]):

        crop_name=CROPS[language][
            list(CROP_RULES.keys()).index(item["crop"])
        ]

        location_name=LOCATION_NAMES[language][
            item["location"]
        ]

        risk_name={
        "Low":T["low_risk"],
        "Medium":T["medium_risk"],
        "High":T["high_risk"]
        }[item["risk"]]

        st.write(
            f"📅 **{item['date']}**  |  "
            f"🌱 {crop_name}  |  "
            f"📍 {location_name}  |  "
            f"📊 {item['score']}/100  |  "
            f"{risk_name}"
        )

    if st.button(T["clear_history"]):

        st.session_state["history_data"]=[]

        st.rerun()

else:

    st.info(T["no_history"])

# =========================================================
# FARMER HELP
# =========================================================

st.divider()

st.subheader(T["help"])

st.write("### "+T["help_title"])

st.write("🌱 "+T["help_1"])
st.write("💧 "+T["help_2"])
st.write("🚰 "+T["help_3"])
st.write("🌦️ "+T["help_4"])
st.write("🚨 "+T["help_5"])

st.info(
    "💡 "+T["help_note"]
)

# =========================================================
# FARM REPORT
# =========================================================

st.divider()

st.subheader(T["farm_report"])

if "risk" in st.session_state:

    crop_display=CROPS[language][
        list(CROP_RULES.keys()).index(
            st.session_state["crop"]
        )
    ]

    location_display=LOCATION_NAMES[language][
        st.session_state["location"]
    ]

    rainfall_display={
    "Low":T["low"],
    "Medium":T["medium"],
    "High":T["high"]
    }[st.session_state["rainfall"]]

    weather_display={
    "Sunny":T["sunny"],
    "Cloudy":T["cloudy"],
    "Rainy":T["rainy"]
    }[st.session_state["weather"]]

    risk_display={
    "Low":T["low_risk"],
    "Medium":T["medium_risk"],
    "High":T["high_risk"]
    }[st.session_state["risk"]]

    report=f"""

{T["title"]}

{T["date"]}:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

{T["crop"]}:
{crop_display}

{T["location"]}:
{location_display}

{T["temperature"]}:
{st.session_state["temperature"]} °C

{T["humidity"]}:
{st.session_state["humidity"]} %

{T["rainfall"]}:
{rainfall_display}

{T["soil_moisture"]}:
{st.session_state["soil"]} %

{T["weather"]}:
{weather_display}

{T["risk_score"]}:
{st.session_state["score"]}/100

{T["risk_level"]}:
{risk_display}

{T["advisory"]}:
{st.session_state["advisory"]}

{T["why"]}:
"""

    for factor in st.session_state["factors"]:
        report+="\n- "+factor[language]

    st.text(report)

    st.download_button(
        T["download"],
        report,
        file_name="My_Farm_Risk_Report.txt",
        mime="text/plain"
    )

else:

    st.info(T["analyze_first"])

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(T["disclaimer"])

st.caption(T["footer"])