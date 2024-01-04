import gradio as gr
from algorithm import Algorithm
import pandas as pd

# Detailed Muscle Groups
muscle_groups = {
    "Leg Muscles": [
        "Quadriceps (Rectus Femoris, Vastus Lateralis, Vastus Medialis, Vastus Intermedius)",
        "Hamstrings (Biceps Femoris, Semitendinosus, Semimembranosus)",
        "Gastrocnemius", "Soleus", "Adductor Magnus", "Tibialis Anterior",
        "Popliteus", "Peroneals (Peroneus Longus, Peroneus Brevis, Peroneus Tertius)",
        "Flexor Hallucis Longus", "Flexor Digitorum Longus",
        "Extensor Hallucis Longus", "Extensor Digitorum Longus"
    ],
    "Hip and Gluteal Muscles": [
        "Gluteus Maximus", "Gluteus Medius", "Gluteus Minimus",
        "Tensor Fasciae Latae", "Iliopsoas", "Sartorius", "Gracilis"
    ],
    "Back Muscles": [
        "Erector Spinae", "Latissimus Dorsi", "Trapezius",
        "Rhomboids", "Levator Scapulae", "Quadratus Lumborum"
    ],
    "Abdominal Muscles": [
        "Rectus Abdominis", "Obliques (External, Internal)",
        "Transverse Abdominis", "Internal and External Intercostals"
    ],
    "Arm Muscles": [
        "Biceps Brachii", "Triceps Brachii", "Brachialis",
        "Brachioradialis", "Anconeus", "Forearm muscles (Flexors and Extensors)"
    ],
    "Shoulder Muscles": [
        "Deltoids (Anterior, Lateral, and Posterior)",
        "Supraspinatus", "Infraspinatus", "Subscapularis",
        "Teres Major", "Teres Minor"
    ],
    "Chest Muscles": [
        "Pectoralis Major", "Pectoralis Minor", "Serratus Anterior"
    ]
    # Add more muscle groups as needed
}
# Function to process the user input and return the suggested equipment
def get_workout_plan(specific_muscles, tolerance):
    # Placeholder for your algorithm's logic
    selected_equipment = Algorithm(specific_muscles, tolerance).method()

    if selected_equipment is None:
        return "No suitable equipment found."
    return f"Suggested equipment for muscles: {', '.join(specific_muscles)} with a tolerance of {tolerance} minutes: {selected_equipment}"

def update_specific_muscles(muscle_category):
    # Get the specific muscles based on the selected category
    return muscle_groups.get(muscle_category, [])

with gr.Blocks() as app:
    gr.Markdown("## Workout Optimizer")
    gr.Markdown("Select specific muscles you want to focus on and enter your wait tolerance to get a suggested equipment.")

    with gr.Row():
        muscle_category = gr.Dropdown(list(muscle_groups.keys()), label="Select Muscle Group Category")
        tolerance = gr.Number(label="Tolerance (minutes)", value=30, step=1)

    specific_muscles = gr.CheckboxGroup(label="Select Specific Muscles")
    
    # Update the specific muscles based on the selected muscle group category
    muscle_category.change(update_specific_muscles, inputs=muscle_category, outputs=specific_muscles)

    output = gr.Textbox(label="Suggested Equipment")

    gr.Button("Get Suggested Equipment").click(
        fn=get_workout_plan,
        inputs=[specific_muscles, tolerance],
        outputs=output
    )

app.launch()