from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler
from qiskit.visualization import circuit_drawer
from process_results import process_results
import matplotlib.pyplot as plt

def run_quantum_simulation(plants, microbes, max_iter, reps):
    sampler = Sampler()
    optimizer = COBYLA(maxiter=max_iter)
    
    plant_hamiltonian = SparsePauliOp.from_list([
        ("II", -1.0), ("IZ", 12.0), ("ZI", 15.0), ("ZZ", -20.0)
    ])
    microbe_hamiltonian = SparsePauliOp.from_list([
        ("II", -1.0), ("ZI", 15.0), ("IZ", 12.0), ("ZZ", -25.0)
    ])

    plant_qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    plant_result = plant_qaoa.compute_minimum_eigenvalue(plant_hamiltonian)
    plant_solution = max(plant_result.eigenstate.binary_probabilities(), 
                       key=plant_result.eigenstate.binary_probabilities().get)
    
    microbe_qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    microbe_result = microbe_qaoa.compute_minimum_eigenvalue(microbe_hamiltonian)
    microbe_solution = max(microbe_result.eigenstate.binary_probabilities(), 
                          key=microbe_result.eigenstate.binary_probabilities().get)

    target_plant = {
        "Root Depth": "deep" if plant_solution[0] == '1' else "shallow",
        "Drought Resistance": "high" if plant_solution[1] == '1' else "low"
    }
    
    target_microbe = {
        "Nitrogen Fixation": "high" if microbe_solution[0] == '1' else "low",
        "Salt Tolerance": "high" if microbe_solution[1] == '1' else "low"
    }

    plant_circuit = plant_qaoa.ansatz.assign_parameters(plant_result.optimal_parameters)
    microbe_circuit = microbe_qaoa.ansatz.assign_parameters(microbe_result.optimal_parameters)

    result_df, specs = process_results(plants, microbes, target_plant, target_microbe, 
                                      plant_hamiltonian, microbe_hamiltonian)
    
    specs['plant_circuit'] = circuit_drawer(plant_circuit, output='mpl')
    specs['microbe_circuit'] = circuit_drawer(microbe_circuit, output='mpl')

    return result_df, specs