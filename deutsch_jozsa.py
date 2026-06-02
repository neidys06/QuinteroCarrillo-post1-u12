from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def oracle_constante(n):
    """Oráculo constante f(x)=0: No altera el sistema."""
    return QuantumCircuit(n + 1)

def oracle_balanceada(n):
    """Oráculo balanceado: Aplica compuertas CNOT de las entradas a la ancilla."""
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i, n)
    return qc

def deutsch_jozsa(oracle_qc, n, shots=1024):
    # n qubits de entrada + 1 qubit ancilla, n bits clásicos para medir la entrada
    qc = QuantumCircuit(n + 1, n)
    
    # Inicialización del qubit ancilla en el estado |-> = H|1>
    qc.x(n)
    qc.h(n)
    
    # Aplicar compuertas Hadamard a los qubits de entrada
    qc.h(range(n))
    
    # Inyectar el oráculo evaluado
    qc.compose(oracle_qc, inplace=True)
    
    # Interferencia: Aplicar Hadamard nuevamente a las entradas
    qc.h(range(n))
    
    # Medir únicamente los qubits de entrada
    qc.measure(range(n), range(n))
    
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    return counts

if __name__ == "__main__":
    n = 2
    print("=== Ejecutando Algoritmo de Deutsch-Jozsa ===")
    
    # Oráculo Constante: Debe colapsar exclusivamente en "00"
    counts_c = deutsch_jozsa(oracle_constante(n), n)
    print(f"Resultado Oráculo Constante: {counts_c}")
    
    # Oráculo Balanceado: Nunca debe producir "00"
    counts_b = deutsch_jozsa(oracle_balanceada(n), n)
    print(f"Resultado Oráculo Balanceado: {counts_b}")
    
    assert "00" in counts_c, "Error: El oráculo constante no retornó '00'"
    assert "00" not in counts_b, "Error: El oráculo balanceado retornó '00'"
    print("OK: Verificación de Deutsch-Jozsa exitosa.")
