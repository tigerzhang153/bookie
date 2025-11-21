import pandas as pd
import numpy as np
import joblib
import os
import logging

logger = logging.getLogger(__name__)

# Load the saved model once at module level
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "ml_model.joblib")

# Load model lazily on first use
_model = None

def _is_valid_model_file(filepath):
    """Check if the file is a valid joblib model file (not a Git LFS pointer)."""
    try:
        # Check file size - Git LFS pointers are usually < 200 bytes
        if os.path.getsize(filepath) < 200:
            return False
        # Try to load it - if it fails, it's not valid
        test_model = joblib.load(filepath)
        return True
    except Exception:
        return False

def _load_model():
    """Load the model from ml_model.joblib if not already loaded."""
    global _model
    if _model is None:
        # Check if file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}. "
                f"Current dir: {os.getcwd()}, Script dir: {script_dir}. "
                f"File may not have been included in Docker image (Git LFS issue)."
            )
        
        # Check if file is valid (not a Git LFS pointer)
        file_size = os.path.getsize(model_path)
        logger.info(f"Model file size: {file_size} bytes")
        
        if file_size < 1000:  # Git LFS pointers are small
            raise FileNotFoundError(
                f"Model file appears to be a Git LFS pointer (size: {file_size} bytes). "
                f"Actual model file not included in Docker image. "
                f"Please ensure Git LFS files are pulled during build."
            )
        
        try:
            _model = joblib.load(model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            error_msg = str(e)
            if "118" in error_msg or "version" in error_msg.lower():
                raise RuntimeError(
                    f"Failed to load model from {model_path}: {error_msg}. "
                    f"This may indicate the file is corrupted or a Git LFS pointer. "
                    f"File size: {file_size} bytes. "
                    f"Please check Cloud Build logs to ensure Git LFS files were pulled."
                )
            raise RuntimeError(f"Failed to load model from {model_path}: {error_msg}")
    return _model

def predicter(game_df):
    """
    Predict point totals using the saved model from ml_model.joblib.
    
    Parameters:
        game_df: pd.DataFrame with features: avgpointtotal_home, avgpointtotal_away, meanpointtotal
        
    Returns:
        float: Predicted point total
    """
    model = _load_model()
    
    # Ensure game_df has the correct features
    required_features = ["avgpointtotal_home", "avgpointtotal_away", "meanpointtotal"]
    if not all(feat in game_df.columns for feat in required_features):
        raise ValueError(f"game_df must contain columns: {required_features}")
    
    # Make prediction
    prediction = model.predict(game_df[required_features])[0]
    return prediction
