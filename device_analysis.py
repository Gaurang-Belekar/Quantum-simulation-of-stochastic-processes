import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

calibration_file_path = 'ibm_brisbane_calibrations_2025-01-26T11_11_11Z.csv'
calibration_data = pd.read_csv(calibration_file_path)
# --- Bar Chart: Single-Qubit Gate Errors ---
plt.figure(figsize=(20, 8))
if '√x (sx) error ' in calibration_data.columns:
    sns.barplot(x='Qubit', y='√x (sx) error ', data=calibration_data)
    plt.title("Single-Qubit Gate Errors", fontsize=14)
    plt.xlabel("Qubit", fontsize=12)
    plt.ylabel("Error Rate", fontsize=12)
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- Bar Chart: Measurement Errors ---
plt.figure(figsize=(20, 8))
if 'Readout assignment error ' in calibration_data.columns:
    sns.barplot(x='Qubit', y='Readout assignment error ', data=calibration_data)
    plt.title("Measurement Errors per Qubit", fontsize=14)
    plt.xlabel("Qubit", fontsize=12)
    plt.ylabel("Error Rate", fontsize=12)
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- Histogram: T1 and T2 Coherence Times ---
if 'T1 (us)' in calibration_data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(calibration_data['T1 (us)'], bins=15, kde=True, color='blue', label='$T_1$ Time')
    plt.title("$T_1$ Coherence Time Distribution", fontsize=14)
    plt.xlabel("$T_1$ Time (us)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

if 'T2 (us)' in calibration_data.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(calibration_data['T2 (us)'], bins=15, kde=True, color='green', label='$T_2$ Time')
    plt.title("$T_2$ Coherence Time Distribution", fontsize=14)
    plt.xlabel("$T_2$ Time (us)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()


# --- Grouped Bar Chart: Simulator vs. Hardware Results ---
# Mocking up grouped data for now (replace with actual values if available)
simulator_probs = {'1111': 0.4, '1011': 0.1, '0111': 0.15, '1110': 0.1}
hardware_probs = {'1111': 0.25, '1011': 0.12, '0111': 0.12, '1110': 0.08}

words = list(simulator_probs.keys())
sim_probs = [simulator_probs[word] for word in words]
hw_probs = [hardware_probs[word] for word in words]

x = range(len(words))
plt.figure(figsize=(10, 6))
plt.bar(x, sim_probs, width=0.4, label="Simulator", align='center')
plt.bar([i + 0.4 for i in x], hw_probs, width=0.4, label="Hardware", align='center')
plt.xticks([i + 0.2 for i in x], words)
plt.title("Simulator vs. Hardware: 4-symbol Probabilities", fontsize=14)
plt.xlabel("4-symbol Words", fontsize=12)
plt.ylabel("Probability", fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("Available Columns in Calibration Data:")
print(calibration_data.columns)

print("\nSample Data:")
print(calibration_data.head())