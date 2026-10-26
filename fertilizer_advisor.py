"""
Fertilizer & Soil Doctor Recommendation Engine
Calculates nutrient deficits against target crop benchmarks and prescribes
exact fertilizer dosages (Urea, DAP, MOP, SSP) and soil amendments (Lime, Gypsum).
"""

# Benchmark standard requirement per crop (N, P, K in kg/ha, ideal pH)
CROP_NUTRIENT_BENCHMARKS = {
    "rice": {"N": 80, "P": 45, "K": 40, "ph": 6.5, "name": "Rice"},
    "maize": {"N": 80, "P": 45, "K": 20, "ph": 6.5, "name": "Maize"},
    "chickpea": {"N": 40, "P": 65, "K": 80, "ph": 7.0, "name": "Chickpea"},
    "kidneybeans": {"N": 25, "P": 65, "K": 20, "ph": 6.0, "name": "Kidney Beans"},
    "pigeonpeas": {"N": 25, "P": 65, "K": 20, "ph": 6.2, "name": "Pigeon Peas"},
    "mothbeans": {"N": 20, "P": 45, "K": 20, "ph": 6.5, "name": "Moth Beans"},
    "mungbean": {"N": 20, "P": 45, "K": 20, "ph": 6.7, "name": "Mung Bean"},
    "blackgram": {"N": 40, "P": 65, "K": 20, "ph": 7.0, "name": "Black Gram"},
    "lentil": {"N": 25, "P": 65, "K": 20, "ph": 6.8, "name": "Lentil"},
    "pomegranate": {"N": 25, "P": 20, "K": 40, "ph": 6.5, "name": "Pomegranate"},
    "banana": {"N": 100, "P": 80, "K": 50, "ph": 6.5, "name": "Banana"},
    "mango": {"N": 25, "P": 25, "K": 30, "ph": 6.5, "name": "Mango"},
    "grapes": {"N": 25, "P": 130, "K": 200, "ph": 6.0, "name": "Grapes"},
    "watermelon": {"N": 100, "P": 20, "K": 50, "ph": 6.5, "name": "Watermelon"},
    "muskmelon": {"N": 100, "P": 20, "K": 50, "ph": 6.5, "name": "Muskmelon"},
    "apple": {"N": 25, "P": 130, "K": 200, "ph": 6.0, "name": "Apple"},
    "orange": {"N": 25, "P": 20, "K": 10, "ph": 6.8, "name": "Orange"},
    "papaya": {"N": 55, "P": 60, "K": 50, "ph": 6.5, "name": "Papaya"},
    "coconut": {"N": 25, "P": 20, "K": 30, "ph": 6.5, "name": "Coconut"},
    "cotton": {"N": 120, "P": 45, "K": 20, "ph": 7.0, "name": "Cotton"},
    "jute": {"N": 80, "P": 45, "K": 40, "ph": 6.8, "name": "Jute"},
    "coffee": {"N": 100, "P": 25, "K": 30, "ph": 6.5, "name": "Coffee"},
}

