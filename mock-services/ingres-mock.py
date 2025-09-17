#!/usr/bin/env python3
"""
Mock INGRES API Server for jalBuddy Development
Simulates real INGRES groundwater data API responses
"""

from flask import Flask, jsonify, request
import json
import random
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Sample district data
DISTRICTS_DATA = {
    "nalanda": {
        "state": "Bihar",
        "blocks": ["Hilsa", "Nalanda", "Asthawan", "Biharsharif", "Rajgir"],
        "geology": "Alluvial",
        "rainfall_avg": 1050
    },
    "jalgaon": {
        "state": "Maharashtra", 
        "blocks": ["Jalgaon", "Bhusawal", "Chopda", "Pachora", "Muktainagar"],
        "geology": "Deccan Trap",
        "rainfall_avg": 750
    },
    "anantapur": {
        "state": "Andhra Pradesh",
        "blocks": ["Anantapur", "Kalyanadurg", "Hindupur", "Penukonda", "Tadipatri"],
        "geology": "Hard Rock",
        "rainfall_avg": 580
    }
}

def generate_realistic_water_level(district, season="post_monsoon"):
    """Generate realistic groundwater levels based on district geology"""
    base_levels = {
        "nalanda": {"pre": 8.5, "post": 6.2, "trend": "declining"},
        "jalgaon": {"pre": 12.3, "post": 8.7, "trend": "stable"}, 
        "anantapur": {"pre": 25.8, "post": 22.1, "trend": "declining"}
    }
    
    if district.lower() in base_levels:
        level = base_levels[district.lower()][season[:4]]
        variation = random.uniform(-1.5, 1.5)
        return round(level + variation, 2)
    return round(random.uniform(8.0, 25.0), 2)

