import streamlit as st
import pandas as pd
import time
from quantum_simulation import run_quantum_simulation
from classic_simulation import run_classical_simulation
from AI_comparison import show_ai_comparison


def main():
    st.set_page_config(page_title="Bio-Matcher", page_icon="🌿🔬", layout="wide")
    st.title("Plant-Microbe Matching System")
    
    st.sidebar.header("Configuration ⚙️")
    tabs = ["Simulation", "AI Comparison"]
    selected_tab = st.sidebar.radio("Mode", tabs)
    
    if selected_tab == "Simulation":
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
                            st.write("#### QAOA Circuits")
                            st.write("**Plant Circuit:**")
                            st.pyplot(specs['plant_circuit'])
                            
                            st.write("**Microbe Circuit:**")
                            st.pyplot(specs['microbe_circuit'])
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
    
    else:
        show_ai_comparison()

if __name__ == "__main__":
    main()