import streamlit as st
import pandas as pd
import time
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler

def calculate_compatibility(row, target_traits):
    score = 0
    for trait, target_value in target_traits.items():
        actual_value = row[trait]
        if actual_value == target_value:
            score += 1
        elif actual_value == "moderate" and target_value == "high":
            score += 0.5
        elif actual_value == "moderate" and target_value == "low":
            score += 0.5
    return score

def main():
    st.set_page_config(page_title="Bio-Matcher", page_icon="🌿🔬")
    st.title("Plant-Microbe Matching System")
    
    st.sidebar.header("Configuration ⚙️")
    method = st.sidebar.radio("Algorithm", ["Quantum", "Classical"], index=0)
    simulate_future = st.sidebar.radio("Simulation Type", ["Realistic", "Futuristic"], index=0)
    
    plants_file = st.sidebar.file_uploader("Upload Plants CSV", type=["csv"])
    microbes_file = st.sidebar.file_uploader("Upload Microbes CSV", type=["csv"])
    
    st.sidebar.subheader("Algorithm Parameters")
    if method == "Quantum":
        max_iter = st.sidebar.slider("QAOA Iterations", 50, 500, 200)
        reps = st.sidebar.slider("QAOA Layers", 1, 5, 2)
    else:
        target_plant = st.sidebar.selectbox("Plant Root Depth Target", ["deep", "shallow"])
        target_drought = st.sidebar.selectbox("Plant Drought Target", ["high", "low"])

    if st.sidebar.button("🚀 Run Simulation"):
        if not plants_file or not microbes_file:
            st.warning("Please upload both CSV files!")
            return
            
        with st.spinner("🔮 Running simulation..."):
            try:
                start_time = time.time()
                plants = pd.read_csv(plants_file)
                microbes = pd.read_csv(microbes_file)

                if method == "Quantum":
                    result_df, specs = run_quantum_simulation(plants, microbes, max_iter, reps)
                else:
                    result_df, specs = run_classical_simulation(plants, microbes, target_plant, target_drought)

                raw_elapsed = time.time() - start_time
                
                if simulate_future == "Futuristic":
                    if method == "Quantum":
                        elapsed_time = raw_elapsed
                    else:
                        elapsed_time = raw_elapsed * 100
                        time.sleep(max(elapsed_time - raw_elapsed, 0))
                else:
                    elapsed_time = raw_elapsed

                st.subheader(f"{method} Results 📊")
                cols = st.columns(3)
                cols[0].metric("Total Pairs", len(result_df))
                cols[1].metric("Compute Time", f"{elapsed_time:.2f}s")
                cols[2].metric("Algorithm", method)
                
                with st.expander("🔍 View Details"):
                    if method == "Quantum":
                        st.write("#### Quantum Specifications")
                        st.code(f"Plant Hamiltonian:\n{specs['plant_hamiltonian']}")
                        st.code(f"Microbe Hamiltonian:\n{specs['microbe_hamiltonian']}")
                    st.write("#### Target Traits")
                    st.json({"Plants": specs['target_plant'], "Microbes": specs['target_microbe']})

                st.dataframe(
                    result_df.head(10)[["Plant", "Microbe", "Trait Match", "Environment"]],
                    column_config={
                        "Trait Match": st.column_config.ProgressColumn(
                            format="%.2f",
                            min_value=0,
                            max_value=100,
                        )
                    },
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")

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

    return process_results(plants, microbes, target_plant, target_microbe, plant_hamiltonian, microbe_hamiltonian)

def run_classical_simulation(plants, microbes, target_plant_depth, target_plant_drought):
    target_plant = {
        "Root Depth": target_plant_depth,
        "Drought Resistance": target_plant_drought
    }
    
    target_microbe = {
        "Nitrogen Fixation": "high",
        "Salt Tolerance": "high"
    }

    return process_results(plants, microbes, target_plant, target_microbe)

def process_results(plants, microbes, target_plant, target_microbe, plant_hamiltonian=None, microbe_hamiltonian=None):
    plants['Score'] = plants.apply(calculate_compatibility, axis=1, args=(target_plant,))
    microbes['Score'] = microbes.apply(calculate_compatibility, axis=1, args=(target_microbe,))

    pairs = []
    for _, plant in plants.iterrows():
        for _, microbe in microbes.iterrows():
            if plant["Optimal Condition"] == microbe["Optimal Condition"]:
                pairs.append({
                    "Plant": plant["Name"],
                    "Microbe": microbe["Name"],
                    "Trait Match": (plant['Score'] + microbe['Score']) * 25,
                    "Environment": plant["Optimal Condition"]
                })

    specs = {
        'target_plant': target_plant,
        'target_microbe': target_microbe,
        'plant_hamiltonian': plant_hamiltonian,
        'microbe_hamiltonian': microbe_hamiltonian
    }

    return pd.DataFrame(pairs).sort_values("Trait Match", ascending=False), specs

if __name__ == "__main__":
    main()