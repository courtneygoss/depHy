from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Chemistry reaction database (example, expand as needed)
REACTION_DATABASE = {
    # Synthesis
    ('H2', 'O2'): {
        'equation': '2H₂ + O₂ → 2H₂O',
        'temperature': 500,  # 500°C (industrial, water synthesis)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 0.5, 'catalyst': 'Pt or Pd',
        'success_rate': 0.98, 'notes': 'Water synthesis, exothermic. Industrial: 500°C, Pt/Pd catalyst.'
    },
    ('N2', 'H2'): {
        'equation': 'N₂ + 3H₂ → 2NH₃',
        'temperature': 450,  # 450°C (Haber process)
        'pressure': 200,     # 200 atm
        'concentration_A': 1.0, 'concentration_B': 3.0, 'catalyst': 'Fe (Haber process)',
        'success_rate': 0.85, 'notes': 'Haber process. Industrial: 450°C, 200 atm, Fe catalyst.'
    },
    ('C', 'O2'): {
        'equation': 'C + O₂ → CO₂',
        'temperature': 700,  # 700°C (combustion)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Combustion of carbon. Standard: 700°C.'
    },
    ('S', 'O2'): {
        'equation': 'S + O₂ → SO₂',
        'temperature': 250,  # 250°C (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Sulfur dioxide formation. Standard: 250°C.'
    },
    ('Na', 'Cl2'): {
        'equation': '2Na + Cl₂ → 2NaCl',
        'temperature': 25,   # Room temp (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Salt synthesis. Room temp.'
    },
    ('K', 'Cl2'): {
        'equation': '2K + Cl₂ → 2KCl',
        'temperature': 25,   # Room temp (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Potassium chloride synthesis. Room temp.'
    },
    ('Ca', 'O2'): {
        'equation': '2Ca + O₂ → 2CaO',
        'temperature': 600,  # 600°C (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Calcium oxide formation. Standard: 600°C.'
    },
    ('Mg', 'O2'): {
        'equation': '2Mg + O₂ → 2MgO',
        'temperature': 650,  # 650°C (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Magnesium oxide formation. Standard: 650°C.'
    },
    ('Fe', 'O2'): {
        'equation': '4Fe + 3O₂ → 2Fe₂O₃',
        'temperature': 25,   # Room temp (rusting)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'Water (moisture)',
        'success_rate': 0.85, 'notes': 'Rust formation. Room temp, needs moisture.'
    },
    ('H2', 'Cl2'): {
        'equation': 'H₂ + Cl₂ → 2HCl',
        'temperature': 25,   # Room temp, light required
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'Light (UV)',
        'success_rate': 0.98, 'notes': 'Hydrogen chloride synthesis. Room temp, UV light.'
    },
    ('H2', 'Br2'): {
        'equation': 'H₂ + Br₂ → 2HBr',
        'temperature': 150,  # 150°C (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'Pt',
        'success_rate': 0.90, 'notes': 'Hydrogen bromide synthesis. 150°C, Pt catalyst.'
    },
    ('H2', 'S'): {
        'equation': 'H₂ + S → H₂S',
        'temperature': 200,  # 200°C (lab)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.90, 'notes': 'Hydrogen sulfide synthesis. 200°C.'
    },
    # Acid-base
    ('HCl', 'NaOH'): {
        'equation': 'HCl + NaOH → NaCl + H₂O',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Neutralization. Room temp.'
    },
    ('HNO3', 'KOH'): {
        'equation': 'HNO₃ + KOH → KNO₃ + H₂O',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Neutralization. Room temp.'
    },
    ('H2SO4', 'Ca(OH)2'): {
        'equation': 'H₂SO₄ + Ca(OH)₂ → CaSO₄ + 2H₂O',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.99, 'notes': 'Neutralization. Room temp.'
    },
    # Combustion
    ('CH4', 'O2'): {
        'equation': 'CH₄ + 2O₂ → CO₂ + 2H₂O',
        'temperature': 650,  # 650°C (methane combustion)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 2.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Methane combustion. 650°C.'
    },
    ('C2H6', 'O2'): {
        'equation': '2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O',
        'temperature': 700,  # 700°C (ethane combustion)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 3.5, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Ethane combustion. 700°C.'
    },
    # Single replacement
    ('Zn', 'HCl'): {
        'equation': 'Zn + 2HCl → ZnCl₂ + H₂',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 2.0, 'catalyst': 'None',
        'success_rate': 0.95, 'notes': 'Hydrogen gas evolution. Room temp.'
    },
    ('Fe', 'CuSO4'): {
        'equation': 'Fe + CuSO₄ → FeSO₄ + Cu',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.95, 'notes': 'Copper displacement. Room temp.'
    },
    # Double replacement
    ('AgNO3', 'NaCl'): {
        'equation': 'AgNO₃ + NaCl → AgCl↓ + NaNO₃',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Precipitation of AgCl. Room temp.'
    },
    ('BaCl2', 'Na2SO4'): {
        'equation': 'BaCl₂ + Na₂SO₄ → BaSO₄↓ + 2NaCl',
        'temperature': 25,   # Room temp
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 1.0, 'catalyst': 'None',
        'success_rate': 0.98, 'notes': 'Precipitation of BaSO₄. Room temp.'
    },
    # Decomposition
    ('H2O2',): {
        'equation': '2H₂O₂ → 2H₂O + O₂',
        'temperature': 50,   # 50°C (lab, with catalyst)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 0.0, 'catalyst': 'MnO₂',
        'success_rate': 0.90, 'notes': 'Hydrogen peroxide decomposition. 50°C, MnO₂ catalyst.'
    },
    ('CaCO3',): {
        'equation': 'CaCO₃ → CaO + CO₂',
        'temperature': 825,  # 825°C (thermal decomposition)
        'pressure': 1.0,     # 1 atm
        'concentration_A': 1.0, 'concentration_B': 0.0, 'catalyst': 'None',
        'success_rate': 0.90, 'notes': 'Thermal decomposition. 825°C.'
    },
    # Add more as needed for all displayed options
}

