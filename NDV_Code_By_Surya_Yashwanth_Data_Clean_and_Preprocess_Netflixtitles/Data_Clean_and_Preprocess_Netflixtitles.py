import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Import kagglehub for direct dataset download
import kagglehub
import os # To help navigate the downloaded path

# --- 1. Load the Dataset ---

kaggle_dataset_id = "padmapriyatr/netflix-titles" # The ID of the Kaggle dataset
csv_filename_in_dataset = "netflix_titles.csv" # The specific CSV file name within the downloaded dataset

try:
    print(f"Attempting to download dataset: {kaggle_dataset_id}...")
    # Download the latest version of the dataset
    download_path = kagglehub.dataset_download(kaggle_dataset_id)
    print(f"Dataset downloaded to: {download_path}")

    # Construct the full path to the CSV file within the downloaded directory
    full_csv_path = os.path.join(download_path, csv_filename_in_dataset)

    if os.path.exists(full_csv_path):
        df = pd.read_csv(full_csv_path)
        print(f"Dataset '{csv_filename_in_dataset}' loaded successfully from downloaded files.")
    else:
        raise FileNotFoundError(f"'{csv_filename_in_dataset}' not found within the downloaded dataset at {download_path}.")

except Exception as e:
    print(f"Error loading dataset from KaggleHub: {e}")
    print("Creating a dummy dataset for demonstration purposes to allow the script to run.")
    # Create a dummy DataFrame for demonstration if the file is not found or download fails
    data = {
        'show_id': ['s1', 's2', 's3', 's4', 's5'],
        'type': ['Movie', 'TV Show', 'Movie', 'Movie', 'TV Show'],
        'title': ['The Grand Heist', 'Stranger Things', 'Bird Box', 'Extraction', 'The Crown'],
        'director': ['Kim Joo-ho', 'The Duffer Brothers', 'Susanne Bier', 'Sam Hargrave', np.nan],
        'cast': ['Kim Yoon-seok, Kim Hye-soo', 'Millie Bobby Brown, Finn Wolfhard', 'Sandra Bullock, Trevante Rhodes', 'Chris Hemsworth, Rudhraksh Jaiswal', 'Claire Foy, Matt Smith'],
        'country': ['South Korea', 'United States', 'United States', 'India', np.nan],
        'date_added': ['September 1, 2021', 'July 15, 2016', 'December 13, 2018', 'April 24, 2020', 'November 4, 2016'],
        'release_year': [2012, 2016, 2018, 2020, 2016],
        'rating': ['TV-14', 'TV-MA', 'R', 'TV-MA', 'TV-MA'],
        'duration': ['135 min', '4 Seasons', '124 min', '117 min', '5 Seasons'],
        'listed_in': ['Comedies, Dramas', 'Sci-Fi & Fantasy, Teen TV Shows', 'Dramas, Sci-Fi & Fantasy', 'Action & Adventure', 'British TV Shows, Dramas'],
        'description': ['A team of thieves...', 'When a young boy vanishes...', 'A woman and her children...', 'A black-market mercenary...', 'Follows the political rivalries...']
    }
    df = pd.DataFrame(data)


print("\n--- Initial Data Info ---")
df.info()

# --- 2. Inspect the Data ---
print("\n--- Missing Values Count ---")
print(df.isnull().sum())

print("\n--- Duplicate Rows Count ---")
print(f"Number of duplicate rows: {df.duplicated().sum()}")

# --- 3. Perform Necessary Data Cleaning Steps ---

# 3.1. Handle Missing Values
# Fill 'director', 'cast', 'country' with 'Unknown'
for col in ['director', 'cast', 'country']:
    df[col].fillna('Unknown', inplace=True)

# Fill 'rating' with the mode (most frequent rating)
df['rating'].fillna(df['rating'].mode()[0], inplace=True)

# Drop rows where 'date_added' is missing, as it's crucial for time-based analysis
# If you prefer to fill, consider using a placeholder like 'January 1, 1900'
df.dropna(subset=['date_added'], inplace=True)

# 3.2. Remove Duplicate Records
df.drop_duplicates(inplace=True)
print(f"\nNumber of rows after removing duplicates: {len(df)}")


# 3.3. Convert Data Types
# Convert 'date_added' to datetime objects
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Handle 'duration' column: convert to numerical minutes for movies and numerical seasons for TV shows
df['duration_minutes'] = np.nan
df['duration_seasons'] = np.nan

# --- FIX for SyntaxWarning: invalid escape sequence '\d' ---
# Changed '(\d+)' to r'(\d+)' to use a raw string for regex
movie_mask = df['type'] == 'Movie'
df.loc[movie_mask, 'duration_minutes'] = df.loc[movie_mask, 'duration'].str.extract(r'(\d+)').astype(float)

