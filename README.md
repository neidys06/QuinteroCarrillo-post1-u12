# Laboratorio: Unidad 12: Computación Emergente y Tendencias
**Arquitectura de Computadores**
**Post-Contenido 1 | Ingeniería de Sistemas | 2026**

---

## Objetivo

Implementar circuitos cuánticos en Python usando Qiskit para construir y simular el estado de Bell, demostrar el algoritmo de Deutsch-Jozsa y explorar el algoritmo de Grover sobre un espacio de búsqueda de 2 qubits, interpretando los histogramas de medición en términos de los principios cuánticos subyacentes.

---

## Estructura del Repositorio

```
quintero_carrillo-post1-u12/
├── README.md
├── bell_state.py        # Paso 1: Estado de Bell |Φ⁺⟩
├── deutsch_jozsa.py     # Paso 2: Algoritmo de Deutsch-Jozsa
├──grover.py            # Paso 3: Algoritmo de Grover (2 qubits)
└── capturas/
    ├── Checkpoint1.png   # Bell State — ejecución y resultados
    ├── Checkpoint2.png   # Deutsch-Jozsa — ambos oráculos
    └── Checkpoint3.png   # Grover — los 4 estados objetivo
```

---

## Entorno de Trabajo

| Requisito | Versión |
|-----------|---------|
| Python | 3.12 |
| Qiskit | 2.4.1 |
| Qiskit-Aer | 0.17.2 |
| Matplotlib | 3.10.9 |
| Sistema Operativo | Ubuntu (WSL2) |

**Instalación:**
```bash
python -m venv quantum_env
source quantum_env/bin/activate
pip install qiskit qiskit-aer matplotlib
```

> Nota: todos los experimentos usan el simulador `AerSimulator` — no se requiere acceso a hardware cuántico real ni cuenta en IBM Quantum.

---

## Paso 1: Estado de Bell — Entrelazamiento Cuántico

### Concepto

El estado de Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 es el estado cuántico entrelazado más simple. Se prepara en dos pasos:

1. **Puerta Hadamard (H)** sobre el qubit 0: lleva el estado |0⟩ a una superposición uniforme (|0⟩ + |1⟩)/√2.
2. **Puerta CNOT** (control = qubit 0, target = qubit 1): crea correlación entre los dos qubits, produciendo el estado entrelazado.

El resultado matemático es que **nunca** pueden aparecer los estados |01⟩ ni |10⟩ en la medición — solo |00⟩ y |11⟩ con probabilidad igual (~50% cada uno). Esto es evidencia directa del **entrelazamiento cuántico**: medir el qubit 0 determina instantáneamente el estado del qubit 1, independientemente de la distancia.

### Diagrama del Circuito

```
q_0: ┤ H ├──■──┤ M ├
     └───┘┌─┴─┐└─┬─┘
q_1: ─────┤ X ├──┼──┤ M ├
          └───┘  │  └─┬─┘
c: 2/════════════╩════╩
                 0    1
```

### Resultados

| Estado medido | Conteos | Porcentaje |
|:---:|:---:|:---:|
| \|00⟩ | 514 | 50.2% |
| \|11⟩ | 510 | 49.8% |
| \|01⟩ | 0 | 0.0% |
| \|10⟩ | 0 | 0.0% |

**Total de disparos:** 1024

```
Resultados Estado de Bell |Φ+> (1024 disparos):
  |00> :  514 (50.2%)
  |11> :  510 (49.8%)
OK: Correlación perfecta verificada con éxito.
```

### Interpretación

Los resultados confirman la **correlación perfecta del entrelazamiento**: los estados |01⟩ y |10⟩ tienen probabilidad exactamente 0, validando que los dos qubits están perfectamente entrelazados. La distribución 50/50 entre |00⟩ y |11⟩ es consistente con la función de onda teórica |Φ⁺⟩ = (|00⟩ + |11⟩)/√2.

### Captura de Checkpoint 1

![Checkpoint 1 — Bell State](capturas/Checkpoint1.png)

---

## Paso 2: Algoritmo de Deutsch-Jozsa

### Concepto

El algoritmo de Deutsch-Jozsa resuelve el siguiente problema: dada una función f: {0,1}ⁿ → {0,1}, determinar si es:
- **Constante**: devuelve el mismo valor (0 ó 1) para todas las entradas.
- **Balanceada**: devuelve 0 para exactamente la mitad de entradas y 1 para la otra mitad.

**Ventaja cuántica:** el algoritmo cuántico necesita **exactamente 1 evaluación del oráculo** para cualquier n, mientras que el algoritmo clásico necesita hasta **2ⁿ⁻¹ + 1** evaluaciones en el peor caso.

Para n = 2 (este laboratorio), el caso clásico requiere hasta **3 evaluaciones** en el peor caso (se deben probar suficientes entradas hasta descartar la hipótesis opuesta). El algoritmo cuántico lo resuelve con **1 sola evaluación**.

### ¿Por qué 1 evaluación es suficiente?

El circuito aplica la transformada de Hadamard para poner todos los qubits de entrada en superposición, luego evalúa el oráculo sobre **todas las entradas simultáneamente** gracias al paralelismo cuántico. Después, la interferencia cuántica cancela todos los caminos para los estados ≠ |0...0⟩ si la función es constante, o los amplifica si es balanceada. Una sola medición posterior revela con certeza cuál es el caso.