def find_reaction(elements):
    """
    Find a reaction in the database that matches the given elements.
    Tries all orderings of the input elements.
    Returns the reaction dict if found, else None.
    """
    for key in REACTION_DATABASE:
        if set(key) == set(elements):
            return REACTION_DATABASE[key]
    return None

# Load ML model and preprocessors
MODEL_PATH = 'model.pkl'
PREPROCESSORS_PATH = 'preprocessors.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(PREPROCESSORS_PATH, 'rb') as f:
        preprocessors = pickle.load(f)
    scaler = preprocessors['scaler']
    encoder = preprocessors['label_encoder']
    print('[depHy] ML model and preprocessors loaded successfully.')
except Exception as e:
    print(f'[depHy] Warning: Could not load ML model or preprocessors: {e}')
    model = None
    scaler = None
    encoder = None

@app.route('/predict-reaction', methods=['POST'])
def predict_reaction():
    """
    API endpoint to predict reaction conditions based on selected elements.
    Expects JSON: {"elements": ["H2", "O2"]}
    Returns: JSON with balanced equation, optimal conditions, and notes.
    """
    data = request.get_json()
    # Validate input
    if not data or 'elements' not in data or len(data['elements']) < 2:
        return jsonify({'error': 'Please provide at least two elements.'}), 400
    elements = data['elements']
    reaction = find_reaction(elements)
    if not reaction:
        return jsonify({'error': f'No known reaction for: {elements}'}), 404
    # Return the reaction details
    return jsonify({
        'balanced_equation': reaction['equation'],
        'optimal_conditions': {
            'temperature': reaction['temperature'],
            'pressure': reaction['pressure'],
            'concentration_A': reaction['concentration_A'],
            'concentration_B': reaction['concentration_B'],
            'catalyst': reaction['catalyst'],
            'success_rate': reaction['success_rate']
        },
        'notes': reaction.get('notes', ''),
        'selected_elements': elements
    })

@app.route('/ping')
def ping():
    """
    Simple health check endpoint.
    Returns 'pong' if the server is running.
    """
    return 'pong', 200

if __name__ == '__main__':
    print("[depHy] API starting on http://127.0.0.1:5001")
    # Run the Flask app in debug mode for easier troubleshooting
    app.run(debug=True, host='127.0.0.1', port=5001) 