# --- FIX for SyntaxWarning: invalid escape sequence '\d' ---
# Changed '(\d+)' to r'(\d+)' to use a raw string for regex
tv_show_mask = df['type'] == 'TV Show'
df.loc[tv_show_mask, 'duration_seasons'] = df.loc[tv_show_mask, 'duration'].str.extract(r'(\d+)').astype(float)

# Drop the original 'duration' column as it's now split
df.drop('duration', axis=1, inplace=True)

# Convert 'release_year' to integer type if it's not already
df['release_year'] = df['release_year'].astype(int)

print("\n--- Data Info After Cleaning ---")
df.info()

# --- 4. Use NumPy for any required numerical transformations or calculations ---
# Calculate the age of the content (years since release)
current_year = pd.Timestamp.now().year
df['content_age'] = current_year - df['release_year']
print(f"\nCalculated 'content_age' using NumPy: {df['content_age'].head()}")

# Example of another NumPy operation: log transform (if applicable, e.g., for skewed numerical data)
# For demonstration, let's apply it to 'content_age' (though it might not be ideal for this specific column)
# df['content_age_log'] = np.log1p(df['content_age']) # log1p handles zero values

# --- 5. Use Pandas for Filtering, Sorting, and Grouping Data ---

# 5.1. Filtering Data
# Filter movies released after 2018
movies_after_2018 = df[(df['type'] == 'Movie') & (df['release_year'] > 2018)]
print(f"\n--- Movies released after 2018 ({len(movies_after_2018)} entries) ---")
print(movies_after_2018[['title', 'release_year', 'type']].head())

# 5.2. Sorting Data
# Sort data by 'release_year' in descending order and then by 'title'
df_sorted = df.sort_values(by=['release_year', 'title'], ascending=[False, True])
print("\n--- Top 5 entries sorted by release_year (desc) and title (asc) ---")
print(df_sorted[['title', 'release_year']].head())

# 5.3. Grouping Data
# Group by 'type' and count the number of entries
content_counts = df.groupby('type').size().reset_index(name='count')
print("\n--- Content type distribution ---")
print(content_counts)

# Group by 'country' and find the average content age
avg_age_by_country = df.groupby('country')['content_age'].mean().sort_values(ascending=False)
print("\n--- Top 5 countries by average content age ---")
print(avg_age_by_country.head())


# --- 6. Provide Summary Statistics and Visual Insights ---

print("\n--- Summary Statistics for Numerical Fields ---")
print(df.describe())

print("\n--- Value Counts for Key Categorical Fields ---")
print("\nType:\n", df['type'].value_counts())
print("\nRating:\n", df['rating'].value_counts().head())
print("\nTop 5 Countries:\n", df['country'].value_counts().head())
print("\nTop 5 Directors:\n", df['director'].value_counts().head())


# --- 7. Visualize Null Value Distributions Using Heatmaps ---
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap After Cleaning')
plt.show()
print("\nNote: The heatmap should now show very few or no missing values, indicating successful cleaning.")

# --- 8. Create a Correlation Matrix of Numerical Fields ---
# Select only numerical columns for correlation matrix
numerical_df = df.select_dtypes(include=[np.number])

# Drop columns that are entirely NaN after type conversion (e.g., duration_minutes for TV Shows)
numerical_df = numerical_df.dropna(axis=1, how='all')

if not numerical_df.empty and len(numerical_df.columns) > 1:
    plt.figure(figsize=(10, 8))
    sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Numerical Fields')
    plt.show()
else:
    print("\nNot enough numerical columns to create a meaningful correlation matrix.")
    print("Numerical columns found:", numerical_df.columns.tolist())


# --- 9. Apply Label Encoding or Other Preprocessing for ML-Readiness ---
# For demonstration, let's encode 'type', 'rating', and 'country'
categorical_cols_for_encoding = ['type', 'rating', 'country']
df_encoded = df.copy() # Create a copy to store encoded data

for col in categorical_cols_for_encoding:
    le = LabelEncoder()
    # Check if the column exists and has values before encoding
    if col in df_encoded.columns and not df_encoded[col].isnull().all():
        df_encoded[f'{col}_encoded'] = le.fit_transform(df_encoded[col])
        print(f"\nLabel Encoding for '{col}':")
        # Display mapping (optional)
        for i, item in enumerate(le.classes_):
            print(f"  {item} -> {i}")
    else:
        print(f"\nSkipping encoding for '{col}' as it's missing or empty.")


print("\n--- First 5 rows of DataFrame with Encoded Columns ---")
print(df_encoded[['title', 'type', 'type_encoded', 'rating', 'rating_encoded', 'country', 'country_encoded']].head())

print("\nData preprocessing and analysis complete!")

# --- Optional: Display and Save Cleaned Data ---
print("\n--- First 5 rows of the Cleaned DataFrame (after all transformations) ---")
print(df.head())

# Save the cleaned DataFrame to a new CSV file
output_filename = 'netflix_titles_cleaned.csv'
df.to_csv(output_filename, index=False)
print(f"\nCleaned data saved to '{output_filename}'")
