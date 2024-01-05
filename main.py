import gradio as gr
import pandas as pd
import json
from algorithm import Algorithm
from suggest import getSuggestion

muscle_groups = {
    "腿": [
        "內收肌短肌",
        "內收肌",
        "腹股沉肌",
        "股二頭肌",
        "小腿肌肉",
        "小腿肌肉 (腓腸肌和腓腸後肌)",
        "脛骨長趾伸肌",
        "長趾伸肌",
        "足長屈肌",
        "屈長跗肌",
        "腓腓肌",
        "腓腸肌 (外側頭)",
        "腓腸肌（內側）",
        "臀大肌",
        "中殿肌",
        "臀小肌",
        "長肌",
        "腿後肌群",
        "臀部外展肌",
        "髖內收肌",
        "髖屈肌",
        "髂腰肌",
        "腓腸肌",
        "腓骨短肌",
        "腓骨長肌",
        "外踝肌",
        "腓骨筋",
        "膝半腱肌",
        "股四頭肌 (直肌、外側肌、內側肌、中間肌)",
        "直肌",
        "縫匠肌",
        "薄膜半腱肌",
        "半腱肌",
        "比目魚肌",
        "湧泉肌",
        "脛骨前肌",
        "廣隔肌",
        "外側廣闊肌",
        "內側肌",
    ],
    "手臂": [
        "肘肌",
        "肱二頭肌",
        "上臂三頭肌",
        "肱桡肌",
        "肩胛肌",
        "前臂肌肉 (屈肌和伸肌)",
        "三頭肌（上臂後方）",
        "肱三頭肌（長頭）",
    ],
    "肩部": ["前三角肌", "三角肌（前束、外束、後束）", "棘下肌", "中於肌", "後三角肌", "肩胛下肌", "超肩胛肌", "肩小圓肌"],
    "背肌": [
        "脊柱舉起肌",
        "脊柱起肌 (脊肌)",
        "背闊肌",
        "舉肩肌",
        "腰背肌 (起立脊肌)",
        "中、下斜方肌",
        "腰方肌",
        "菱形肌大肌",
        "斜方肌小束",
        "菱形肌",
        "肩胛小肌",
        "斜方肌",
        "伸肩肌下束",
        "斜方肌 (中部和下部纖維)",
    ],
    "腹肌": ["外腹斜肌", "內斜方肌", "肋間內外肌", "內外斜肌", "腹斜肌", "腹直肌", "橫腹肌"],
    "胸肌": ["胸大肌", "胸大肌(鎖骨頭部)", "胸大肌 (胸骨部分)", "腋窩肌", "前鋸肌"],
}


def get_workout_plan(*args):
    # Translate the muscle groups into Chinese
    trans_dict = {}
    with open("data/translate_C2E_dict.json", "r") as f:
        trans_dict = json.load(f)

    # The last argument is tolerance, and the rest are selected muscle groups
    selected_muscles = [trans_dict[muscle] for group in args[:-1] for muscle in group]
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

    output_string = ""
    # output_string += "Suggested workout plan for: " + ', '.join(selected_muscles) + "\n"
    # output_string += "Total cost: " + str(cost) + " minutes\n\n"
    output_string += "Workout Plan:\n\n"
    image_html = ""
    for equipment, wait_time in result:
        output_string += f"{equipment} - wait for {wait_time} minutes\n"
        combined, totalTime = getSuggestion([equipment])
        output_string += f"      around {totalTime} minutes workouts\n"
        for exercise in combined:
            output_string += "        - " + exercise
        output_string += "\n"
        # Read the local image file
        image_name = equipment.replace("\\", "_")
        # print(image_name)
        image_html += f"<img src='file/images/{image_name}.webp' style='max-width:300px; max-height:300px;'>"

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
