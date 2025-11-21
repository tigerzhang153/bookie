import pandas as pd
import numpy as np
import joblib
import os
import logging

logger = logging.getLogger(__name__)

# Load the saved model once at module level
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "ml_model.joblib")

# Cloud Storage fallback (only used if local file is a Git LFS pointer)
MODEL_BUCKET = os.environ.get("MODEL_BUCKET", "bookie-ai-dc1f8-models")
MODEL_BLOB = os.environ.get("MODEL_BLOB", "ml_model.joblib")

# Load model lazily on first use
_model = None

def _download_from_gcs():
    """Download model from Cloud Storage if local file is a Git LFS pointer."""
    try:
        from google.cloud import storage
        logger.info(f"Downloading model from gs://{MODEL_BUCKET}/{MODEL_BLOB}")
        client = storage.Client()
        bucket = client.bucket(MODEL_BUCKET)
        blob = bucket.blob(MODEL_BLOB)
        blob.download_to_filename(model_path)
        file_size = os.path.getsize(model_path)
        if file_size < 100000000:
            raise RuntimeError(f"Downloaded file too small: {file_size} bytes")
        logger.info(f"Model downloaded successfully: {file_size} bytes")
        return True
    except ImportError:
        logger.warning("google-cloud-storage not available")
        return False
    except Exception as e:
        logger.error(f"Failed to download from Cloud Storage: {e}")
        return False

def _load_model():
    """Load the model from ml_model.joblib if not already loaded."""
    global _model
    if _model is None:
        # Check if file exists
        if not os.path.exists(model_path):
            logger.warning(f"Model file not found locally, trying Cloud Storage...")
            if not _download_from_gcs():
                raise FileNotFoundError(
                    f"Model file not found: {model_path}. "
                    f"Please upload model to gs://{MODEL_BUCKET}/{MODEL_BLOB}"
                )
        else:
            # Check if file is a Git LFS pointer
            file_size = os.path.getsize(model_path)
            if file_size < 100000000:  # Less than 100MB = likely Git LFS pointer
                logger.warning(f"Model file is Git LFS pointer ({file_size} bytes), downloading from Cloud Storage...")
                if not _download_from_gcs():
                    raise FileNotFoundError(
                        f"Model file is a Git LFS pointer (size: {file_size} bytes). "
                        f"Please upload model to gs://{MODEL_BUCKET}/{MODEL_BLOB}"
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
