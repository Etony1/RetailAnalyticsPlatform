from pathlib import Path

# ======================================================
# Retail Analytics Platform Configuration
# ======================================================

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

# Create folders automatically
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Record counts
NUM_CUSTOMERS = 20      # Start small for testing
NUM_PRODUCTS = 2000
NUM_STORES = 50
NUM_EMPLOYEES = 50
NUM_SUPPLIERS = 15
NUM_ORDERS = 100

# Random seed
RANDOM_SEED = 42