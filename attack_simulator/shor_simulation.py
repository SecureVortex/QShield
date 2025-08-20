def shor_factorization_simulation(N):
    """Simulate Shor's algorithm for integer factorization."""
    # Placeholder: actual Shor's simulation would use Qiskit or PennyLane
    # Here we simply use classical factorization for demonstration
    factors = []
    for i in range(2, N):
        if N % i == 0:
            factors.append(i)
    return factors