def generate_water_quality_data(district):
    """Generate realistic water quality parameters"""
    quality_ranges = {
        "nalanda": {"tds": (450, 750), "fluoride": (0.3, 0.8), "nitrate": (10, 35)},
        "jalgaon": {"tds": (650, 950), "fluoride": (0.5, 1.2), "nitrate": (20, 45)},
        "anantapur": {"tds": (800, 1400), "fluoride": (0.8, 2.1), "nitrate": (35, 80)}
    }
    
    ranges = quality_ranges.get(district.lower(), {"tds": (400, 1000), "fluoride": (0.5, 1.5), "nitrate": (20, 50)})
    
    return {
        "tds": round(random.uniform(*ranges["tds"]), 1),
        "fluoride": round(random.uniform(*ranges["fluoride"]), 2),
        "nitrate": round(random.uniform(*ranges["nitrate"]), 1),
        "chloride": round(random.uniform(50, 250), 1),
        "ph": round(random.uniform(6.5, 8.5), 1),
        "hardness": round(random.uniform(150, 450), 1)
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "INGRES Mock API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/districts', methods=['GET'])
def get_districts():
    """List all available districts"""
    districts = []
    for name, data in DISTRICTS_DATA.items():
        districts.append({
            "district": name.title(),
            "state": data["state"],
            "blocks_count": len(data["blocks"]),
            "geology": data["geology"]
        })
    
    return jsonify({
        "status": "success",
        "data": districts,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/groundwater/level', methods=['GET'])
def get_groundwater_level():
    """Get groundwater level data"""
    district = request.args.get('district', 'nalanda').lower()
    block = request.args.get('block')
    season = request.args.get('season', 'post_monsoon')
    
    # Simulate processing delay
    time.sleep(random.uniform(0.2, 0.8))
    
    if district not in DISTRICTS_DATA:
        return jsonify({"error": "District not found"}), 404
    
    level = generate_realistic_water_level(district, season)
    district_data = DISTRICTS_DATA[district]
    
    # Determine status based on level
    if level < 10:
        status = "Good"
        category = "Safe"
    elif level < 20:
        status = "Moderate" 
        category = "Semi-Critical"
    else:
        status = "Poor"
        category = "Critical"
    
    response_data = {
        "district": district.title(),
        "state": district_data["state"],
        "block": block or random.choice(district_data["blocks"]),
        "water_level_mbgl": level,
        "season": season,
        "status": status,
        "gec_category": category,
        "trend": district_data.get("trend", "stable"),
        "measurement_date": (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
        "source": "CGWB-INGRES",
        "coordinates": {
            "latitude": round(random.uniform(12.0, 28.0), 4),
            "longitude": round(random.uniform(74.0, 88.0), 4)
        }
    }
    
    return jsonify({
        "status": "success",
        "data": response_data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/groundwater/quality', methods=['GET'])
def get_water_quality():
    """Get water quality data"""
    district = request.args.get('district', 'nalanda').lower()
    
    time.sleep(random.uniform(0.3, 0.7))
    
    if district not in DISTRICTS_DATA:
        return jsonify({"error": "District not found"}), 404
    
    quality_data = generate_water_quality_data(district)
    district_data = DISTRICTS_DATA[district]
    
    # Determine potability
    potable = True
    issues = []
    
    if quality_data["fluoride"] > 1.5:
        potable = False
        issues.append("High fluoride")
    if quality_data["nitrate"] > 45:
        potable = False  
        issues.append("High nitrate")
    if quality_data["tds"] > 1000:
        issues.append("High TDS")
    
    response_data = {
        "district": district.title(),
        "state": district_data["state"],
        "parameters": quality_data,
        "potable": potable,
        "issues": issues,
        "recommendation": "Suitable for irrigation" if not potable else "Safe for drinking",
        "sampling_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
        "lab": "CGWB Regional Lab",
        "source": "CGWB-INGRES"
    }
    
    return jsonify({
        "status": "success", 
        "data": response_data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/rainfall', methods=['GET'])
def get_rainfall_data():
    """Get rainfall and recharge data"""
    district = request.args.get('district', 'nalanda').lower()
    year = request.args.get('year', datetime.now().year)
    
    time.sleep(random.uniform(0.2, 0.6))
    
    if district not in DISTRICTS_DATA:
        return jsonify({"error": "District not found"}), 404
    
    district_data = DISTRICTS_DATA[district]
    avg_rainfall = district_data["rainfall_avg"]
    
    # Generate seasonal data
    current_rainfall = round(avg_rainfall * random.uniform(0.7, 1.3), 1)
    deviation = round(((current_rainfall - avg_rainfall) / avg_rainfall) * 100, 1)
    
    response_data = {
        "district": district.title(),
        "state": district_data["state"],
        "year": int(year),
        "total_rainfall_mm": current_rainfall,
        "normal_rainfall_mm": avg_rainfall,
        "deviation_percent": deviation,
        "status": "Normal" if abs(deviation) < 20 else ("Excess" if deviation > 0 else "Deficient"),
        "recharge_estimate": {
            "potential_mm": round(current_rainfall * 0.15, 1),
            "percentage_of_rainfall": 15
        },
        "monsoon_performance": {
            "sw_monsoon": round(current_rainfall * 0.85, 1),
            "ne_monsoon": round(current_rainfall * 0.15, 1)
        },
        "source": "IMD-INGRES"
    }
    
    return jsonify({
        "status": "success",
        "data": response_data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/drilling/recommendation', methods=['GET'])
def get_drilling_recommendation():
    """Get borewell drilling recommendations"""
    district = request.args.get('district', 'nalanda').lower()
    
    time.sleep(random.uniform(0.4, 0.9))
    
    if district not in DISTRICTS_DATA:
        return jsonify({"error": "District not found"}), 404
    
    district_data = DISTRICTS_DATA[district]
    geology = district_data["geology"]
    
    # Success probability based on geology
    success_rates = {
        "Alluvial": random.randint(70, 85),
        "Deccan Trap": random.randint(60, 75),
        "Hard Rock": random.randint(45, 65)
    }
    
    success_rate = success_rates.get(geology, 60)
    
    # Depth recommendations based on geology
    depth_ranges = {
        "Alluvial": (80, 150),
        "Deccan Trap": (120, 200),
        "Hard Rock": (150, 250)
    }
    
    min_depth, max_depth = depth_ranges.get(geology, (100, 200))
    
    response_data = {
        "district": district.title(),
        "state": district_data["state"],
        "geology": geology,
        "success_probability_percent": success_rate,
        "recommended_depth_range": {
            "minimum_m": min_depth,
            "maximum_m": max_depth,
            "optimal_m": random.randint(min_depth + 20, max_depth - 20)
        },
        "drilling_season": "Post-monsoon (October-December)",
        "precautions": [
            "Ensure NOC from local groundwater authority",
            "Maintain minimum 100m distance from existing borewells",
            "Install proper casing to prevent contamination"
        ],
        "expected_yield": {
            "minimum_lpm": random.randint(500, 1000),
            "maximum_lpm": random.randint(1500, 3000)
        },
        "source": "CGWB-INGRES"
    }
    
    return jsonify({
        "status": "success",
        "data": response_data,
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🌊 Starting INGRES Mock API Server...")
    print("Available endpoints:")
    print("  GET /api/health - Health check")
    print("  GET /api/districts - List districts")
    print("  GET /api/groundwater/level?district=<name> - Water levels")
    print("  GET /api/groundwater/quality?district=<name> - Water quality")
    print("  GET /api/rainfall?district=<name> - Rainfall data")
    print("  GET /api/drilling/recommendation?district=<name> - Drilling advice")
    
    app.run(host='0.0.0.0', port=8081, debug=True)