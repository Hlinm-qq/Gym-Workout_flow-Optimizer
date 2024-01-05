import gradio as gr
import pandas as pd
from algorithm import Algorithm
from suggest import getSuggestion

muscle_groups = {
    "Leg Muscles": [
        "Quadriceps (Rectus Femoris, Vastus Lateralis, Vastus Medialis, Vastus Intermedius)",
        "Hamstrings (Biceps Femoris, Semitendinosus, Semimembranosus)",
        "Gastrocnemius", "Soleus", "Adductor Magnus", "Tibialis Anterior",
        "Popliteus", "Calves (Gastrocnemius and Soleus)", "Hip Adductors",
        "Hip Abductors", "Hip Flexors", "Peroneals", "Gracilis"
    ],
    "Gluteal Muscles": [
        "Gluteus Maximus", "Gluteus Medius", "Gluteus Minimus", "Tensor Fasciae Latae"
    ],
    "Back Muscles": [
        "Erector Spinae", "Latissimus Dorsi", "Trapezius", "Rhomboids",
        "Levator Scapulae", "Serratus Anterior (Upper side of ribs)", "Quadratus Lumborum"
    ],
    "Abdominal Muscles": [
        "Rectus Abdominis", "External Obliques", "Internal Obliques",
        "Transverse Abdominis", "Internal and External Intercostals"
    ],
    "Arm Muscles": [
        "Biceps Brachii", "Triceps Brachii (Back of upper arm)", "Brachialis",
        "Brachioradialis", "Forearm muscles (Flexors and Extensors)", "Anconeus"
    ],
    "Shoulder Muscles": [
        "Deltoids (Anterior, Lateral, and Posterior)", "Supraspinatus",
        "Infraspinatus", "Subscapularis", "Teres Major", "Teres Minor",
        "Posterior Deltoid", "Pectoralis Major (Clavicular Head)",
        "Pectoralis Major (Sternal Head)", "Pectoralis Minor"
    ],
    "Chest Muscles": [
        "Pectoralis Major", "Pectoralis Minor"
    ]
}

def get_workout_plan(*args):
    # The last argument is tolerance, and the rest are selected muscle groups
    selected_muscles = [muscle for group in args[:-1] for muscle in group]
    tolerance = args[-1]

    # Load equipment data
    df = pd.read_csv("data/equipment.csv")
    
    # User input is already a list of selected muscle groups
    userInput = [selected_muscles, int(tolerance)]
    algorithm = Algorithm(userInput)
    
    # Run the algorithm and get the result
    result, cost = algorithm.method()
    
    # Handle the output of the algorithm
    if not result:
        return "No suitable workout plan found."
    
    output_string=""
    # output_string += "Suggested workout plan for: " + ', '.join(selected_muscles) + "\n"
    # output_string += "Total cost: " + str(cost) + " minutes\n\n"
    output_string += "Workout Plan:\n"
    for equipment, wait_time in result:
        output_string += f"{equipment} - wait for {wait_time} minutes\n"
        combined, totalTime = getSuggestion([equipment])
        output_string += f'      around {totalTime} minutes workouts\n'
        for exercise in combined:
            output_string += '        - ' + exercise
    
    return output_string


# Create Gradio interface without collapsible sections
inputs = [gr.CheckboxGroup(choices=choices, label=label) for label, choices in muscle_groups.items()]
inputs.append(gr.Dropdown(choices=[0, 10, 20, 30], label="Tolerance (minutes)"))

interface = gr.Interface(
    fn=get_workout_plan,
    inputs=inputs,
    outputs="text",
    title="Workout Optimizer",
    description="Select muscle groups from each category and your wait tolerance to get a workout plan."
)

if __name__ == "__main__":
    interface.launch()