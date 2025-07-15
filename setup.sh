#!/bin/bash

echo "🚀 Setting up ScoutAI - Fantasy Football Draft Assistant"
echo "========================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Train the ML model
echo ""
echo "🤖 Training Machine Learning Model..."
echo "This may take a few minutes..."
python train_model.py

echo "✅ Backend setup complete!"
cd ..

# Setup Extension
echo ""
echo "🔧 Setting up Extension..."
cd extension

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Build the extension
echo "Building the extension..."
npm run build

echo "✅ Extension setup complete!"
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "To load the extension in Chrome:"
echo "  1. Open Chrome and go to chrome://extensions/"
echo "  2. Enable 'Developer mode'"
echo "  3. Click 'Load unpacked'"
echo "  4. Select the 'extension/dist' folder"
echo ""
echo "To test the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python test_api.py"
echo ""
echo "To retrain the model:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python train_model.py"
echo ""
echo "Happy drafting! 🏈" 