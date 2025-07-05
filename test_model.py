#!/usr/bin/env python3
"""
Test script for the depHy reaction prediction model
"""

import numpy as np
import pickle
from app import load_and_train_model

def test_model_directly():
    """Test the model directly without the API"""
    
    print("Testing depHy Reaction Prediction Model")
    print("=" * 50)
    
    # Load the model and preprocessors
    load_and_train_model()
    
    # Load the saved model and preprocessors
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('preprocessors.pkl', 'rb') as f:
        preprocessors = pickle.load(f)
        label_encoder = preprocessors['label_encoder']
        scaler = preprocessors['scaler']
    
    # Test cases
    test_cases = [
        {
            "name": "High temperature, high pressure, with catalyst",
            "temperature": 250,
            "pressure": 2.5,
            "concentration_A": 0.8,
            "concentration_B": 0.7,
            "catalyst": "yes"
        },
        {
            "name": "Low temperature, low pressure, no catalyst",
            "temperature": 50,
            "pressure": 0.8,
            "concentration_A": 0.2,
            "concentration_B": 0.3,
            "catalyst": "no"
        },
        {
            "name": "Moderate conditions with catalyst",
            "temperature": 150,
            "pressure": 1.5,
            "concentration_A": 0.5,
            "concentration_B": 0.5,
            "catalyst": "yes"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        # Prepare features
        catalyst_encoded = label_encoder.transform([test_case['catalyst']])[0]
        features = np.array([[
            test_case['temperature'],
            test_case['pressure'],
            test_case['concentration_A'],
            test_case['concentration_B'],
            catalyst_encoded
        ]])
        
        # Create DataFrame with proper column names to avoid warnings
        import pandas as pd
        features_df = pd.DataFrame(features, columns=['temperature', 'pressure', 'concentration_A', 'concentration_B', 'catalyst_encoded'])
        
        # Scale features
        features_scaled = scaler.transform(features_df)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Get probability for predicted class
        predicted_prob = probabilities[list(model.classes_).index(prediction)]
        
        # Display results
        print(f"Input conditions:")
        print(f"  Temperature: {test_case['temperature']} °C")
        print(f"  Pressure: {test_case['pressure']} atm")
        print(f"  Concentration A: {test_case['concentration_A']} mol/L")
        print(f"  Concentration B: {test_case['concentration_B']} mol/L")
        print(f"  Catalyst: {test_case['catalyst']}")
        
        print(f"\nPrediction: {prediction}")
        print(f"Confidence: {predicted_prob:.3f}")
        
        print(f"\nProbabilities:")
        for outcome, prob in zip(model.classes_, probabilities):
            print(f"  {outcome}: {prob:.3f}")
    
    print(f"\n" + "=" * 50)
    print("Model testing completed successfully!")
    print("The API is ready to use.")

if __name__ == "__main__":
    test_model_directly() 