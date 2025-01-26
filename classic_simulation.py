from process_results import process_results

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