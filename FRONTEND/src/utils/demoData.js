export const demoIntents = {
  groundwater: {
    key: 'groundwater',
    en: {
      title: 'Groundwater Level',
      userQuery: 'Show groundwater level for Nalanda, Bihar',
      summary: 'Latest groundwater depth from surface: 12.4 m (Safe Zone)',
      details: [
        { label: 'District', value: 'Nalanda' },
        { label: 'State', value: 'Bihar' },
        { label: 'Last updated', value: '2 hours ago' },
        { label: 'Trend', value: 'Stable ↔' },
      ],
      suggestion: 'Would you like weekly alerts for this location?'
    },
    hi: {
      title: 'भूजल स्तर',
      userQuery: 'नालंदा, बिहार के लिए भूजल स्तर दिखाएं',
      summary: 'नवीनतम भूजल गहराई: सतह से 12.4 मीटर (सुरक्षित क्षेत्र)',
      details: [
        { label: 'जिला', value: 'नालंदा' },
        { label: 'राज्य', value: 'बिहार' },
        { label: 'अंतिम अपडेट', value: '2 घंटे पहले' },
        { label: 'रुझान', value: 'स्थिर ↔' },
      ],
      suggestion: 'क्या आप इस स्थान के लिए साप्ताहिक अलर्ट चाहते हैं?'
    }
  },
  rainfall: {
    key: 'rainfall',
    en: {
      title: 'Rainfall Impact',
      userQuery: 'How will monsoon affect groundwater in Jalgaon?',
      summary: 'Projected recharge: +8% this season (Normal Monsoon)',
      details: [
        { label: 'Region', value: 'Jalgaon, MH' },
        { label: 'Season', value: 'SW Monsoon' },
        { label: 'Forecast', value: 'Normal (+3%)' },
        { label: 'Recharge', value: '+8% expected' },
      ],
      suggestion: 'See advisories for water harvesting structures.'
    },
    hi: {
      title: 'वर्षा प्रभाव',
      userQuery: 'जलगांव में मानसून का भूजल पर क्या प्रभाव होगा?',
      summary: 'अनुमानित रिचार्ज: इस सीजन +8% (सामान्य मानसून)',
      details: [
        { label: 'क्षेत्र', value: 'जलगांव, महाराष्ट्र' },
        { label: 'सीजन', value: 'दक्षिण पश्चिम मानसून' },
        { label: 'पूर्वानुमान', value: 'सामान्य (+3%)' },
        { label: 'रिचार्ज', value: '+8% अपेक्षित' },
      ],
      suggestion: 'वाटर हार्वेस्टिंग संरचनाओं के लिए सलाह देखें।'
    }
  },
  boring: {
    key: 'boring',
    en: {
      title: 'Boring Success Probability',
      userQuery: 'Where should I drill a borewell in Anantapur?',
      summary: 'Recommended zone: 2 km NE (Success probability: 72%)',
      details: [
        { label: 'Optimal depth', value: '180–220 m' },
        { label: 'Lithology', value: 'Weathered hard rock' },
        { label: 'Risk level', value: 'Moderate' },
        { label: 'Advisory', value: 'Avoid over-extraction during Rabi' },
      ],
      suggestion: 'Open map with recommended drilling corridor.'
    },
    hi: {
      title: 'बोरिंग सफलता संभावना',
      userQuery: 'अनंतपुर में बोरवेल कहाँ करना चाहिए?',
      summary: 'अनुशंसित क्षेत्र: 2 किमी उत्तर-पूर्व (सफलता संभावना: 72%)',
      details: [
        { label: 'उत्तम गहराई', value: '180–220 मी.' },
        { label: 'शैल-विज्ञान', value: 'वेदरिंग हार्ड रॉक' },
        { label: 'जोखिम स्तर', value: 'मध्यम' },
        { label: 'सलाह', value: 'रबी सीजन में अति-निकासी न करें' },
      ],
      suggestion: 'सुझाए गए ड्रिलिंग कॉरिडोर के साथ मानचित्र खोलें।'
    }
  },
  quality: {
    key: 'quality',
    en: {
      title: 'Water Quality Advisory',
      userQuery: 'Is groundwater safe for drinking in Bhavnagar?',
      summary: 'TDS: 820 mg/L (Within acceptable range for irrigation)',
      details: [
        { label: 'Fluoride', value: '0.8 mg/L' },
        { label: 'Nitrate', value: '30 mg/L' },
        { label: 'Category', value: 'Safe with treatment' },
        { label: 'Recommendation', value: 'RO + remineralization for drinking' },
      ],
      suggestion: 'See CGWB quality guidelines summary.'
    },
    hi: {
      title: 'जल गुणवत्ता परामर्श',
      userQuery: 'भावनगर में पीने के लिए भूजल सुरक्षित है?',
      summary: 'TDS: 820 mg/L (सिंचाई हेतु स्वीकार्य सीमा में)',
      details: [
        { label: 'फ्लोराइड', value: '0.8 mg/L' },
        { label: 'नाइट्रेट', value: '30 mg/L' },
        { label: 'श्रेणी', value: 'उपचार के साथ सुरक्षित' },
        { label: 'सिफारिश', value: 'पीने हेतु RO + री- मिनरलाइजेशन' },
      ],
      suggestion: 'CGWB गुणवत्ता दिशानिर्देश सारांश देखें।'
    }
  },
  gec: {
    key: 'gec',
    en: {
      title: 'GEC-2015 Guidelines',
      userQuery: 'Explain GEC-2015 categories for my block',
      summary: 'Block status: Semi-Critical (Stage of development: 75%)',
      details: [
        { label: 'Extraction', value: 'High in pre-monsoon' },
        { label: 'Recharge', value: 'Below long-term avg' },
        { label: 'Action', value: 'Regulate new abstraction' },
        { label: 'Note', value: 'Promote recharge structures' },
      ],
      suggestion: 'Show category criteria and mitigation checklist.'
    },
    hi: {
      title: 'GEC-2015 दिशानिर्देश',
      userQuery: 'मेरे ब्लॉक के लिए GEC-2015 श्रेणियां समझाएँ',
      summary: 'ब्लॉक स्थिति: अर्ध-समालोचनात्मक (विकास चरण: 75%)',
      details: [
        { label: 'निकासी', value: 'प्री-मानसून में अधिक' },
        { label: 'रिचार्ज', value: 'दीर्घकालिक औसत से कम' },
        { label: 'कार्य', value: 'नई निकासी नियंत्रित करें' },
        { label: 'नोट', value: 'रिचार्ज संरचनाओं को बढ़ावा दें' },
      ],
      suggestion: 'श्रेणी मानदंड और शमन चेकलिस्ट दिखाएँ।'
    }
  },
  irrigation: {
    key: 'irrigation',
    en: {
      title: 'Irrigation Advisory',
      userQuery: 'What is the irrigation schedule for wheat in Haryana?',
      summary: 'Optimal irrigation: 4-5 times during crop cycle (Current: Pre-sowing)',
      details: [
        { label: 'Crop', value: 'Wheat (Rabi)' },
        { label: 'Growth stage', value: 'Pre-sowing preparation' },
        { label: 'Water requirement', value: '450-500 mm total' },
        { label: 'Next irrigation', value: 'Crown root stage (21 DAS)' },
      ],
      suggestion: 'Monitor soil moisture at 15cm depth for optimal timing.'
    },
    hi: {
      title: 'सिंचाई सलाह',
      userQuery: 'हरियाणा में गेहूं के लिए सिंचाई कार्यक्रम क्या है?',
      summary: 'इष्टतम सिंचाई: फसल चक्र में 4-5 बार (वर्तमान: बुआई पूर्व)',
      details: [
        { label: 'फसल', value: 'गेहूं (रबी)' },
        { label: 'वृद्धि चरण', value: 'बुआई पूर्व तैयारी' },
        { label: 'जल आवश्यकता', value: '450-500 मिमी कुल' },
        { label: 'अगली सिंचाई', value: 'क्राउन रूट स्टेज (21 DAS)' },
      ],
      suggestion: 'इष्टतम समय के लिए 15 सेमी गहराई पर मिट्टी की नमी की निगरानी करें।'
    }
  },
  dwlr: {
    key: 'dwlr',
    en: {
      title: 'DWLR Live Telemetry',
      userQuery: 'Show live DWLR readings for Station #1186',
      summary: 'Real-time WL: 11.9 m | Battery: 92% | Signal: Good',
      details: [
        { label: 'Station', value: '#1186' },
        { label: 'Sampling', value: 'Every 30 mins' },
        { label: 'Alerts', value: 'No anomalies detected' },
        { label: 'Graph', value: 'Last 24h: -0.2 m' },
      ],
      suggestion: 'Enable SMS alerts for threshold breach.'
    },
    hi: {
      title: 'DWLR लाइव टेलीमेट्री',
      userQuery: 'स्टेशन #1186 के लाइव DWLR रीडिंग दिखाएँ',
      summary: 'रीयल-टाइम जलस्तर: 11.9 मी | बैटरी: 92% | सिग्नल: अच्छा',
      details: [
        { label: 'स्टेशन', value: '#1186' },
        { label: 'सैंपलिंग', value: 'हर 30 मिनट' },
        { label: 'अलर्ट', value: 'कोई असामान्यता नहीं' },
        { label: 'ग्राफ', value: 'पिछले 24 घंटे: -0.2 मी' },
      ],
      suggestion: 'सीमा उल्लंघन पर एसएमएस अलर्ट सक्षम करें।'
    }
  }
};
