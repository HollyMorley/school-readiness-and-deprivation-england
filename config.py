from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

EYFSP_PATH = RAW_DATA_DIR / "eyfsp" / "1_eyfsp_headline_measures_2022_2025.csv"
IMD_PATH = (RAW_DATA_DIR / "iod" /
            "File_10_-_IoD2019_Local_Authority_District_Summaries__lower"
            "-tier__.xlsx")
DATABASE_PATH = PROJECT_ROOT / "data" / "early_years.db"
TAKEUP_PATH = (RAW_DATA_DIR / "eyp" /
               "1_early_years_provision_children_registered_2018_2025.csv")
OFSTED_PATH = (RAW_DATA_DIR / "ofsted" /
               "5_early_years_provision_ofsted_2025.csv")
SEN_PATH = (RAW_DATA_DIR / "sen" /
            "4_early_years_provision_ethnicity_sen_2018_2025.csv")
EY_REVIEW_IND = 93472
OBESITY_IND = 90319
