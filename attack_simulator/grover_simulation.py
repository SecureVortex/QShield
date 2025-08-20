def grover_search_simulation(target, database):
    """Simulate Grover's algorithm for unstructured search."""
    # Placeholder for quantum search: linear search for demonstration
    for idx, item in enumerate(database):
        if item == target:
            return idx
    return -1
