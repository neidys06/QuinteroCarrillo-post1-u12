import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def bell_state_experiment(shots=1024):
    os.makedirs('capturas', exist_ok=True)
    
    # 2 qubits y 2 bits clásicos
    qc = QuantumCircuit(2, 2)
    
    qc.h(0)     # Hadamard en qubit 0 (Superposición)
    qc.cx(0, 1) # CNOT (Control=0, Target=1, Entrelazamiento)
    qc.measure([0, 1], [0, 1]) # Medición de ambos qubits
    
    # Simulación local con AerSimulator
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()
    
    print(f"Resultados Estado de Bell |Φ+> ({shots} disparos):")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        print(f" | {state}> : {count:4d} ({pct:.1f}%)")
        
    # Validación estricta de correlación cuántica perfecta
    assert "01" not in counts and "10" not in counts, "ERROR: Se detectaron estados no entrelazados"
    print("OK: Correlación perfecta verificada con éxito.")
    
    print("\nRepresentación del Circuito en Texto:")
    print(qc.draw(output='text'))
    
    # Guardar histograma de resultados
    fig = plot_histogram(counts)
    fig.savefig("capturas/bell_histogram.png", dpi=150)
    plt.close(fig)
    return counts

if __name__ == "__main__":
    bell_state_experiment()
