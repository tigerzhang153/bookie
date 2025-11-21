import pandas as pd
import numpy as np
import joblib
import os
import logging

logger = logging.getLogger(__name__)

# Load the saved model once at module level
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "ml_model.joblib")

# Cloud Storage configuration (fallback if local file not available)
MODEL_BUCKET = os.environ.get("MODEL_BUCKET", "bookie-ai-dc1f8-models")
MODEL_BLOB = os.environ.get("MODEL_BLOB", "ml_model.joblib")

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

def _download_model_from_gcs():
    """Download model from Google Cloud Storage if local file is not available."""
    try:
        from google.cloud import storage
        
        logger.info(f"Attempting to download model from gs://{MODEL_BUCKET}/{MODEL_BLOB}")
        client = storage.Client()
        bucket = client.bucket(MODEL_BUCKET)
        blob = bucket.blob(MODEL_BLOB)
        
        # Download to the expected location
        blob.download_to_filename(model_path)
        logger.info(f"Model downloaded successfully from Cloud Storage to {model_path}")
        
        # Verify the downloaded file
        file_size = os.path.getsize(model_path)
        if file_size < 1000000:  # Should be ~149MB
            raise RuntimeError(f"Downloaded model file too small ({file_size} bytes)")
        
        return True
    except ImportError:
        logger.warning("google-cloud-storage not available, skipping Cloud Storage download")
        return False
    except Exception as e:
        logger.error(f"Failed to download model from Cloud Storage: {str(e)}")
        return False

def _load_model():
    """Load the model from ml_model.joblib if not already loaded."""
    global _model
    if _model is None:
        # Check if file exists and is valid
        file_exists = os.path.exists(model_path)
        file_valid = False
        
        if file_exists:
            file_size = os.path.getsize(model_path)
            logger.info(f"Model file found: {model_path}, size: {file_size} bytes")
            
            # Check if file is valid (not a Git LFS pointer)
            if file_size < 1000000:  # Git LFS pointers are small (< 1MB)
                logger.warning(f"Model file appears to be a Git LFS pointer (size: {file_size} bytes). Attempting to download from Cloud Storage...")
                # Try to download from Cloud Storage
                if _download_model_from_gcs():
                    file_size = os.path.getsize(model_path)
                    file_valid = file_size >= 1000000
                else:
                    raise FileNotFoundError(
                        f"Model file is a Git LFS pointer (size: {file_size} bytes) and download from Cloud Storage failed. "
                        f"Please upload the model to gs://{MODEL_BUCKET}/{MODEL_BLOB}"
                    )
            else:
                file_valid = True
        else:
            logger.warning(f"Model file not found locally: {model_path}. Attempting to download from Cloud Storage...")
            # Try to download from Cloud Storage
            if _download_model_from_gcs():
                file_size = os.path.getsize(model_path)
                file_valid = file_size >= 1000000
            else:
                raise FileNotFoundError(
                    f"Model file not found: {model_path}. "
                    f"Current dir: {os.getcwd()}, Script dir: {script_dir}. "
                    f"Please upload the model to gs://{MODEL_BUCKET}/{MODEL_BLOB} or ensure it's included in the Docker image."
                )
        
        # Load the model
        try:
            _model = joblib.load(model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            error_msg = str(e)
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
