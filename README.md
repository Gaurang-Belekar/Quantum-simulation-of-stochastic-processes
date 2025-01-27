# ***Statistical complexity and quantum simulation of stochastic processes***

## **Overview**
This project explores the simulation and analysis of stochastic processes, focusing on **classical** and **quantum complexity**. It includes implementations for the **Upset-Gambler process**, a non-Markovian system, and demonstrates how quantum systems can efficiently model such processes. Two distinct simulation methods are implemented for running the Upset-Gambler process:  
1. Encoding outputs onto **four separate registers** and measuring all at once.  
2. Using a **single register** with repeated measurement and resetting after each step.

Key objectives:
- Compare **classical complexity** ($C_\mu$) and **quantum complexity** ($C_q$) for stochastic processes.
- Simulate processes using **Qiskit** and analyze results from both simulators and quantum hardware.
- Study **hardware calibration data** to understand its impact on quantum performance.

---

## **Features**
- Classical and quantum complexity calculation for stochastic processes.
- Two simulation methods for the Upset-Gambler process:
  - **Method 1**: Outputs encoded onto **4 separate registers**.
  - **Method 2**: Outputs generated via **single register resetting**.
- Hardware execution of quantum circuits on **IBM Quantum devices**.
- Calibration data analysis, including **coherence times**, **gate errors**, and **measurement errors**.

---
## Directory Structure

```
stochastic-process-simulation/
├── complexity_analysis.py             # Classical and quantum complexity analysis
├── device_analysis.py                 # Analysis of IBM Quantum hardware calibration data
├── ibm_brisbane_calibrations_2025...  # Calibration data (CSV file)
├── m1_upset_gambler_simulator.py      # Method 1: Upset-Gambler simulation (Simulator)
├── m1_upset_gambler_QPU.py            # Method 1: Upset-Gambler simulation (Quantum Hardware)
├── m2_upset_gambler_simulator.py      # Method 2: Upset-Gambler simulation (Simulator)
├── m2_upset_gambler_QPU.py            # Method 2: Upset-Gambler simulation (Quantum Hardware)
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```
---

## **Simulation Methods**
### **Method 1: Multiple Registers**
- Outputs are encoded into **four separate registers**, representing four output symbols of the process.
- All registers are measured at the end of the circuit.
- **Advantage**: Provides a clean mapping of all symbols simultaneously.  
- **Example**: Circuit creates and measures outputs like $[x_1, x_2, x_3, x_4]$.

### **Method 2: Single Register**
- A single register is **measured and reset repeatedly** to produce each output symbol sequentially.
- **Advantage**: Reduces hardware qubit usage, making it efficient for noisy or limited devices.  
- **Example**: Sequential generation of $[x_1], [x_2], [x_3], [x_4]$ over time.

---

## **Getting Started**

### **Prerequisites**
- Python 3.9+
- Libraries:
  - `qiskit`, `qiskit_aer`, `qiskit_ibm_runtime`
  - `matplotlib`, `numpy`, `pandas`, `seaborn`
- Access to **IBM Quantum**:
  - Create an account at [IBM Quantum](https://quantum-computing.ibm.com/).
  - Retrieve your API token and set it up in Qiskit.

### **Installation**
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Gaurang-Belekar/Quantum-simulation-of-stochastic-processes.git
cd  Quantum-simulation-of-stochastic-processes
pip install -r requirements.txt
```
---
### Usage

1. Classical and Quantum Complexity Analysis

Run the script to compute and plot classical and quantum complexities for the Upset-Gambler process:

```bash
python complexity_analysis.py
```

2. Simulating the Upset-Gambler Process

Method 1 (Four Registers - Simulator):

```bash
python m1_upset_gambler_simulator.py
```

Method 2 (Single Register - Simulator):

```bash
python m2_upset_gambler_simulator.py
```

3. Running on IBM Quantum Hardware

Method 1 (Four Registers - Hardware):

```bash
python m1_upset_gambler_QPU.py
```
Method 2 (Single Register - Hardware):

```bash
python m2_upset_gambler_QPU.py
```

4. Hardware Calibration Data Analysis

Analyze IBM Quantum hardware calibration data for coherence times, gate errors, and other metrics:

```bash
python device_analysis.py
```


### ***Note: Please add your IBM ACCESS TOKEN in the m1 and m2 QPU files to run it on actual hardware***

---
## Results

***Simulation Insights:***
- Both methods successfully simulate the process, but Method 2 (single register) is more hardware-efficient.
- Classical vs Quantum Complexity: Quantum systems ($C_q$) are more memory-efficient compared to classical systems ($C_\mu$).

***Hardware Observations:***
- Noise and decoherence affect the fidelity of the quantum hardware results.
- Hardware calibration data highlights coherence times and error rates that influence performance.

---
### Contributing

Contributions are welcome! Please follow these steps:
1.	Fork the repository.
2.	Create a feature branch:

```bash
git checkout -b feature-name
```

3.	Commit changes and open a pull request.

---
## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
## Reference
    [1] Felix C. Binder, Jayne Thompson and Mile Gu, Phys. Rev. Lett. 120, 240502 (2018)
    [2] Farrokh Vatan and Colin Williams, Phys. Rev. A 69, 032315 (2004)
    [3] Thomas J. Elliott, Chengran Yang, Felix C. Binder, Andrew J. P. Garner, Jayne Thompson and Mile Gu, Phys. Rev. Lett. 125, 260501 (2020).

