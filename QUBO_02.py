#Obs: Based on the tutorial:

# https://qiskit-community.github.io/qiskit-optimization/tutorials/03_minimum_eigen_optimizer.html

from qiskit_algorithms.utils import algorithm_globals
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization import QuadraticProgram


# Optional: silence harmless SciPy sparse efficiency warnings
import warnings
try:
    from scipy.sparse import SparseEfficiencyWarning
    warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)
except Exception:
    pass


def main() -> None:
    # -------------------------
    # Create a QUBO
    # -------------------------
    qubo = QuadraticProgram()
    qubo.binary_var("x")
    qubo.binary_var("y")
    qubo.binary_var("z")
    qubo.minimize(
        linear=[1, -2, 3],
        quadratic={("x", "y"): 1, ("x", "z"): -1, ("y", "z"): 2},
    )

    print(qubo.prettyprint())

    # -------------------------
    # Convert to Ising form
    # -------------------------
    op, offset = qubo.to_ising()
    print(f"offset: {offset}")
    print("operator:")
    print(op)

    # (Optional demo) convert back from Ising to a quadratic program
    qp = QuadraticProgram()
    qp.from_ising(op, offset, linear=True)
    print(qp.prettyprint())

    # -------------------------
    # Solve with QAOA: One repetition
    # -------------------------
    seed = 10598
    algorithm_globals.random_seed = seed

    sampler = StatevectorSampler(default_shots=1024, seed=seed)

    print("\nSolution with QAOA (One Repetition):\n")
    qaoa_mes = QAOA(
        sampler=sampler,
        optimizer=COBYLA(),
        reps=1,
        #optional parameter: (beta, gamma) for reps=1
        #initial_point=[0.0, 0.0],
    )
    qaoa = MinimumEigenOptimizer(qaoa_mes)
    qaoa_result = qaoa.solve(qubo)
    print(qaoa_result.prettyprint())

    # -------------------------
    # Sampling statistics (One repetition)
    # -------------------------
    print("variable order:", [var.name for var in qaoa_result.variables])
    print("Sampling statistics: ")
    for s in qaoa_result.samples:
        print(s)




    # -------------------------
    # Solve with QAOA: two repetitions
    # -------------------------
    seed = 10598
    algorithm_globals.random_seed = seed

    sampler = StatevectorSampler(default_shots=1024, seed=seed)

    print("\nSolution with QAOA (Two Repetitions):\n")
    qaoa_mes = QAOA(
        sampler=sampler,
        optimizer=COBYLA(),
        reps=2,
        #optional parameter: (beta, gamma) for reps=2
        #initial_point=[0.0, 0.0,0.0,0.0], 
    )
    qaoa = MinimumEigenOptimizer(qaoa_mes)
    qaoa_result = qaoa.solve(qubo)
    print(qaoa_result.prettyprint())

    # -------------------------
    # Sampling statistics (Two repetitions)
    # -------------------------
    print("variable order:", [var.name for var in qaoa_result.variables])
    print("Sampling statistics: ")
    for s in qaoa_result.samples:
        print(s)




    # -------------------------
    # Solve Exactly (for comparison purposes)
    # This will only work for very small instances
    # -------------------------


    print("\nExact Solution:\n")
    exact_mes = NumPyMinimumEigensolver()
    exact = MinimumEigenOptimizer(exact_mes)
    exact_result = exact.solve(qubo)
    print(exact_result.prettyprint())




if __name__ == "__main__":
    main()
