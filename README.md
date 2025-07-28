# depHy - Chemical Reaction Prediction API

A Flask-based API that predicts chemical reaction outcomes using machine learning. The API analyzes reaction conditions like temperature, pressure, concentration, and catalyst presence to predict whether a reaction will be successful, result in low yield, or fail to react.

## Features

- **Machine Learning Model**: Uses RandomForestClassifier for prediction
- **Data Preprocessing**: Automatic encoding of categorical variables and normalization of numeric features
- **Sample Data Generation**: Creates realistic chemical reaction data if no dataset is provided
- **RESTful API**: Clean JSON-based API endpoints
- **Input Validation**: Comprehensive validation of reaction conditions
- **Probability Scores**: Returns confidence scores for all possible outcomes

## API Endpoints

### POST `/predict-reaction`
Predicts the outcome of a chemical reaction based on input conditions.

**Request Body:**
```json
{
  "temperature": 150,
  "pressure": 1.5,
  "concentration_A": 0.5,
  "concentration_B": 0.5,
  "catalyst": "yes"
}
```

**Response:**
```json
{
  "predicted_outcome": "success",
  "confidence": 0.85,
  "probabilities": {
    "success": 0.85,
    "low_yield": 0.12,
    "no_reaction": 0.03
  },
  "input_conditions": {
    "temperature": 150,
    "pressure": 1.5,
    "concentration_A": 0.5,
    "concentration_B": 0.5,
    "catalyst": "yes"
  }
}
```

### GET `/health`
Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "depHy Reaction Prediction API is running"
}
```

### GET `/`
API information and documentation.

## Input Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| temperature | float | 25-300 °C | Reaction temperature |
| pressure | float | 0.5-3.0 atm | Reaction pressure |
| concentration_A | float | 0.1-1.0 mol/L | Concentration of reactant A |
| concentration_B | float | 0.1-1.0 mol/L | Concentration of reactant B |
| catalyst | string | "yes" or "no" | Presence of catalyst |

## Output Classes

- **success**: Reaction proceeds successfully with good yield
- **low_yield**: Reaction occurs but with limited product formation
- **no_reaction**: No significant reaction occurs under given conditions

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
python app.py
```

The API will start on `http://localhost:5001`

### 3. Test the API

```bash
python test_api.py
```

## Dataset Structure

The API expects a CSV file named `reaction_data.csv` with the following columns:

- `temperature` (°C): Reaction temperature
- `pressure` (atm): Reaction pressure  
- `concentration_A` (mol/L): Concentration of reactant A
- `concentration_B` (mol/L): Concentration of reactant B
- `catalyst` (yes/no): Presence of catalyst
- `reaction_outcome` (success/low_yield/no_reaction): Observed outcome

If no dataset is provided, the API will automatically generate realistic sample data.

## Machine Learning Pipeline

1. **Data Loading**: Reads CSV data or generates sample data
2. **Preprocessing**: 
   - Encodes categorical variables using LabelEncoder
   - Normalizes numeric features using StandardScaler
3. **Model Training**: Trains RandomForestClassifier with 100 estimators
4. **Model Persistence**: Saves trained model and preprocessors for reuse
5. **Prediction**: Scales input features and predicts outcome with probabilities

## Example Usage

### Using curl

```bash
curl -X POST http://localhost:5001/predict-reaction \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 200,
    "pressure": 2.0,
    "concentration_A": 0.6,
    "concentration_B": 0.6,
    "catalyst": "yes"
  }'
```

### Using Python requests

```python
import requests

data = {
    "temperature": 200,
    "pressure": 2.0,
    "concentration_A": 0.6,
    "concentration_B": 0.6,
    "catalyst": "yes"
}

response = requests.post("http://localhost:5001/predict-reaction", json=data)
result = response.json()
print(f"Predicted outcome: {result['predicted_outcome']}")
```

## Model Performance

The RandomForest model typically achieves:
- Training accuracy: ~95-98%
- Test accuracy: ~85-92%

Performance may vary based on the quality and quantity of training data.

## Error Handling

The API includes comprehensive error handling for:
- Missing required fields
- Invalid data types
- Out-of-range values
- Model loading failures
- Prediction errors

## Development

### Project Structure

```
depHy-Chem-Website/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── test_api.py        # API testing script
├── reaction_data.csv  # Training dataset (auto-generated)
├── model.pkl          # Trained model (auto-generated)
├── preprocessors.pkl  # Data preprocessors (auto-generated)
├── index.html         # Frontend website
└── README.md          # This file
```

### Adding Custom Data

To use your own reaction data:

1. Create a CSV file named `reaction_data.csv` with the required columns
2. Delete existing `model.pkl` and `preprocessors.pkl` files (if they exist)
3. Restart the API - it will retrain with your data

## License

This project is part of the depHy chemical optimization platform.

## Support

For questions or issues, please contact the development team.
