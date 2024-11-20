import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def load_data(file_path):
    # Define the column names as expected from the dataset (e.g., KDD Cup 1999)
    column_names = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
        'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
        'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
        'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label'
    ]
    
    # Load the data into a DataFrame
    df = pd.read_csv('Train.txt', names=column_names, index_col=False,header=None)
    print(df)
    return df

def preprocess_data(df):
    # Initialize the label encoder
    le = LabelEncoder()
    
    # Apply label encoding only to the categorical columns (protocol_type, service, flag, label)
    categorical_columns = ['protocol_type', 'service', 'flag', 'label']
    
    for column in categorical_columns:
        df[column] = le.fit_transform(df[column])
    
    # Features (X) are all columns except 'label', and 'label' is the target (y)
    X = df.drop('label', axis=1)
    y = df['label']
    return X, y

def train_model(X, y):
    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the Random Forest Classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model
    rf_classifier.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = rf_classifier.predict(X_test)
    
    # Print the classification report
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    return rf_classifier

def main():
    # Load the training and testing data
    train_data = load_data('Train.txt')
    test_data = load_data('Test.txt')
    
    # Preprocess the data
    X_train, y_train = preprocess_data(train_data)
    X_test, y_test = preprocess_data(test_data)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Save the trained model to a file
    joblib.dump(model, 'traffic_model.pkl')
    print("Model saved as traffic_model.pkl")

if __name__ == "__main__":
    main()
