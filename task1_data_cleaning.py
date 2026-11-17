import pandas as pd
from pathlib import Path

# -----------------------------------------
# STEP 1: LOAD NETFLIX DATASET
# -----------------------------------------

file_path = "data/Dataset.xlsx"

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")

print("\nFirst 5 Rows:")
print(df.head())

print("\nOriginal Dataset Shape:")
print(df.shape)


# -----------------------------------------
# STEP 2: CHECK MISSING VALUES
# -----------------------------------------

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Records Before Cleaning:")
print(df.duplicated().sum())


# -----------------------------------------
# STEP 3: CLEAN TEXT COLUMNS
# -----------------------------------------

text_columns = [
    "type",
    "title",
    "director",
    "country",
    "rating",
    "duration",
    "listed_in"
]

for column in text_columns:

    # Convert text columns into string format
    df[column] = df[column].astype("string")

    # Remove extra spaces
    df[column] = df[column].str.strip()

    # Replace blank strings with missing values
    df[column] = df[column].replace("", pd.NA)


# -----------------------------------------
# STEP 4: HANDLE MISSING VALUES
# -----------------------------------------

# Fill missing titles with a placeholder
df["title"] = df["title"].fillna("Unknown Title")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())


# -----------------------------------------
# STEP 5: REMOVE DUPLICATE RECORDS
# -----------------------------------------

duplicates_removed = df.duplicated().sum()

df = df.drop_duplicates()

print("\nDuplicate Records Removed:")
print(duplicates_removed)


# -----------------------------------------
# STEP 6: STANDARDIZE TYPE COLUMN
# -----------------------------------------

type_mapping = {
    "movie": "Movie",
    "tv show": "TV Show"
}

standardized_type = df["type"].str.casefold().map(type_mapping)

df["type"] = standardized_type.fillna(df["type"])


# -----------------------------------------
# STEP 7: STANDARDIZE COUNTRY COLUMN
# -----------------------------------------

# Remove extra spaces and normalize spacing
df["country"] = df["country"].str.replace(
    r"\s+", " ", regex=True
)


# -----------------------------------------
# STEP 8: STANDARDIZE RATING COLUMN
# -----------------------------------------

df["rating"] = df["rating"].str.upper()


# -----------------------------------------
# STEP 9: FINAL DATA VERIFICATION
# -----------------------------------------

print("\nData Cleaning and Standardization Completed!")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Duplicate Records:")
print(df.duplicated().sum())

print("\nFinal Type Values:")
print(df["type"].unique())

print("\nFinal Rating Values:")
print(df["rating"].unique())


# -----------------------------------------
# STEP 10: EXPORT CLEANED DATASET
# -----------------------------------------

output_folder = Path("outputs")

# Create output folder if it does not exist
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "Netflix_Cleaned.xlsx"

# Export cleaned dataset to Excel
df.to_excel(output_file, index=False)

print("\nCleaned dataset exported successfully!")
print("File Location:", output_file)
print("Total Records Exported:", len(df))