def analyze_soil_and_fertilizer(n_val, p_val, k_val, ph_val, target_crop):
    """
    Computes nutrient health, deficits, and calculates standard fertilizer prescription.
    """
    target_crop = target_crop.lower().strip()
    benchmark = CROP_NUTRIENT_BENCHMARKS.get(target_crop, {"N": 60, "P": 40, "K": 40, "ph": 6.5, "name": target_crop.title()})
    
    n_diff = benchmark["N"] - n_val
    p_diff = benchmark["P"] - p_val
    k_diff = benchmark["K"] - k_val
    ph_diff = ph_val - benchmark["ph"]
    
    # Nutrient Status Categorization
    def get_status(diff, tolerance=15):
        if diff > tolerance:
            return {"status": "Deficient", "level": "Low", "color": "danger", "badge": "⚠️ Deficient"}
        elif diff < -tolerance:
            return {"status": "Excessive", "level": "High", "color": "warning", "badge": "⚡ High"}
        else:
            return {"status": "Optimal", "level": "Good", "color": "success", "badge": "✅ Optimal"}

    n_status = get_status(n_diff, 15)
    p_status = get_status(p_diff, 15)
    k_status = get_status(k_diff, 15)
    
    # pH Diagnosis
    if ph_val < 5.8:
        ph_status = {"status": "Acidic", "level": "Low pH", "color": "danger", "badge": "🧪 Highly Acidic"}
        ph_remedy = "Apply Agricultural Lime (Calcium Carbonate / Dolomite) at 200-300 kg/acre to neutralize soil acidity."
    elif ph_val > 7.8:
        ph_status = {"status": "Alkaline", "level": "High pH", "color": "warning", "badge": "🧂 Alkaline / Saline"}
        ph_remedy = "Apply Gypsum (Calcium Sulfate) at 150-250 kg/acre and incorporate organic compost or green manure to lower soil alkalinity."
    else:
        ph_status = {"status": "Ideal", "level": "Optimal pH", "color": "success", "badge": "🌿 Optimal pH"}
        ph_remedy = "Soil pH is in the optimal range for maximum nutrient bioavailability."
        
    # Fertilizer Dosage Calculation (Per Acre estimation: 1 Hectare = 2.47 Acres)
    # Urea provides 46% N
    # DAP provides 18% N and 46% P2O5
    # MOP (Potash) provides 60% K2O
    
    prescriptions = []
    
    # 1. Phosphorus & Nitrogen using DAP
    dap_kg_acre = 0
    urea_kg_acre = 0
    mop_kg_acre = 0
    
    if p_diff > 0:
        # P deficit per acre
        p_def_acre = (p_diff / 2.47)
        dap_kg_acre = round((p_def_acre / 0.46), 1)
        # DAP also delivers 18% N
        n_delivered_by_dap = dap_kg_acre * 0.18
        prescriptions.append({
            "fertilizer": "DAP (Diammonium Phosphate 18-46-0)",
            "dosage": f"{dap_kg_acre} kg / acre",
            "purpose": f"Corrects Phosphorus deficit (+{round(p_diff, 1)} kg/ha required)",
            "timing": "Apply as basal dose during final land preparation before sowing.",
            "icon": "📦"
        })
    else:
        n_delivered_by_dap = 0
        
    # 2. Remaining Nitrogen via Urea
    n_remaining_def = n_diff - (n_delivered_by_dap * 2.47)
    if n_remaining_def > 0:
        n_def_acre = (n_remaining_def / 2.47)
        urea_kg_acre = round((n_def_acre / 0.46), 1)
        prescriptions.append({
            "fertilizer": "Urea (46% Nitrogen)",
            "dosage": f"{urea_kg_acre} kg / acre",
            "purpose": f"Corrects Nitrogen deficit (+{round(n_diff, 1)} kg/ha required)",
            "timing": "Split into 2-3 doses: 50% at vegetative stage, 50% at tillering/flowering.",
            "icon": "🌱"
        })
    elif n_diff < -20:
        prescriptions.append({
            "fertilizer": "Zero Additional Nitrogen Required",
            "dosage": "0 kg / acre",
            "purpose": "Soil already contains excess nitrogen. Avoid chemical N to prevent lodging & pest infestation.",
            "timing": "Monitor foliage color and irrigate regularly.",
            "icon": "🛡️"
        })
        
    # 3. Potassium via MOP (Muriate of Potash)
    if k_diff > 0:
        k_def_acre = (k_diff / 2.47)
        mop_kg_acre = round((k_def_acre / 0.60), 1)
        prescriptions.append({
            "fertilizer": "MOP (Muriate of Potash 0-0-60)",
            "dosage": f"{mop_kg_acre} kg / acre",
            "purpose": f"Corrects Potassium deficit (+{round(k_diff, 1)} kg/ha required)",
            "timing": "Apply 50% basal and 50% before panicle initiation / fruit swelling.",
            "icon": "⚡"
        })
        
    # 4. Organic & Micronutrient Booster
    prescriptions.append({
        "fertilizer": "Well-Decomposed Farmyard Manure (FYM) / Vermicompost",
        "dosage": "2 - 3 tonnes / acre",
        "purpose": "Enhances soil microbial activity, moisture retention, and cation exchange capacity.",
        "timing": "Incorporate into soil 15-20 days prior to sowing.",
        "icon": "🪱"
    })
    
    # Soil Health Index (0 - 100%)
    n_score = max(0, 100 - abs(n_diff) * 1.2)
    p_score = max(0, 100 - abs(p_diff) * 1.2)
    k_score = max(0, 100 - abs(k_diff) * 1.2)
    ph_score = max(0, 100 - abs(ph_diff) * 35)
    overall_health = round((n_score * 0.3 + p_score * 0.25 + k_score * 0.25 + ph_score * 0.2), 1)
    
    return {
        "target_crop": benchmark["name"],
        "overall_health_score": min(100.0, max(10.0, overall_health)),
        "nutrients": {
            "nitrogen": {"value": n_val, "ideal": benchmark["N"], "diff": round(n_diff, 1), "status": n_status},
            "phosphorus": {"value": p_val, "ideal": benchmark["P"], "diff": round(p_diff, 1), "status": p_status},
            "potassium": {"value": k_val, "ideal": benchmark["K"], "diff": round(k_diff, 1), "status": k_status},
            "ph": {"value": ph_val, "ideal": benchmark["ph"], "diff": round(ph_diff, 2), "status": ph_status, "remedy": ph_remedy}
        },
        "prescriptions": prescriptions
    }
