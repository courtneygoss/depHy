from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Chemistry reaction database (example, expand as needed)
REACTION_DATABASE = {
    # Synthesis
    ('H2', 'O2'): {
        'equation': '2H₂ + O₂ → 2H₂O',
        'temperature': 400, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'Pt or Pd', 'success_rate': 0.95, 'notes': 'Water synthesis, exothermic.'
    },
    ('N2', 'H2'): {
        'equation': 'N₂ + 3H₂ → 2NH₃',
        'temperature': 450, 'pressure': 200, 'concentration_A': 0.5, 'concentration_B': 1.5, 'catalyst': 'Fe (Haber process)', 'success_rate': 0.85, 'notes': 'Haber process.'
    },
    ('C', 'O2'): {
        'equation': 'C + O₂ → CO₂',
        'temperature': 800, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Combustion of carbon.'
    },
    ('S', 'O2'): {
        'equation': 'S + O₂ → SO₂',
        'temperature': 300, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.95, 'notes': 'Sulfur dioxide formation.'
    },
    ('Na', 'Cl2'): {
        'equation': '2Na + Cl₂ → 2NaCl',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Salt synthesis.'
    },
    ('K', 'Cl2'): {
        'equation': '2K + Cl₂ → 2KCl',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Potassium chloride synthesis.'
    },
    ('Ca', 'O2'): {
        'equation': '2Ca + O₂ → 2CaO',
        'temperature': 500, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Calcium oxide formation.'
    },
    ('Mg', 'O2'): {
        'equation': '2Mg + O₂ → 2MgO',
        'temperature': 600, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Magnesium oxide formation.'
    },
    ('Fe', 'O2'): {
        'equation': '4Fe + 3O₂ → 2Fe₂O₃',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.85, 'notes': 'Rust formation.'
    },
    ('H2', 'Cl2'): {
        'equation': 'H₂ + Cl₂ → 2HCl',
        'temperature': 200, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'Light', 'success_rate': 0.98, 'notes': 'Hydrogen chloride synthesis.'
    },
    ('H2', 'Br2'): {
        'equation': 'H₂ + Br₂ → 2HBr',
        'temperature': 300, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.90, 'notes': 'Hydrogen bromide synthesis.'
    },
    ('H2', 'S'): {
        'equation': 'H₂ + S → H₂S',
        'temperature': 400, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.90, 'notes': 'Hydrogen sulfide synthesis.'
    },
    # Acid-base
    ('HCl', 'NaOH'): {
        'equation': 'HCl + NaOH → NaCl + H₂O',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Neutralization.'
    },
    ('HNO3', 'KOH'): {
        'equation': 'HNO₃ + KOH → KNO₃ + H₂O',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Neutralization.'
    },
    ('H2SO4', 'Ca(OH)2'): {
        'equation': 'H₂SO₄ + Ca(OH)₂ → CaSO₄ + 2H₂O',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.99, 'notes': 'Neutralization.'
    },
    # Combustion
    ('CH4', 'O2'): {
        'equation': 'CH₄ + 2O₂ → CO₂ + 2H₂O',
        'temperature': 600, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 1.0, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Methane combustion.'
    },
    ('C2H6', 'O2'): {
        'equation': '2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O',
        'temperature': 700, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 1.5, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Ethane combustion.'
    },
    # Single replacement
    ('Zn', 'HCl'): {
        'equation': 'Zn + 2HCl → ZnCl₂ + H₂',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.95, 'notes': 'Hydrogen gas evolution.'
    },
    ('Fe', 'CuSO4'): {
        'equation': 'Fe + CuSO₄ → FeSO₄ + Cu',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.95, 'notes': 'Copper displacement.'
    },
    # Double replacement
    ('AgNO3', 'NaCl'): {
        'equation': 'AgNO₃ + NaCl → AgCl↓ + NaNO₃',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Precipitation of AgCl.'
    },
    ('BaCl2', 'Na2SO4'): {
        'equation': 'BaCl₂ + Na₂SO₄ → BaSO₄↓ + 2NaCl',
        'temperature': 25, 'pressure': 1.0, 'concentration_A': 0.5, 'concentration_B': 0.5, 'catalyst': 'None', 'success_rate': 0.98, 'notes': 'Precipitation of BaSO₄.'
    },
    # Decomposition
    ('H2O2',): {
        'equation': '2H₂O₂ → 2H₂O + O₂',
        'temperature': 50, 'pressure': 1.0, 'concentration_A': 1.0, 'concentration_B': 0.0, 'catalyst': 'MnO₂', 'success_rate': 0.90, 'notes': 'Hydrogen peroxide decomposition.'
    },
    ('CaCO3',): {
        'equation': 'CaCO₃ → CaO + CO₂',
        'temperature': 825, 'pressure': 1.0, 'concentration_A': 1.0, 'concentration_B': 0.0, 'catalyst': 'None', 'success_rate': 0.90, 'notes': 'Thermal decomposition.'
    },
    # Add more as needed for all displayed options
}

def find_reaction(elements):
    # Try all orderings
    for key in REACTION_DATABASE:
        if set(key) == set(elements):
            return REACTION_DATABASE[key]
    return None

@app.route('/predict-reaction', methods=['POST'])
def predict_reaction():
    data = request.get_json()
    if not data or 'elements' not in data or len(data['elements']) < 2:
        return jsonify({'error': 'Please provide at least two elements.'}), 400
    elements = data['elements']
    reaction = find_reaction(elements)
    if not reaction:
        return jsonify({'error': f'No known reaction for: {elements}'}), 404
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
    return 'pong', 200

if __name__ == '__main__':
    print("[depHy] API starting on http://127.0.0.1:5001")
    app.run(debug=True, host='127.0.0.1', port=5001) 