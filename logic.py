import pandas as pd
import json

def load_csv(file_path):
    """Load CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def load_json(file_path):
    """Load JSON file into a DataFrame. Expecting a structure with 'meta' and 'data'."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data["data"])

def save_csv(df, file_path):
    """Save a DataFrame to CSV."""
    df.to_csv(file_path, index=True)
    print(df)

def save_json(df, file_path):
    """Save a DataFrame to JSON with meta data."""
    json_data = {
        "meta": {
            "source": "Exported from Statistical Analysis App",
            "columns": df.columns.tolist()
        },
        "data": df.to_dict(orient="records")
    }
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)

def group_data(df, by_column):
    """Group the data by a specified column and return aggregated means."""
    return df.groupby(by_column).mean()

def filter_data(df, column, value):
    """Filter rows in the DataFrame where the specified column equals the given value."""
    return df[df[column] == value]
