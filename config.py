import os

class Config:
    """configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    # Add additional configuration variables as needed

# Use the Render database URL if available, otherwise use a local file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gadgetgo.db'
    
    # Fix for some postgres drivers that use 'postgres://' instead of 'postgresql://'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False