### Diagrama del Circuito (n = 2)

```
      Oráculo
q_0: ─┤ H ├──[Oracle]──┤ H ├──┤ M ├
q_1: ─┤ H ├──[Oracle]──┤ H ├──┤ M ├
q_2: ─┤X├─┤ H ├──[Oracle]────────── (ancilla, no se mide)
```

### Resultados

| Oráculo | Resultado medido | Interpretación |
|:---:|:---:|:---:|
| Constante (f(x)=0) | {`'00'`: 1024} | Todos los bits son 0 → función **constante**  |
| Balanceado (CNOT) | {`'11'`: 1024} | Algún bit es 1 → función **balanceada**  |

```
=== Ejecutando Algoritmo de Deutsch-Jozsa ===
Resultado Oráculo Constante: {'00': 1024}
Resultado Oráculo Balanceado: {'11': 1024}
OK: Verificación de Deutsch-Jozsa exitosa.
```

### Interpretación

Los resultados son **deterministas** (probabilidad 100%), lo que demuestra la ventaja cuántica: no hay ambigüedad estadística como en los algoritmos clásicos probabilistas. El oráculo constante siempre produce |00⟩, y el balanceado nunca produce |00⟩, tal como predice la teoría.

### Captura de Checkpoint 2

![Checkpoint 2 — Deutsch-Jozsa](capturas/Checkpoint2.png)

---

## Paso 3: Algoritmo de Grover (2 Qubits)

### Concepto

El algoritmo de Grover busca un elemento marcado en una base de datos no estructurada de N elementos con complejidad O(√N), frente a O(N) del caso clásico (**aceleración cuadrática**).

Para n = 2 qubits el espacio tiene N = 4 elementos. El número óptimo de iteraciones de Grover es:

k = ⌊π/4 · √N⌋ = ⌊π/4 · 2⌋ = **1 iteración**

Con 1 iteración, el estado objetivo alcanza probabilidad de amplitud ≈ 100%.

### ¿Por qué 1 iteración es suficiente para n = 2?

Con 4 estados equiprobables (amplitud = 1/2 cada uno), el **oráculo de fase** invierte la amplitud del estado objetivo (lo marca con fase −1). Luego el **difusor** (inversión alrededor de la media) amplifica ese estado marcado y suprime los demás. Tras 1 iteración para N = 4, la amplitud del estado objetivo pasa de 1/2 a exactamente 1 (probabilidad = 100%).

### Circuito: Oráculo de fase + Difusor

```
Superposición:  H⊗H  →  oráculo de fase  →  difusor (H·X·CZ·X·H)  →  medición
```

### Resultados

| Estado objetivo | Estado encontrado | Conteos | Probabilidad | Resultado |
|:---:|:---:|:---:|:---:|:---:|
| \|00⟩ | \|00⟩ | 1024 | 100.0% | CORRECTO |
| \|01⟩ | \|01⟩ | 1024 | 100.0% | CORRECTO |
| \|10⟩ | \|10⟩ | 1024 | 100.0% | CORRECTO |
| \|11⟩ | \|11⟩ | 1024 | 100.0% | CORRECTO |

```
=== Ejecutando Algoritmo de Grover (2 Qubits) ===
Grover buscando Objetivo |00>:
  |00>: 1024 (100.0%)
Estado con máxima probabilidad: |00> -> CORRECTO

Grover buscando Objetivo |01>:
  |01>: 1024 (100.0%)
Estado con máxima probabilidad: |01> -> CORRECTO

Grover buscando Objetivo |10>:
  |10>: 1024 (100.0%)
Estado con máxima probabilidad: |10> -> CORRECTO

Grover buscando Objetivo |11>:
  |11>: 1024 (100.0%)
Estado con máxima probabilidad: |11> -> CORRECTO
```

### Interpretación

Los 4 estados objetivo fueron encontrados con probabilidad 100%, confirmando que **1 iteración de Grover es exactamente óptima para n = 2**. En un buscador clásico, en el peor caso se necesitarían 4 evaluaciones para encontrar el elemento marcado; el algoritmo de Grover lo hace siempre en 1 sola pasada por el circuito.

### Captura de Checkpoint 3

![Checkpoint 3 — Grover](capturas/Checkpoint3.png)

---

## Resumen de Resultados

| Experimento | Estado esperado | Verificación | Observación |
|:---:|:---:|:---:|:---|
| Bell \|Φ⁺⟩ | Solo \|00⟩ y \|11⟩, ~50/50 |  | Correlación perfecta, entrelazamiento confirmado |
| Deutsch-Jozsa Constante | \|00⟩ con 100% | | Determinista, 1 evaluación |
| Deutsch-Jozsa Balanceado | ≠ \|00⟩ con 100% |  | Determinista, 1 evaluación |
| Grover \|00⟩ | \|00⟩ con >90% | 100% | Amplitud perfecta con 1 iteración |
| Grover \|01⟩ | \|01⟩ con >90% | 100% | Amplitud perfecta con 1 iteración |
| Grover \|10⟩ | \|10⟩ con >90% | 100% | Amplitud perfecta con 1 iteración |
| Grover \|11⟩ | \|11⟩ con >90% | 100% | Amplitud perfecta con 1 iteración |

---
