#Configuration settings
class Config:
    """Base configuration."""
    SECRET_KEY = 'your-secret-key'  # Replace with a secure key
    MONGO_URI = 'mongodb://localhost:27017/melascandb'  # Use your MongoDB URI here
    DEBUG = True  # Set to False in production

# Add any other settings as needed, e.g., email settings, JWT, etc.
