from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# Define the unitary operation U
def apply_unitary_U(qc, p, q):
    """
    Apply the unitary operation U to the quantum circuit.
    Args:
        qc (QuantumCircuit): The quantum circuit to which U is applied.
        p (float): Probability of emitting '0' from state A.
        q (float): Probability of emitting '0' from state B.
    """
    # Define angles based on probabilities
    theta_A = 2 * np.arccos(np.sqrt(p))
    theta_B = 2 * np.arccos(np.sqrt(q))

    # Apply controlled rotations based on the defined angles
    qc.cry(theta_A, 0, 1)  # Controlled-RY gate with angle theta_A
    qc.cx(0, 1)            # CNOT gate
    qc.cry(theta_B, 0, 1)  # Controlled-RY gate with angle theta_B
    qc.cx(0, 1)            # CNOT gate

# Function to calculate classical complexity C_mu
def classical_complexity(p, q):
    """Calculate classical statistical complexity (C_mu)."""
    if p == q:
        return 0  # Biased coin has no statistical complexity
    pi_A = 1 / (1 + p)  # Stationary probability for state A
    pi_B = p / (1 + p)  # Stationary probability for state B
    return -pi_A * np.log2(pi_A) - pi_B * np.log2(pi_B)

# Define parameters
q_fixed = 0.8  # Fixed q value for the plot
p_values = np.linspace(0.1, 1.0, 50)  # Range of p values for the plot

# Compute classical complexity for each p
C_mu_values = [classical_complexity(p, q_fixed) for p in p_values]

# Plot classical complexity
plt.figure(figsize=(8, 5))
plt.plot(p_values, C_mu_values, label=r"$C_\mu$ (Classical Complexity)", color="red")
plt.xlabel("p")
plt.ylabel("Classical Complexity ($C_\mu$)")
plt.title(r"Classical Complexity ($C_\mu$) vs $p$ for $q = 0.7$")
plt.legend()
plt.grid()
plt.show()
