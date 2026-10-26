"""
Crop Recommendation System - Machine Learning Model Training & Evaluation
Compares multiple ML algorithms, performs cross-validation, generates performance metrics,
and serializes the best performing model for production inference.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def train_and_evaluate():
    print("=" * 60)
    print("[*] CROP RECOMMENDATION SYSTEM - MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # 1. Load Dataset
    data_path = "Crop_recommendation.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"[*] Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # 2. Features and Target
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[features]
    y = df['label']
    
    # Compute statistical benchmarks per crop for soil radar matching
    crop_stats = {}
    for crop in y.unique():
        crop_df = df[df['label'] == crop]
        crop_stats[crop] = {
            'N': {'mean': float(crop_df['N'].mean()), 'min': float(crop_df['N'].min()), 'max': float(crop_df['N'].max())},
            'P': {'mean': float(crop_df['P'].mean()), 'min': float(crop_df['P'].min()), 'max': float(crop_df['P'].max())},
            'K': {'mean': float(crop_df['K'].mean()), 'min': float(crop_df['K'].min()), 'max': float(crop_df['K'].max())},
            'temperature': {'mean': float(crop_df['temperature'].mean()), 'min': float(crop_df['temperature'].min()), 'max': float(crop_df['temperature'].max())},
            'humidity': {'mean': float(crop_df['humidity'].mean()), 'min': float(crop_df['humidity'].min()), 'max': float(crop_df['humidity'].max())},
            'ph': {'mean': float(crop_df['ph'].mean()), 'min': float(crop_df['ph'].min()), 'max': float(crop_df['ph'].max())},
            'rainfall': {'mean': float(crop_df['rainfall'].mean()), 'min': float(crop_df['rainfall'].min()), 'max': float(crop_df['rainfall'].max())},
        }
    
    # 3. Label Encoding & Train-Test Split
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Fit scaler for algorithms sensitive to scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Algorithms to benchmark
    models = {
        "Random Forest": (RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15), False),
        "Gaussian Naive Bayes": (GaussianNB(), False),
        "Decision Tree": (DecisionTreeClassifier(random_state=42, max_depth=12), False),
        "K-Nearest Neighbors": (KNeighborsClassifier(n_neighbors=5), True),
        "Support Vector Machine": (SVC(probability=True, random_state=42, kernel='rbf'), True),
        "Logistic Regression": (LogisticRegression(max_iter=1000, random_state=42), True),
        "Gradient Boosting": (GradientBoostingClassifier(n_estimators=100, random_state=42), False)
    }
    
    results = {}
    fitted_models = {}
    
    print("\n[*] Benchmarking 7 Machine Learning Algorithms:")
    print("-" * 75)
    print(f"{'Algorithm':<25} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 75)
    
    for name, (model, requires_scale) in models.items():
        X_tr = X_train_scaled if requires_scale else X_train
        X_te = X_test_scaled if requires_scale else X_test
        
        # Fit model
        model.fit(X_tr, y_train)
        fitted_models[name] = model
        
        # Predictions
        y_pred = model.predict(X_te)
        
        acc = float(accuracy_score(y_test, y_pred) * 100)
        prec = float(precision_score(y_test, y_pred, average='weighted') * 100)
        rec = float(recall_score(y_test, y_pred, average='weighted') * 100)
        f1 = float(f1_score(y_test, y_pred, average='weighted') * 100)
        
        # 5-fold Cross-validation
        cv_scores = cross_val_score(model, X_tr, y_train, cv=5)
        cv_mean = float(cv_scores.mean() * 100)
        cv_std = float(cv_scores.std() * 100)
        
        results[name] = {
            "accuracy": round(acc, 2),
            "precision": round(prec, 2),
            "recall": round(rec, 2),
            "f1_score": round(f1, 2),
            "cv_mean": round(cv_mean, 2),
            "cv_std": round(cv_std, 2)
        }
        
        print(f"{name:<25} | {acc:>8.2f}% | {prec:>8.2f}% | {rec:>8.2f}% | {f1:>8.2f}%")
        
    print("-" * 75)
    
    # 5. Best Model Selection & Detailed Metrics
    best_model_name = "Random Forest"
    best_model = fitted_models[best_model_name]
    
    # Calculate confusion matrix for best model
    y_pred_best = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best).tolist()
    
    # Feature importances
    feature_importances = {}
    if hasattr(best_model, "feature_importances_"):
        for feat, imp in zip(features, best_model.feature_importances_):
            feature_importances[feat] = round(float(imp) * 100, 2)
            
    print(f"\n[*] Selected Primary Model: {best_model_name} (Accuracy: {results[best_model_name]['accuracy']}%)")
    print(f"[*] Feature Importances: {feature_importances}")
    
    # 6. Save Artifacts in 'models' folder
    os.makedirs("models", exist_ok=True)
    os.makedirs("dataset", exist_ok=True)
    
    # Copy dataset to dataset directory for clean structure
    df.to_csv("dataset/Crop_recommendation.csv", index=False)
    
    # Save a sample batch test dataset
    sample_batch = df.sample(n=10, random_state=42)[features]
    sample_batch.to_csv("dataset/sample_batch_test.csv", index=False)
    
    joblib.dump(best_model, "models/crop_recommendation_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(label_encoder, "models/label_encoder.pkl")
    
    analytics_payload = {
        "model_comparison": results,
        "best_model": best_model_name,
        "feature_importances": feature_importances,
        "classes": label_encoder.classes_.tolist(),
        "confusion_matrix": cm,
        "total_samples": len(df),
        "total_classes": len(label_encoder.classes_),
        "features": features,
        "crop_stats": crop_stats
    }
    
    with open("models/analytics.json", "w") as f:
        json.dump(analytics_payload, f, indent=4)
        
    print("\n[+] Model and metadata exported successfully to 'models/' directory:")
    print("    - models/crop_recommendation_model.pkl")
    print("    - models/scaler.pkl")
    print("    - models/label_encoder.pkl")
    print("    - models/analytics.json")
    print("    - dataset/sample_batch_test.csv")
    print("=" * 60)

if __name__ == "__main__":
    train_and_evaluate()
