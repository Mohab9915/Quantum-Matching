from calculate_compatibility import calculate_compatibility
import pandas as pd

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