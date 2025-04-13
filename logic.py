import pandas as pd
import json
import numpy as np
from scipy import stats

# === FILE I/O & NORMALIZATION ===

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return normalize_dataframe(df)

def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data["data"])
    return normalize_dataframe(df)

def save_csv(df, file_path):
    df.to_csv(file_path, index=True)
    print("CSV saved.")

def save_json(df, file_path):
    json_data = {
        "meta": {
            "source": "Exported from Statistical Analysis App",
            "columns": df.columns.tolist()
        },
        "data": df.to_dict(orient="records")
    }
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)
    print("JSON saved.")

def normalize_dataframe(df):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    return df

def split_tables(df, table_identifier="table"):
    if table_identifier in df.columns:
        return {tid: sub_df.reset_index(drop=True) for tid, sub_df in df.groupby(table_identifier)}
    return {"default": df.copy()}

def describe_data(df):
    return df.describe(include="all")

def correlation_matrix(df):
    return df.select_dtypes(include=[np.number]).corr()

def create_pivot_table(df, index, columns, values, aggfunc='mean'):
    return pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)

# === BASE GRAPH CLASS WITH AXIS CUSTOMIZATION ===

class BaseGraph:
    def __init__(self, df, column):
        self.df = df
        self.column = column
        self.data = None
        # Axis customization defaults; subclasses with axes can use these.
        self.x_label = None
        self.y_label = None
        self.x_range = None  # Tuple (min, max)
        self.y_range = None

    def prepare_data(self):
        raise NotImplementedError("Subclasses must implement prepare_data.")

    def set_x_label(self, label):
        self.x_label = label

    def set_y_label(self, label):
        self.y_label = label

    def set_x_range(self, min_val, max_val):
        self.x_range = (min_val, max_val)

    def set_y_range(self, min_val, max_val):
        self.y_range = (min_val, max_val)

    def get_default_axes(self):
        """
        Calculate default axes based on prepared data.
        If not overridden, returns None; subclasses should implement as needed.
        """
        return None

    def get_statistics(self):
        """
        Compute graph-specific statistics.
        Each subclass should override this.
        """
        return {}

# === GRAPH CLASSES ===

class BarChartGraph(BaseGraph):
    def prepare_data(self):
        counts = self.df[self.column].value_counts()
        self.data = {"categories": list(map(str, counts.index)),
                     "counts": counts.values.tolist()}
        return self.data

    def get_default_axes(self):
        if self.data:
            return {"x": {"labels": self.data["categories"]},
                    "y": {"min": 0, "max": max(self.data["counts"])}}
        return None

    def get_statistics(self):
        # Frequency distribution summary: mode and number of unique items.
        col_data = self.df[self.column].dropna()
        return {
            "unique": col_data.nunique(),
            "mode": col_data.mode().tolist() if not col_data.mode().empty else None
        }

class PieChartGraph(BaseGraph):
    def __init__(self, df, column):
        super().__init__(df, column)
        self.merge_map = None  # Example: { "vegetable": ["carrot", "potato"] }

    def set_merge_map(self, merge_map):
        self.merge_map = merge_map

    def prepare_data(self):
        counts = self.df[self.column].value_counts()
        data = {"labels": list(map(str, counts.index)),
                "values": counts.values.tolist()}
        if self.merge_map:
            merged = {}
            for label, value in zip(data["labels"], data["values"]):
                merged[label] = merged.get(label, 0) + value
            for new_label, group in self.merge_map.items():
                merged_value = sum(merged.pop(lbl, 0) for lbl in group)
                if merged_value > 0:
                    merged[new_label] = merged_value
            data = {"labels": list(merged.keys()), "values": list(merged.values())}
        self.data = data
        return self.data

    def get_statistics(self):
        # Return the proportion of each category
        if self.data:
            total = sum(self.data["values"])
            proportions = [val / total for val in self.data["values"]]
            return {"proportions": proportions}
        return {}

class HistogramGraph(BaseGraph):
    def __init__(self, df, column, bins=10, range_min=None, range_max=None):
        super().__init__(df, column)
        self.bins = bins
        self.range_min = range_min
        self.range_max = range_max

    def set_bins(self, bins):
        self.bins = bins

    def set_range(self, range_min, range_max):
        self.range_min = range_min
        self.range_max = range_max

    def prepare_data(self):
        values = self.df[self.column].dropna().values
        hrange = None
        if self.range_min is not None and self.range_max is not None:
            hrange = (self.range_min, self.range_max)
        counts, bin_edges = np.histogram(values, bins=self.bins, range=hrange)
        bins_labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
        self.data = {"bins": bins_labels, "counts": counts.tolist()}
        return self.data

    def get_default_axes(self):
        if self.data:
            # X-axis from first bin to last bin and y-axis from 0 to max count.
            # Attempt to convert bin labels to numeric ranges.
            try:
                first_bin = float(self.data["bins"][0].split('-')[0])
                last_bin = float(self.data["bins"][-1].split('-')[1])
            except Exception:
                first_bin, last_bin = 0, len(self.data["bins"])
            return {"x": {"min": first_bin, "max": last_bin},
                    "y": {"min": 0, "max": max(self.data["counts"])}}        
        return None

    def get_statistics(self):
        col = self.df[self.column].dropna()
        return {
            "mean": col.mean(),
            "median": col.median(),
            "std": col.std(),
            "skew": col.skew()
        }

