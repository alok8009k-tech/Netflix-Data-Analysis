import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Load cleaned dataset
file_path = "outputs/Netflix_Cleaned.xlsx"
df = pd.read_excel(file_path)

print("Dataset loaded successfully!")

# Check required column
if "type" not in df.columns:
    raise ValueError("The dataset does not contain the required 'type' column.")

# Count Movies and TV Shows
content_counts = df["type"].value_counts()

if content_counts.empty:
    raise ValueError("No content type data is available for analysis.")

print("\nContent Type Count:")
print(content_counts)

# Calculate percentage
content_percentage = (content_counts / content_counts.sum()) * 100

print("\nContent Type Percentage:")
print(content_percentage.round(2))

# Summarize key findings
most_common_type = content_counts.idxmax()
most_common_count = int(content_counts.max())
most_common_percentage = float(content_percentage.loc[most_common_type])

movie_count = int(content_counts.get("Movie", 0))
tv_show_count = int(content_counts.get("TV Show", 0))

count_difference = abs(movie_count - tv_show_count)
total_content = int(content_counts.sum())

summary = (
    "NETFLIX CONTENT TYPE ANALYSIS - KEY FINDINGS\n"
    "============================================\n"
    f"Total content records analyzed: {total_content}\n"
    f"Movies: {movie_count} ({content_percentage.get('Movie', 0):.2f}%)\n"
    f"TV Shows: {tv_show_count} ({content_percentage.get('TV Show', 0):.2f}%)\n"
    f"Most common content type: {most_common_type} "
    f"({most_common_count} titles, {most_common_percentage:.2f}%)\n"
    f"Difference between Movies and TV Shows: {count_difference} titles\n"
)

print("\n" + summary)

# Save key findings
with open("outputs/content_type_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

# Bar Chart
plt.figure(figsize=(8, 5))

content_counts.plot(kind="bar")

plt.title("Netflix Movies vs TV Shows")
plt.xlabel("Content Type")
plt.ylabel("Total Count")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("outputs/content_type_bar_chart.png")
plt.show()
plt.close()

# Pie Chart
plt.figure(figsize=(7, 7))

content_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Netflix Content Type Distribution")
plt.ylabel("")

plt.tight_layout()
plt.savefig("outputs/content_type_pie_chart.png")
plt.show()
plt.close()

print("\nTask 2 completed successfully!")
print("Charts and summary saved in the outputs folder.")