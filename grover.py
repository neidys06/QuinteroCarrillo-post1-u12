import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def grover_2qubits(target="11", shots=1024):
    os.makedirs('capturas', exist_ok=True)
    qc = QuantumCircuit(2, 2)
    
    # Paso 1: Inicialización en superposición uniforme
    qc.h([0, 1])
    
    # Paso 2: Oráculo de fase para marcar el estado objetivo invirtiendo su amplitud
    if target == "11":
        qc.cz(0, 1)
    elif target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == "01":
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)
    elif target == "10":
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)
        
    # Paso 3: Operador de difusión (Inversión alrededor de la media)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    
    # Medición del registro de qubits
    qc.measure([0, 1], [0, 1])
    
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    
    print(f"Grover buscando Objetivo |{target}>:")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        print(f"  |{state}>: {count:4d} ({pct:.1f}%)")
        
    top = max(counts, key=counts.get)
    status = "CORRECTO" if top == target else "ERROR"
    print(f"Estado con máxima probabilidad: |{top}> -> {status}")
    
    # Guardar el histograma correspondiente en la carpeta de capturas
    fig = plot_histogram(counts)
    fig.savefig(f"capturas/grover_{target}.png", dpi=150)
    plt.close(fig)
    return counts

if __name__ == "__main__":
    print("=== Ejecutando Algoritmo de Grover (2 Qubits) ===")
    for objetivo in ["00", "01", "10", "11"]:
        grover_2qubits(target=objetivo)
        print()
