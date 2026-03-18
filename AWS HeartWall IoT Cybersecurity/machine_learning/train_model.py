import boto3
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import io

# 1. Connessione a LocalStack
s3 = boto3.client('s3', endpoint_url='http://localhost:14566', 
                  aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')
BUCKET_NAME = "heartwall-telemetry"

def load_data_from_s3():
    print("Scaricamento dati da LocalStack S3...")
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    all_data = []
    
    if 'Contents' not in response:
        print("Il bucket è vuoto! Fai girare l'emulatore per qualche minuto.")
        return None

    for obj in response['Contents']:
        content = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        data = json.loads(content['Body'].read().decode('utf-8'))
        all_data.append(data)
    
    return pd.DataFrame(all_data)

def train():
    df = load_data_from_s3()
    if df is None or len(df) < 20:
        print("Dati insufficienti per l'addestramento.")
        return

    # Prepariamo le feature (X) e il bersaglio (y)
    # Usiamo heart_rate e battery_level per capire se è un attacco
    X = df[['heart_rate', 'battery_level']]
    y = df['is_malicious']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Creazione del modello
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Salvataggio locale del modello "intelligente"
    joblib.dump(model, "heart_shield_model.joblib")
    print("="*50)
    print("MODELLO ADDESTRATO E SALVATO: heart_shield_model.joblib")
    print(f"Accuratezza test: {model.score(X_test, y_test) * 100:.2f}%")
    print("="*50)

if __name__ == "__main__":
    train()