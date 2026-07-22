from pathlib import Path
# from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
BRONZE_DATA_DIR = DATA_DIR / "bronze"
SILVER_DATA_DIR = DATA_DIR / "silver"
GOLD_DATA_DIR = DATA_DIR / "gold"
REPORTS_DIR = BASE_DIR / "reports"

for directory in [
    RAW_DATA_DIR,
    BRONZE_DATA_DIR,
    SILVER_DATA_DIR,
    GOLD_DATA_DIR,
    REPORTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
# ======================================================
# Retail Analytics Platform Configuration
# ======================================================

# Record counts
NUM_CUSTOMERS = 20      # Start small for testing
NUM_PRODUCTS = 2000
NUM_STORES = 50
NUM_EMPLOYEES = 50
NUM_SUPPLIERS = 15
NUM_ORDERS = 100

# Random seed
RANDOM_SEED = 42


