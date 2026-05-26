import sqlite3
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import EYFSP_PATH, IMD_PATH, DATABASE_PATH


def load_data(report: bool = True) -> dict[str, pd.DataFrame]:
    # --- Load EYFSP data ---
    eyfsp_df = pd.read_csv(EYFSP_PATH)

    # Convert numeric columns that are stored as strings due to suppressed values
    for col in ["gld_children_percent", "gld_children_count", "children_count",
                "elgs_expected_average", "all_elgs_expected_children_count",
                "all_elgs_expected_children_percent",
                "comm_lang_lit_expected_children_count",
                "comm_lang_lit_expected_children_percent"]:
        eyfsp_df[col] = pd.to_numeric(eyfsp_df[col], errors="coerce")

    if report:
        print("\nEYFSP DataFrame:\n======================================")
        print(eyfsp_df.shape)
        print(eyfsp_df.columns.tolist())

    # --- Load deprivation data ---

    deprivation_dfs = {
        "imd": pd.read_excel(IMD_PATH, sheet_name="IMD"),
        "iod_income": pd.read_excel(IMD_PATH, sheet_name="Income"),
        "iod_employment": pd.read_excel(IMD_PATH, sheet_name="Employment"),
        "iod_education": pd.read_excel(IMD_PATH, sheet_name="Education"),
        "iod_health": pd.read_excel(IMD_PATH, sheet_name="Health"),
        "iod_crime": pd.read_excel(IMD_PATH, sheet_name="Crime"),
        "iod_barriers": pd.read_excel(IMD_PATH, sheet_name="Barriers"),
        "iod_living": pd.read_excel(IMD_PATH, sheet_name="Living"),
        "iod_idaci": pd.read_excel(IMD_PATH, sheet_name="IDACI"),
        "iod_idaopi": pd.read_excel(IMD_PATH, sheet_name="IDAOPI"),
    }
    deprivation_feature_names = [
        "IMD",
        "Income",
        "Employment",
        "Education, Skills, and Training",
        "Health Deprivation and Disability",
        "Crime",
        "Barriers to Housing and Services",
        "Living Environment",
        "IDACI",
        "IDAOPI",
    ]
    if len(deprivation_dfs.keys()) != len(deprivation_feature_names):
        raise ValueError(
            "Number of deprivation DataFrames does not match number of "
            "feature names.")

    for (df_name, df), feat_name in zip(deprivation_dfs.items(), deprivation_feature_names):
        df.rename(columns={
            "Local Authority District code (2019)": "la_code",
            "Local Authority District name (2019)": "la_name",
            f"{feat_name} - Average score ": "avg_score",
            f"{feat_name} - Rank of average score ": "rank_avg_score",
        }, inplace=True)

        if report:
            print(
                f"\n{df_name} DataFrame renamed:\n======================================")
            print(df.shape)
            print(df.columns.tolist())

    # Add EYFSP data to dict
    dfs = deprivation_dfs
    dfs["eyfsp"] = eyfsp_df

    return dfs


def sanity_check(eyfsp_df: pd.DataFrame, imd_df: pd.DataFrame):
    # --- EYFSP sanity check ---
    percent_gld_expected_202425 = 68.3
    # reported on DfE website under 'Headline measures' at
    # https://explore-education-statistics.service.gov.uk/find-statistics
    # /early-years-foundation-stage-profile-results/2024-25/explore#featured
    # -tables-section
    conditions = {
        "time_period": 202425,
        "geographic_level": "National",
        "breakdown_topic": "Total",
        "breakdown": "Total",
        "sex": "Total",
    }
    mask = True
    for col, val in conditions.items():
        mask = mask & (eyfsp_df[col] == val)

    percent_gld_202425 = eyfsp_df.loc[mask, "gld_children_percent"].values
    len_percent_gld_202425 = len(percent_gld_202425)
    if len_percent_gld_202425 != 1:
        raise ValueError(
            f"Expected exactly one row matching the conditions, but found "
            f"{len_percent_gld_202425} rows.")
    if not np.isclose(pd.to_numeric(percent_gld_202425)[0],
                      percent_gld_expected_202425, atol=0.1):
        raise ValueError(
            "Expected and actual percent_gld_202425 values do not match.")

    # --- IMD sanity check ---
    most_deprived_la_expected = 'Blackpool'
    # reported in 'Statistical release - Main findings' at
    # https://www.gov.uk/government/statistics/english-indices-of
    # -deprivation-2019
    most_deprived_idx = imd_df["rank_avg_score"].idxmin()
    most_deprived_la = imd_df.loc[most_deprived_idx, "la_name"]
    if most_deprived_la != most_deprived_la_expected:
        raise ValueError(
            f"Expected most deprived rank to be "
            f"{most_deprived_la_expected}, but found "
            f"{most_deprived_la.values[0]}.")

def write_to_database(dfs: dict[str, pd.DataFrame]):
    with sqlite3.connect(DATABASE_PATH) as conn:
        for df_name, df in dfs.items():
            df.to_sql(f"{df_name}", conn, if_exists="replace", index=False)


def build_database():
    dfs = load_data(report=True)
    sanity_check(dfs["eyfsp"], dfs["imd"])
    write_to_database(dfs)
    print("Finished building database.")


if __name__ == "__main__":
    build_database()

# conn_eyfsp = sqlite3.connect(EYFSP_PATH)
# conn_imd = sqlite3.connect(IMD_PATH)
