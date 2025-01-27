from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import matplotlib.pyplot as plt
import numpy as np

# Define the upset-gambler process parameters
p = 0.2  # Probability of emitting '0' from state A
q = 0.7  # Probability of emitting '0' from state B

# Define transition probabilities for the process
def transition(current_state, symbol):
    if current_state == 'A':
        return 'B' if symbol == 0 else 'A'
    elif current_state == 'B':
        return 'A'

# Define angles for the RY gates based on the probabilities
angles = {
    'A': 2 * np.arccos(np.sqrt(p)),  # Rotation for state A
    'B': 2 * np.arccos(np.sqrt(q))   # Rotation for state B
}

# Simulate the circuit for multiple shots to gather statistics
num_shots = 100
counts = {}

# Initialize Qiskit Runtime Service
service = QiskitRuntimeService(channel='ibm_quantum', instance='ibm-q/open/main', token='***') # Enter your IBM Access token
# Select the least busy backend
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
print(f"Backend selected: {backend.name}")

# Function to create a single circuit for 4-symbol word generation
def create_circuit(initial_state):
    current_state = initial_state
    qc = QuantumCircuit(1, 1)  # Single qubit and single classical bit
    for _ in range(4):
        # Apply RY gate based on the current state
        qc.ry(angles[current_state], 0)
        # Measure the qubit
        qc.measure(0, 0)
        # Reset the qubit for the next iteration
        qc.reset(0)
        # Transition logic handled dynamically during measurement
    return qc

# Generate and compile the circuit
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)

with Session(backend=backend) as session:

    for _ in range(num_shots):
        current_state = 'A'
        output_symbols = []
        qc = create_circuit(current_state)

        compiled_circuit = pm.run(qc)

        # Submit job for a single shot using a session
    
        sampler = Sampler(mode=session)
        job = sampler.run([compiled_circuit])
        print(f"Job ID: {job.job_id()}")

        # Wait for the job to complete and retrieve the result
        pub_result = job.result()[0]
        pub_counts = pub_result.data.c.get_counts()

        # Process counts to extract the measured symbol
        measured_symbol = int(list(pub_counts.keys())[0])
        output_symbols.append(measured_symbol)

        # Transition to the next state based on the emitted symbol
        current_state = transition(current_state, measured_symbol)

    # Join the emitted symbols to form a 4-symbol word
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
plt.title('4-symbol Word Probabilities from Hardware Execution', fontsize=16)
plt.xticks(rotation=90, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Show plot
plt.show()
