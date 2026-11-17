import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# STEP 1: LOAD DATASET
# ==========================================

df = pd.read_excel("outputs/Netflix_Cleaned.xlsx")

output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

print("\n====================================")
print("    NETFLIX YEAR-WISE ANALYSIS")
print("====================================")


# ==========================================
# STEP 2: DATA VALIDATION
# ==========================================

print("\n===== DATA VALIDATION =====")

print("Total Records:", len(df))

print("Total Columns:", len(df.columns))

print("Missing Release Years:",
      df["release_year"].isna().sum())

print("\nSample Release Year Data:")
print(df["release_year"].head(10))


# ==========================================
# STEP 3: DATA CLEANING
# ==========================================

# Convert release year into numeric format
df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

# Remove records with missing release year
df_year = df.dropna(
    subset=["release_year"]
).copy()

# Convert release year into integer
df_year["release_year"] = (
    df_year["release_year"].astype(int)
)

print("\n===== DATA CLEANING =====")

print("Valid Year Records:", len(df_year))

print("Removed Records:", len(df) - len(df_year))

print("Unique Release Years:",
      df_year["release_year"].nunique())


# ==========================================
# STEP 4: YEAR-WISE CONTENT ANALYSIS
# ==========================================

year_counts = (
    df_year["release_year"]
    .value_counts()
    .sort_index()
)

print("\n===== YEAR-WISE CONTENT COUNT =====")

print(year_counts)


# ==========================================
# STEP 5: TOP 10 RELEASE YEARS
# ==========================================

top_10_years = (
    year_counts
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 RELEASE YEARS =====")

print(top_10_years)


# ==========================================
# STEP 6: HIGHEST CONTENT RELEASE YEAR
# ==========================================

highest_year = year_counts.idxmax()

highest_count = year_counts.max()

print("\n===== HIGHEST RELEASE YEAR =====")

print("Year:", highest_year)

print("Total Content:", highest_count)


# ==========================================
# STEP 7: MOVIES VS TV SHOWS
# ==========================================

year_type_counts = (
    df_year.groupby(
        ["release_year", "type"]
    )
    .size()
    .unstack(fill_value=0)
)

print("\n===== MOVIES VS TV SHOWS =====")

print(year_type_counts)


# ==========================================
# STEP 8: SAVE CSV FILES
# ==========================================

# Save complete year-wise analysis
year_counts.to_csv(
    output_folder / "year_wise_content.csv",
    index_label="Release Year",
    header=["Content Count"]
)

# Save Movies vs TV Shows analysis
year_type_counts.to_csv(
    output_folder / "year_wise_type_analysis.csv",
    index_label="Release Year"
)

# Save Top 10 release years
top_10_years.to_csv(
    output_folder / "top_10_release_years.csv",
    index_label="Release Year",
    header=["Content Count"]
)

print("\nCSV FILES SAVED SUCCESSFULLY!")


# ==========================================
# STEP 9: YEAR-WISE TREND CHART
# ==========================================

# Focus on years from 2000 onwards
recent_years = year_counts[
    year_counts.index >= 2000
]

plt.figure(figsize=(14, 6))

plt.plot(
    recent_years.index,
    recent_years.values,
    marker="o"
)

plt.title(
    "Netflix Content Release Trend (2000 Onwards)",
    fontsize=15
)

plt.xlabel("Release Year")

plt.ylabel("Number of Titles")

plt.grid(
    True,
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    output_folder / "year_wise_trend_chart.png",
    dpi=300
)

plt.show()


# ==========================================
# STEP 10: MOVIES VS TV SHOWS CHART
# ==========================================

top_10_comparison = year_type_counts.loc[
    top_10_years.index
]

top_10_comparison.plot(
    kind="bar",
    figsize=(14, 6)
)

plt.title(
    "Movies vs TV Shows by Top 10 Release Years",
    fontsize=15
)

plt.xlabel("Release Year")

plt.ylabel("Number of Titles")

plt.xticks(rotation=45)

plt.legend(title="Content Type")

plt.tight_layout()

plt.savefig(
    output_folder / "movies_vs_tv_shows_yearly.png",
    dpi=300
)

plt.show()


# ==========================================
# STEP 11: FINAL SUMMARY
# ==========================================

print("\n====================================")
print("          FINAL SUMMARY")
print("====================================")

print("Total Netflix Records:", len(df))

print("Valid Year Records:", len(df_year))

print("Unique Release Years:",
      df_year["release_year"].nunique())

print("Highest Release Year:", highest_year)

print("Content Released in That Year:",
      highest_count)

print("\nTASK 4 COMPLETED SUCCESSFULLY!")

print("====================================")