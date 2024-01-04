import gradio as gr
import pandas as pd
from algorithm import Algorithm
from suggest import getExerSuggestion

# Function that processes the user input and returns the suggestion
def get_workout_plan(muscle_group, tolerance):
    # Load equipment data
    df = pd.read_csv("data/equipment.csv")
    # Process the user input
    userInput = [muscle_group, int(tolerance)]  # Convert tolerance to integer
    algorithm = Algorithm(userInput)
    # Run the algorithm and get the result
    result, cost = algorithm.method()
    if result:
        exerciseSuggest = getExerSuggestion(result)
    # Handle the output of the algorithm
    if result is None:
        return "No suitable workout plan found."
    output1 = f"Suggested workout plan for: {muscle_group} with cost: {cost}"
    return output1

# Create Gradio interface
interface = gr.Interface(
    fn=get_workout_plan,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter muscle group here..."),
        gr.Dropdown(choices=[0, 10, 20, 30], label="Tolerance (minutes)")
    ],
    outputs="text",
    title="Workout Optimizer",
    description="Enter the muscle group you want to focus on and select your wait tolerance to get a workout plan."
)

if __name__ == "__main__":
    interface.launch()
