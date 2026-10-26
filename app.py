"""
Crop Recommendation System - Production Flask Application
Integrates Machine Learning inference, agronomy intelligence, fertilizer advisory,
real-time weather synchronization, multi-model benchmark analytics, and
RAG Document Intelligence Agent.
"""

import os
import io
import json
import csv
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from crop_database import CROPS_DATA
from fertilizer_advisor import analyze_soil_and_fertilizer
from weather_service import fetch_live_weather, REGIONAL_PRESETS
from rag_service import rag_agent_manager, DOCS_DIR

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB max upload

# Base Paths & Artifacts Loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODELS_DIR, "crop_recommendation_forest.json")
ANALYTICS_PATH = os.path.join(MODELS_DIR, "analytics.json")

# Load the compact random forest representation and analytics metadata.
try:
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)
    with open(ANALYTICS_PATH, "r") as f:
        analytics_data = json.load(f)
    print("[*] Successfully loaded crop model and analytics metadata.")
except Exception as e:
    print(f"[!] Crop model not loaded ({e}).")
    model, analytics_data = None, {}

FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']


def predict_probabilities(features):
    """Return RandomForestClassifier probabilities using the exported tree data."""
    class_count = len(model["classes"])
    totals = [0.0] * class_count

    for tree in model["trees"]:
        node = 0
        while tree["left"][node] != -1:
            feature_index = tree["feature"][node]
            if features[feature_index] <= tree["threshold"][node]:
                node = tree["left"][node]
            else:
                node = tree["right"][node]

        values = tree["leaf_values"][node]
        total = sum(values)
        if total:
            for class_index, value in enumerate(values):
                totals[class_index] += value / total

    tree_count = len(model["trees"])
    return [value / tree_count for value in totals]

