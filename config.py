from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

EYFSP_PATH = RAW_DATA_DIR / "eyfsp" / "1_eyfsp_headline_measures_2022_2025.csv"
IMD_PATH = (RAW_DATA_DIR / "iod" /
            "File_10_-_IoD2019_Local_Authority_District_Summaries__lower"
            "-tier__.xlsx")
DATABASE_PATH = PROJECT_ROOT / "data" / "early_years.db"
