import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# STEP 1: CREATE OUTPUT FOLDER AND LOAD DATA
# ==========================================

output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

file_path = output_folder / "Netflix_Cleaned.xlsx"

if not file_path.exists():
    raise FileNotFoundError(
        "Netflix_Cleaned.xlsx file was not found in the outputs folder."
    )

df = pd.read_excel(file_path)

print("\n================================")
print("     NETFLIX COUNTRY ANALYSIS")
print("================================")


# ==========================================
# STEP 2: DATA VALIDATION
# ==========================================

print("\n===== DATA VALIDATION =====")

print("Total Records:", len(df))
print("Total Columns:", len(df.columns))

# Check required column
if "country" not in df.columns:
    raise ValueError("Country column is missing from the dataset.")

# Actual blank / NaN values
actual_missing = df["country"].isna().sum()

# Count placeholder values such as Not Given
country_text = df["country"].astype("string").str.strip()

placeholder_mask = (
    country_text.str.lower().isin(
        ["", "not given", "unknown", "nan", "none"]
    )
    & country_text.notna()
)

placeholder_count = placeholder_mask.sum()

print("Actual Missing Country Values:", actual_missing)
print("Not Given / Unknown Country Records:", placeholder_count)

print("\nSample Country Data:")
print(df["country"].head(10))


# ==========================================
# STEP 3: COUNTRY DATA CLEANING
# ==========================================

countries = df["country"].astype("string")

# Remove extra spaces
countries = countries.str.strip()

# Identify missing and placeholder values
missing_mask = (
    countries.isna() |
    countries.str.lower().isin(
        ["", "not given", "unknown", "nan", "none"]
    )
)

# Count records with unavailable country information
missing_count = int(missing_mask.sum())

# Remove missing country records
countries = countries[~missing_mask]

# Split multiple countries into separate entries
countries = countries.str.split(",")

# Convert multiple countries into separate rows
countries = countries.explode()

# Remove extra spaces again
countries = countries.str.strip()

# Remove empty values
countries = countries[
    countries.notna() &
    (countries != "")
]

if countries.empty:
    raise ValueError("No valid country data available for analysis.")

print("\n===== DATA CLEANING =====")

print("Records with Missing Country:", missing_count)
print("Valid Country Entries:", len(countries))
print("Unique Countries:", countries.nunique())


# ==========================================
# STEP 4: COUNTRY-WISE ANALYSIS
# ==========================================

country_counts = countries.value_counts()

print("\n===== TOP 10 COUNTRIES =====")

top_10 = country_counts.head(10)

print(top_10)


# ==========================================
# STEP 5: INDIA ANALYSIS
# ==========================================

print("\n===== INDIA ANALYSIS =====")

if "India" in country_counts.index:

    india_rank = country_counts.index.get_loc("India") + 1

    india_count = country_counts["India"]

    print("India Rank:", india_rank)
    print("India Content Count:", india_count)

else:

    india_rank = None
    india_count = 0

    print("India data not found in dataset.")


# ==========================================
# STEP 6: SAVE ANALYSIS RESULTS
# ==========================================

# Save Top 10 countries
top_10.to_csv(
    output_folder / "top_10_countries.csv",
    index_label="Country",
    header=["Content Count"]
)

# Save complete country analysis
country_counts.to_csv(
    output_folder / "all_countries_analysis.csv",
    index_label="Country",
    header=["Content Count"]
)

print("\nCSV Files Saved Successfully!")


# ==========================================
# STEP 7: CREATE BAR CHART
# ==========================================

plt.figure(figsize=(12, 6))

top_10.plot(
    kind="bar",
    edgecolor="black"
)

plt.title(
    "Top 10 Countries on Netflix",
    fontsize=16
)

plt.xlabel("Countries", fontsize=12)

plt.ylabel(
    "Number of Movies and TV Shows",
    fontsize=12
)

plt.xticks(rotation=45)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

# Save chart
plt.savefig(
    output_folder / "top_10_countries_chart.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# STEP 8: FINAL SUMMARY
# ==========================================

print("\n================================")
print("       FINAL ANALYSIS")
print("================================")

print("Total Netflix Records:", len(df))
print("Actual Missing Country Values:", actual_missing)
print("Not Given / Unknown Country Records:", placeholder_count)
print("Total Records with Missing Country:", missing_count)
print("Valid Country Entries:", len(countries))
print("Total Unique Countries:", countries.nunique())

if not country_counts.empty:

    print("Top Country:", country_counts.index[0])
    print("Top Country Content:", country_counts.iloc[0])

if india_rank is not None:

    print("India Rank:", india_rank)
    print("India Content:", india_count)

print("\nTASK 3 COMPLETED SUCCESSFULLY!")
print("CSV files and chart saved in the outputs folder.")
print("================================")