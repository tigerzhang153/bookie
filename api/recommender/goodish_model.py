import pandas as pd
import numpy as np
import joblib
import os

# Load the saved model once at module level
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "ml_model.joblib")

# Load model lazily on first use
_model = None

def _load_model():
    """Load the model from ml_model.joblib if not already loaded."""
    global _model
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}. Current dir: {os.getcwd()}, Script dir: {script_dir}")
        
        # Check file size to detect Git LFS pointer
        file_size = os.path.getsize(model_path)
        if file_size < 1000000:  # Git LFS pointers are small
            raise FileNotFoundError(
                f"Model file appears to be a Git LFS pointer (size: {file_size} bytes). "
                f"Expected ~149MB. Please ensure Git LFS files are pulled during Docker build."
            )
        
        try:
            _model = joblib.load(model_path)
        except Exception as e:
            error_msg = str(e)
            if "118" in error_msg:
                raise RuntimeError(
                    f"Failed to load model (error 118): File may be corrupted or a Git LFS pointer. "
                    f"File size: {file_size} bytes. Expected ~149MB. "
                    f"Please ensure the actual model file is included in the Docker image."
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
