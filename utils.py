# utils.py
import os
import matplotlib.pyplot as plt
from scipy import stats

def calculate_correlation(array1, array2):
    correlation, p_value = stats.pearsonr(array1, array2)
    r_squared = correlation**2
    return correlation, r_squared, p_value

def save_and_show(filename: str, folder: str = "images"):
    """
    Saves the current matplotlib figure to the given folder (default: ./images/),
    then shows and closes the plot.
    """
    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, folder)
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()
    print(f"✅ Saved figure to: {os.path.abspath(filepath)}")
