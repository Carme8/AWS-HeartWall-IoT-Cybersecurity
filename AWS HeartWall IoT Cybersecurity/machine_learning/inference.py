import joblib
import os
import json

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def predict_fn(input_data, model):
    # Analisi dei dati biometrici
    # Se il pattern non corrisponde alla firma del battito normale -> Anomalia
    prediction = model.predict_proba(input_data)
    return {"anomaly_score": prediction[0][1]}