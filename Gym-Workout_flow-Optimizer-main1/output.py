import pandas as pd
from algorithm import Algorithm
import heuristic_1 as heuristics

def read_equipment_data():
    df = pd.read_csv("data/equipment.csv")
    return df

def get_user_input():
    muscle_group = input("What muscle group do you want to focus on? ")
    return muscle_group

def process_user_input(user_input, equipment_data):
    # Process the user input to filter/select equipment
    # This is a placeholder function
    filtered_equipment = equipment_data[equipment_data['muscle_groups'].str.contains(user_input, na=False)]
    return filtered_equipment

def apply_algorithm(filtered_equipment):
    # Use the Algorithm class or any other logic to process the filtered equipment
    # Placeholder for algorithm 
    algorithm = Algorithm()
    # Example method call, replace with actual methods and logic
    result = algorithm.method(filtered_equipment)
    return result

def integrate_heuristics(result):
    # Integrate heuristic functions to refine the result
    refined_result = heuristics.heuristic_function(result)
    return refined_result
    
def main():
    equipment_data = read_equipment_data()
    user_input = get_user_input() #muscle group
    filtered_equipment = process_user_input(user_input, equipment_data) #equipment that fits the training
    algorithm_result = apply_algorithm(filtered_equipment)#applying A* Algorithm
    final_suggestion = integrate_heuristics(algorithm_result)
    
    print("Suggested Workout Plan:")
    print(final_suggestion)

if __name__ == "__main__":
    main()
