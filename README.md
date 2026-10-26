# Crop Recommendation System

A Flask app for crop recommendations from soil and climate readings, with fertilizer advice, weather information, batch CSV predictions, crop reference data, and agronomy document Q&A.

## Features

- Recommends crops from nitrogen, phosphorus, potassium, temperature, humidity, soil pH, and rainfall inputs.
- Offers fertilizer guidance, crop details, analytics, and regional weather presets.
- Accepts CSV files for batch predictions.
- Includes a compact JSON random forest for hosting without the full scikit-learn runtime.
- Provides optional document-assisted agronomy Q&A when provider keys are configured.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python app.py
```

Open `http://127.0.0.1:5000`.

`requirements.txt` contains the light runtime dependencies. `requirements-dev.txt` adds the packages used to retrain the model.

## Crop prediction API

Send a JSON request to `POST /api/predict`:

```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.9,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 202.9
}
```

Other useful routes include `GET /api/crops`, `GET /api/analytics`, and `POST /api/batch-predict`.

## Deployment

The app is configured for Vercel. Deploy with `vercel --prod` from the project root.

Live app: https://crop-recommendation-roan.vercel.app
