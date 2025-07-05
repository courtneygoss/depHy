from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for the model and preprocessors
model = None
label_encoder = None
scaler = None

# Chemical reaction database
REACTION_DATABASE = {
    # Hydrogen reactions
    "H2 + O2": {
        "equation": "2H₂ + O₂ → 2H₂O",
        "optimal_temp": 400,
        "catalyst": "Pt or Pd",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "H2 + Cl2": {
        "equation": "H₂ + Cl₂ → 2HCl",
        "optimal_temp": 200,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    "H2 + N2": {
        "equation": "3H₂ + N₂ → 2NH₃",
        "optimal_temp": 450,
        "catalyst": "Fe (Haber process)",
        "pressure": 200,
        "success_rate": 0.85
    },
    "H2 + Br2": {
        "equation": "H₂ + Br₂ → 2HBr",
        "optimal_temp": 300,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Carbon reactions
    "C + O2": {
        "equation": "C + O₂ → CO₂",
        "optimal_temp": 800,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "C + H2": {
        "equation": "C + 2H₂ → CH₄",
        "optimal_temp": 500,
        "catalyst": "Ni",
        "pressure": 10,
        "success_rate": 0.90
    },
    "C + CO2": {
        "equation": "C + CO₂ → 2CO",
        "optimal_temp": 1000,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.85
    },
    
    # Nitrogen reactions
    "N2 + O2": {
        "equation": "N₂ + O₂ → 2NO",
        "optimal_temp": 2000,
        "catalyst": "None (high temp)",
        "pressure": 1.0,
        "success_rate": 0.70
    },
    "N2 + H2": {
        "equation": "N₂ + 3H₂ → 2NH₃",
        "optimal_temp": 450,
        "catalyst": "Fe",
        "pressure": 200,
        "success_rate": 0.85
    },
    
    # Oxygen reactions
    "O2 + C": {
        "equation": "O₂ + C → CO₂",
        "optimal_temp": 800,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "O2 + S": {
        "equation": "O₂ + S → SO₂",
        "optimal_temp": 300,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "O2 + P": {
        "equation": "O₂ + P₄ → 2P₂O₅",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    
    # Chlorine reactions
    "Cl2 + H2": {
        "equation": "Cl₂ + H₂ → 2HCl",
        "optimal_temp": 200,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    "Cl2 + Na": {
        "equation": "Cl₂ + 2Na → 2NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "Cl2 + Fe": {
        "equation": "3Cl₂ + 2Fe → 2FeCl₃",
        "optimal_temp": 200,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Sodium reactions
    "Na + Cl2": {
        "equation": "2Na + Cl₂ → 2NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "Na + H2O": {
        "equation": "2Na + 2H₂O → 2NaOH + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "Na + O2": {
        "equation": "4Na + O₂ → 2Na₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    
    # Potassium reactions
    "K + Cl2": {
        "equation": "2K + Cl₂ → 2KCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "K + H2O": {
        "equation": "2K + 2H₂O → 2KOH + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Sulfur reactions
    "S + O2": {
        "equation": "S + O₂ → SO₂",
        "optimal_temp": 300,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "S + H2": {
        "equation": "S + H₂ → H₂S",
        "optimal_temp": 400,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Iron reactions
    "Fe + O2": {
        "equation": "4Fe + 3O₂ → 2Fe₂O₃",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.85
    },
    "Fe + Cl2": {
        "equation": "2Fe + 3Cl₂ → 2FeCl₃",
        "optimal_temp": 200,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Copper reactions
    "Cu + O2": {
        "equation": "2Cu + O₂ → 2CuO",
        "optimal_temp": 400,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    "Cu + AgNO3": {
        "equation": "Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Zinc reactions
    "Zn + HCl": {
        "equation": "Zn + 2HCl → ZnCl₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    "Zn + CuSO4": {
        "equation": "Zn + CuSO₄ → ZnSO₄ + Cu",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Aluminum reactions
    "Al + O2": {
        "equation": "4Al + 3O₂ → 2Al₂O₃",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    "Al + HCl": {
        "equation": "2Al + 6HCl → 2AlCl₃ + 3H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Magnesium reactions
    "Mg + O2": {
        "equation": "2Mg + O₂ → 2MgO",
        "optimal_temp": 600,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "Mg + HCl": {
        "equation": "Mg + 2HCl → MgCl₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    
    # Calcium reactions
    "Ca + O2": {
        "equation": "2Ca + O₂ → 2CaO",
        "optimal_temp": 500,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "Ca + H2O": {
        "equation": "Ca + 2H₂O → Ca(OH)₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Phosphorus reactions
    "P + O2": {
        "equation": "P₄ + 5O₂ → 2P₂O₅",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "P + Cl2": {
        "equation": "P₄ + 6Cl₂ → 4PCl₃",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Bromine reactions
    "Br2 + H2": {
        "equation": "Br₂ + H₂ → 2HBr",
        "optimal_temp": 300,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    "Br2 + Na": {
        "equation": "Br₂ + 2Na → 2NaBr",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "Br2 + Fe": {
        "equation": "3Br₂ + 2Fe → 2FeBr₃",
        "optimal_temp": 200,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Carbon monoxide reactions
    "CO + O2": {
        "equation": "2CO + O₂ → 2CO₂",
        "optimal_temp": 400,
        "catalyst": "Pt or Pd",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "CO + H2": {
        "equation": "CO + 3H₂ → CH₄ + H₂O",
        "optimal_temp": 300,
        "catalyst": "Ni",
        "pressure": 10,
        "success_rate": 0.85
    },
    
    # Sulfur dioxide reactions
    "SO2 + O2": {
        "equation": "2SO₂ + O₂ → 2SO₃",
        "optimal_temp": 450,
        "catalyst": "V₂O₅",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    "SO2 + H2O": {
        "equation": "SO₂ + H₂O → H₂SO₃",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Nitric oxide reactions
    "NO + O2": {
        "equation": "2NO + O₂ → 2NO₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    "NO + H2": {
        "equation": "2NO + 2H₂ → N₂ + 2H₂O",
        "optimal_temp": 300,
        "catalyst": "Pt",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Ammonia reactions
    "NH3 + O2": {
        "equation": "4NH₃ + 5O₂ → 4NO + 6H₂O",
        "optimal_temp": 800,
        "catalyst": "Pt",
        "pressure": 1.0,
        "success_rate": 0.85
    },
    "NH3 + HCl": {
        "equation": "NH₃ + HCl → NH₄Cl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    
    # Hydrogen bromide reactions
    "HBr + NaOH": {
        "equation": "HBr + NaOH → NaBr + H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    "HBr + KOH": {
        "equation": "HBr + KOH → KBr + H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.98
    },
    
    # Hydrogen sulfide reactions
    "H2S + O2": {
        "equation": "2H₂S + 3O₂ → 2SO₂ + 2H₂O",
        "optimal_temp": 400,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "H2S + NaOH": {
        "equation": "H₂S + 2NaOH → Na₂S + 2H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Water reactions
    "H2O + Na": {
        "equation": "2H₂O + 2Na → 2NaOH + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "H2O + K": {
        "equation": "2H₂O + 2K → 2KOH + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "H2O + Ca": {
        "equation": "2H₂O + Ca → Ca(OH)₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Acid-base reactions
    "H2SO4 + NaOH": {
        "equation": "H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "HNO3 + NaOH": {
        "equation": "HNO₃ + NaOH → NaNO₃ + H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "CH3COOH + NaOH": {
        "equation": "CH₃COOH + NaOH → CH₃COONa + H₂O",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Salt formation reactions
    "NaCl + AgNO3": {
        "equation": "NaCl + AgNO₃ → NaNO₃ + AgCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "KCl + AgNO3": {
        "equation": "KCl + AgNO₃ → KNO₃ + AgCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "CaCl2 + Na2CO3": {
        "equation": "CaCl₂ + Na₂CO₃ → 2NaCl + CaCO₃",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Metal displacement reactions
    "FeCl3 + NaOH": {
        "equation": "FeCl₃ + 3NaOH → Fe(OH)₃ + 3NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "CuSO4 + NaOH": {
        "equation": "CuSO₄ + 2NaOH → Cu(OH)₂ + Na₂SO₄",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "ZnCl2 + NaOH": {
        "equation": "ZnCl₂ + 2NaOH → Zn(OH)₂ + 2NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "AlCl3 + NaOH": {
        "equation": "AlCl₃ + 3NaOH → Al(OH)₃ + 3NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "MgCl2 + NaOH": {
        "equation": "MgCl₂ + 2NaOH → Mg(OH)₂ + 2NaCl",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    
    # Additional metal reactions
    "Li + H2O": {
        "equation": "2Li + 2H₂O → 2LiOH + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "Ba + H2O": {
        "equation": "Ba + 2H₂O → Ba(OH)₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    "Sr + H2O": {
        "equation": "Sr + 2H₂O → Sr(OH)₂ + H₂",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    },
    
    # Non-metal reactions
    "I2 + Na": {
        "equation": "I₂ + 2Na → 2NaI",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "F2 + Na": {
        "equation": "F₂ + 2Na → 2NaF",
        "optimal_temp": 25,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.99
    },
    "Si + O2": {
        "equation": "Si + O₂ → SiO₂",
        "optimal_temp": 1000,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.95
    },
    "B + O2": {
        "equation": "4B + 3O₂ → 2B₂O₃",
        "optimal_temp": 800,
        "catalyst": "None needed",
        "pressure": 1.0,
        "success_rate": 0.90
    }
}

def find_reaction(elements):
    """Find the best matching reaction for given elements"""
    if len(elements) < 2:
        return None
    
    # Sort elements for consistent matching
    sorted_elements = sorted(elements)
    
    # Try different combinations
    for i in range(len(sorted_elements)):
        for j in range(i + 1, len(sorted_elements)):
            # Try both orders
            reaction_key1 = f"{sorted_elements[i]} + {sorted_elements[j]}"
            reaction_key2 = f"{sorted_elements[j]} + {sorted_elements[i]}"
            
            if reaction_key1 in REACTION_DATABASE:
                return reaction_key1, REACTION_DATABASE[reaction_key1]
            elif reaction_key2 in REACTION_DATABASE:
                return reaction_key2, REACTION_DATABASE[reaction_key2]
    
    return None

def calculate_optimal_conditions(reaction_data, elements):
    """Calculate optimal conditions based on reaction data"""
    base_temp = reaction_data["optimal_temp"]
    base_pressure = reaction_data["pressure"]
    
    # Adjust based on number of elements (more complex reactions need higher temps)
    temp_adjustment = len(elements) * 10
    optimal_temp = base_temp + temp_adjustment
    
    # Pressure adjustment for gas reactions
    if any(elem in ["H2", "O2", "N2", "Cl2"] for elem in elements):
        optimal_pressure = base_pressure * 1.2
    else:
        optimal_pressure = base_pressure
    
    return {
        "temperature": optimal_temp,
        "pressure": optimal_pressure,
        "catalyst": reaction_data["catalyst"],
        "success_rate": reaction_data["success_rate"]
    }

def load_and_train_model():
    """Load data, preprocess, and train the model"""
    global model, label_encoder, scaler
    
    # Check if model files exist
    if os.path.exists('model.pkl') and os.path.exists('preprocessors.pkl'):
        # Load existing model and preprocessors
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('preprocessors.pkl', 'rb') as f:
            preprocessors = pickle.load(f)
            label_encoder = preprocessors['label_encoder']
            scaler = preprocessors['scaler']
        print("Loaded existing model and preprocessors")
        return
    
    # Load the dataset
    try:
        df = pd.read_csv('reaction_data.csv')
        print(f"Loaded dataset with {len(df)} samples")
    except FileNotFoundError:
        print("reaction_data.csv not found. Creating sample data...")
        df = create_sample_data()
        df.to_csv('reaction_data.csv', index=False)
        print("Created sample reaction_data.csv")
    
    # Preprocess the data
    # Encode categorical variables
    label_encoder = LabelEncoder()
    df['catalyst_encoded'] = label_encoder.fit_transform(df['catalyst'])
    
    # Prepare features and target
    feature_columns = ['temperature', 'pressure', 'concentration_A', 'concentration_B', 'catalyst_encoded']
    X = df[feature_columns]
    y = df['reaction_outcome']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalize numeric features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    print(f"Model training completed:")
    print(f"Training accuracy: {train_score:.3f}")
    print(f"Test accuracy: {test_score:.3f}")
    
    # Save the model and preprocessors
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('preprocessors.pkl', 'wb') as f:
        pickle.dump({
            'label_encoder': label_encoder,
            'scaler': scaler
        }, f)
    print("Model and preprocessors saved")

def create_sample_data():
    """Create sample reaction data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    # Generate realistic chemical reaction data
    temperature = np.random.normal(150, 50, n_samples)  # °C
    temperature = np.clip(temperature, 25, 300)  # Reasonable range
    
    pressure = np.random.normal(1.5, 0.5, n_samples)  # atm
    pressure = np.clip(pressure, 0.5, 3.0)  # Reasonable range
    
    concentration_A = np.random.normal(0.5, 0.2, n_samples)  # mol/L
    concentration_A = np.clip(concentration_A, 0.1, 1.0)
    
    concentration_B = np.random.normal(0.5, 0.2, n_samples)  # mol/L
    concentration_B = np.clip(concentration_B, 0.1, 1.0)
    
    catalyst = np.random.choice(['yes', 'no'], n_samples, p=[0.6, 0.4])
    
    # Create reaction outcomes based on conditions
    reaction_outcome = []
    for i in range(n_samples):
        # Higher temperature and pressure favor success
        temp_factor = (temperature[i] - 25) / 275  # Normalize to 0-1
        pressure_factor = (pressure[i] - 0.5) / 2.5  # Normalize to 0-1
        conc_factor = min(concentration_A[i], concentration_B[i])  # Limiting reagent
        
        # Catalyst significantly improves success rate
        catalyst_bonus = 0.3 if catalyst[i] == 'yes' else 0
        
        # Calculate success probability
        success_prob = (temp_factor * 0.3 + pressure_factor * 0.2 + conc_factor * 0.3 + catalyst_bonus)
        success_prob = np.clip(success_prob, 0, 1)
        
        # Determine outcome
        if success_prob > 0.7:
            reaction_outcome.append('success')
        elif success_prob > 0.3:
            reaction_outcome.append('low_yield')
        else:
            reaction_outcome.append('no_reaction')
    
    return pd.DataFrame({
        'temperature': temperature,
        'pressure': pressure,
        'concentration_A': concentration_A,
        'concentration_B': concentration_B,
        'catalyst': catalyst,
        'reaction_outcome': reaction_outcome
    })

@app.route('/predict-reaction', methods=['POST'])
def predict_reaction():
    """Predict reaction outcome and provide optimal conditions"""
    try:
        # Get input data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if this is a molecule-based request
        if 'elements' in data and data['elements']:
            elements = data['elements']
            
            # Find the reaction
            reaction_result = find_reaction(elements)
            
            if reaction_result is None:
                return jsonify({
                    'error': f'No known reaction found for elements: {", ".join(elements)}. Please select different elements.',
                    'available_reactions': list(REACTION_DATABASE.keys())
                }), 400
            
            reaction_key, reaction_data = reaction_result
            
            # Calculate optimal conditions
            optimal_conditions = calculate_optimal_conditions(reaction_data, elements)
            
            # Temperature conversion functions
            def celsius_to_kelvin(celsius):
                return celsius + 273.15
            
            def kelvin_to_celsius(kelvin):
                return kelvin - 273.15
            
            temp_celsius = optimal_conditions['temperature']
            temp_kelvin = celsius_to_kelvin(temp_celsius)
            
            # Prepare response
            response = {
                'reaction_found': True,
                'reaction_key': reaction_key,
                'balanced_equation': reaction_data['equation'],
                'optimal_conditions': {
                    'temperature_celsius': temp_celsius,
                    'temperature_kelvin': round(temp_kelvin, 2),
                    'pressure': optimal_conditions['pressure'],
                    'catalyst': optimal_conditions['catalyst'],
                    'success_rate': optimal_conditions['success_rate']
                },
                'selected_elements': elements,
                'recommendations': {
                    'temperature_range_celsius': f"{temp_celsius-50} - {temp_celsius+50} °C",
                    'temperature_range_kelvin': f"{round(celsius_to_kelvin(temp_celsius-50), 2)} - {round(celsius_to_kelvin(temp_celsius+50), 2)} K",
                    'pressure_range': f"{optimal_conditions['pressure']*0.8:.1f} - {optimal_conditions['pressure']*1.2:.1f} atm",
                    'catalyst_notes': optimal_conditions['catalyst'] if optimal_conditions['catalyst'] != "None needed" else "No catalyst required"
                }
            }
            
            return jsonify(response)
        
        # Fallback to original temperature/pressure-based prediction
        # Validate required fields
        required_fields = ['temperature', 'pressure', 'concentration_A', 'concentration_B', 'catalyst']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract features
        temperature = float(data['temperature'])
        pressure = float(data['pressure'])
        concentration_A = float(data['concentration_A'])
        concentration_B = float(data['concentration_B'])
        catalyst = str(data['catalyst']).lower()
        
        # Validate input ranges
        if not (25 <= temperature <= 300):
            return jsonify({'error': 'Temperature must be between 25 and 300 °C'}), 400
        if not (0.5 <= pressure <= 3.0):
            return jsonify({'error': 'Pressure must be between 0.5 and 3.0 atm'}), 400
        if not (0.1 <= concentration_A <= 1.0):
            return jsonify({'error': 'Concentration A must be between 0.1 and 1.0 mol/L'}), 400
        if not (0.1 <= concentration_B <= 1.0):
            return jsonify({'error': 'Concentration B must be between 0.1 and 1.0 mol/L'}), 400
        if catalyst not in ['yes', 'no']:
            return jsonify({'error': 'Catalyst must be "yes" or "no"'}), 400
        
        # Encode catalyst
        catalyst_encoded = label_encoder.transform([catalyst])[0]
        
        # Prepare features
        features = np.array([[temperature, pressure, concentration_A, concentration_B, catalyst_encoded]])
        
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
        
        # Prepare response
        response = {
            'predicted_outcome': prediction,
            'confidence': float(predicted_prob),
            'probabilities': {
                'success': float(probabilities[list(model.classes_).index('success')]),
                'low_yield': float(probabilities[list(model.classes_).index('low_yield')]),
                'no_reaction': float(probabilities[list(model.classes_).index('no_reaction')])
            },
            'input_conditions': {
                'temperature': temperature,
                'pressure': pressure,
                'concentration_A': concentration_A,
                'concentration_B': concentration_B,
                'catalyst': catalyst
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/available-reactions', methods=['GET'])
def get_available_reactions():
    """Get list of available reactions"""
    return jsonify({
        'reactions': list(REACTION_DATABASE.keys()),
        'total_reactions': len(REACTION_DATABASE)
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'message': 'depHy Reaction Prediction API is running'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        'name': 'depHy Reaction Prediction API',
        'version': '2.0.0',
        'endpoints': {
            'POST /predict-reaction': 'Predict reaction outcome and optimal conditions',
            'GET /available-reactions': 'Get list of available reactions',
            'GET /health': 'Health check',
            'GET /': 'API information'
        },
        'example_request': {
            'elements': ['H2', 'O2']
        }
    })

if __name__ == '__main__':
    # Load and train the model on startup
    print("Initializing depHy Reaction Prediction API...")
    load_and_train_model()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001) 