#!/usr/bin/env python3
"""
Training script for ScoutAI ML model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.ml_model import ScoutAIModel
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Train the ScoutAI model"""
    print("🏈 Training ScoutAI Fantasy Football Model")
    print("=" * 50)
    
    # Initialize model
    model = ScoutAIModel()
    
    # Generate training data
    print("📊 Generating training data...")
    training_data = model.generate_training_data(num_samples=20000)
    print(f"Generated {len(training_data)} training samples")
    
    # Train model
    print("🤖 Training XGBoost model...")
    results = model.train_model(data=training_data, test_size=0.2)
    
    # Print results
    print("\n📈 Training Results:")
    print(f"  MSE: {results['mse']:.4f}")
    print(f"  MAE: {results['mae']:.4f}")
    print(f"  R²: {results['r2']:.4f}")
    print(f"  Training samples: {results['training_samples']}")
    print(f"  Test samples: {results['test_samples']}")
    
    # Model info
    model_info = model.get_model_info()
    print(f"\n📋 Model Information:")
    print(f"  Version: {model_info['version']}")
    print(f"  Features: {model_info['features']}")
    print(f"  Model path: {model_info['model_path']}")
    print(f"  Loaded: {model_info['loaded']}")
    
    print("\n✅ Model training complete!")
    print("The model is now ready to provide draft recommendations.")
    
    # Test the model
    print("\n🧪 Testing model with sample data...")
    from app.models.schemas import Player, Roster
    
    test_roster = Roster(
        QB=["Patrick Mahomes"],
        RB=["Christian McCaffrey"],
        WR=[],
        TE=[],
        K=[],
        DST=[]
    )
    
    test_players = [
        Player(name="Saquon Barkley", position="RB", team="NYG", adp=8.5, projected_points=245.3),
        Player(name="Stefon Diggs", position="WR", team="BUF", adp=12.3, projected_points=235.7),
        Player(name="Josh Allen", position="QB", team="BUF", adp=15.8, projected_points=310.5)
    ]
    
    try:
        recommendations = model.get_recommendations(
            current_pick=3,
            current_round=1,
            user_roster=test_roster,
            available_players=test_players
        )
        
        print(f"✅ Model test successful! Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec.player.name} ({rec.player.position}) - {rec.confidence_score:.1%} confidence")
            
    except Exception as e:
        print(f"❌ Model test failed: {e}")

if __name__ == "__main__":
    main() 