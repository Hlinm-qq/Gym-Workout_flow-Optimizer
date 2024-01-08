import gradio as gr
import pandas as pd
import json
from algorithm import Algorithm
from suggest import getSuggestion

# Get muscle groups
muscle_groups = {}
with open("data/category_cn.json", "r") as f:
    muscle_groups = json.load(f)


def list_target_related_equip(selected_muscles, algorithm):
    translator = {}
    with open("data/translate_E2C_dict.json") as f:
        translator = json.load(f)
    df = algorithm.equipmentStatus.copy()

    # Get all muscle_groups and fill into the df
    df["muscle_groups"] = list(algorithm.jsonData.values())

    # Get the equipments that match selected_muscles
    matched_df = df[
        pd.DataFrame(df.muscle_groups.tolist())
        .isin(selected_muscles)
        .any(axis=1)
        .values
    ]

    # Grape only the muscle groups specified in selected_muscles
    selected_muscles_dict = {}
    for key, muscles in algorithm.jsonData.items():
        content = [
            translator[muscle]
            for muscle in muscles
            if any(m == muscle for m in selected_muscles)
        ]
        if content != []:
            selected_muscles_dict[key] = content
    # Update the muscle_groups col
    matched_df.loc[:, "muscle_groups"] = list(selected_muscles_dict.values())

    # Reorder the col
    matched_df = matched_df.loc[
        :,
        [
            "id",
            "equipment",
            "number",
            "capacity",
            "available number",
            "expected usage time for occupied equipments",
            "waiting number",
            "expected usage time for waiting people",
            "muscle_groups",
        ],
    ]
    # print(matched_df)
    return matched_df


def get_workout_plan(*args):
    # Translate the muscle groups into Chinese
    trans_dict = {}
    with open("data/translate_C2E_dict.json", "r") as f:
        trans_dict = json.load(f)

    # The last argument is tolerance, and the rest are selected muscle groups
    selected_muscles = [trans_dict[muscle] for group in args[:-1] for muscle in group]
    tolerance = args[-1]

    # Load equipment data
    # df = pd.read_csv("data/equipment.csv")

    # User input is already a list of selected muscle groups
    userInput = [selected_muscles, int(tolerance)]
    algorithm = Algorithm(userInput)

    # Run the algorithm and get the result
    result, cost = algorithm.method()

    # Handle the output of the algorithm
    if not result:
        return "No suitable workout plan found."

    output_string = ""
    # output_string += "Suggested workout plan for: " + ', '.join(selected_muscles) + "\n"
    # output_string += "Total cost: " + str(cost) + " minutes\n\n"
    output_string += "Workout Plan:\n\n"
    image_html = ""
    for equipment, wait_time in result:
        output_string += f"{equipment} - wait for {wait_time} minutes\n"

        # no special exercise suggestion if equipment is treadmill
        if equipment != "treadmill":
            combined, totalTime = getSuggestion([equipment])
            output_string += f"      around {totalTime} minutes workouts\n"
            for exercise in combined:
                output_string += "        - " + exercise
        output_string += "\n"

        # Read the local image file
        image_name = equipment.replace("\\", "_")
        # print(image_name)
        image_html += f"<img src='file/images/{image_name}.webp' style='background-color:white; width:300px; max-height:300px;'>"

    # Get info of all match equipment
    # match_equipment_list = list_target_related_equip(selected_muscles, algorithm)
    return [output_string, image_html]


# Create Gradio interface without collapsible sections
inputs = [
    gr.CheckboxGroup(choices=choices, label=label)
    for label, choices in muscle_groups.items()
]
inputs.append(gr.Dropdown(choices=[0, 10, 20, 30], label="Tolerance (minutes)"))

interface = gr.Interface(
    fn=get_workout_plan,
    inputs=inputs,
    outputs=["text", "html"],
    title="Workout Optimizer",
    description="Select muscle groups from each category and your wait tolerance to get a workout plan.",
)

if __name__ == "__main__":
    interface.launch(allowed_paths=["."])
