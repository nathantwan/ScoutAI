import numpy as np
import pandas as pd
import pickle
import logging
from typing import List, Dict, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
from app.models.schemas import Player, Roster, Recommendation, Position
import os

logger = logging.getLogger(__name__)

class ScoutAIModel:
    """Real ML model for fantasy football draft recommendations"""
    
    def __init__(self, model_path: str = "models/scoutai_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.model_version = "1.0.0"
        self.is_model_loaded = False
        self.feature_columns = [
            'position_qb', 'position_rb', 'position_wr', 'position_te', 'position_k', 'position_dst',
            'adp', 'projected_points', 'bye_week',
            'roster_qb_count', 'roster_rb_count', 'roster_wr_count', 'roster_te_count', 'roster_k_count', 'roster_dst_count',
            'current_round', 'current_pick',
            'position_need_score', 'adp_value', 'points_value'
        ]
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.scaler = model_data['scaler']
                    self.label_encoders = model_data['label_encoders']
                    self.is_model_loaded = True
                logger.info("ML model loaded successfully from disk")
            else:
                logger.warning("No trained model found. Please train the model first.")
                self.is_model_loaded = False
        except Exception as e:
            logger.error(f"Error loading ML model: {e}")
            self.is_model_loaded = False
    
    def _save_model(self):
        """Save the trained model to disk"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'version': self.model_version
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def generate_training_data(self, num_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic training data for the model"""
        np.random.seed(42)
        
        data = []
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        
        for _ in range(num_samples):
            # Generate player features
            position = np.random.choice(positions)
            adp = np.random.uniform(1, 200)
            projected_points = np.random.uniform(50, 400)
            bye_week = np.random.randint(1, 18)
            
            # Generate roster state
            roster_counts = {
                'QB': np.random.randint(0, 3),
                'RB': np.random.randint(0, 6),
                'WR': np.random.randint(0, 6),
                'TE': np.random.randint(0, 3),
                'K': np.random.randint(0, 2),
                'DST': np.random.randint(0, 2)
            }
            
            current_round = np.random.randint(1, 16)
            current_pick = np.random.randint(1, 13)
            
            # Calculate position need score
            target_counts = {'QB': 1, 'RB': 3, 'WR': 3, 'TE': 1, 'K': 1, 'DST': 1}
            position_need = max(0, (target_counts[position] - roster_counts[position]) / target_counts[position])
            
            # Calculate ADP value (lower ADP = higher value)
            adp_value = max(0, (200 - adp) / 200)
            
            # Calculate points value
            points_value = min(1.0, projected_points / 400)
            
            # Create feature vector
            features = {
                'position_qb': 1 if position == 'QB' else 0,
                'position_rb': 1 if position == 'RB' else 0,
                'position_wr': 1 if position == 'WR' else 0,
                'position_te': 1 if position == 'TE' else 0,
                'position_k': 1 if position == 'K' else 0,
                'position_dst': 1 if position == 'DST' else 0,
                'adp': adp,
                'projected_points': projected_points,
                'bye_week': bye_week,
                'roster_qb_count': roster_counts['QB'],
                'roster_rb_count': roster_counts['RB'],
                'roster_wr_count': roster_counts['WR'],
                'roster_te_count': roster_counts['TE'],
                'roster_k_count': roster_counts['K'],
                'roster_dst_count': roster_counts['DST'],
                'current_round': current_round,
                'current_pick': current_pick,
                'position_need_score': position_need,
                'adp_value': adp_value,
                'points_value': points_value
            }
            
            # Generate target (draft recommendation score)
            # This is a simplified scoring function - in practice, you'd use real draft data
            target_score = (
                position_need * 0.4 +
                adp_value * 0.3 +
                points_value * 0.3 +
                np.random.normal(0, 0.1)  # Add some noise
            )
            target_score = max(0, min(1, target_score))  # Clamp to [0, 1]
            
            features['target_score'] = target_score
            data.append(features)
        
        return pd.DataFrame(data)
    
    def train_model(self, data: Optional[pd.DataFrame] = None, test_size: float = 0.2):
        """Train the XGBoost model"""
        logger.info("Starting model training...")
        
        # Generate training data if none provided
        if data is None:
            data = self.generate_training_data()
        
        # Prepare features and target
        X = data[self.feature_columns]
        y = data['target_score']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train XGBoost model
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            objective='reg:squarederror'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model training complete!")
        logger.info(f"MSE: {mse:.4f}")
        logger.info(f"MAE: {mae:.4f}")
        logger.info(f"R²: {r2:.4f}")
        
        # Save model
        self._save_model()
        self.is_model_loaded = True
        
        return {
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def _prepare_features(self, player: Player, roster: Roster, current_round: int, current_pick: int) -> np.ndarray:
        """Prepare features for a single player"""
        # Position one-hot encoding
        position_features = {
            'QB': [1, 0, 0, 0, 0, 0],
            'RB': [0, 1, 0, 0, 0, 0],
            'WR': [0, 0, 1, 0, 0, 0],
            'TE': [0, 0, 0, 1, 0, 0],
            'K': [0, 0, 0, 0, 1, 0],
            'DST': [0, 0, 0, 0, 0, 1]
        }
        
        # Roster counts
        roster_counts = {
            'QB': len(roster.QB),
            'RB': len(roster.RB),
            'WR': len(roster.WR),
            'TE': len(roster.TE),
            'K': len(roster.K),
            'DST': len(roster.DST)
        }
        
        # Calculate position need
        target_counts = {'QB': 1, 'RB': 3, 'WR': 3, 'TE': 1, 'K': 1, 'DST': 1}
        position_need = max(0, (target_counts[player.position] - roster_counts[player.position]) / target_counts[player.position])
        
        # Calculate ADP value
        adp = player.adp or 100
        adp_value = max(0, (200 - adp) / 200)
        
        # Calculate points value
        projected_points = player.projected_points or 200
        points_value = min(1.0, projected_points / 400)
        
        # Create feature vector
        features = position_features[player.position] + [
            adp,
            projected_points,
            player.bye_week or 8,
            roster_counts['QB'],
            roster_counts['RB'],
            roster_counts['WR'],
            roster_counts['TE'],
            roster_counts['K'],
            roster_counts['DST'],
            current_round,
            current_pick,
            position_need,
            adp_value,
            points_value
        ]
        
        return np.array(features).reshape(1, -1)
    
    def predict_score(self, player: Player, roster: Roster, current_round: int, current_pick: int) -> float:
        """Predict draft recommendation score for a player"""
        if not self.is_model_loaded:
            raise RuntimeError("Model not loaded. Please train the model first.")
        
        features = self._prepare_features(player, roster, current_round, current_pick)
        features_scaled = self.scaler.transform(features)
        score = self.model.predict(features_scaled)[0]
        return max(0, min(1, score))  # Clamp to [0, 1]
    
    def get_recommendations(
        self,
        current_pick: int,
        current_round: int,
        user_roster: Roster,
        available_players: List[Player]
    ) -> List[Recommendation]:
        """Generate draft recommendations using the trained model"""
        
        if not self.is_model_loaded:
            raise RuntimeError("ML model not loaded. Please train the model first.")
        
        # Score all available players
        player_scores = []
        for player in available_players:
            try:
                score = self.predict_score(player, user_roster, current_round, current_pick)
                player_scores.append((player, score))
            except Exception as e:
                logger.warning(f"Error scoring player {player.name}: {e}")
                continue
        
        # Sort by score and take top 3
        player_scores.sort(key=lambda x: x[1], reverse=True)
        top_players = player_scores[:3]
        
        # Generate recommendations
        recommendations = []
        for player, score in top_players:
            # Calculate additional metrics
            boom_prob = min(0.3, score * 0.4)  # Simplified boom probability
            vor = score * 50  # Simplified value over replacement
            
            recommendation = Recommendation(
                player=player,
                confidence_score=score,
                predicted_points=player.projected_points or 200.0,
                boom_probability=boom_prob,
                value_over_replacement=vor,
                explanation=self._generate_explanation(player, score, user_roster, current_round),
                risk_level=self._calculate_risk_level(player, score)
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_explanation(self, player: Player, score: float, roster: Roster, current_round: int) -> str:
        """Generate explanation for recommendation"""
        explanations = []
        
        # Position need analysis
        roster_counts = {
            'QB': len(roster.QB),
            'RB': len(roster.RB),
            'WR': len(roster.WR),
            'TE': len(roster.TE),
            'K': len(roster.K),
            'DST': len(roster.DST)
        }
        
        target_counts = {'QB': 1, 'RB': 3, 'WR': 3, 'TE': 1, 'K': 1, 'DST': 1}
        current_count = roster_counts[player.position]
        target_count = target_counts[player.position]
        
        if current_count < target_count:
            explanations.append(f"Need {target_count - current_count} more {player.position}")
        else:
            explanations.append(f"Good {player.position} depth")
        
        # ADP analysis
        if player.adp and player.adp < 20:
            explanations.append("Elite ADP value")
        elif player.adp and player.adp < 50:
            explanations.append("Good ADP value")
        
        # Points analysis
        if player.projected_points and player.projected_points > 250:
            explanations.append("High projected points")
        
        # Round strategy
        if current_round <= 3:
            if player.position in ['RB', 'WR']:
                explanations.append("Early round priority")
        elif current_round >= 10:
            if player.position in ['K', 'DST']:
                explanations.append("Late round target")
        
        if not explanations:
            explanations.append("Solid all-around value")
        
        return ". ".join(explanations)
    
    def _calculate_risk_level(self, player: Player, score: float) -> str:
        """Calculate risk level for a player"""
        risk_factors = 0
        
        # ADP risk
        if player.adp and player.adp > 100:
            risk_factors += 1
        
        # Points risk
        if player.projected_points and player.projected_points < 150:
            risk_factors += 1
        
        # Score risk
        if score < 0.3:
            risk_factors += 1
        
        if risk_factors >= 2:
            return "high"
        elif risk_factors >= 1:
            return "medium"
        else:
            return "low"
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self.is_model_loaded
    
    def get_version(self) -> str:
        """Get model version"""
        return self.model_version
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'version': self.model_version,
            'loaded': self.is_model_loaded,
            'features': len(self.feature_columns),
            'model_path': self.model_path
        }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores from the trained model"""
        if not self.is_model_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Please train the model first.")
        
        try:
            # Get feature importance from XGBoost model
            importance_scores = self.model.feature_importances_
            
            # Create dictionary mapping feature names to importance scores
            feature_importance = dict(zip(self.feature_columns, importance_scores))
            
            # Sort by importance (descending)
            sorted_importance = dict(sorted(
                feature_importance.items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
            return sorted_importance
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            return {}
    
    def get_top_features(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get top N most important features with their scores"""
        feature_importance = self.get_feature_importance()
        
        top_features = []
        for i, (feature, importance) in enumerate(list(feature_importance.items())[:top_n]):
            top_features.append({
                'rank': i + 1,
                'feature': feature,
                'importance': float(importance),
                'percentage': float(importance * 100)
            })
        
        return top_features 