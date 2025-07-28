import requests
import json

def test_prediction_api():
    """Test the reaction prediction API with sample data"""
    
    # API endpoint
    url = "http://localhost:5001/predict-reaction"
    
    # Sample reaction conditions
    test_cases = [
        {
            "name": "High temperature, high pressure, with catalyst",
            "data": {
                "temperature": 250,
                "pressure": 2.5,
                "concentration_A": 0.8,
                "concentration_B": 0.7,
                "catalyst": "yes"
            }
        },
        {
            "name": "Low temperature, low pressure, no catalyst",
            "data": {
                "temperature": 50,
                "pressure": 0.8,
                "concentration_A": 0.2,
                "concentration_B": 0.3,
                "catalyst": "no"
            }
        },
        {
            "name": "Moderate conditions with catalyst",
            "data": {
                "temperature": 150,
                "pressure": 1.5,
                "concentration_A": 0.5,
                "concentration_B": 0.5,
                "catalyst": "yes"
            }
        }
    ]
    
    print("Testing depHy Reaction Prediction API")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Make POST request
            response = requests.post(url, json=test_case['data'])
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"Input conditions:")
                for key, value in result['input_conditions'].items():
                    print(f"  {key}: {value}")
                
                print(f"\nPrediction: {result['predicted_outcome']}")
                print(f"Confidence: {result['confidence']:.3f}")
                
                print(f"\nProbabilities:")
                for outcome, prob in result['probabilities'].items():
                    print(f"  {outcome}: {prob:.3f}")
                    
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the API. Make sure the Flask server is running on port 5001.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:5001/health")
        if response.status_code == 200:
            result = response.json()
            print(f"\nHealth Check: {result['status']}")
            print(f"Model loaded: {result['model_loaded']}")
            print(f"Message: {result['message']}")
        else:
            print(f"Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to health check endpoint on port 5001")

if __name__ == "__main__":
    test_health_check()
    test_prediction_api() 