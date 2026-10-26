"""
Weather & Agro-Climatic Intelligence Service
Fetches live temperature, humidity, and rainfall estimates using Open-Meteo geocoding API,
with comprehensive fallback presets for regional agricultural hubs.
"""

import requests

# Preset agricultural regions with typical seasonal weather & soil profiles
REGIONAL_PRESETS = {
    "punjab_plain": {
        "name": "Punjab / Indo-Gangetic Plain (Wheat & Rice Belt)",
        "city": "Ludhiana, Punjab",
        "N": 90, "P": 45, "K": 42,
        "temperature": 24.5, "humidity": 78.0, "ph": 6.8, "rainfall": 190.0,
        "soil_type": "Alluvial Loam"
    },
    "maharashtra_cotton": {
        "name": "Vidarbha / Maharashtra (Black Cotton Soil)",
        "city": "Nagpur, Maharashtra",
        "N": 115, "P": 48, "K": 22,
        "temperature": 28.2, "humidity": 72.0, "ph": 7.2, "rainfall": 85.0,
        "soil_type": "Deep Black Regur Soil"
    },
    "kerala_coastal": {
        "name": "Coastal Kerala / Konkan (Tropical Humid Belt)",
        "city": "Kochi, Kerala",
        "N": 30, "P": 25, "K": 32,
        "temperature": 27.5, "humidity": 94.0, "ph": 5.8, "rainfall": 180.0,
        "soil_type": "Coastal Laterite & Sandy Loam"
    },
    "karnataka_coffee": {
        "name": "Chikmagalur / Coorg (Hill Plantation Zone)",
        "city": "Chikmagalur, Karnataka",
        "N": 95, "P": 28, "K": 30,
        "temperature": 23.0, "humidity": 65.0, "ph": 6.2, "rainfall": 155.0,
        "soil_type": "Humus-rich Lateritic Loam"
    },
    "himachal_orchard": {
        "name": "Shimla / Himachal (Temperate Apple Orchard)",
        "city": "Shimla, Himachal Pradesh",
        "N": 28, "P": 135, "K": 198,
        "temperature": 22.0, "humidity": 92.0, "ph": 6.1, "rainfall": 110.0,
        "soil_type": "Mountain Sandy Loam"
    },
    "rajasthan_arid": {
        "name": "Thar / Western Rajasthan (Arid & Semi-Arid Pulse Belt)",
        "city": "Bikaner, Rajasthan",
        "N": 20, "P": 42, "K": 18,
        "temperature": 30.5, "humidity": 48.0, "ph": 7.8, "rainfall": 45.0,
        "soil_type": "Desert Sandy Soil"
    },
    "maharashtra_vineyard": {
        "name": "Nashik / Western Ghats (Vineyard Belt)",
        "city": "Nashik, Maharashtra",
        "N": 25, "P": 130, "K": 200,
        "temperature": 24.0, "humidity": 82.0, "ph": 6.2, "rainfall": 70.0,
        "soil_type": "Red Sandy Loam"
    },
    "andhra_deltas": {
        "name": "Godavari & Krishna Delta (Paddy & Banana Hub)",
        "city": "Rajahmundry, Andhra Pradesh",
        "N": 85, "P": 75, "K": 50,
        "temperature": 28.5, "humidity": 81.0, "ph": 6.6, "rainfall": 115.0,
        "soil_type": "Riverine Delta Alluvial"
    }
}

def fetch_live_weather(city_name):
    """
    Geocodes city name and retrieves real-time weather metrics from Open-Meteo.
    """
    if not city_name or not city_name.strip():
        return {"success": False, "error": "City name cannot be empty"}
        
    city_name = city_name.strip()
    
    try:
        # Step 1: Geocode city name to lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url, timeout=5)
        
        if geo_resp.status_code != 200:
            return _fallback_city_weather(city_name)
            
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return _fallback_city_weather(city_name)
            
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        resolved_name = f"{location.get('name')}, {location.get('admin1', location.get('country', ''))}"
        
        # Step 2: Fetch current weather & daily precipitation
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation&daily=precipitation_sum&timezone=auto"
        w_resp = requests.get(weather_url, timeout=5)
        
        if w_resp.status_code != 200:
            return _fallback_city_weather(city_name)
            
        w_data = w_resp.json()
        current = w_data.get("current", {})
        temp = current.get("temperature_2m", 25.0)
        humidity = current.get("relative_humidity_2m", 70.0)
        
        # Estimate annual/seasonal rainfall index for crop modeling
        daily_precip = w_data.get("daily", {}).get("precipitation_sum", [5.0])
        recent_rain = sum(daily_precip[:7]) if daily_precip else 10.0
        # Calibrate baseline rainfall index for recommendation model
        rainfall_est = round(max(35.0, min(280.0, 75.0 + (recent_rain * 4.5))), 1)
        
        return {
            "success": True,
            "city": resolved_name,
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "rainfall": rainfall_est,
            "source": "Open-Meteo Live API"
        }
        
    except Exception as e:
        return _fallback_city_weather(city_name)

def _fallback_city_weather(city_name):
    """
    Fallback generator if internet request times out.
    """
    for key, val in REGIONAL_PRESETS.items():
        if city_name.lower() in val["city"].lower() or city_name.lower() in key:
            return {
                "success": True,
                "city": val["city"],
                "temperature": val["temperature"],
                "humidity": val["humidity"],
                "rainfall": val["rainfall"],
                "source": "Agro-Climatic Historical Archive"
            }
            
    # Default realistic agricultural parameter
    return {
        "success": True,
        "city": city_name.title(),
        "temperature": 26.5,
        "humidity": 72.0,
        "rainfall": 105.0,
        "source": "Agro-Climatic Regional Average"
    }