@app.route("/")
def index():
    """Renders the primary single-page application dashboard."""
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predicts optimal crop and alternative candidates given soil and environmental parameters.
    """
    if model is None:
        return jsonify({"success": False, "error": "Model not initialized. Run train_model.py first."}), 500
        
    try:
        data = request.get_json(force=True)
        
        # Extract and validate inputs
        n = float(data.get("N", 0))
        p = float(data.get("P", 0))
        k = float(data.get("K", 0))
        temp = float(data.get("temperature", 25.0))
        humidity = float(data.get("humidity", 70.0))
        ph = float(data.get("ph", 6.5))
        rainfall = float(data.get("rainfall", 100.0))
        
        probabilities = predict_probabilities([n, p, k, temp, humidity, ph, rainfall])
        top_indices = sorted(range(len(probabilities)), key=lambda idx: probabilities[idx], reverse=True)[:3]
        
        recommendations = []
        for idx in top_indices:
            crop_label = model["classes"][idx]
            prob = probabilities[idx] * 100
            crop_info = CROPS_DATA.get(crop_label, {
                "name": crop_label.title(),
                "scientific_name": "Agro species",
                "category": "Agricultural Crop",
                "icon": "🌱",
                "season": "Seasonal",
                "duration": "90-120 days",
                "soil_type": "Loam / Alluvial",
                "water_requirement": "Moderate",
                "economic_value": "Standard market demand.",
                "best_practices": ["Follow standard cultivation practices."],
                "fertilizer_guide": "Apply balanced NPK as recommended."
            })
            
            recommendations.append({
                "crop": crop_label,
                "confidence": round(prob, 2),
                "info": crop_info
            })
            
        primary = recommendations[0]
        alternatives = recommendations[1:]
        
        # Radar Chart Data: Compare input parameters with statistical ideal benchmark for top crop
        crop_stats = analytics_data.get("crop_stats", {}).get(primary["crop"], {})
        
        radar_metrics = {
            "labels": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Temperature (°C)", "Humidity (%)", "pH Scale (x10)", "Rainfall (mm/2)"],
            "user_values": [
                round(n, 1),
                round(p, 1),
                round(k, 1),
                round(temp, 1),
                round(humidity, 1),
                round(ph * 10, 1),
                round(rainfall / 2, 1)
            ],
            "crop_ideals": [
                round(crop_stats.get("N", {}).get("mean", n), 1),
                round(crop_stats.get("P", {}).get("mean", p), 1),
                round(crop_stats.get("K", {}).get("mean", k), 1),
                round(crop_stats.get("temperature", {}).get("mean", temp), 1),
                round(crop_stats.get("humidity", {}).get("mean", humidity), 1),
                round(crop_stats.get("ph", {}).get("mean", ph) * 10, 1),
                round(crop_stats.get("rainfall", {}).get("mean", rainfall) / 2, 1)
            ]
        }
        
        # Soil health quick check
        fertilizer_quick = analyze_soil_and_fertilizer(n, p, k, ph, primary["crop"])
        
        return jsonify({
            "success": True,
            "primary_recommendation": primary,
            "alternatives": alternatives,
            "radar_data": radar_metrics,
            "fertilizer_overview": fertilizer_quick,
            "inputs": {
                "N": n, "P": p, "K": k, "temperature": temp,
                "humidity": humidity, "ph": ph, "rainfall": rainfall
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/fertilizer-recommend", methods=["POST"])
def fertilizer_recommend():
    """Calculates soil nutrient deficits and precise fertilizer prescriptions."""
    try:
        data = request.get_json(force=True)
        n = float(data.get("N", 50))
        p = float(data.get("P", 50))
        k = float(data.get("K", 50))
        ph = float(data.get("ph", 6.5))
        crop = str(data.get("target_crop", "rice"))
        
        result = analyze_soil_and_fertilizer(n, p, k, ph, crop)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/weather", methods=["GET"])
def get_weather():
    """Fetches live weather or preset agro-climatic data for a city."""
    city = request.args.get("city", "New Delhi")
    weather_info = fetch_live_weather(city)
    return jsonify(weather_info)

@app.route("/api/presets", methods=["GET"])
def get_presets():
    """Returns regional agricultural presets."""
    return jsonify({"success": True, "presets": REGIONAL_PRESETS})

@app.route("/api/crops", methods=["GET"])
def get_crops():
    """Returns catalog of all 22 supported crops with full agronomic details."""
    return jsonify({"success": True, "crops": CROPS_DATA})

@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    """Returns model benchmark performance, confusion matrix, and feature importances."""
    return jsonify({"success": True, "analytics": analytics_data})

@app.route("/api/batch-predict", methods=["POST"])
def batch_predict():
    """Processes bulk CSV soil tests and returns recommendations."""
    if model is None:
        return jsonify({"success": False, "error": "Model not ready"}), 500
        
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
        
    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"success": False, "error": "Please upload a valid .csv file"}), 400
        
    try:
        reader = csv.DictReader(io.StringIO(file.read().decode("utf-8-sig")))
        columns = reader.fieldnames or []
        for col in FEATURES:
            if col not in columns:
                return jsonify({"success": False, "error": f"Missing required column: {col}"}), 400

        results = []
        for i, row in enumerate(reader):
            features = [float(row[col]) for col in FEATURES]
            probabilities = predict_probabilities(features)
            pred_idx = max(range(len(probabilities)), key=lambda idx: probabilities[idx])
            crop_name = model["classes"][pred_idx]
            confidence = max(probabilities) * 100
            
            results.append({
                "sample_id": int(i + 1),
                "N": features[0],
                "P": features[1],
                "K": features[2],
                "temperature": features[3],
                "humidity": features[4],
                "ph": features[5],
                "rainfall": features[6],
                "recommended_crop": crop_name.title(),
                "confidence": round(confidence, 2)
            })
            
        return jsonify({"success": True, "total_samples": len(results), "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to parse CSV: {str(e)}"}), 400

@app.route("/api/download-sample-csv", methods=["GET"])
def download_sample_csv():
    """Provides a sample CSV template for testing batch prediction."""
    csv_path = os.path.join(BASE_DIR, "dataset", "sample_batch_test.csv")
    if os.path.exists(csv_path):
        return send_file(csv_path, mimetype="text/csv", as_attachment=True, download_name="sample_soil_tests.csv")
    return jsonify({"error": "Sample file not found"}), 404

# =========================================================================
# RAG DOCUMENT INTELLIGENCE & AGENT API ENDPOINTS
# =========================================================================

@app.route("/api/rag/status", methods=["GET"])
def rag_status():
    """Returns current RAG agent status, indexed files, and chunk counts."""
    openai_k, groq_k = rag_agent_manager.get_api_keys()
    return jsonify({
        "success": True,
        "files": rag_agent_manager.indexed_files,
        "chunks": rag_agent_manager.total_chunks,
        "status": rag_agent_manager.status,
        "has_openai_key": bool(openai_k),
        "has_groq_key": bool(groq_k)
    })

@app.route("/api/rag/upload", methods=["POST"])
def rag_upload():
    """Uploads one or more PDF files and rebuilds the vector knowledge base."""
    if "files" not in request.files and "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    uploaded_files = request.files.getlist("files") or [request.files["file"]]
    saved_count = 0
    for f in uploaded_files:
        if f and f.filename and f.filename.lower().endswith(".pdf"):
            filename = secure_filename(f.filename)
            save_path = os.path.join(DOCS_DIR, filename)
            f.save(save_path)
            saved_count += 1

    if saved_count == 0:
        return jsonify({"success": False, "error": "No valid PDF documents were found in upload"}), 400

    # Re-index
    indexing_result = rag_agent_manager.reload_documents()
    return jsonify({
        "success": True,
        "message": f"Successfully uploaded and indexed {saved_count} PDF document(s).",
        "details": indexing_result
    })

@app.route("/api/rag/query", methods=["POST"])
def rag_query():
    """Executes conversational Q&A over the indexed agricultural documents."""
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        history = data.get("history", [])

        if not query:
            return jsonify({"success": False, "error": "Query cannot be empty"}), 400

        result = rag_agent_manager.answer_query(query, chat_history=history)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/rag/delete", methods=["POST"])
def rag_delete():
    """Deletes a specific PDF document and re-indexes remaining."""
    try:
        data = request.get_json(force=True)
        filename = secure_filename(data.get("filename", ""))
        if not filename:
            return jsonify({"success": False, "error": "Filename required"}), 400

        target = os.path.join(DOCS_DIR, filename)
        if os.path.exists(target):
            os.remove(target)
            indexing_result = rag_agent_manager.reload_documents()
            return jsonify({"success": True, "message": f"Deleted {filename}", "details": indexing_result})
        return jsonify({"success": False, "error": "File not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/rag/load-sample", methods=["POST"])
def rag_load_sample():
    """Ensures standard Agronomy Handbook is present in doc_files and re-indexes."""
    pdf_path = os.path.join(DOCS_DIR, "Sustainable_Farming_and_Agronomy_Handbook.pdf")
    if not os.path.exists(pdf_path):
        import subprocess
        subprocess.run(["python", "generate_handbook.py"], cwd=BASE_DIR)
    
    indexing_result = rag_agent_manager.reload_documents()
    return jsonify({
        "success": True,
        "message": "Loaded preloaded Agronomy Handbook successfully!",
        "details": indexing_result
    })

@app.route("/api/rag/config-keys", methods=["POST"])
def rag_config_keys():
    """Allows setting GROQ_API_KEY and OPENAI_API_KEY into .env directly from the UI."""
    try:
        data = request.get_json(force=True)
        groq_key = data.get("groq_api_key", "").strip()
        openai_key = data.get("openai_api_key", "").strip()

        env_path = os.path.join(BASE_DIR, ".env")
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                lines = f.readlines()

        env_dict = {}
        for l in lines:
            if "=" in l and not l.strip().startswith("#"):
                k, v = l.strip().split("=", 1)
                env_dict[k.strip()] = v.strip()

        if groq_key:
            env_dict["GROQ_API_KEY"] = groq_key
            os.environ["GROQ_API_KEY"] = groq_key
        if openai_key:
            env_dict["OPENAI_API_KEY"] = openai_key
            os.environ["OPENAI_API_KEY"] = openai_key

        with open(env_path, "w") as f:
            for k, v in env_dict.items():
                f.write(f"{k}={v}\n")

        # Reload RAG documents with new embeddings / LLM
        rag_agent_manager.reload_documents()

        return jsonify({
            "success": True,
            "message": "API keys updated successfully!",
            "status": rag_agent_manager.status
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Exportable Flask app for Vercel serverless function.
if __name__ == "__main__":
    # When run locally, start the development server.
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting Crop Recommendation System Server at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
