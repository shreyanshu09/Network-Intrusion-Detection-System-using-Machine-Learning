import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

def load_model(model_path):
    return joblib.load(model_path)

def preprocess_data(df):
    le = LabelEncoder()
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = le.fit_transform(df[column])
    return df

def classify_traffic(model, data_path):
    df = pd.read_csv(data_path)
    df = preprocess_data(df)
    
    predictions = model.predict(df)
    df['prediction'] = predictions
    
    # Map numeric predictions back to string labels
    label_map = {0: 'Normal', 1: 'DoS', 2: 'Probe', 3: 'R2L', 4: 'U2R'}
    df['prediction'] = df['prediction'].map(label_map)
    
    # Convert results to a format that can be JSON serialized
    results = df['prediction'].value_counts().to_dict()
    results = {k: int(v) for k, v in results.items()}  # Ensure all values are integers
    
    # Get the last non-null prediction
    last_prediction = df['prediction'].dropna().iloc[-1] if not df['prediction'].isna().all() else 'Normal'
    
    return results, last_prediction