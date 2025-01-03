# EDA Application

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """Load dataset from the given file path."""
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def inspect_data(data):
    """Prints basic information about the dataset."""
    print("\n--- Dataset Info ---")
    print(data.info())
    print("\n--- First 5 Rows ---")
    print(data.head())
    print("\n--- Summary Statistics ---")
    print(data.describe())

def clean_data(data):
    """Handle missing values and clean the dataset."""
    print("\n--- Handling Missing Values ---")
    missing_values = data.isnull().sum()
    print(missing_values[missing_values > 0])
    # Example: Fill numeric columns with mean and categorical with mode
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col].fillna(data[col].mode()[0], inplace=True)
        else:
            data[col].fillna(data[col].mean(), inplace=True)
    print("\nMissing values handled.")
    return data

def visualize_data(data):
    """Create visualizations for EDA."""
    print("\n--- Creating Visualizations ---")
    # Plot distributions of numeric columns
    numeric_cols = data.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(data[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.show()

    # Heatmap of correlations
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

def find_insights(data):
    """Extract simple insights from the dataset."""
    print("\n--- Insights ---")
    # Example: Correlation insights
    correlations = data.corr()
    high_corr = correlations.unstack().sort_values(ascending=False)
    print("Top Correlations:\n", high_corr[high_corr < 1.0].head(10))

def main():
    """Main function to run the EDA application."""
    file_path = input("Enter the dataset file path: ")
    data = load_data(file_path)
    if data is not None:
        inspect_data(data)
        data = clean_data(data)
        visualize_data(data)
        find_insights(data)
    else:
        print("Failed to load the dataset.")

if __name__ == "__main__":
    main()
