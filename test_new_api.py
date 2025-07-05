#!/usr/bin/env python3
"""
Test script for the new depHy reaction prediction API with molecule selection
"""

import requests
import json

def test_molecule_api():
    """Test the new molecule-based reaction prediction API"""
    
    # API endpoint
    url = "http://localhost:5001/predict-reaction"
    
    # Test cases for different reactions
    test_cases = [
        {
            "name": "Hydrogen + Oxygen (Water formation)",
            "data": {
                "elements": ["H2", "O2"]
            }
        },
        {
            "name": "Carbon + Oxygen (CO2 formation)",
            "data": {
                "elements": ["C", "O2"]
            }
        },
        {
            "name": "Nitrogen + Hydrogen (Ammonia formation)",
            "data": {
                "elements": ["N2", "H2"]
            }
        },
        {
            "name": "Sodium + Chlorine (Salt formation)",
            "data": {
                "elements": ["Na", "Cl2"]
            }
        },
        {
            "name": "Bromine + Hydrogen (Hydrogen bromide)",
            "data": {
                "elements": ["Br2", "H2"]
            }
        },
        {
            "name": "Carbon monoxide + Oxygen (CO2 formation)",
            "data": {
                "elements": ["CO", "O2"]
            }
        },
        {
            "name": "Sulfur dioxide + Oxygen (SO3 formation)",
            "data": {
                "elements": ["SO2", "O2"]
            }
        },
        {
            "name": "Ammonia + Hydrochloric acid (Ammonium chloride)",
            "data": {
                "elements": ["NH3", "HCl"]
            }
        },
        {
            "name": "Sulfuric acid + Sodium hydroxide (Neutralization)",
            "data": {
                "elements": ["H2SO4", "NaOH"]
            }
        },
        {
            "name": "Copper + Silver nitrate (Displacement)",
            "data": {
                "elements": ["Cu", "AgNO3"]
            }
        }
    ]
    
    print("Testing depHy Molecule-Based Reaction Prediction API")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Make POST request
            response = requests.post(url, json=test_case['data'])
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"Selected Elements: {' + '.join(result['selected_elements'])}")
                print(f"Balanced Equation: {result['balanced_equation']}")
                print(f"Optimal Temperature: {result['optimal_conditions']['temperature_celsius']} °C / {result['optimal_conditions']['temperature_kelvin']} K")
                print(f"Optimal Pressure: {result['optimal_conditions']['pressure']} atm")
                print(f"Recommended Catalyst: {result['optimal_conditions']['catalyst']}")
                print(f"Success Rate: {result['optimal_conditions']['success_rate']*100:.1f}%")
                print(f"Temperature Range (Celsius): {result['recommendations']['temperature_range_celsius']}")
                print(f"Temperature Range (Kelvin): {result['recommendations']['temperature_range_kelvin']}")
                print(f"Pressure Range: {result['recommendations']['pressure_range']}")
                print(f"Catalyst Notes: {result['recommendations']['catalyst_notes']}")
                    
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the API. Make sure the Flask server is running on port 5001.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def test_available_reactions():
    """Test the available reactions endpoint"""
    try:
        response = requests.get("http://localhost:5001/available-reactions")
        if response.status_code == 200:
            result = response.json()
            print(f"\nAvailable Reactions ({result['total_reactions']} total):")
            for i, reaction in enumerate(result['reactions'], 1):
                print(f"  {i}. {reaction}")
        else:
            print(f"Failed to get available reactions: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to available reactions endpoint on port 5001")

if __name__ == "__main__":
    test_available_reactions()
    test_molecule_api() 