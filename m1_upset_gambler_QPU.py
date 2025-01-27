from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer, AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler 

# Define the upset-gambler process parameters
p = 0.2  # Probability of emitting '0' from state A
q = 0.7  # Probability of emitting '0' from state B

# Define transition probabilities for the process
# Transition from current state (A or B) based on emitted symbol
def transition(current_state, symbol):
    if current_state == 'A':
        return 'B' if symbol == 0 else 'A'
    elif current_state == 'B':
        return 'A'  # Always transitions to A

# Create a quantum circuit with 4 qubits
num_registers = 4
qc = QuantumCircuit(num_registers, num_registers)  # 4 qubits, 4 classical bits for measurement

# Define angles for the RY gates based on the probabilities
angles = {
    'A': 2 * np.arccos(np.sqrt(p)),  # Rotation for state A
    'B': 2 * np.arccos(np.sqrt(q))   # Rotation for state B
}

# Initialize the system in state |A> (state A corresponds to qubit initialized to |0>)
current_state = 'A'

# Apply the circuit for each of the 4 registers
for i in range(num_registers):
    # Apply RY gate based on the current state
    qc.ry(angles[current_state], i)

    # Simulate symbol emission by randomly sampling based on the probability
    emitted_symbol = np.random.choice([0, 1], p=[p if current_state == 'A' else q, 1 - (p if current_state == 'A' else q)])

    # Transition to the next state based on the emitted symbol
    current_state = transition(current_state, emitted_symbol)

# Measure all qubits
qc.measure(range(num_registers), range(num_registers))

service = QiskitRuntimeService()
backend = service.least_busy(
    operational=True, simulator=False, min_num_qubits=127
)
 
print(backend.name)
 
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(compiled_circuit)
print(f">>> Circuit ops (ISA): {isa_circuit.count_ops()}")
sampler = Sampler(mode=backend)
job = sampler.run([(isa_circuit)])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='****' # Enter your IBM Access token
)
job = service.job('****') # Enter your Sessions token
job_result = job.result()

counts = job_result[0].data.c.get_counts()
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
