from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import DraftRequest, DraftResponse
from app.models.ml_model import ScoutAIModel
import logging

router = APIRouter()

# Initialize the ML model
ml_model = ScoutAIModel()

@router.post("/suggest", response_model=DraftResponse)
async def get_draft_suggestions(request: DraftRequest):
    """
    Generate draft recommendations based on current draft state.
    
    This endpoint analyzes the current draft situation and provides
    intelligent player recommendations with confidence scores.
    """
    try:
        # Get recommendations from ML model
        recommendations = ml_model.get_recommendations(
            current_pick=request.current_pick,
            current_round=request.current_round,
            user_roster=request.user_roster,
            available_players=request.available_players
        )
        
        return DraftResponse(recommendations=recommendations)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.get("/status")
async def get_model_status():
    """Get the status of the ML model"""
    return {
        "model_loaded": ml_model.is_loaded(),
        "model_version": ml_model.get_version(),
        "model_info": ml_model.get_model_info()
    }

@router.post("/train")
async def train_model(background_tasks: BackgroundTasks, num_samples: int = 20000):
    """
    Train the ML model with synthetic data.
    
    This endpoint triggers model training in the background.
    You can check the training status via the /status endpoint.
    """
    try:
        # Start training in background
        background_tasks.add_task(ml_model.train_model, num_samples=num_samples)
        
        return {
            "message": "Model training started in background",
            "num_samples": num_samples,
            "status": "training"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting model training: {str(e)}"
        )

@router.post("/train-sync")
async def train_model_sync(num_samples: int = 20000):
    """
    Train the ML model synchronously (this may take a while).
    
    This endpoint trains the model and returns the results.
    """
    try:
        # Generate training data
        training_data = ml_model.generate_training_data(num_samples=num_samples)
        
        # Train model
        results = ml_model.train_model(data=training_data, test_size=0.2)
        
        return {
            "message": "Model training completed",
            "results": results,
            "model_info": ml_model.get_model_info()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error training model: {str(e)}"
        )

@router.delete("/model")
async def delete_model():
    """Delete the current trained model"""
    try:
        import os
        if os.path.exists(ml_model.model_path):
            os.remove(ml_model.model_path)
            ml_model.is_model_loaded = False
            return {"message": "Model deleted successfully"}
        else:
            return {"message": "No model found to delete"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting model: {str(e)}"
        )

@router.get("/model-info")
async def get_model_info():
    """Get detailed information about the current model"""
    try:
        return ml_model.get_model_info()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model info: {str(e)}"
        ) 