class LineChartGraph(BaseGraph):
    def prepare_data(self):
        self.data = {"x": list(range(len(self.df[self.column]))),
                     "y": self.df[self.column].tolist()}
        return self.data

    def get_default_axes(self):
        if self.data:
            return {"x": {"min": min(self.data["x"]), "max": max(self.data["x"])},
                    "y": {"min": min(self.data["y"]), "max": max(self.data["y"])}}
        return None

    def get_statistics(self):
        y_series = self.df[self.column].dropna()
        reg = stats.linregress(range(len(y_series)), y_series)
        return {"slope": reg.slope, "intercept": reg.intercept, "r_value": reg.rvalue}

class ScatterChartGraph(BaseGraph):
    def prepare_data(self):
        self.data = {"x": list(range(len(self.df[self.column]))),
                     "y": self.df[self.column].tolist()}
        return self.data

    def get_default_axes(self):
        if self.data:
            return {"x": {"min": min(self.data["x"]), "max": max(self.data["x"])},
                    "y": {"min": min(self.data["y"]), "max": max(self.data["y"])}}
        return None

    def get_statistics(self):
        y_series = self.df[self.column].dropna()
        if len(y_series) > 1:
            reg = stats.linregress(range(len(y_series)), y_series)
            return {"slope": reg.slope, "r_value": reg.rvalue}
        return {}

class BoxPlotGraph(BaseGraph):
    def prepare_data(self):
        values = self.df[self.column].dropna().values
        if len(values) == 0:
            self.data = {}
        else:
            self.data = {
                "min": float(np.min(values)),
                "q1": float(np.percentile(values, 25)),
                "median": float(np.median(values)),
                "q3": float(np.percentile(values, 75)),
                "max": float(np.max(values))
            }
        return self.data

    def get_statistics(self):
        return self.data

class AreaChartGraph(BaseGraph):
    def prepare_data(self):
        x_vals = list(range(len(self.df[self.column])))
        self.data = {"x": x_vals,
                     "y": self.df[self.column].tolist(),
                     "baseline": [0] * len(x_vals)}
        return self.data

    def get_default_axes(self):
        if self.data:
            return {"x": {"min": min(self.data["x"]), "max": max(self.data["x"])},
                    "y": {"min": min(self.data["y"]), "max": max(self.data["y"])}}
        return None

    def get_statistics(self):
        y_series = self.df[self.column].dropna()
        return {"area": np.trapz(y_series, dx=1)}

class BubbleChartGraph:
    def __init__(self, df, x_column, y_column, size_column, size_scale=1.0):
        self.df = df
        self.x_column = x_column
        self.y_column = y_column
        self.size_column = size_column
        self.size_scale = size_scale
        self.data = None
        # Axis customization can be added if needed.
        self.x_label = None
        self.y_label = None
        self.x_range = None
        self.y_range = None

    def set_size_scale(self, scale):
        self.size_scale = scale

    def set_x_label(self, label):
        self.x_label = label

    def set_y_label(self, label):
        self.y_label = label

    def set_x_range(self, min_val, max_val):
        self.x_range = (min_val, max_val)

    def set_y_range(self, min_val, max_val):
        self.y_range = (min_val, max_val)

    def prepare_data(self):
        x = self.df[self.x_column].tolist()
        y = self.df[self.y_column].tolist()
        sizes = (self.df[self.size_column] * self.size_scale).tolist()
        self.data = {"x": x, "y": y, "sizes": sizes}
        return self.data

    def get_default_axes(self):
        if self.data:
            return {"x": {"min": min(self.data["x"]), "max": max(self.data["x"])},
                    "y": {"min": min(self.data["y"]), "max": max(self.data["y"])}}
        return None

    def get_statistics(self):
        # Simple correlation as an example.
        x_series = self.df[self.x_column].dropna()
        y_series = self.df[self.y_column].dropna()
        if len(x_series) > 1 and len(y_series) > 1:
            reg = stats.linregress(x_series, y_series)
            return {"slope": reg.slope, "r_value": reg.rvalue}
        return {}

# === Numeric Representation Utility ===

class NumericRepresentation:
    def __init__(self, df, column):
        self.df = df
        self.column = column
        self.data = None

    def prepare_data(self):
        if pd.api.types.is_numeric_dtype(self.df[self.column]):
            self.data = self.df[self.column].tolist()
        else:
            cats = list(self.df[self.column].unique())
            mapping = {cat: i for i, cat in enumerate(cats)}
            numeric_values = self.df[self.column].map(mapping).tolist()
            self.data = {"mapping": mapping, "numeric_values": numeric_values}
        return self.data

# === Axis Normalizer Utility ===

class AxisNormalizer:
    @staticmethod
    def normalize(series):
        min_val, max_val = series.min(), series.max()
        if min_val == max_val:
            return series - min_val
        return (series - min_val) / (max_val - min_val)

# === ADVANCED STATISTICAL FUNCTIONS ===

def perform_regression(x, y):
    return stats.linregress(x, y)

def compute_heatmap_data(df):
    return correlation_matrix(df)