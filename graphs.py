import matplotlib.pyplot as plt

# Updated glassmorphism-inspired style for charts:
plt.rcdefaults()  # Reset to default settings
plt.rcParams.update({
    'axes.facecolor': (0.2, 0.2, 0.2, 0.3),      # Dark, semi-transparent axes background
    'figure.facecolor': (0.2, 0.2, 0.2, 0.0),    # Transparent figure background
    'savefig.facecolor': (0.2, 0.2, 0.2, 0.0),
    'axes.edgecolor': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'text.color': 'white',
    'grid.color': (1, 1, 1, 0.2),                # Light grid with low opacity
    'grid.linestyle': '--',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial']
})


def create_empty_figure():
    """Return an empty matplotlib figure."""
    return plt.figure()

def plot_bar_chart(df, column):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df[column].value_counts().plot(kind="bar", ax=ax, title=f"Bar Chart of {column}")
    return fig

def plot_pie_chart(df, column):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df[column].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax, title=f"Pie Chart of {column}")
    return fig

def plot_histogram(df, column):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df[column].plot(kind="hist", ax=ax, title=f"Histogram of {column}")
    return fig

def plot_line_chart(df, column):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df[column].plot(kind="line", ax=ax, title=f"Line Chart of {column}")
    return fig

def plot_scatter_plot(df, column):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(df.index, df[column])
    ax.set_xlabel("Index")
    ax.set_ylabel(column)
    ax.set_title(f"Scatter Plot of {column}")
    return fig
