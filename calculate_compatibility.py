import pandas as pd

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
