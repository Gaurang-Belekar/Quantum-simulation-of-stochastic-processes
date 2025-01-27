from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer, AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# Define the upset-gambler process parameters
p = 0.2  # Probability of emitting '0' from state A
q = 0.7  # Probability of emitting '0' from state B

# Define transition probabilities for the process
def transition(current_state, symbol):
    if current_state == 'A':
        return 'B' if symbol == 0 else 'A'
    elif current_state == 'B':
        return 'A'

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)  # Single qubit and single classical bit for measurement

# Define angles for the RY gates based on the probabilities
angles = {
    'A': 2 * np.arccos(np.sqrt(p)),  # Rotation for state A
    'B': 2 * np.arccos(np.sqrt(q))   # Rotation for state B
}

# Initialize the system in state |A> (state A corresponds to qubit initialized to |0>)
current_state = 'A'
output_symbols = []

# Apply the circuit for 4 output symbols
for _ in range(4):
    # Apply RY gate based on the current state
    qc.ry(angles[current_state], 0)

    # Measure the qubit
    qc.measure(0, 0)

    # Simulate the circuit to determine the emitted symbol
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1).result()
    measured_symbol = int(list(result.get_counts(qc).keys())[0])

    # Record the emitted symbol
    output_symbols.append(measured_symbol)

    # Transition to the next state based on the emitted symbol
    current_state = transition(current_state, measured_symbol)

    # Reset the qubit
    qc.reset(0)

# Join the emitted symbols to form a 4-symbol word
word = ''.join(map(str, output_symbols))
print(f"Generated 4-symbol word: {word}")

# Simulate the circuit for multiple shots to gather statistics
num_shots = 1000
counts = {}
for _ in range(num_shots):
    current_state = 'A'
    qc = QuantumCircuit(1, 1)
    output_symbols = []

    for _ in range(4):
        qc.ry(angles[current_state], 0)
        qc.measure(0, 0)
        simulator = AerSimulator()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1).result()
        measured_symbol = int(list(result.get_counts(qc).keys())[0])
        output_symbols.append(measured_symbol)
        current_state = transition(current_state, measured_symbol)
        qc.reset(0)

    word = ''.join(map(str, output_symbols))
    counts[word] = counts.get(word, 0) + 1

# Normalize probabilities
total_counts = sum(counts.values())
binary_labels = list(counts.keys())
probabilities = [counts[label] / total_counts for label in binary_labels]

# Sort the labels and probabilities in ascending binary order
sorted_indices = np.argsort(binary_labels)
binary_labels = np.array(binary_labels)[sorted_indices]
probabilities = np.array(probabilities)[sorted_indices]

# Plot the sorted probabilities
plt.figure(figsize=(8, 6))
plt.bar(binary_labels, probabilities)

plt.xlabel('4-symbol words', fontsize=14)
plt.ylabel('Probability', fontsize=14)
plt.title('4-symbol Word Probabilities (p=0.2, q=0.7)', fontsize=16)
plt.xticks(rotation=90, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Show plot
plt.show()
