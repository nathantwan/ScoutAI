# ScoutAI - Fantasy Football Draft Assistant

A professional Chrome extension that provides intelligent draft recommendations during fantasy football drafts on ESPN and Yahoo Fantasy platforms.

## Project Structure

```
ScoutAI/
├── extension/           # Chrome extension (React + Vite + Tailwind)
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── content/     # Content scripts
│   │   ├── background/  # Background scripts
│   │   └── utils/       # Utility functions
│   ├── public/          # Static assets
│   └── dist/           # Built extension
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── models/     # ML models and data models
│   │   ├── api/        # API endpoints
│   │   └── utils/      # Utility functions
│   ├── train_model.py  # ML model training script
│   ├── test_api.py     # Backend testing script
│   └── requirements.txt
└── README.md
```

## Features

- **Real-time Draft Detection**: Automatically detects active drafts on ESPN and Yahoo Fantasy
- **Intelligent Recommendations**: ML-powered player suggestions with confidence scores
- **Roster Analysis**: Current roster summary and needs assessment
- **Cross-Platform Support**: ESPN Fantasy and Yahoo Fantasy (extensible for other platforms)
- **Professional UI**: Clean, modern interface built with React and Tailwind CSS

## Machine Learning Model

### 🤖 Model Architecture

The ScoutAI system uses an **XGBoost regression model** to predict draft recommendation scores. The model considers:

**Features (17 total):**
- **Position encoding** (6 features): One-hot encoding for QB, RB, WR, TE, K, DST
- **Player stats** (3 features): ADP, projected points, bye week
- **Roster state** (6 features): Current count of each position on roster
- **Draft context** (2 features): Current round and pick number
- **Derived features** (3 features): Position need score, ADP value, points value

**Target:** Draft recommendation score (0-1, higher = better recommendation)

### 📊 Training Data

The model is trained on **synthetic data** that simulates realistic draft scenarios:

- **20,000 training samples** (configurable)
- **Realistic feature distributions** based on fantasy football patterns
- **Position-specific strategies** (RB/WR priority early, K/DST late)
- **Roster construction logic** (target counts per position)

### 🧪 Model Training

```bash
# Train the model
cd backend
source venv/bin/activate
python train_model.py

# Or use the API endpoint
curl -X POST "http://localhost:8000/api/v1/train-sync?num_samples=20000"
```

**Training Process:**
1. Generate synthetic training data
2. Split into train/test sets (80/20)
3. Scale features using StandardScaler
4. Train XGBoost regressor
5. Evaluate with MSE, MAE, and R² metrics
6. Save model to disk for production use

### 📈 Model Performance

Typical performance metrics:
- **MSE**: ~0.02-0.04 (lower is better)
- **MAE**: ~0.12-0.15 (lower is better)
- **R²**: ~0.75-0.85 (higher is better)

### 🔄 Model Management

**API Endpoints:**
- `GET /api/v1/status` - Check model status
- `POST /api/v1/train` - Train model (background)
- `POST /api/v1/train-sync` - Train model (synchronous)
- `GET /api/v1/model-info` - Get model details
- `DELETE /api/v1/model` - Delete current model

**Model Persistence:**
- Models are saved to `backend/models/scoutai_model.pkl`
- Includes model, scaler, and metadata
- Automatic loading on server startup

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model:**
   ```bash
   python train_model.py
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`

### Extension Setup

1. Navigate to the extension directory:
   ```bash
   cd extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the extension:
   ```bash
   npm run build
   ```

4. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `extension/dist` folder

### Development

For development with hot reloading:

```bash
# In the extension directory
npm run dev
```

## API Documentation

### POST /suggest

Generate draft recommendations based on current draft state.

**Request Body:**
```json
{
  "current_pick": 1,
  "current_round": 1,
  "user_roster": {
    "QB": ["Patrick Mahomes"],
    "RB": ["Christian McCaffrey"],
    "WR": [],
    "TE": [],
    "K": [],
    "DST": []
  },
  "available_players": [
    {
      "name": "Saquon Barkley",
      "position": "RB",
      "team": "NYG",
      "adp": 12.5,
      "projected_points": 245.3
    }
  ]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "player": {
        "name": "Saquon Barkley",
        "position": "RB",
        "team": "NYG"
      },
      "confidence_score": 0.85,
      "predicted_points": 245.3,
      "boom_probability": 0.25,
      "value_over_replacement": 45.2,
      "explanation": "High-upside RB with strong floor",
      "risk_level": "medium"
    }
  ]
}
```

### Model Training Endpoints

**Train Model (Background):**
```bash
curl -X POST "http://localhost:8000/api/v1/train?num_samples=20000"
```

**Train Model (Synchronous):**
```bash
curl -X POST "http://localhost:8000/api/v1/train-sync?num_samples=20000"
```

**Check Model Status:**
```bash
curl "http://localhost:8000/api/v1/status"
```

## Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate
python test_api.py
```

This will test:
- Health endpoint
- Model status
- Model training
- Model info
- Recommendations API

### Model Testing

```bash
cd backend
source venv/bin/activate
python train_model.py
```

This will:
- Train the model with synthetic data
- Display training metrics
- Test the model with sample data

## Architecture

### Extension Components

- **Content Scripts**: Detect draft pages and inject the sidebar
- **React Sidebar**: Main UI component with draft recommendations
- **Background Script**: Handle extension lifecycle and API communication
- **Manifest V3**: Modern Chrome extension manifest

### Backend Components

- **FastAPI**: RESTful API with automatic documentation
- **XGBoost Model**: ML recommendation engine with feature engineering
- **Data Models**: Pydantic models for type safety
- **CORS**: Configured for extension communication

### ML Pipeline

1. **Feature Engineering**: Extract 17 features from draft state
2. **Model Training**: XGBoost regression on synthetic data
3. **Model Persistence**: Save/load trained models
4. **Real-time Prediction**: Score players during drafts
5. **Recommendation Generation**: Top 3 players with explanations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 