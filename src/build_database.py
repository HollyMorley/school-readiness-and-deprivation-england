import sqlite3
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import EYFSP_PATH, IMD_PATH, DATABASE_PATH


def load_data(report: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    eyfsp_df = pd.read_csv(EYFSP_PATH)
    imd_df = pd.read_excel(IMD_PATH, sheet_name="IMD")

    if report:
        print("\nEYFSP DataFrame:\n======================================")
        print(eyfsp_df.shape)
        print(eyfsp_df.columns.tolist())

    imd_df.rename(columns={
        "Local Authority District code (2019)": "la_code",
        "Local Authority District name (2019)": "la_name",
        "IMD - Average rank ": "avg_rank",
        "IMD - Rank of average rank ": "rank_avg_rank",
        "IMD - Average score ": "avg_score",
        "IMD - Rank of average score ": "rank_avg_score",
        "IMD - Proportion of LSOAs in most deprived 10% nationally ":
            "prop_lsoas_deprived_10",
        "IMD - Rank of proportion of LSOAs in most deprived 10% nationally "
        "": "rank_prop_lsoas_deprived_10",
        "IMD 2019 - Extent ": "extent",
        "IMD 2019 - Rank of extent ": "rank_extent",
        "IMD 2019 - Local concentration ": "local_concentration",
        "IMD 2019 - Rank of local concentration ": "rank_local_concentration",
    }, inplace=True)

    if report:
        print(
            "\nIMD DataFrame renamed:\n======================================")
        print(imd_df.shape)
        print(imd_df.columns.tolist())

    return eyfsp_df, imd_df


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

def write_to_database(eyfsp_df: pd.DataFrame, imd_df: pd.DataFrame):
    with sqlite3.connect(DATABASE_PATH) as conn:
        eyfsp_df.to_sql("eyfsp", conn, if_exists="replace", index=False)
        imd_df.to_sql("imd", conn, if_exists="replace", index=False)

        print(f"Number of rows written to 'eyfsp' table: {len(eyfsp_df)}")
        print(f"Number of rows written to 'imd' table: {len(imd_df)}")


def build_database():
    eyfsp_df, imd_df = load_data(report=True)
    sanity_check(eyfsp_df, imd_df)
    write_to_database(eyfsp_df, imd_df)
    print("Finished building database.")


if __name__ == "__main__":
    build_database()

# conn_eyfsp = sqlite3.connect(EYFSP_PATH)
# conn_imd = sqlite3.connect(IMD_PATH)
